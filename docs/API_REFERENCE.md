# RAG API Reference

Complete API documentation for the Clockify Help RAG system.

---

## Error Codes

All endpoints return standard HTTP status codes with descriptive error messages.

| Code | Name | Meaning | Action |
|------|------|---------|--------|
| 200 | OK | Success | Result ready in response body |
| 400 | Bad Request | Malformed request | Check request format/syntax |
| 401 | Unauthorized | Missing or invalid API token | Add `x-api-token` header |
| 422 | Validation Error | Invalid parameters | Check query length, k bounds (1-20), namespace exists |
| 429 | Rate Limited | Too many requests | Wait before retrying (10 req/sec limit per IP) |
| 500 | Internal Error | Server error | Check logs, verify index loaded |
| 503 | Service Unavailable | Dependency offline | Verify Ollama/LLM running, index accessible |

---

## GET /search

Vector similarity search over Clockify Help documentation.

Returns top-k most relevant documents with optional reranking.

### Request

```bash
curl -H "x-api-token: YOUR_TOKEN" \
  "http://localhost:7000/search?q=timesheet&k=5&namespace=clockify-help"
```

### Parameters

| Name | Type | Required | Description | Bounds |
|------|------|----------|-------------|--------|
| `q` | string | Yes | Search query | 1-2000 chars |
| `k` | integer | No | Number of results to return | 1-20 (default: 5) |
| `namespace` | string | No | Filter results to namespace | Must exist in system |

### Response (200 OK)

```json
{
  "query": "timesheet",
  "count": 5,
  "request_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "results": [
    {
      "rank": 1,
      "url": "https://clockify.me/help/article/timesheet",
      "title": "How to submit a timesheet",
      "score": 0.8547,
      "text": "To submit a timesheet in Clockify, go to your Projects section...",
      "namespace": "clockify-help",
      "chunk_id": "3c59dc048e8850243be8079a5c74d079",
      "rerank_metadata": {
        "reranker_used": true,
        "reranker_available": true,
        "fallback_reason": null
      }
    },
    {
      "rank": 2,
      "url": "https://clockify.me/help/article/approval",
      "title": "Timesheet approval workflow",
      "score": 0.7834,
      "namespace": "clockify-help",
      "chunk_id": "e4d909c290d0fb1ca068ffaddf22cbd0"
    }
  ]
}
```

### Error Examples

**Missing token (401):**
```bash
curl "http://localhost:7000/search?q=test"
# Response: 401 Unauthorized
```

**Query too long (422):**
```bash
curl -H "x-api-token: token" \
  "http://localhost:7000/search?q=$(python -c 'print(\"a\"*2001)')"
# Response: 422 Validation Error - "Query too long (max 2000 chars)"
```

**Invalid k (422):**
```bash
curl -H "x-api-token: token" \
  "http://localhost:7000/search?q=test&k=21"
# Response: 422 Validation Error - "k out of range [1, 20]"
```

**Rate limited (429):**
```bash
# After 10+ requests within 1 second
# Response: 429 Too Many Requests
# Header: Retry-After: 1
```

---

## POST /chat

Generate a conversational answer grounded in Clockify Help documentation.

Uses `/search` to retrieve relevant documents, then passes them to an LLM for synthesis.

### Request

```bash
curl -X POST -H "x-api-token: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I submit a timesheet?",
    "k": 3
  }' \
  http://localhost:7000/chat
```

### Parameters (JSON body)

| Name | Type | Required | Description | Bounds |
|------|------|----------|-------------|--------|
| `question` | string | Yes | Question to answer | 1-2000 chars |
| `k` | integer | No | Sources to retrieve | 1-20 (default: 5) |
| `namespace` | string | No | Filter sources to namespace | Must exist |

### Response (200 OK)

```json
{
  "answer": "To submit a timesheet [1], go to your Projects section [1] and track time [2]. Once complete, submit it to your manager [1] for approval [3].",
  "sources": [
    {
      "rank": 1,
      "url": "https://clockify.me/help/article/timesheet",
      "title": "How to submit a timesheet",
      "score": 0.8547,
      "namespace": "clockify-help",
      "chunk_id": "3c59dc048e8850243be8079a5c74d079"
    },
    {
      "rank": 2,
      "url": "https://clockify.me/help/article/tracking",
      "title": "How to track time",
      "score": 0.7834,
      "namespace": "clockify-help",
      "chunk_id": "e4d909c290d0fb1ca068ffaddf22cbd0"
    },
    {
      "rank": 3,
      "url": "https://clockify.me/help/article/approval",
      "title": "Timesheet approval workflow",
      "score": 0.7123,
      "namespace": "clockify-help",
      "chunk_id": "a5771bce93e200bd9d86f07e1b375b81"
    }
  ],
  "citations_found": 3,
  "model_used": "gpt-oss:20b",
  "latency_ms": {
    "retrieval": 45,
    "llm": 287,
    "total": 332
  },
  "meta": {
    "request_id": "7c6e05ec-c481-11ec-9621-0242ac130002",
    "temperature": 0.0,
    "model": "gpt-oss:20b",
    "namespaces_used": ["clockify-help"],
    "k": 3,
    "api_type": "ollama"
  }
}
```

