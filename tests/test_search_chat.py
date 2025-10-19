"""Test search and chat endpoints."""

import os
import json
import pytest
import importlib
from pathlib import Path

# Skip tests if index is missing
INDEX_DIR = Path("index/faiss")
SKIP_IF_NO_INDEX = pytest.mark.skipif(
    not (INDEX_DIR / "clockify" / "index.bin").exists(),
    reason="FAISS index not found. Run 'make embed' first."
)


@SKIP_IF_NO_INDEX
def test_search_endpoint_mock(client):
    """Test /search endpoint with mock mode."""
    os.environ["MOCK_LLM"] = "true"

    response = client.get(
        "/search?q=timesheet&k=5",
        headers={"x-api-token": "change-me"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) >= 1, "Should retrieve at least 1 result"

    # Check result structure
    result = data["results"][0]
    assert "score" in result
    assert "title" in result or "url" in result
    assert 0 <= result["score"] <= 2.0, "Cosine score should be in [0, 2] range"


@SKIP_IF_NO_INDEX
def test_chat_endpoint_mock(client):
    """Test /chat endpoint with mock mode."""
    os.environ["MOCK_LLM"] = "true"

    response = client.post(
        "/chat",
        json={
            "question": "How do I create a project?",
            "k": 5,
            "namespace": None
        },
        headers={"x-api-token": "change-me"}
    )

    assert response.status_code == 200
    data = response.json()

    # Check response structure
    assert "answer" in data
    assert "sources" in data
    assert "latency_ms" in data
    assert "meta" in data

    # Check non-empty answer and sources
    assert len(data["answer"]) > 0, "Answer should not be empty"
    assert isinstance(data["sources"], list), "Sources should be a list"
    assert len(data["sources"]) > 0, "Should have at least 1 source"

    # Check source structure
    source = data["sources"][0]
    assert "title" in source or "url" in source
    assert "namespace" in source
    assert "score" in source

    # Check latency breakdown
    assert "retrieval" in data["latency_ms"]
    assert "llm" in data["latency_ms"]
    assert "total" in data["latency_ms"]


@SKIP_IF_NO_INDEX
def test_health_endpoint(client):
    """Test /health endpoint shows index normalization."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert "ok" in data
    assert "namespaces" in data
    assert "index_normalized" in data

    # If indexes are loaded, they should be normalized
    if data["ok"]:
        assert data["index_normalized"] is True, "Indexes should be L2-normalized"


@SKIP_IF_NO_INDEX
def test_chat_non_streaming_when_disabled(client):
    """Ensure /chat works with stream=false when STREAMING_ENABLED=false."""
    os.environ["MOCK_LLM"] = "true"
    os.environ["STREAMING_ENABLED"] = "false"
    import src.server
    importlib.reload(src.server)
    from src.server import app as reloaded_app
    from fastapi.testclient import TestClient
    client_reloaded = TestClient(reloaded_app)

    payload = {"question": "ping?", "k": 1}
    r = client_reloaded.post("/chat", json=payload, headers={"x-api-token": "change-me"})
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)


@pytest.fixture
def client():
    """FastAPI test client."""
    from fastapi.testclient import TestClient
    from src.server import app

    return TestClient(app)
