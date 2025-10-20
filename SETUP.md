# Clockify Help RAG - Complete Setup Guide

**Production-ready Retrieval Augmented Generation system for Clockify Help documentation**

## Quick Start (5 minutes)

```bash
# 1. Clone and prepare environment
git clone https://github.com/apet97/clrag.git
cd clrag
python -m venv .venv
source .venv/bin/activate  # or: .venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure
cp .env.sample .env
# Edit .env and set:
#   HELP_DIR=/absolute/path/to/clockify_help_scrape
#   LLM_BASE_URL=http://10.127.0.192:11434  (or your Ollama host)
#   ENV=dev

# 4. Prepare Ollama models (requires Ollama running on target host)
ollama pull nomic-embed-text:latest
ollama pull gpt-oss:20b

# 5. Ingest Clockify Help documentation
make ingest

# 6. Start API server
make serve

# 7. (Optional) Start UI in another terminal
make ui
# Then visit: http://localhost:8080
```

---

## System Architecture

### Core Components

**1. Ingestion Pipeline** (`src/ingest.py`)
- Scans `HELP_DIR` for `.html`, `.htm`, `.md` files
- Enforces **strict allowlist**: only `https://clockify.me/help/*` URLs
- Extracts canonical URLs from `<link rel="canonical">` or derives from filenames
- Chunks text (~512 tokens with 64-token overlap)
- Embeds via Ollama `/api/embeddings` (nomic-embed-text:latest)
- Builds FAISS IndexFlatIP with L2 normalization
- Output: `index/faiss/clockify-help/` directory

**2. Encoding** (`src/encode.py`)
- Ollama integration (not sentence-transformers)
- Functions: `encode_query()` (with LRU cache), `encode_texts()`
- L2 normalization on all vectors
- Model: `nomic-embed-text:latest` (768-dim)

**3. API Server** (`src/server.py`)
- FastAPI endpoints: `/search`, `/chat`, `/health`, `/config`
- Namespace: `clockify-help` (deterministic, sorted)
- **Determinism**: stable sort before dedup, seeds at startup, temperature=0.0
- **Citations**: safe parsing (strip URLs first, then `[(\d{1,2})]`)
- **Telemetry**: request_id, temperature, latencies in `meta`
- **Security**: constant-time auth, input validation (Pydantic), rate limiting
- **Observability**: /metrics endpoint (Prometheus format)

**4. Minimal UI** (`ui/`)
- Static HTML + JavaScript (no auth, no storage)
- Search tab: query input, results table with rank/URL/score
- Chat tab: question input, answer with inline citations, sources list
- Configurable API endpoint and token

### Data Flow

```
Scraped HTML/MD files (HELP_DIR)
    ↓
[Ingestion] Extract URLs (allowlist check), chunk, embed
    ↓
FAISS Index (index/faiss/clockify-help/)
    ↓
[Server] /search or /chat request
    ↓
Retrieve + rank (stable sort, dedup by URL)
    ↓
(Optional) LLM generation with citations
    ↓
Response with metadata (request_id, temperature, etc)
```

---

## Environment Configuration

### Required Variables

```bash
# API Server
API_HOST=0.0.0.0
API_PORT=7000
API_TOKEN=change-me          # Set to real token in production!
ENV=dev                       # or: staging, prod

# LLM (Ollama)
LLM_API_TYPE=ollama
LLM_BASE_URL=http://10.127.0.192:11434
LLM_MODEL=gpt-oss:20b
LLM_TEMPERATURE=0.0           # Determinism: must be 0.0
LLM_TIMEOUT_SECONDS=30

# Embeddings (Ollama)
EMBEDDING_MODEL=nomic-embed-text:latest
RETRIEVAL_K=5                 # Default number of results

# Indexing
NAMESPACES=clockify-help
HELP_DIR=/path/to/clockify_help_scrape
CHUNK_TARGET_TOKENS=512
CHUNK_OVERLAP_TOKENS=64
```

### Optional Variables

```bash
# Security
RATE_LIMIT_RPS=10             # Per-IP rate limit
UI_ORIGIN=http://localhost:8080  # For CORS
ALLOW_ADMIN_IN_PROD=false     # Allow /admin endpoints in production

# Logging
LOG_LEVEL=INFO                # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## API Endpoints

### GET `/search?q=<query>&k=<results>&namespace=<ns>`

**Request:**
```bash
curl -H "x-api-token: change-me" \
  "http://localhost:7000/search?q=timesheet&k=5"
