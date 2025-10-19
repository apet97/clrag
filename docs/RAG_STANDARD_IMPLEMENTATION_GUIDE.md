# RAG Standard v1: Quick Implementation Guide

## Current Status (Session Summary)

✅ **Completed Production Hardening (Fixes 1-10)**
- Standardized model naming (gpt-oss:20b)
- Python 3.11 + pinned dependencies
- HTTPX hardening with timeouts, pooling, retries
- Bearer token authentication
- Config validation on startup
- Logging sanitization (redact tokens, cap responses)
- /live and /ready health probes
- 24 comprehensive tests for LLM client

✅ **Branch Created**: `rag-standard-v1`

✅ **Documentation**: docs/RAG_STANDARD.md with full spec

## Immediate Next Steps (Critical Path)

### 1. Build Vocabulary Module (src/rag/vocab.py)
```python
# Quick sketch - adapt existing glossary.py
import json
from pathlib import Path

def load_vocabulary(csv_path: str) -> dict:
    """Load glossary CSV → deterministic JSON vocab."""
    terms = {}
    # Read glossary.csv, parse term|aliases|type
    # Store as {term_lower: {term, aliases: [], type, notes}}
    # Sort keys for determinism
    return dict(sorted(terms.items()))

def build_vocabulary_json(csv_path: str, output_path: str):
    vocab = load_vocabulary(csv_path)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    json.dump(vocab, open(output_path, 'w'), indent=2, sort_keys=True)
    print(f"Built vocabulary: {len(vocab)} terms → {output_path}")

def alias_match(query: str, vocab: dict) -> list[str]:
    """Case-insensitive alias matching → A1 determinism."""
    query_lower = query.lower()
    matches = []
    for term, data in vocab.items():
        if query_lower in term or any(query_lower in alias for alias in data.get('aliases', [])):
            matches.append(term)
    return sorted(matches)  # Sort for determinism
```

### 2. Metrics Module (src/rag/metrics.py)
```python
# Track latency for A7 validation
import time
from loguru import logger

class LatencyTracker:
    def __init__(self):
        self.timers = {}

    def start(self, key: str):
        self.timers[key] = time.time()

    def end(self, key: str) -> float:
        if key not in self.timers:
            return 0
        elapsed = time.time() - self.timers[key]
        logger.debug(f"Timer '{key}': {elapsed*1000:.1f}ms")
        return elapsed

tracker = LatencyTracker()
```

### 3. Test Suite for A1–A8

Create minimal fixture-based tests:

```
tests/
├── fixtures/
│   ├── clockify_sample_page.html
│   ├── tiny_faiss_index.bin
│   └── test_vocabulary.json
├── test_chunker.py           # A6: token constraints
├── test_vocab.py             # A1: determinism
├── test_canonicalization.py  # A5: URL variants
├── test_retrieval.py         # A1, A4, A7
└── test_rag_e2e.py          # A2, A3 (gold set)
```

### 4. API Integration

Update src/server.py /search endpoint:
```python
@app.get("/search")
def search(q: str, k: int = 5, ...):
    """Returns {query, k, results: [{url, title, snippet, score, chunk_id}]}"""
    from src.rag.retrieval import retrieve
    from src.rag.metrics import tracker

    tracker.start("search")
    results = retrieve(q, k=k)
    tracker.end("search")

    return {
        "query": q,
        "k": k,
        "results": results
    }

@app.post("/chat")
def chat(req: ChatRequest, ...):
    """Returns {answer, citations: [...], citation_map: {...}}"""
    from src.rag.retrieval import retrieve
    from src.llm_client import LLMClient

    # Retrieve context
    hits = retrieve(req.question, k=5)

    # Build LLM prompt with citations
    context = "\n".join([f"[{i+1}] {h['title']}\n{h['snippet']}"
                         for i, h in enumerate(hits)])

    # Get answer
    llm = LLMClient()
    answer = llm.chat([
        {"role": "system", "content": "Answer only from provided context. Use citations [1], [2], etc."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {req.question}"}
    ])

    # Extract citations from answer (regex: \[(\d+)\])
    import re
    citations = [hits[int(m)-1]['chunk_id'] for m in re.findall(r'\[(\d+)\]', answer) if int(m) <= len(hits)]

    return {
        "answer": answer,
        "citations": citations,
        "citation_map": {h['chunk_id']: {"url": h['url'], "title": h['title']} for h in hits}
    }
```

