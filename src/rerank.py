#!/usr/bin/env python3
"""Cross-encoder reranking for result quality improvement."""

import logging
import os
from typing import List, Dict
from dotenv import load_dotenv

try:
    from sentence_transformers import CrossEncoder
except ImportError:
    CrossEncoder = None

load_dotenv()

logger = logging.getLogger(__name__)

USE_RERANKER = os.getenv("USE_RERANKER", "true").lower() == "true"
RERANKER_MODEL = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-base")
RERANKER_BATCH_SIZE = int(os.getenv("RERANKER_BATCH_SIZE", "32"))
RERANKER_TOP_K = int(os.getenv("RERANKER_TOP_K", "5"))

_reranker = None


def init_reranker():
    """Load reranker model on first use."""
    global _reranker
    if USE_RERANKER and _reranker is None:
        if not CrossEncoder:
            logger.warning("sentence-transformers not available; reranking disabled")
            return None
        try:
            _reranker = CrossEncoder(RERANKER_MODEL)
            logger.info(f"✓ Loaded reranker: {RERANKER_MODEL}")
        except Exception as e:
            logger.error(f"Failed to load reranker: {e}")
    return _reranker


def rerank(query: str, chunks: List[Dict], top_k: int = RERANKER_TOP_K) -> List[Dict]:
    """Rerank chunks using cross-encoder."""
    if not USE_RERANKER or len(chunks) == 0:
        return chunks

    reranker = init_reranker()
    if not reranker:
        return chunks

    try:
        # Prepare pairs
        pairs = [[query, c["text"]] for c in chunks]

        # Score
        scores = reranker.predict(pairs, batch_size=RERANKER_BATCH_SIZE)

        # Sort by score
        ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)

        # Return top_k with new scores
        result = []
        for chunk, score in ranked[:top_k]:
            chunk["rerank_score"] = float(score)
            result.append(chunk)

        logger.debug(f"Reranked {len(chunks)} → {len(result)} chunks")
        return result

    except Exception as e:
        logger.error(f"Reranking error: {e}")
        return chunks[:top_k]
