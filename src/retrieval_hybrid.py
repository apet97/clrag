#!/usr/bin/env python3
"""Hybrid retrieval: fusion of dense embeddings and BM25 lexical search."""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None
    logging.warning("rank_bm25 not installed; BM25 scoring will be unavailable")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class HybridRetriever:
    """Combine dense vector search and BM25 lexical search with late fusion."""

    def __init__(
        self,
        alpha: float = 0.6,
        k_dense: int = 40,
        k_bm25: int = 40,
        k_final: int = 12,
    ):
        """
        Initialize hybrid retriever.

        Args:
            alpha: Weight for dense search (0-1). Final score = alpha*dense + (1-alpha)*bm25
            k_dense: Number of results from dense search
            k_bm25: Number of results from BM25 search
            k_final: Number of final results to return
        """
        self.alpha = max(0, min(1, alpha))  # Clamp to [0, 1]
        self.k_dense = k_dense
        self.k_bm25 = k_bm25
        self.k_final = k_final
        self.bm25_index: Optional[BM25Okapi] = None
        self.chunks: List[Dict] = []

    def build_bm25_index(self, chunks: List[Dict]) -> bool:
        """
        Build BM25 index from chunks.

        Args:
            chunks: List of chunk dicts with 'text', 'title', 'section' fields

        Returns:
            True if index built successfully
        """
        if not BM25Okapi:
            logger.warning("rank_bm25 not available; BM25 indexing disabled")
            return False

        self.chunks = chunks
        corpus = []

        for chunk in chunks:
            # Combine text, title, and section for ranking
            text = chunk.get("text", "")
            title = chunk.get("title", "")
            section = chunk.get("section", "")
            combined = f"{title} {section} {text}".strip()
            corpus.append(combined.split())

        if not corpus:
            logger.warning("Empty corpus for BM25 indexing")
            return False

        self.bm25_index = BM25Okapi(corpus)
        logger.info(f"Built BM25 index for {len(corpus)} chunks")
        return True

    def _normalize_scores(self, scores: np.ndarray) -> np.ndarray:
        """Min-max normalize scores to [0, 1]."""
        if len(scores) == 0:
            return scores
        min_val = scores.min()
        max_val = scores.max()
        if max_val == min_val:
            return np.ones_like(scores)
        return (scores - min_val) / (max_val - min_val + 1e-9)

    def retrieve_dense(
        self,
        query_embedding: np.ndarray,
        faiss_index: "faiss.Index",
        chunk_ids: List[int],
    ) -> List[Tuple[int, float]]:
        """
        Retrieve top-k results using dense embeddings.

        Args:
            query_embedding: Query embedding (1, dim)
            faiss_index: FAISS index
            chunk_ids: List of chunk IDs in FAISS

        Returns:
            List of (chunk_id, score) tuples
        """
        if faiss_index is None or len(chunk_ids) == 0:
            return []

        D, I = faiss_index.search(query_embedding, min(self.k_dense, len(chunk_ids)))

        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx >= 0 and idx < len(chunk_ids):
                results.append((chunk_ids[idx], float(dist)))

        return results

    def retrieve_bm25(self, query: str) -> List[Tuple[int, float]]:
        """
        Retrieve top-k results using BM25.

        Args:
            query: Text query

        Returns:
            List of (chunk_index, score) tuples
        """
        if not self.bm25_index or not self.chunks:
            return []

        tokens = query.lower().split()
        scores = self.bm25_index.get_scores(tokens)

        # Get top-k indices by score, include all non-zero results
        top_indices = np.argsort(-scores)[: min(self.k_bm25, len(scores))]

        results = []
        for idx in top_indices:
            results.append((idx, float(scores[idx])))

        # Filter out zeros only if we have results
        if results and all(score == 0.0 for _, score in results):
            return []

        return [r for r in results if r[1] > 0.0] or results[0:1]

    def fuse_results(
        self,
        dense_results: List[Tuple[int, float]],
        bm25_results: List[Tuple[int, float]],
    ) -> List[Tuple[int, float]]:
        """
        Fuse dense and BM25 results using late fusion.

        Args:
            dense_results: Results from dense search (chunk_id, score)
            bm25_results: Results from BM25 search (chunk_index, score)

        Returns:
            Sorted list of (chunk_id, fused_score) tuples
        """
        # Normalize scores to [0, 1]
        dense_dict = {}
        if dense_results:
            dense_scores = np.array([s for _, s in dense_results])
            normalized_dense = self._normalize_scores(dense_scores)
            for (chunk_id, _), norm_score in zip(dense_results, normalized_dense):
                dense_dict[chunk_id] = norm_score

        bm25_dict = {}
        if bm25_results:
            bm25_scores = np.array([s for _, s in bm25_results])
            normalized_bm25 = self._normalize_scores(bm25_scores)
            for (chunk_idx, _), norm_score in zip(bm25_results, normalized_bm25):
                bm25_dict[chunk_idx] = norm_score

        # Fuse: only alpha matters for dense, 1-alpha for BM25
        fused = {}
        all_keys = set(dense_dict.keys()) | set(bm25_dict.keys())

        for key in all_keys:
            dense_score = dense_dict.get(key, 0.0)
            bm25_score = bm25_dict.get(key, 0.0)
            fused[key] = self.alpha * dense_score + (1 - self.alpha) * bm25_score

        # Sort by fused score
        sorted_results = sorted(fused.items(), key=lambda x: x[1], reverse=True)
        return sorted_results[: self.k_final]

    def retrieve(
        self,
        query: str,
        query_embedding: np.ndarray,
        faiss_index: "faiss.Index" = None,
        chunk_ids: List[int] = None,
    ) -> List[Dict]:
        """
        Perform hybrid retrieval: dense + BM25 + fusion.

        Args:
            query: Text query
            query_embedding: Query embedding
            faiss_index: FAISS index (optional, for dense search)
            chunk_ids: Mapping of FAISS indices to chunk IDs (optional)

        Returns:
            List of (chunk_dict, fused_score) tuples
        """
        dense_results = []
        if faiss_index is not None and chunk_ids:
            dense_results = self.retrieve_dense(query_embedding, faiss_index, chunk_ids)

        bm25_results = self.retrieve_bm25(query)

        fused = self.fuse_results(dense_results, bm25_results)

        # Map back to chunk dicts
        results = []
        for chunk_id, score in fused:
            if chunk_id < len(self.chunks):
                chunk = self.chunks[chunk_id].copy()
                chunk["hybrid_score"] = score
                results.append(chunk)

        return results