```

**Response:**
```json
{
  "query": "timesheet",
  "count": 5,
  "request_id": "a1b2c3d4-...",
  "results": [
    {
      "rank": 1,
      "url": "https://clockify.me/help/article/timesheet",
      "title": "How to submit a timesheet",
      "namespace": "clockify-help",
      "score": 0.8547,
      "chunk_id": "..."
    },
    ...
  ]
}
```

**Key Features:**
- Sequential rank (1, 2, 3, ...)
- Unique URLs (deduplicated)
- request_id for tracing
- Deterministic (same query → same top-k)

---

### POST `/chat`

**Request:**
```bash
curl -X POST -H "x-api-token: change-me" \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I submit a timesheet?", "k": 5}' \
  http://localhost:7000/chat
```

**Response:**
```json
{
  "answer": "To submit a timesheet [1], go to Projects [1] and clock in [2].",
  "sources": [
    {
      "title": "How to submit a timesheet",
      "url": "https://clockify.me/help/article/timesheet",
      "namespace": "clockify-help",
      "score": 0.8547,
      "chunk_id": "..."
    },
    ...
  ],
  "citations_found": 2,
  "model_used": "gpt-oss:20b",
  "latency_ms": {
    "retrieval": 45,
    "llm": 287,
    "total": 332
  },
  "meta": {
    "request_id": "a1b2c3d4-...",
    "temperature": 0.0,
    "model": "gpt-oss:20b",
    "namespaces_used": ["clockify-help"],
    "k": 5,
    "api_type": "ollama"
  }
}
```

**Key Features:**
- Answer grounded in retrieved sources only
- Citations [n] map to source indices
- Temperature exposed for determinism verification
- Full latency breakdown
- No hallucinations (no sources → no citations)

---

### GET `/health`

Check system status:

```bash
curl -H "x-api-token: change-me" \
  http://localhost:7000/health
```

Returns: namespaces, index metrics, embedding dimension, LLM status

---

### GET `/metrics`

Prometheus-format metrics:

```bash
curl http://localhost:7000/metrics
```

Includes:
- `requests_total{endpoint,code}`: Request counters
- `retrieval_latency_ms`: Histogram
- `llm_latency_ms`: Histogram

---

## UI Usage

### Starting the UI

```bash
# In another terminal
make ui
# or manually:
python -m http.server -d ui 8080
```

Visit: **http://localhost:8080**

### Configuration

At the top of the page:
- **API Base**: Change if API is on different host/port
- **Token**: Your API token (not persisted)
- **k**: Number of results to retrieve (1-20)

### Search Tab

1. Enter a search query (e.g., "how do I submit a timesheet?")
2. Click **Search**
3. View results with rank, title, URL, score
4. Click URLs to open in new tab

### Chat Tab

1. Enter a question
2. Click **Ask**
3. View answer with inline citations [1], [2], etc.
4. See list of grounding sources
5. Check metadata (model, temperature, request_id, latencies)

---

## RAG Axioms (Determinism & Grounding)

| Axiom | Guarantee | Implementation |
|-------|-----------|---|
| **0 (Auth)** | Token required, constant-time check | `hmac.compare_digest()` |
| **1 (Determinism)** | Identical queries → identical top-k | Seeds (0), stable sort, temperature=0.0 |
| **2 (Citations)** | Grounded in sources, no hallucinations | Safe parsing, citation floor |
| **3 (L2 Norm)** | Vectors normalized to unit length | `np.linalg.norm(v) ≈ 1.0` |
| **4 (Dedup)** | Unique URLs in results | URL-based deduplication |
| **5 (Rerank)** | Optional, graceful fallback | Skips if unavailable |
| **6 (Grounding)** | Sources only, no hallucinations | No sources → no citations |
| **7 (Rank)** | Sequential 1-based rank field | Rank added after dedup |
| **9 (Regex Safety)** | No false positives on [2024] or URLs | URL stripping first |

---

## Troubleshooting

### Issue: `LLM_BASE_URL is required`

**Solution**: Set `LLM_BASE_URL` in .env to your Ollama host:
```bash
LLM_BASE_URL=http://10.127.0.192:11434
```

### Issue: Index not found

**Solution**: Run ingestion first:
```bash
make ingest
```

Check that `HELP_DIR` points to valid scraped files and `index/faiss/clockify-help/` was created.

### Issue: 401 Unauthorized

**Solution**: Ensure API token is set correctly:
```bash
# In UI config or curl header:
curl -H "x-api-token: YOUR_TOKEN" http://localhost:7000/search?q=test
```

### Issue: 429 Rate Limited

**Solution**: Wait 1 second between requests, or increase `RATE_LIMIT_RPS`:
```bash
RATE_LIMIT_RPS=20
```

### Issue: Citations don't match sources

**Solution**: Check that LLM model and temperature are correct:
- Model: `gpt-oss:20b` (configured)
- Temperature: `0.0` (for determinism)

If citations still don't match, check logs for citation parsing warnings.

---

## Testing & Evaluation

### Unit Tests

```bash
# Run all tests
pytest -q

