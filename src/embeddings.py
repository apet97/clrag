"""Embeddings module using E5 model with correct prefixes and L2 normalization."""

import os
import numpy as np
from typing import Optional
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-base")

_embedder: Optional[SentenceTransformer] = None


def get_embedder() -> SentenceTransformer:
    """Get or load the global embedder instance."""
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBEDDING_MODEL)
        _embedder.max_seq_length = 512
    return _embedder


def embed_passages(texts: list[str]) -> np.ndarray:
    """Embed passages with E5 'passage: ' prefix and L2 normalization.

    Args:
        texts: List of passage texts to embed

    Returns:
        L2-normalized embeddings as float32 array (batch_size, 768)
    """
    prefixed = [f"passage: {text.strip()}" for text in texts]
    embedder = get_embedder()
    embeddings = embedder.encode(prefixed, convert_to_numpy=True).astype(np.float32)
    # L2-normalize: divide by norm + epsilon to avoid division by zero
    embeddings = embeddings / (np.linalg.norm(embeddings, axis=1, keepdims=True) + 1e-12)
    return embeddings


def embed_query(text: str) -> np.ndarray:
    """Embed query with E5 'query: ' prefix and L2 normalization.

    Args:
        text: Query text to embed

    Returns:
        L2-normalized embedding as float32 array (1, 768)
    """
    prefixed = f"query: {text.strip()}"
    embedder = get_embedder()
    embedding = embedder.encode([prefixed], convert_to_numpy=True).astype(np.float32)
    # L2-normalize
    embedding = embedding / (np.linalg.norm(embedding, axis=1, keepdims=True) + 1e-12)
    return embedding