# Global hybrid retriever instance
_hybrid_retriever: Optional[HybridRetriever] = None


def get_hybrid_retriever() -> HybridRetriever:
    """Get or create global hybrid retriever instance."""
    global _hybrid_retriever
    if _hybrid_retriever is None:
        alpha = float(os.getenv("HYBRID_ALPHA", "0.6"))
        k_dense = int(os.getenv("K_DENSE", "40"))
        k_bm25 = int(os.getenv("K_BM25", "40"))
        k_final = int(os.getenv("K_FINAL", "12"))
        _hybrid_retriever = HybridRetriever(alpha, k_dense, k_bm25, k_final)
    return _hybrid_retriever


if __name__ == "__main__":
    # Test hybrid retriever
    retriever = HybridRetriever(alpha=0.6)

    # Mock chunks
    chunks = [
        {
            "id": 0,
            "text": "PTO is paid time off for employees",
            "title": "PTO Policy",
            "section": "Benefits",
        },
        {
            "id": 1,
            "text": "Billable rate is the rate charged to clients",
            "title": "Billing Rates",
            "section": "Pricing",
        },
        {
            "id": 2,
            "text": "A timesheet is a record of work hours",
            "title": "Timesheets",
            "section": "Tracking",
        },
    ]

    retriever.build_bm25_index(chunks)

    # Test BM25 retrieval
    query = "What is PTO?"
    results = retriever.retrieve_bm25(query)
    print(f"Query: {query}")
    print(f"BM25 Results: {results}")
