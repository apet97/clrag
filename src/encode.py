"""
Query encoding with caching, normalization, and thread-safe model loading.

AXIOM 3: Use sentence-transformers "intfloat/multilingual-e5-base".
Normalize vectors to unit length before indexing and querying.
"""

import os
import threading
from functools import lru_cache
from typing import Optional

import numpy as np
from loguru import logger
from sentence_transformers import SentenceTransformer


# Thread-safe global model
_model_lock = threading.Lock()
_model: Optional[SentenceTransformer] = None


def _get_model() -> SentenceTransformer:
    """Lazy-load embedding model with thread safety."""
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                model_name = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-base")
                logger.info(f"Loading embedding model: {model_name}")
                _model = SentenceTransformer(model_name)
                _model.max_seq_length = 512
                logger.info(f"Model loaded. Embedding dimension: {_model.get_sentence_embedding_dimension()}")
    return _model


@lru_cache(maxsize=512)
def _encode_cached(text: str) -> tuple:
    """
    Encode text to normalized embedding with LRU cache.
    Cache uses tuple (cached numpy arrays not allowed, so return as tuple).
    """
    model = _get_model()
    # Encode with normalization
    embedding = model.encode(
        [text.strip()],
        convert_to_numpy=True,
        normalize_embeddings=True  # AXIOM 3: Normalize to unit vectors
    )[0]
    # Verify normalization
    norm = np.linalg.norm(embedding)
    if not (0.99 <= norm <= 1.01):  # Allow small float error
        embedding = embedding / (norm + 1e-8)
    return tuple(embedding)


def encode_query(text: str) -> np.ndarray:
    """
    Encode a single query string to normalized embedding.
    Uses LRU cache to avoid re-encoding.
    """
    cached_tuple = _encode_cached(text.strip())
    return np.array(cached_tuple, dtype=np.float32)


def encode_texts(texts: list[str]) -> np.ndarray:
    """
    Encode multiple texts to normalized embeddings (batch).
    Returns matrix of shape (len(texts), embedding_dim).
    """
    model = _get_model()
    texts_stripped = [t.strip() for t in texts]
    embeddings = model.encode(
        texts_stripped,
        convert_to_numpy=True,
        normalize_embeddings=True  # AXIOM 3: Normalize
    )
    return embeddings.astype(np.float32)


def get_embedding_dimension() -> int:
    """Return embedding dimension for FAISS index setup."""
    model = _get_model()
    return model.get_sentence_embedding_dimension()


def warmup():
    """Warmup embedding model with anchor queries to compile kernels."""
    logger.info("Warming up embedding model...")
    anchor_terms = [
        "timesheet",
        "project",
        "kiosk",
        "invoice",
        "time off",
        "billable rate",
        "estimate",
        "sso",
    ]
    try:
        for term in anchor_terms:
            _ = encode_query(term)
        logger.info(f"Warmup complete. LRU cache size: {_encode_cached.cache_info().currsize}")
    except Exception as e:
        logger.warning(f"Warmup failed: {e}")


if __name__ == "__main__":
    # Test normalization
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
