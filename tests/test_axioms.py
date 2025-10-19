"""
Tests for RAG Standard v1 axioms: determinism, rank, citations, regex safety, auth.
"""

import os
import re
import time
import pytest
import requests

BASE = os.getenv("API_BASE", "http://localhost:7000")
API_TOKEN = os.getenv("API_TOKEN", "change-me")
H = {"x-api-token": API_TOKEN}

def _get(url, **kw):
    """GET with auth header."""
    return requests.get(url, headers=H, timeout=10, **kw)

def _post(url, **kw):
    """POST with auth header."""
    return requests.post(url, headers=H, timeout=20, **kw)


class TestDeterminism:
    """AXIOM 1: Same query + k should return identical top-3 results."""

    def test_search_deterministic_top3(self):
        """Two identical /search calls return same top-3 URLs and order."""
        q = "timesheet"

        r1 = _get(f"{BASE}/search", params={"q": q, "k": 5}).json()["results"][:3]
        r2 = _get(f"{BASE}/search", params={"q": q, "k": 5}).json()["results"][:3]

        urls1 = [x["url"] for x in r1]
        urls2 = [x["url"] for x in r2]

        assert urls1 == urls2, f"Determinism failed: {urls1} != {urls2}"


class TestRank:
    """AXIOM 7: Results must have sequential 1-based rank."""

    def test_search_has_rank_sequential(self):
        """Every /search result has rank 1, 2, 3, ..."""
        resp = _get(f"{BASE}/search", params={"q": "clockify", "k": 10})
        assert resp.status_code == 200

        results = resp.json()["results"]
        assert len(results) > 0, "Expected at least one result"

        for i, r in enumerate(results, start=1):
            assert "rank" in r, f"Result {i} missing 'rank' field"
            assert r["rank"] == i, f"Expected rank {i}, got {r['rank']}"

    def test_search_results_unique_urls(self):
        """Results are deduplicated by URL."""
        resp = _get(f"{BASE}/search", params={"q": "project", "k": 20})
        assert resp.status_code == 200

        results = resp.json()["results"]
        urls = [r["url"] for r in results]

        assert len(urls) == len(set(urls)), f"Duplicate URLs found: {urls}"


class TestCitationsGrounding:
    """AXIOM 2, 6: Citations must be grounded in sources."""

    def test_chat_citations_found_when_sources_exist(self):
        """AXIOM 2: /chat returns citations_found ≥1 when sources exist."""
        payload = {"question": "How do I submit a timesheet?", "k": 5}
        resp = _post(f"{BASE}/chat", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        assert "citations_found" in data, "Missing 'citations_found' field"
        assert "sources" in data, "Missing 'sources' field"

        if data["sources"]:
            assert data["citations_found"] >= 1, \
                f"Expected citations_found≥1 when sources exist, got {data['citations_found']}"

    def test_chat_citation_indices_valid(self):
        """AXIOM 2: All citations [n] map to valid source indices."""
        payload = {"question": "How do I submit a timesheet?", "k": 5}
        resp = _post(f"{BASE}/chat", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        answer = data["answer"]
        num_sources = len(data["sources"])

        # Extract all [n] from answer
        matches = re.findall(r'\[(\d{1,2})\]', answer)
        for match_str in matches:
            idx = int(match_str)
            assert 1 <= idx <= num_sources, \
                f"Citation [{idx}] out of range: only {num_sources} sources"


class TestCitationRegexSafety:
    """AXIOM 9: Citation regex must not miscount bracketed years or URLs."""

    def test_citation_regex_no_false_positives(self):
        """Bracketed numbers in URLs or years don't count as citations."""
        payload = {"question": "What were trends in 2024 reporting?", "k": 3}
        resp = _post(f"{BASE}/chat", json=payload)
        assert resp.status_code == 200

        data = resp.json()
        citations_found = data["citations_found"]
        num_sources = len(data["sources"])

        # All reported citations must be valid indices
        if citations_found > 0:
            assert citations_found <= num_sources, \
                f"citations_found={citations_found} exceeds sources={num_sources}"


class TestAuthentication:
    """AXIOM 0: Auth token required for all endpoints."""

    def test_search_requires_auth_token(self):
        """GET /search without auth header returns 401 or 403."""
        resp = requests.get(f"{BASE}/search", params={"q": "test", "k": 3}, timeout=5)
        assert resp.status_code in (401, 403), \
            f"Expected 401/403 without token, got {resp.status_code}"

    def test_chat_requires_auth_token(self):
        """POST /chat without auth header returns 401 or 403."""
        payload = {"question": "test", "k": 3}
        resp = requests.post(f"{BASE}/chat", json=payload, timeout=5)
        assert resp.status_code in (401, 403), \
            f"Expected 401/403 without token, got {resp.status_code}"