### Citation Format

Citations in the answer are marked as `[n]` where `n` is the 1-based index into the `sources` array.

- `[1]` refers to `sources[0]`
- `[2]` refers to `sources[1]`
- No sources → no citations (deterministic, no hallucinations)

### Latency Breakdown

| Metric | Meaning |
|--------|---------|
| `retrieval_ms` | Time to search and rerank documents |
| `llm_ms` | Time for LLM to generate answer |
| `total_ms` | End-to-end latency |

---

## GET /health

Check system status and readiness.

### Request

```bash
curl -H "x-api-token: YOUR_TOKEN" \
  http://localhost:7000/health
```

### Response (200 OK)

```json
{
  "status": "ok",
  "index_loaded": true,
  "namespaces": ["clockify-help"],
  "vector_count": 127,
  "embedding_dim": 768,
  "embedding_model": "nomic-embed-text:latest",
  "llm_model": "gpt-oss:20b",
  "cache_stats": {
    "search_cache_size": 234,
    "encoding_cache_info": {
      "hits": 1245,
      "misses": 89,
      "currsize": 87
    }
  },
  "warnings": []
}
```

### Response with Warnings (200 OK, but degraded)

```json
{
  "status": "ok",
  "index_loaded": true,
  "namespaces": ["clockify-help"],
  "warnings": [
    "Reranker unavailable - falling back to BM25 scores",
    "LLM connection slow (p95: 5000ms)"
  ],
  "uptime_seconds": 86400
}
```

---

## GET /metrics

Prometheus-format metrics for monitoring.

### Request

```bash
curl -H "x-api-token: YOUR_TOKEN" \
  http://localhost:7000/metrics
```

### Response (200 OK)

```prometheus
# HELP rag_search_latency_ms Search latency in milliseconds
# TYPE rag_search_latency_ms histogram
rag_search_latency_ms_bucket{le="50"} 234
rag_search_latency_ms_bucket{le="100"} 567
rag_search_latency_ms_bucket{le="200"} 892
rag_search_latency_ms_bucket{le="500"} 1456
rag_search_latency_ms_bucket{le="1000"} 1499
rag_search_latency_ms_bucket{le="+Inf"} 1500
rag_search_latency_ms_sum 98765.43
rag_search_latency_ms_count 1500

# HELP rag_embedding_latency_ms Embedding latency
# TYPE rag_embedding_latency_ms histogram
rag_embedding_latency_ms_bucket{le="10"} 234
rag_embedding_latency_ms_bucket{le="50"} 1234
...

# HELP rag_cache_hits_total LRU cache hits
# TYPE rag_cache_hits_total counter
rag_cache_hits_total 1245

# HELP rag_cache_misses_total LRU cache misses
# TYPE rag_cache_misses_total counter
rag_cache_misses_total 89

# HELP rag_requests_total Total API requests
# TYPE rag_requests_total counter
rag_requests_total{endpoint="/search",code="200"} 1456
rag_requests_total{endpoint="/search",code="429"} 44
rag_requests_total{endpoint="/chat",code="200"} 234
rag_requests_total{endpoint="/health",code="200"} 5000
```

---

## Troubleshooting

### "Results returned but all answers generic"

**Symptoms:**
- Search returns results but chat answer is vague
- `rerank_metadata.reranker_used == false`

**Root Cause:**
Reranker module unavailable; falling back to raw embedding scores

**Solution:**
1. Check `/health` endpoint - look for reranker warnings
2. Verify FlagEmbedding is installed: `pip list | grep FlagEmbedding`
3. Check logs for reranker initialization errors
4. Consider tuning `query_expand()` to broaden retrieval before reranking

### "Latency spiked from 100ms to 2s"

**Symptoms:**
- P95 latency suddenly high
- Random requests slow, others fast

**Root Cause:**
- Embedding cache was cleared
- Query expansion creating many vectors
- Ollama model unloaded (slow warm-up)

**Solution:**
1. Check embedding cache hit rate in `/health`: `cache_stats.encoding_cache_info.hits / (hits + misses)`
2. Verify Ollama models loaded: `curl http://ollama:11434/api/tags`
3. Monitor Ollama memory: may need to increase allocated memory
4. Check network - if latency is consistent, may be Ollama load

### "401 Unauthorized"

**Symptoms:**
```json
{"detail": "unauthorized"}
```

**Solution:**
1. Ensure `x-api-token` header is present in request
2. Verify token value matches `API_TOKEN` environment variable
3. In production, token must NOT be "change-me"
4. Check if token contains special characters - may need URL encoding

### "429 Too Many Requests"

**Symptoms:**
```json
{"detail": "Rate limited"}
```

**Root Cause:**
>10 requests/second from same IP

