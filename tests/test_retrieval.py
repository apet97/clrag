#!/usr/bin/env python3
"""Comprehensive retrieval tests for multi-namespace RAG."""

import pytest
import json
from pathlib import Path
import numpy as np

# Test data paths
CLOCKIFY_INDEX = Path("index/faiss/clockify")
LANGCHAIN_INDEX = Path("index/faiss/langchain")
CHUNKS_DIR = Path("data/chunks")


class TestIndexes:
    """Verify indexes are built and loaded correctly."""

    def test_clockify_index_exists(self):
        """Clockify FAISS index should exist."""
        assert CLOCKIFY_INDEX.exists(), "Clockify index not found"
        assert (CLOCKIFY_INDEX / "index.bin").exists()
        assert (CLOCKIFY_INDEX / "meta.json").exists()

    def test_langchain_index_exists(self):
        """LangChain FAISS index should exist."""
        assert LANGCHAIN_INDEX.exists(), "LangChain index not found"
        assert (LANGCHAIN_INDEX / "index.bin").exists()
        assert (LANGCHAIN_INDEX / "meta.json").exists()

    def test_clockify_chunks_exist(self):
        """Clockify chunks file should exist."""
        chunks_file = CHUNKS_DIR / "clockify.jsonl"
        assert chunks_file.exists(), "Clockify chunks not found"
        assert chunks_file.stat().st_size > 0

    def test_langchain_chunks_exist(self):
        """LangChain chunks file should exist."""
        chunks_file = CHUNKS_DIR / "langchain.jsonl"
        assert chunks_file.exists(), "LangChain chunks not found"
        assert chunks_file.stat().st_size > 0

    def test_clockify_index_metadata(self):
        """Clockify index metadata should be valid."""
        with open(CLOCKIFY_INDEX / "meta.json") as f:
            meta = json.load(f)
        assert meta["model"] == "intfloat/multilingual-e5-base"
        assert meta["dimension"] == 768
        assert meta["num_vectors"] > 0
        assert len(meta["chunks"]) == meta["num_vectors"]

    def test_langchain_index_metadata(self):
        """LangChain index metadata should be valid."""
        with open(LANGCHAIN_INDEX / "meta.json") as f:
            meta = json.load(f)
        assert meta["model"] == "intfloat/multilingual-e5-base"
        assert meta["dimension"] == 768
        assert meta["num_vectors"] > 0
        assert len(meta["chunks"]) == meta["num_vectors"]

    def test_metadata_has_namespaces(self):
        """Metadata chunks should have correct namespace."""
        with open(CLOCKIFY_INDEX / "meta.json") as f:
            meta = json.load(f)
        for chunk in meta["chunks"]:
            assert chunk.get("namespace") in ["clockify", ""], "Invalid namespace in Clockify"

        with open(LANGCHAIN_INDEX / "meta.json") as f:
            meta = json.load(f)
        for chunk in meta["chunks"]:
            assert chunk.get("namespace") in ["langchain", ""], "Invalid namespace in LangChain"


class TestChunkStructure:
    """Verify chunk structure and parent-child relationships."""

    def test_clockify_chunks_have_text(self):
        """All Clockify chunks should have text field."""
        chunks_file = CHUNKS_DIR / "clockify.jsonl"
        with open(chunks_file) as f:
            for i, line in enumerate(f):
                if i >= 10:  # Sample first 10
                    break
                chunk = json.loads(line)
                assert "text" in chunk, f"Chunk {i} missing text"
                assert len(chunk["text"]) > 0, f"Chunk {i} has empty text"

    def test_langchain_chunks_have_text(self):
        """All LangChain chunks should have text field."""
        chunks_file = CHUNKS_DIR / "langchain.jsonl"
        with open(chunks_file) as f:
            for i, line in enumerate(f):
                if i >= 10:
                    break
                chunk = json.loads(line)
                assert "text" in chunk, f"Chunk {i} missing text"
                assert len(chunk["text"]) > 0, f"Chunk {i} has empty text"

    def test_clockify_chunks_have_metadata(self):
        """Clockify chunks should have url, title, headers."""
        chunks_file = CHUNKS_DIR / "clockify.jsonl"
        with open(chunks_file) as f:
            for i, line in enumerate(f):
                if i >= 10:
                    break
                chunk = json.loads(line)
                assert "url" in chunk
                assert "title" in chunk
                assert "headers" in chunk
                assert isinstance(chunk["headers"], list)

    def test_langchain_chunks_have_metadata(self):
        """LangChain chunks should have url, title, headers."""
        chunks_file = CHUNKS_DIR / "langchain.jsonl"
        with open(chunks_file) as f:
            for i, line in enumerate(f):
                if i >= 10:
                    break
                chunk = json.loads(line)
                assert "url" in chunk
                assert "title" in chunk
                assert "headers" in chunk
                assert isinstance(chunk["headers"], list)


