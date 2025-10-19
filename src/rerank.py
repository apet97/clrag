"""Cross-encoder reranking for improved relevance."""
from __future__ import annotations
import os
from typing import Any


# Module-level singleton for cross-encoder model
_model: Any = None


def load(model_name: str = "BAAI/bge-reranker-large"):
    """
    Load cross-encoder model (lazy singleton).

    Args:
        model_name: Hugging Face model identifier

    Returns:
        Loaded CrossEncoder instance
    """
    global _model

    if _model is None:
        # Optional: skip reranking if RERANKING_DISABLED env var set
        if os.getenv("RERANKING_DISABLED") == "true":
            return None

        try:
            from sentence_transformers import CrossEncoder

            _model = CrossEncoder(model_name, trust_remote_code=True)
        except ImportError:
            import warnings

            warnings.warn(
                "sentence_transformers not installed. Reranking disabled. "
                "Install: pip install sentence_transformers"
            )
            _model = False  # Sentinel: tried and failed

    return None if _model is False else _model


def rerank(
    query: str,
    candidates: list[dict[str, Any]],
    topk: int = 8
) -> list[dict[str, Any]]:
    """
    Rerank candidates using cross-encoder, with fallback if model unavailable.

    Args:
        query: Search query
        candidates: List of {"text": str, "meta": {...}, "score": float} dicts
        topk: Number of results to return

    Returns:
        Reranked candidates (top-k), sorted by rerank score descending
    """
    model = load()

    if model is None:
        # Model unavailable: fall back to original scoring
        return sorted(candidates, key=lambda x: x.get("score", 0.0), reverse=True)[:topk]

    # Compute reranking scores
    pairs = [(query, c["text"]) for c in candidates]

    try:
        scores = model.predict(pairs).tolist()
    except Exception as e:
        import warnings

        warnings.warn(f"Reranking failed ({e}). Falling back to original scores.")
        return sorted(candidates, key=lambda x: x.get("score", 0.0), reverse=True)[:topk]

    # Annotate candidates with rerank score
    for c, s in zip(candidates, scores):
        c["rerank_score"] = float(s)

    # Sort by rerank score and return top-k
    return sorted(candidates, key=lambda x: x.get("rerank_score", 0.0), reverse=True)[:topk]