**Solution:**
1. Add request throttling: wait 100ms between requests
2. Increase rate limit (dev only): `RATE_LIMIT_RPS=50`
3. If behind proxy: configure X-Forwarded-For header
4. For batch operations: consider async queue + slower ingestion

### "503 Service Unavailable"

**Symptoms:**
- LLM endpoints fail
- Index cannot be loaded

**Solution:**
1. Check Ollama server: `curl http://10.127.0.192:11434/api/tags`
2. Verify index files exist: `ls -la index/faiss/clockify-help/`
3. Check logs for startup validation errors
4. Restart server if index was recently rebuilt: `make ingest` then `make serve`

---

## Rate Limiting

The API applies per-IP rate limiting:

- **Limit:** 10 requests per second (configurable via `RATE_LIMIT_RPS`)
- **Window:** 1 second (sliding)
- **Response:** 429 with `Retry-After: 1` header

Example with backoff:

```python
import time
import requests

MAX_RETRIES = 3
for attempt in range(MAX_RETRIES):
    resp = requests.get(url, headers=headers)
    if resp.status_code == 429:
        wait_time = int(resp.headers.get("Retry-After", 1))
        print(f"Rate limited, waiting {wait_time}s...")
        time.sleep(wait_time)
        continue
    break
```

---

## Determinism & Reproducibility

All endpoints guarantee deterministic results:

- ✅ Same query → same top-k results (byte-for-byte identical)
- ✅ Temperature fixed at 0.0 (no LLM randomness)
- ✅ Namespace ordering deterministic (sorted)
- ✅ RNG seeded at startup

Example:

```bash
# First request
$ curl -H "x-api-token: token" "http://localhost:7000/search?q=timesheet&k=3"
# {results: [{rank: 1, url: "...", score: 0.8547}, ...]}

# Second request (identical)
$ curl -H "x-api-token: token" "http://localhost:7000/search?q=timesheet&k=3"
# {results: [{rank: 1, url: "...", score: 0.8547}, ...]}  <- IDENTICAL

# Third request after restart
$ # (after restarting server)
$ curl -H "x-api-token: token" "http://localhost:7000/search?q=timesheet&k=3"
# {results: [{rank: 1, url: "...", score: 0.8547}, ...]}  <- STILL IDENTICAL
```

---

## Security

### Authentication

All endpoints require the `x-api-token` header:

```bash
curl -H "x-api-token: YOUR_SECURE_TOKEN" \
  http://localhost:7000/search?q=test
```

Token validation uses constant-time comparison (resistant to timing attacks).

### Input Validation

- Queries sanitized (no injection attacks)
- k parameter clamped to [1, 20]
- Namespace validated against known list
- Citation regex uses fixed-width matching (no false positives)

### CORS

In production, CORS is restricted to `UI_ORIGIN` environment variable.

Frontend requests must come from allowed domain:

```bash
# .env
UI_ORIGIN=https://myapp.example.com

# Requests from other origins will be rejected with 403
```

---

## Examples

### Python Client

```python
import requests

class RAGClient:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url
        self.headers = {"x-api-token": api_token}

    def search(self, query: str, k: int = 5) -> dict:
        resp = requests.get(
            f"{self.base_url}/search",
            params={"q": query, "k": k},
            headers=self.headers
        )
        resp.raise_for_status()
        return resp.json()

    def chat(self, question: str, k: int = 5) -> dict:
        resp = requests.post(
            f"{self.base_url}/chat",
            json={"question": question, "k": k},
            headers=self.headers
        )
        resp.raise_for_status()
        return resp.json()

# Usage
client = RAGClient("http://localhost:7000", "your-token")
results = client.search("How do I submit a timesheet?", k=3)
for r in results["results"]:
    print(f"[{r['rank']}] {r['title']}: {r['score']:.2%}")
```

### JavaScript Client

```javascript
class RAGClient {
  constructor(baseUrl, apiToken) {
    this.baseUrl = baseUrl;
    this.headers = { 'x-api-token': apiToken };
  }

  async search(query, k = 5) {
    const url = new URL(`${this.baseUrl}/search`);
    url.searchParams.set('q', query);
    url.searchParams.set('k', k);

    const resp = await fetch(url, { headers: this.headers });
    if (!resp.ok) throw new Error(`${resp.status}: ${await resp.text()}`);
    return resp.json();
  }

  async chat(question, k = 5) {
    const resp = await fetch(`${this.baseUrl}/chat`, {
      method: 'POST',
      headers: { ...this.headers, 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, k })
    });
    if (!resp.ok) throw new Error(`${resp.status}: ${await resp.text()}`);
    return resp.json();
  }
}

// Usage
const client = new RAGClient('http://localhost:7000', 'your-token');
const answer = await client.chat('How do I submit a timesheet?', 3);
console.log(answer.answer);
answer.sources.forEach((s, i) => {
  console.log(`[${i+1}] ${s.title}: ${s.url}`);
});
```

---

**Last Updated:** 2025-10-20
**Version:** 1.0 (RAG v1)