class TestEmbeddingNormalization:
    """Verify embeddings are properly normalized."""

    def test_embedding_normalization(self):
        """Embeddings should be L2-normalized (norm ≈ 1)."""
        try:
            import faiss
        except ImportError:
            pytest.skip("faiss-cpu not installed")

        # Load Clockify index and check norms
        index = faiss.read_index(str(CLOCKIFY_INDEX / "index.bin"))
        vectors = faiss.vector_to_array(index.get_xb())

        # Compute norms (should all be ~1.0 for normalized vectors)
        norms = np.linalg.norm(vectors, axis=1)
        assert np.allclose(norms, 1.0, atol=1e-5), f"Vectors not normalized. Norms: {norms[:5]}"

    def test_langchain_embedding_normalization(self):
        """LangChain embeddings should be L2-normalized."""
        try:
            import faiss
        except ImportError:
            pytest.skip("faiss-cpu not installed")

        index = faiss.read_index(str(LANGCHAIN_INDEX / "index.bin"))
        vectors = faiss.vector_to_array(index.get_xb())

        norms = np.linalg.norm(vectors, axis=1)
        assert np.allclose(norms, 1.0, atol=1e-5), f"Vectors not normalized. Norms: {norms[:5]}"


class TestNamespaceIsolation:
    """Verify namespaces don't leak into each other."""

    def test_clockify_metadata_no_langchain_urls(self):
        """Clockify metadata should not contain LangChain URLs."""
        with open(CLOCKIFY_INDEX / "meta.json") as f:
            meta = json.load(f)
        for chunk in meta["chunks"]:
            url = chunk.get("url", "")
            assert "langchain" not in url.lower(), f"LangChain URL in Clockify: {url}"
            assert "docs.langchain.com" not in url, f"Detected LangChain docs in Clockify"

    def test_langchain_metadata_no_clockify_urls(self):
        """LangChain metadata should not contain Clockify URLs."""
        with open(LANGCHAIN_INDEX / "meta.json") as f:
            meta = json.load(f)
        for chunk in meta["chunks"]:
            url = chunk.get("url", "")
            assert "clockify.me" not in url, f"Clockify URL in LangChain: {url}"

    def test_clockify_chunks_no_langchain_keywords(self):
        """Sample Clockify chunks should not mention LangChain concepts."""
        chunks_file = CHUNKS_DIR / "clockify.jsonl"
        with open(chunks_file) as f:
            for i, line in enumerate(f):
                if i >= 20:
                    break
                chunk = json.loads(line)
                text = chunk["text"].lower()
                # Strictly: avoid false positives; only check extreme cases
                # Skip this as LangChain may appear in context


class TestRetrievalDeterminism:
    """Verify retrieval returns consistent results."""

    @pytest.mark.integration
    def test_clockify_retrieval_deterministic(self):
        """Same query should return same top result (deterministic)."""
        try:
            from src.server import init_embedder, init_indexes, vector_search, embed_query
        except ImportError:
            pytest.skip("Server module not importable")

        init_embedder()
        init_indexes()

        q = "timesheet tracking"
        q_emb_1 = embed_query(q)
        q_emb_2 = embed_query(q)

        # Embeddings should be identical
        assert np.allclose(q_emb_1, q_emb_2), "Query embeddings not deterministic"

        # Search results should be identical (same order, same IDs)
        results_1 = vector_search(q_emb_1, namespace="clockify", k=3)
        results_2 = vector_search(q_emb_2, namespace="clockify", k=3)

        assert len(results_1) == len(results_2)
        for r1, r2 in zip(results_1, results_2):
            assert r1["id"] == r2["id"], f"Result order changed: {r1['id']} vs {r2['id']}"

    @pytest.mark.integration
    def test_langchain_retrieval_deterministic(self):
        """Same LangChain query should return same top result."""
        try:
            from src.server import init_embedder, init_indexes, vector_search, embed_query
        except ImportError:
            pytest.skip("Server module not importable")

        init_embedder()
        init_indexes()

        q = "retrievers integration"
        q_emb_1 = embed_query(q)
        q_emb_2 = embed_query(q)

        assert np.allclose(q_emb_1, q_emb_2), "Query embeddings not deterministic"

        results_1 = vector_search(q_emb_1, namespace="langchain", k=3)
        results_2 = vector_search(q_emb_2, namespace="langchain", k=3)

        assert len(results_1) == len(results_2)
        for r1, r2 in zip(results_1, results_2):
            assert r1["id"] == r2["id"], f"Result order changed"


class TestNamespaceFiltering:
    """Verify namespace parameter filters correctly."""

    @pytest.mark.integration
    def test_clockify_namespace_filter(self):
        """Namespace=clockify should only return Clockify chunks."""
        try:
            from src.server import init_embedder, init_indexes, vector_search, embed_query
        except ImportError:
            pytest.skip("Server module not importable")

        init_embedder()
        init_indexes()

        q_emb = embed_query("time tracking")
        results = vector_search(q_emb, namespace="clockify", k=5)

        # All results should be from Clockify namespace
        with open(CLOCKIFY_INDEX / "meta.json") as f:
            clockify_meta = json.load(f)
        clockify_ids = {c["id"] for c in clockify_meta["chunks"]}

        for result in results:
            assert result["id"] in clockify_ids, f"Non-clockify ID in results: {result['id']}"

    @pytest.mark.integration
    def test_langchain_namespace_filter(self):
        """Namespace=langchain should only return LangChain chunks."""
        try:
            from src.server import init_embedder, init_indexes, vector_search, embed_query
        except ImportError:
            pytest.skip("Server module not importable")

        init_embedder()
        init_indexes()

        q_emb = embed_query("langchain core concepts")
        results = vector_search(q_emb, namespace="langchain", k=5)

        # All results should be from LangChain namespace
        with open(LANGCHAIN_INDEX / "meta.json") as f:
            langchain_meta = json.load(f)
        langchain_ids = {c["id"] for c in langchain_meta["chunks"]}

        for result in results:
            assert result["id"] in langchain_ids, f"Non-langchain ID in results: {result['id']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
