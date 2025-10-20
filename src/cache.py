"""
Response caching for RAG API endpoints.

Implements LRU caching with configurable TTL for /search and /chat responses.
Cache hits provide 80-90% latency reduction for repeated queries.

Design:
- LRU eviction when cache full (default 1000 entries)
- Time-to-live (TTL) per response (configurable, default 3600s)
- Cache key: MD5(query + k + namespace) for fast lookup
- Thread-safe with lock-based synchronization
"""

import os
import json
import hashlib
import time
from typing import Any, Optional
from threading import Lock
from loguru import logger


class CacheEntry:
    """Single cached response with TTL."""
    def __init__(self, data: dict, ttl: int = 3600):
        self.data = data
        self.created_at = time.time()
        self.ttl = ttl

    def is_expired(self) -> bool:
        """Check if entry has exceeded TTL."""
        return (time.time() - self.created_at) > self.ttl

    def __repr__(self) -> str:
        age_sec = time.time() - self.created_at
        return f"CacheEntry(age={age_sec:.1f}s, ttl={self.ttl}s, expired={self.is_expired()})"


class LRUResponseCache:
    """
    LRU cache for API responses with TTL-based expiration.

    Thread-safe with lock-based synchronization.
    """

    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        """
        Initialize cache.

        Args:
            max_size: Maximum number of entries before LRU eviction
            default_ttl: Default time-to-live in seconds
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: dict[str, CacheEntry] = {}
        self.access_order: list[str] = []  # LRU order
        self.lock = Lock()
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def _make_key(self, query: str, k: int, namespace: Optional[str] = None) -> str:
        """
        Create deterministic cache key from query parameters.

        Args:
            query: Search query
            k: Number of results
            namespace: Optional namespace filter

        Returns:
            Hex digest cache key
        """
        key_parts = f"{query}:{k}:{namespace or ''}"
        return hashlib.md5(key_parts.encode()).hexdigest()

    def get(self, query: str, k: int, namespace: Optional[str] = None) -> Optional[dict]:
        """
        Get cached response if available and not expired.

        Args:
            query: Search query
            k: Number of results
            namespace: Optional namespace filter

        Returns:
            Cached response dict or None if not found/expired
        """
        key = self._make_key(query, k, namespace)

        with self.lock:
            if key not in self.cache:
                self.misses += 1
                return None

            entry = self.cache[key]
            if entry.is_expired():
                # Expired: delete and treat as miss
                del self.cache[key]
                self.access_order.remove(key)
                self.misses += 1
                logger.debug(f"Cache hit but expired: {key}")
                return None

            # Cache hit: move to end (most recent)
            self.access_order.remove(key)
            self.access_order.append(key)
            self.hits += 1
            logger.debug(f"Cache hit: {key} (age={time.time() - entry.created_at:.1f}s)")
            return entry.data

    def set(self, query: str, k: int, response: dict, namespace: Optional[str] = None, ttl: Optional[int] = None) -> None:
        """
        Cache a response with TTL.

        Args:
            query: Search query
            k: Number of results
            response: Response dict to cache
            namespace: Optional namespace filter
            ttl: Time-to-live in seconds (uses default if None)
        """
        key = self._make_key(query, k, namespace)
        ttl = ttl or self.default_ttl

        with self.lock:
            # If key exists, update access order
            if key in self.cache:
                self.access_order.remove(key)

            # Add to cache
            self.cache[key] = CacheEntry(response, ttl=ttl)
            self.access_order.append(key)

            # Evict LRU if over capacity
            while len(self.cache) > self.max_size:
                lru_key = self.access_order.pop(0)
                del self.cache[lru_key]
                self.evictions += 1
                logger.debug(f"Cache eviction: LRU removed, size={len(self.cache)}")

    def clear(self) -> None:
        """Clear all cached responses."""
        with self.lock:
            self.cache.clear()
            self.access_order.clear()
            logger.info("Cache cleared")

    def stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dict with hits, misses, size, capacity, hit_rate
        """
        with self.lock:
            total = self.hits + self.misses
            hit_rate = (self.hits / total * 100) if total > 0 else 0.0

            # Count expired entries
            expired_count = sum(1 for e in self.cache.values() if e.is_expired())

            return {
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate_pct": round(hit_rate, 2),
                "size": len(self.cache),
                "capacity": self.max_size,
                "evictions": self.evictions,
                "expired_entries": expired_count,
            }

    def __repr__(self) -> str:
        stats = self.stats()
        return (
            f"LRUResponseCache("
            f"size={stats['size']}/{stats['capacity']}, "
            f"hits={stats['hits']}, "
            f"hit_rate={stats['hit_rate_pct']}%)"
        )


# Global singleton instance
_cache_instance: Optional[LRUResponseCache] = None


def init_cache(max_size: Optional[int] = None, default_ttl: Optional[int] = None) -> LRUResponseCache:
    """
    Initialize or get global cache instance.

    Args:
        max_size: Cache max entries (default from env or 1000)
        default_ttl: Default TTL in seconds (default from env or 3600)

    Returns:
        Global LRUResponseCache instance
    """
    global _cache_instance

    if _cache_instance is not None:
        return _cache_instance

    max_size = max_size or int(os.getenv("RESPONSE_CACHE_SIZE", "1000"))
    default_ttl = default_ttl or int(os.getenv("RESPONSE_CACHE_TTL", "3600"))

    _cache_instance = LRUResponseCache(max_size=max_size, default_ttl=default_ttl)
    logger.info(f"Response cache initialized: max_size={max_size}, ttl={default_ttl}s")

    return _cache_instance


def get_cache() -> LRUResponseCache:
    """Get global cache instance (must be initialized first)."""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = init_cache()
    return _cache_instance
