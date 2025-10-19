"""
Optional cross-encoder reranking.

AXIOM 5: Use "BAAI/bge-reranker-base" if available. If not installed, skip silently.
Never block retrieval on reranker availability.
"""

import os
from typing import Optional

from loguru import logger

try:
    from FlagEmbedding import FlagReranker
    RERANK_AVAILABLE = True
except ImportError:
    RERANK_AVAILABLE = False
    logger.debug("FlagEmbedding not installed. Reranking disabled. Install with: pip install FlagEmbedding")


_reranker: Optional[FlagReranker] = None


def _get_reranker() -> Optional[FlagReranker]:
    """Lazy-load reranker if available."""
    global _reranker
    if not RERANK_AVAILABLE:
        return None

    if _reranker is None:
        try:
            logger.info("Loading reranker model: BAAI/bge-reranker-base")
            _reranker = FlagReranker("BAAI/bge-reranker-base", use_fp16=False)
            logger.info("Reranker loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load reranker: {e}. Continuing without reranking.")
            return None

    return _reranker


def rerank(query: str, docs: list[dict], topk: int) -> list[dict]:
    """
    Rerank documents using cross-encoder if available.
    Falls back to score-based sorting if reranker not available.
    """
    if not docs:
        return []

    reranker = _get_reranker()
    if reranker is None:
        sorted_docs = sorted(docs, key=lambda x: x.get("score", 0), reverse=True)
        return sorted_docs[:topk]

    try:
        pairs = [(query, d.get("text", "")) for d in docs]
        scores = reranker.compute_score(pairs, normalize=True)
        ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        
        out = []
        for doc, score in ranked[:topk]:
            doc_copy = dict(doc)
            doc_copy["score"] = float(score)
            out.append(doc_copy)
        return out
    except Exception as e:
        logger.warning(f"Reranking failed: {e}. Falling back to original scores.")
        sorted_docs = sorted(docs, key=lambda x: x.get("score", 0), reverse=True)
        return sorted_docs[:topk]


def is_available() -> bool:
    """Return whether reranking is available."""
    return RERANK_AVAILABLE and _get_reranker() is not None
