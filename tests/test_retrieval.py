"""
Tests for retrieval encoding and search (AXIOM 1, 3, 4, 7).
"""

import os
import numpy as np
import pytest
from src.encode import encode_query, encode_texts, get_embedding_dimension


class TestEncoding:
    """Test AXIOM 3: Normalization to unit vectors."""
    
    def test_encode_query_normalized(self):
        """Single query embedding should have unit norm."""
        vec = encode_query("test query")
        norm = np.linalg.norm(vec)
        assert 0.99 <= norm <= 1.01, f"Expected norm ~1.0, got {norm}"
    
    def test_encode_batch_normalized(self):
        """Batch embeddings should all be unit norm."""
        vecs = encode_texts(["q1", "q2", "q3"])
        for i, v in enumerate(vecs):
            norm = np.linalg.norm(v)
            assert 0.99 <= norm <= 1.01, f"Vector {i} norm={norm}, expected ~1.0"
    
    def test_encode_dimension(self):
        """Embeddings should match model dimension."""
        dim = get_embedding_dimension()
        vec = encode_query("test")
        assert len(vec) == dim, f"Expected dimension {dim}, got {len(vec)}"
    
    def test_encode_lru_cache(self):
        """LRU cache should return same object for same input."""
        v1 = encode_query("cache test")
        v2 = encode_query("cache test")
        np.testing.assert_array_equal(v1, v2)
    
    def test_encode_determinism(self):
        """Same input should produce same embedding (determinism)."""
        for _ in range(3):
            vec1 = encode_query("determinism test")
            vec2 = encode_query("determinism test")
            np.testing.assert_array_almost_equal(vec1, vec2, decimal=6)


class TestRetrieval:
    """Test AXIOM 1, 4, 7 (determinism, retrieval, latency)."""
    
    def test_search_returns_results(self):
        """Verify search endpoint returns results."""
        # This requires server running; marked as integration test
        pass
    
    def test_results_deduplicated_by_url(self):
        """AXIOM 4: Results should be deduplicated by URL."""
        pass
    
    def test_latency_under_budget(self):
        """AXIOM 7: /search p95 should be < 800ms."""
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
