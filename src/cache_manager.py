#!/usr/bin/env python3
"""
Query and Result Caching Manager

Implements intelligent caching for query analysis and search results
to reduce latency and improve performance.
"""

import json
import time
from typing import Dict, List, Optional, Any
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages caching for queries and results with TTL support."""

    def __init__(self, default_ttl: int = 3600):
        """
        Initialize cache manager.

        Args:
            default_ttl: Default time-to-live in seconds (default: 1 hour)
        """
        self.default_ttl = default_ttl
        self.query_cache: Dict[str, Dict[str, Any]] = {}
        self.result_cache: Dict[str, Dict[str, Any]] = {}
        self.stats = {
            "query_hits": 0,
            "query_misses": 0,
            "result_hits": 0,
            "result_misses": 0,
        }

    def _is_expired(self, timestamp: float, ttl: int) -> bool:
        """Check if cached item has expired."""
        return time.time() - timestamp > ttl

    def get_query_analysis(self, query: str) -> Optional[Dict]:
        """
        Get cached query analysis if available and not expired.

        Args:
            query: The query string

        Returns:
            Cached analysis dict or None
        """
        cache_key = query.lower().strip()

        if cache_key in self.query_cache:
            entry = self.query_cache[cache_key]
            if not self._is_expired(entry["timestamp"], self.default_ttl):
                self.stats["query_hits"] += 1
                logger.debug(f"Query cache hit: {query}")
                return entry["data"]
            else:
                del self.query_cache[cache_key]

        self.stats["query_misses"] += 1
        return None

    def set_query_analysis(self, query: str, analysis: Dict) -> None:
        """
        Cache query analysis result.

        Args:
            query: The query string
            analysis: The analysis result dict
        """
        cache_key = query.lower().strip()
        self.query_cache[cache_key] = {
            "data": analysis,
            "timestamp": time.time(),
        }
        logger.debug(f"Cached query analysis for: {query}")

    def get_search_results(self, query: str, namespace: str, k: int) -> Optional[List]:
        """
        Get cached search results if available.

        Args:
            query: The search query
            namespace: Document namespace
            k: Number of results

        Returns:
            Cached results list or None
        """
        cache_key = f"{query.lower().strip()}:{namespace}:{k}"

        if cache_key in self.result_cache:
            entry = self.result_cache[cache_key]
            if not self._is_expired(entry["timestamp"], self.default_ttl):
                self.stats["result_hits"] += 1
                logger.debug(f"Result cache hit: {query} (k={k})")
                return entry["data"]
            else:
                del self.result_cache[cache_key]

        self.stats["result_misses"] += 1
        return None

    def set_search_results(
        self, query: str, namespace: str, k: int, results: List
    ) -> None:
        """
        Cache search results.

        Args:
            query: The search query
            namespace: Document namespace
            k: Number of results
            results: The search results list
        """
        cache_key = f"{query.lower().strip()}:{namespace}:{k}"
        self.result_cache[cache_key] = {
            "data": results,
            "timestamp": time.time(),
        }
        logger.debug(f"Cached search results for: {query} (k={k})")

    def clear(self) -> None:
        """Clear all caches."""
        self.query_cache.clear()
        self.result_cache.clear()
        logger.info("Cache cleared")

    def clear_expired(self) -> int:
        """
        Clear expired entries from both caches.

        Returns:
            Number of entries removed
        """
        removed = 0

        expired_queries = [
            k
            for k, v in self.query_cache.items()
            if self._is_expired(v["timestamp"], self.default_ttl)
        ]
        for k in expired_queries:
            del self.query_cache[k]
            removed += 1

        expired_results = [
            k
            for k, v in self.result_cache.items()
            if self._is_expired(v["timestamp"], self.default_ttl)
        ]
        for k in expired_results:
            del self.result_cache[k]
            removed += 1

        if removed > 0:
            logger.debug(f"Removed {removed} expired cache entries")

        return removed

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Stats dict with hit/miss counts and rates
        """
        query_total = self.stats["query_hits"] + self.stats["query_misses"]
        result_total = self.stats["result_hits"] + self.stats["result_misses"]

        return {
            "query_cache": {
                "hits": self.stats["query_hits"],
                "misses": self.stats["query_misses"],
                "hit_rate": (
                    self.stats["query_hits"] / query_total * 100
                    if query_total > 0
                    else 0
                ),
                "size": len(self.query_cache),
            },
            "result_cache": {
                "hits": self.stats["result_hits"],
                "misses": self.stats["result_misses"],
                "hit_rate": (
                    self.stats["result_hits"] / result_total * 100
                    if result_total > 0
                    else 0
                ),
                "size": len(self.result_cache),
            },
        }


# Global cache instance
_cache_manager = None


def get_cache_manager() -> CacheManager:
    """Get or create global cache manager instance."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


def cache_query_analysis(func):
    """Decorator to cache query analysis results."""

    @wraps(func)
    def wrapper(self, query: str):
        cache = get_cache_manager()
        cached_result = cache.get_query_analysis(query)

        if cached_result is not None:
            return cached_result

        result = func(self, query)
        cache.set_query_analysis(query, result)
        return result

    return wrapper


def cache_search_results(func):
    """Decorator to cache search results."""

    @wraps(func)
    def wrapper(self, query: str, namespace: str, k: int):
        cache = get_cache_manager()
        cached_result = cache.get_search_results(query, namespace, k)

        if cached_result is not None:
            return cached_result

        result = func(self, query, namespace, k)
        cache.set_search_results(query, namespace, k, result)
        return result

    return wrapper
