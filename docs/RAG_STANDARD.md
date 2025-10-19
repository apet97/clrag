# RAG Standard v1: Specification & Status

## Vision
A lean, deterministic RAG layer for Clockify help content retrieval with strict axioms on correctness, latency, and grounding.

## Non-Negotiable Axioms (A1–A8)

| Axiom | Requirement | Status |
|-------|------------|--------|
| **A1** | Determinism | Same corpus+config → identical top-3 results |
| **A2** | Grounding | Every /chat sentence supported by ≥1 cited chunk |
| **A3** | Recall | 10-item gold set: ≥80% have support in top-5 |
| **A4** | Allowlist | Citations only from approved domains |
| **A5** | Canonicalization | URL variants collapse to one doc_id |
| **A6** | Chunking | Max 1200 tokens, ≤10% overflow, overlap ≈150±20 |
| **A7** | Latency | /search p95 ≤300 ms on 20-query batch |
| **A8** | No Weakening | Tests never stripped or relaxed |

## Architecture

### Modules (src/rag/)
```
src/rag/
├── __init__.py
├── vocab.py          # Vocabulary from glossary.csv; alias matching
├── chunk.py          # Sentence-aware, token-aware chunker (→ A6)
├── embed.py          # Ollama embeddings; L2 normalize
├── index_faiss.py    # FAISS FlatIP; save/load
├── query_expand.py   # Expand with glossary aliases
├── retrieval.py      # Vector top_k_raw=50 → re-score → k (→ A1, A4, A7)
├── pipeline.py       # Orchestration: ingest() → embed_index() → retrieve()
├── metrics.py        # Latency timers for p50/p95
└── canonicalize.py   # URL normalization (→ A5)
```

### API Contracts

#### GET /search
```json
{
  "query": "How do I submit a timesheet?",
  "k": 5,
  "results": [
    {
      "url": "https://help.clockify.me/article/...",
      "title": "Submit Timesheet",
      "snippet": "To submit a timesheet, click...",
      "score": 0.92,
      "chunk_id": "doc_id:3",
      "glossary_terms": ["timesheet", "submit"]
    }
  ]
}
```

#### POST /chat
```json
{
  "question": "How do I submit a weekly timesheet?",
  "answer": "To submit a weekly timesheet, go to the Timesheets tab and click Submit...",
  "citations": ["doc_id:3", "doc_id:7"],
  "citation_map": {
    "doc_id:3": {
      "url": "https://help.clockify.me/article/xyz",
      "title": "Submit Timesheet"
    }
  }
}
```

#### GET /health (enhanced)
```json
{
  "rag_ok": true,
  "rag_details": "Index loaded: 1250 chunks, 4 namespaces",
  "index_metrics": {
    "total_chunks": 1250,
    "total_vectors": 1250,
    "dimension": 768
  }
}
```

### Configuration (.env)

```bash
# RAG Configuration
RAG_ALLOWLIST_DOMAINS=help.clockify.me,clockify.me
RAG_CRAWL_START_URLS=https://help.clockify.me/
RAG_MAX_PAGES=500

# Chunking
RAG_CHUNK_MIN_TOKENS=800
RAG_CHUNK_MAX_TOKENS=1200
RAG_CHUNK_OVERLAP=150

# Embeddings
RAG_EMBEDDING_BACKEND=ollama
RAG_EMBEDDING_MODEL=nomic-embed-text:latest

# Retrieval
RAG_INDEX_TYPE=flat
RAG_TOP_K=5
RAG_TOP_K_RAW=50
RAG_USE_BM25=false

# Performance budget
RAG_P95_SEARCH_MS=300
```

## Test Strategy

### A1–A3: Correctness (unit + integration)
- **test_chunker.py** → A6 enforcement
- **test_vocab.py** → deterministic alias matching
- **test_canonicalization.py** → A5 URL normalization
- **test_retrieval.py** → A1 (same inputs = same top-3), A4 (allowlist), A7 (latency)
- **test_rag_e2e.py** → A3 (10-item gold set ≥80% recall @ top-5)

### A2: Grounding (post-generation check)
- Parse LLM response for citations
- Verify each sentence has ≥1 citation
- Track in /chat response

### Fixtures
```
tests/fixtures/
├── clockify_help_page1.html     # Sample Clockify page
├── clockify_help_page2.html     # Another page
├── tiny_faiss_index.bin         # Pre-built FAISS for determinism
└── tiny_vocabulary.json         # Glossary slice
```

## Running RAG Standard v1

```bash
# 1. Setup and build vocabulary
source .venv/bin/activate
python src/rag/vocab.py --build data/glossary.csv --output data/vocabulary.json

# 2. Run tests (all axioms)
pytest tests/test_chunker.py tests/test_vocab.py tests/test_canonicalization.py \
        tests/test_retrieval.py tests/test_rag_e2e.py -v

# 3. Start server
make serve &

# 4. Test endpoints
curl 'http://localhost:7000/search?q=timesheet&k=5'
curl -X POST http://localhost:7000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question": "How do I submit a timesheet?"}'
```

## Checkpoints

- [ ] Vocabulary loads deterministically (A1)
- [ ] Chunks meet max token and overlap constraints (A6)
- [ ] URLs canonicalize correctly (A5)
- [ ] /search returns allowlisted domains only (A4)
- [ ] /search p95 latency < 300ms on 20 queries (A7)
- [ ] 10-item gold set achieves ≥80% recall @ top-5 (A3)
- [ ] /chat citations grounded in retrieved chunks (A2)
- [ ] All tests preserve original thresholds (A8)

## Known Limitations & Next Steps

1. **Live Crawling**: Makefile target `make crawl` uses fixtures for tests; live crawl separate
2. **BM25 Hybrid**: Disabled by default (RAG_USE_BM25=false); can enable for recall boost
3. **Reranking**: Cross-encoder reranking available but not in critical path
4. **Streaming**: /chat does not stream; single response with full citations

---

**Branch**: `rag-standard-v1`
**Target**: Commit with all A1–A8 passing