### 5. Configuration Update

Add to .env.sample:
```bash
# RAG Configuration
RAG_ALLOWLIST_DOMAINS=help.clockify.me,clockify.me
RAG_EMBEDDING_MODEL=nomic-embed-text:latest
RAG_TOP_K=5
RAG_TOP_K_RAW=50
RAG_CHUNK_MIN_TOKENS=800
RAG_CHUNK_MAX_TOKENS=1200
RAG_CHUNK_OVERLAP=150
RAG_P95_SEARCH_MS=300
```

## Testing Axioms

```bash
# A1: Determinism (same inputs → same top-3)
pytest tests/test_retrieval.py::test_deterministic_results -v

# A2: Grounding (every /chat sentence cited)
pytest tests/test_rag_e2e.py::test_grounding -v

# A3: Recall (gold set ≥80% @ top-5)
pytest tests/test_rag_e2e.py::test_gold_set_recall -v

# A4: Allowlist (domain check)
pytest tests/test_retrieval.py::test_domain_allowlist -v

# A5: Canonicalization (URL variants)
pytest tests/test_canonicalization.py -v

# A6: Chunking (token constraints)
pytest tests/test_chunker.py -v

# A7: Latency (p95 < 300ms)
pytest tests/test_retrieval.py::test_latency_p95 -v

# A8: No weakening (all pass)
pytest tests/ -v --tb=short
```

## Makefile Targets to Add

```makefile
.PHONY: vocab embed index search chat test gold

vocab:
	@python src/rag/vocab.py --build data/glossary.csv --output data/vocabulary.json

embed:
	@python -c "from src.rag.pipeline import embed_index; embed_index()"

index:
	@python -c "from src.rag.pipeline import build_faiss; build_faiss()"

search:
	@curl 'http://localhost:7000/search?q=timesheet&k=5' | python -m json.tool

chat:
	@curl -X POST http://localhost:7000/chat \
	  -H 'Content-Type: application/json' \
	  -d '{"question": "How do I submit a timesheet?"}' | python -m json.tool

test:
	@pytest tests/test_chunker.py tests/test_vocab.py tests/test_canonicalization.py \
	        tests/test_retrieval.py tests/test_rag_e2e.py -q

gold:
	@pytest tests/test_rag_e2e.py::test_gold_set_recall -v
```

## Files to Create/Modify

| File | Action | Priority |
|------|--------|----------|
| src/rag/vocab.py | Create | HIGH |
| src/rag/metrics.py | Create | HIGH |
| src/rag/__init__.py | Expose API | HIGH |
| tests/test_retrieval.py | Create/enhance | HIGH |
| tests/test_rag_e2e.py | Create | HIGH |
| tests/fixtures/* | Create HTML + JSON | MEDIUM |
| src/server.py | Minimal edits | MEDIUM |
| .env.sample | Add RAG_* vars | MEDIUM |
| docs/OPERATIONS.md | Create | LOW |
| Makefile | Add targets | LOW |

## Commit Strategy

```bash
# Once all axioms pass:
git add -A
git commit -m "RAG Standard v1: ingest→chunk→embed→FAISS→retrieve→chat. Tests and docs. Meets A1–A8.

- vocab.py: deterministic glossary loading (A1)
- metrics.py: latency tracking (A7)
- test_chunker.py: token constraints (A6)
- test_vocab.py: alias matching (A1)
- test_canonicalization.py: URL normalization (A5)
- test_retrieval.py: domain allowlist + determinism (A4, A1, A7)
- test_rag_e2e.py: gold set + grounding (A3, A2)
- /search and /chat wired with proper response schemas
- Config in .env.sample with RAG_* vars
- Makefile with vocab, embed, index, search, chat, test, gold targets"
```

## Success Criteria

✅ All A1–A8 tests pass
✅ /search returns <300ms p95 on 20-query batch
✅ /chat citations grounded in retrieved chunks
✅ 10-item gold set achieves ≥80% recall @ top-5
✅ Zero regressions in existing LLM health tests

---

**Estimated Effort**: 3–4 hours focused implementation
**Complexity**: Moderate (existing foundation solid)
**Risk**: Low (tests-first approach validates each axiom)
