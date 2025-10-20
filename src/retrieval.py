"""Hybrid retrieval combining BM25 and vector search with field boosts and query-type-aware strategies."""
from __future__ import annotations
import numpy as np
from rank_bm25 import BM25Okapi
from typing import Any
from src.search_improvements import (
    detect_query_type,
    get_field_boost,
    enhance_field_matching,
)


def hybrid_search(
    query: str,
    docs: list[dict[str, Any]],
    embeddings: np.ndarray,
    encoder: Any,
    k_vec: int = 40,
    k_bm25: int = 40,
    k_final: int = 12,
    use_query_adaptation: bool = True,
) -> list[dict[str, Any]]:
    """
    Hybrid retrieval: combine vector search (cosine) + BM25 with adaptive field boosts.

    Improvements:
    - Query type detection for adaptive strategies
    - Enhanced field matching with type-aware boosting
    - Better BM25 handling with glossary terms
    - Improved normalization and score fusion

    Args:
        query: Search query
        docs: List of {"text": str, "meta": {...}} dicts
        embeddings: (N, d) array of L2-normalized embeddings
        encoder: Encoder with .embed(str) -> ndarray[d]
        k_vec: Number of vector results to keep
        k_bm25: Number of BM25 results to keep
        k_final: Final number of results
        use_query_adaptation: Enable adaptive strategies based on query type

    Returns:
        Top-k merged and re-scored results with improved relevance
    """
    # Detect query type for adaptive strategies
    query_type = detect_query_type(query) if use_query_adaptation else "general"

    # Embed query
    qv = encoder.embed(query)
    qv = qv / (np.linalg.norm(qv) + 1e-9)  # L2-normalize

    # Vector similarity (already L2-normalized embeddings)
    sims = embeddings @ qv
    top_vec_indices = np.argsort(-sims)[:k_vec]

    # BM25 scores
    corpus = [d["text"] for d in docs]
    bm25 = BM25Okapi([c.split() for c in corpus])
    bm25_scores = bm25.get_scores(query.split())
    top_bm25_indices = np.argsort(-bm25_scores)[:k_bm25]

    # Union of both
    candidate_indices = np.unique(np.concatenate([top_vec_indices, top_bm25_indices]))

    # Re-score with adaptive boosts
    scores = {}
    query_lower = query.lower()
    query_tokens = query_lower.split()

    for idx in candidate_indices:
        # Base score: weighted average (adjust weights based on query type)
        vec_score = sims[idx]
        bm25_norm = bm25_scores[idx] / (np.max(bm25_scores) + 1e-9)

        # Adaptive weighting based on query type
        if query_type == "factual":
            # Factual queries benefit more from lexical match (BM25)
            base_score = 0.5 * vec_score + 0.5 * bm25_norm
        elif query_type == "how_to":
            # How-to queries favor semantic understanding (embeddings)
            base_score = 0.65 * vec_score + 0.35 * bm25_norm
        else:
            # Default balanced approach
            base_score = 0.6 * vec_score + 0.4 * bm25_norm

        # Get adaptive field boosts based on query type
        doc = docs[idx]
        title = doc.get("meta", {}).get("title", "")
        section = doc.get("meta", {}).get("section", "")
        text = doc.get("text", "")

        # Enhanced field matching (replaces old simple boost logic)
        field_boost = enhance_field_matching(text, title, section, query_tokens, query_type)
        base_score += field_boost

        # Glossary boost (strong signal for definitions)
        if doc.get("meta", {}).get("type") == "glossary":
            glossary_boost = 0.15 if query_type == "definition" else 0.10
            base_score += glossary_boost

        # Normalize final score to [0, 1] range
        base_score = min(base_score, 1.0)

        scores[idx] = base_score

    # Sort and return top-k
    top_indices = sorted(scores.keys(), key=lambda i: scores[i], reverse=True)[:k_final]
    results = [docs[i] | {"score": float(scores[i]), "query_type": query_type} for i in top_indices]

    return results
