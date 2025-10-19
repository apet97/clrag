"""Hybrid retrieval combining BM25 and vector search with field boosts."""
from __future__ import annotations
import numpy as np
from rank_bm25 import BM25Okapi
from typing import Any


def hybrid_search(
    query: str,
    docs: list[dict[str, Any]],
    embeddings: np.ndarray,
    encoder: Any,
    k_vec: int = 40,
    k_bm25: int = 40,
    k_final: int = 12
) -> list[dict[str, Any]]:
    """
    Hybrid retrieval: combine vector search (cosine) + BM25 with field boosts.

    Args:
        query: Search query
        docs: List of {"text": str, "meta": {...}} dicts
        embeddings: (N, d) array of L2-normalized embeddings
        encoder: Encoder with .embed(str) -> ndarray[d]
        k_vec: Number of vector results to keep
        k_bm25: Number of BM25 results to keep
        k_final: Final number of results

    Returns:
        Top-k merged and re-scored results
    """
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

    # Re-score with boosts
    scores = {}
    for idx in candidate_indices:
        # Base score: weighted average
        vec_score = sims[idx]
        bm25_norm = bm25_scores[idx] / (np.max(bm25_scores) + 1e-9)
        base_score = 0.6 * vec_score + 0.4 * bm25_norm

        # Field boosts
        title = docs[idx].get("meta", {}).get("title", "").lower()
        section = docs[idx].get("meta", {}).get("section", "").lower()
        query_lower = query.lower()
        query_tokens = query_lower.split()

        # Title match boost
        if any(token in title for token in query_tokens):
            base_score += 0.08

        # Section match boost
        if any(token in section for token in query_tokens):
            base_score += 0.05

        # Glossary boost
        if docs[idx].get("meta", {}).get("type") == "glossary":
            base_score += 0.10

        scores[idx] = base_score

    # Sort and return top-k
    top_indices = sorted(scores.keys(), key=lambda i: scores[i], reverse=True)[:k_final]
    results = [docs[i] | {"score": float(scores[i])} for i in top_indices]

    return results
