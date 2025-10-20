"""
Query encoding with Ollama via /api/embeddings endpoint.
L2 normalization and LRU caching. Deterministic, offline-first.

AXIOM 3: Normalize vectors to unit length before indexing and querying.
"""

import os
import requests
from functools import lru_cache
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import numpy as np
from loguru import logger

OLLAMA_BASE_URL = os.getenv("LLM_BASE_URL", "http://10.127.0.192:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text:latest")

logger.info(f"Encoding: Ollama at {OLLAMA_BASE_URL}, model {EMBEDDING_MODEL}")

# Connection pooling for batch embeddings (faster than per-request connections)
_session = None

def _get_session() -> requests.Session:
    """Get or create a requests session with connection pooling."""
    global _session
    if _session is None:
        _session = requests.Session()
        # Retry strategy: 3 retries with exponential backoff
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=10)
        _session.mount("http://", adapter)
        _session.mount("https://", adapter)
        logger.debug("HTTP session initialized with connection pooling")
    return _session


@lru_cache(maxsize=512)
def _encode_cached(text: str) -> tuple:
    """
    Encode text via Ollama /api/embeddings with LRU cache.
    Returns tuple (for hashable caching). L2-normalized.
    """
    try:
        url = f"{OLLAMA_BASE_URL}/api/embeddings"
        payload = {"model": EMBEDDING_MODEL, "prompt": text.strip()}
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code != 200:
            logger.error(f"Ollama /api/embeddings: {resp.status_code} {resp.text[:200]}")
            raise RuntimeError(f"Ollama failed: {resp.status_code}")

        data = resp.json()
        embedding = np.array(data.get("embedding"), dtype=np.float32)

        # L2 normalize (AXIOM 3)
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        return tuple(embedding)
    except Exception as e:
        logger.error(f"Encoding error: {e}")
        raise


def encode_query(text: str) -> np.ndarray:
    """
    Encode single query with LRU cache + L2 normalization.
    """
    cached_tuple = _encode_cached(text.strip())
    return np.array(cached_tuple, dtype=np.float32)


def encode_texts(texts: list[str]) -> np.ndarray:
    """
    Batch encode texts via Ollama with connection pooling (no cache, deterministic, L2-normalized).
    Returns matrix of shape (len(texts), embedding_dim).

    Connection pooling provides 30-50% latency improvement over per-request connections.
    """
    try:
        url = f"{OLLAMA_BASE_URL}/api/embeddings"
        embeddings = []
        session = _get_session()

        for text in texts:
            payload = {"model": EMBEDDING_MODEL, "prompt": text.strip()}
            resp = session.post(url, json=payload, timeout=30)
            if resp.status_code != 200:
                logger.error(f"Ollama batch embedding: {resp.status_code}")
                raise RuntimeError(f"Ollama failed: {resp.status_code}")

            data = resp.json()
            embedding = np.array(data.get("embedding"), dtype=np.float32)

            # L2 normalize (AXIOM 3)
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm

            embeddings.append(embedding)

        return np.array(embeddings, dtype=np.float32)
    except Exception as e:
        logger.error(f"Batch encoding error: {e}")
        raise


def warmup():
    """Test Ollama connectivity and embedding model readiness."""
    logger.info(f"Testing Ollama at {OLLAMA_BASE_URL}...")
    try:
        url = f"{OLLAMA_BASE_URL}/api/embeddings"
        payload = {"model": EMBEDDING_MODEL, "prompt": "test"}
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            dim = len(data.get("embedding", []))
            logger.info(f"✓ Ollama ready: {EMBEDDING_MODEL} (dim={dim})")
        else:
            logger.warning(f"Ollama status {resp.status_code}")
    except Exception as e:
        logger.warning(f"Ollama test failed: {e}")


if __name__ == "__main__":
    # Test single query
    vec = encode_query("test query")
    norm = np.linalg.norm(vec)
    print(f"Single query embedding norm: {norm:.6f} (should be ~1.0)")
    assert 0.99 <= norm <= 1.01, f"Normalization failed: {norm}"

    # Test batch
    vecs = encode_texts(["query 1", "query 2", "query 3"])
    print(f"Batch shape: {vecs.shape}")
    for i, v in enumerate(vecs):
        n = np.linalg.norm(v)
        print(f"  Vector {i} norm: {n:.6f}")
        assert 0.99 <= n <= 1.01, f"Batch normalization failed on vector {i}: {n}"

    print("✓ All encoding tests passed")