# Run specific test class
pytest tests/test_axioms.py::TestDeterminism -v

# Run with coverage
pytest --cov=src tests/
```

### Axiom Validation

```bash
# Comprehensive evaluation (axioms 1-9)
make eval-axioms

# This runs:
python eval/run_eval.py http://localhost:7000
```

Output includes:
- Recall@5, Recall@10
- MRR@5, MRR@10
- Latency p50, p95
- Pass/fail vs. targets (Recall@5 ≥ 0.70, p95 ≤ 800ms)

---

## Production Deployment

### Pre-Production Checklist

- [ ] Set `ENV=prod` in .env
- [ ] Change `API_TOKEN` to a strong random value
- [ ] Set `LLM_BASE_URL` to production Ollama host
- [ ] Set `UI_ORIGIN` to allowed frontend domain (CORS)
- [ ] Verify `LLM_TEMPERATURE=0.0` (determinism)
- [ ] Run `make eval-axioms` and ensure all metrics pass
- [ ] Run `pytest -q` and ensure all tests pass
- [ ] Review logs for errors: `LOG_LEVEL=INFO`

### Running on a Server

```bash
# Option 1: Using uvicorn directly
uvicorn src.server:app --host 0.0.0.0 --port 7000 --workers 4

# Option 2: Using gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.server:app

# Option 3: Using systemd (example)
sudo systemctl restart clockify-rag
```

### Monitoring

- **Metrics**: Scrape `/metrics` with Prometheus
- **Health**: Call `/health` periodically (should be < 1s)
- **Logs**: Monitor `LOG_LEVEL` output for errors
- **Rate Limit**: Track 429 responses in `/metrics`

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         UI (Browser)                        │
│                  (Search + Chat tabs)                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
                         [CORS Check]
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Server                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ /search    /chat    /health    /metrics    /config   │   │
│  └──────────────────────────────────────────────────────┘   │
│          ↓                    ↓                               │
│  [Rate Limit] [Auth Check] [Input Validation]              │
│          ↓                    ↓                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │             Retrieval Engine                         │   │
│  │  - Encode query (Ollama /api/embeddings)            │   │
│  │  - FAISS search (normalized vectors)                │   │
│  │  - Stable sort + dedup by URL                       │   │
│  │  - Cap to k results                                  │   │
│  └──────────────────────────────────────────────────────┘   │
│          ↓                                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  (Optional) LLM Generation                           │   │
│  │  - /api/chat on Ollama (gpt-oss:20b)               │   │
│  │  - Temperature=0.0 (deterministic)                  │   │
│  │  - Safe citation parsing                            │   │
│  └──────────────────────────────────────────────────────┘   │
│          ↓                                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Response + Telemetry                               │   │
│  │  - request_id (UUID)                                │   │
│  │  - temperature, model, latencies                    │   │
│  │  - Metrics counters/histograms                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
                         ┌─────────────┐
                         │  FAISS      │
                         │  Index      │
                         │  (on disk)  │
                         └─────────────┘
                              ↓
                         ┌─────────────┐
                         │  Ollama     │
                         │  (embeddings│
                         │   + chat)   │
                         └─────────────┘
```

---

## Support

- **GitHub Issues**: https://github.com/apet97/clrag/issues
- **Documentation**: See `INGESTION.md` and `DELIVERABLES.md`
- **Axioms**: See `RAG Standard v1` in this guide

---

## License & Attribution

**RAG v1 hardening**: Deterministic retrieval, safe citations, production security, complete observability.

Axiom-based testing ensures:
- ✅ Determinism (AXIOM 1)
- ✅ Grounding (AXIOM 2, 6)
- ✅ No hallucinations
- ✅ Security (constant-time auth, AXIOM 0)
- ✅ Performance (latency budgets)

