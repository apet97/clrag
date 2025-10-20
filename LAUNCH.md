# RAG System - Complete Launch Guide

**Get a production-grade RAG chat system running in 5 minutes.**

This guide covers everything from cloning the repository to accessing the chat interface and API endpoints.

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Clone the Repository
```bash
git clone https://github.com/apet97/clrag.git
cd clrag
```

### Step 2: Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.sample .env
```

Edit `.env` to set your configuration:
```bash
# Required: Set a secure token for production
API_TOKEN=your-secure-token-here

# Optional: If using remote Ollama (default: http://10.127.0.192:11434)
LLM_BASE_URL=http://10.127.0.192:11434

# Optional: Port for the API (default: 7000)
API_PORT=7000
```

### Step 5: Start the Server
```bash
python -m src.server
```

**Output should show:**
```
INFO     | src.server:startup:... ✓ Ollama embedding model ready: dim=768
INFO     | src.server:startup:... ✓ Response cache initialized: LRUResponseCache(...)
INFO     | src.server:startup:... ✅ RAG System startup complete
```

### Step 6: Access the Chat Interface
Open your browser and navigate to:
```
http://localhost:7000
```

You'll see:
- **Search Tab**: Vector similarity search over documentation
- **Chat Tab**: AI-powered Q&A grounded in source material
- **Config Panel**: API token, k-parameter slider

---

## 🔌 API Endpoints

All endpoints require the `x-api-token` header set in the UI or your requests.

### `/search` - Vector Similarity Search

**GET request:**
```bash
curl -H "x-api-token: your-secure-token-here" \
  "http://localhost:7000/search?q=how+to+submit+timesheet&k=5"
```

**Response:**
```json
{
  "query": "how to submit timesheet",
  "count": 5,
  "request_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "results": [
    {
      "rank": 1,
      "url": "https://clockify.me/help/article/timesheet",
      "title": "How to submit a timesheet",
      "score": 0.8547,
      "text": "To submit a timesheet in Clockify...",
      "namespace": "clockify-help"
    }
  ]
}
```

**Parameters:**
- `q` (required): Search query (1-2000 characters)
- `k` (optional): Number of results (1-20, default: 5)
- `namespace` (optional): Filter to specific namespace

### `/chat` - AI-Powered Chat with Citations

**POST request:**
```bash
curl -X POST -H "x-api-token: your-secure-token-here" \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I submit a timesheet?", "k": 3}' \
  http://localhost:7000/chat
```

**Response:**
```json
{
  "answer": "To submit a timesheet [1], go to your Projects section [1] and track time [2]. Once complete, submit it to your manager [1] for approval [3].",
  "sources": [
    {
      "rank": 1,
      "url": "https://clockify.me/help/article/timesheet",
      "title": "How to submit a timesheet",
      "score": 0.8547,
      "namespace": "clockify-help"
    },
    {
      "rank": 2,
      "url": "https://clockify.me/help/article/tracking",
      "title": "How to track time",
      "score": 0.7834,
      "namespace": "clockify-help"
    },
    {
      "rank": 3,
      "url": "https://clockify.me/help/article/approval",
      "title": "Timesheet approval workflow",
      "score": 0.7123,
      "namespace": "clockify-help"
    }
  ],
  "citations_found": 3,
  "model_used": "gpt-oss:20b",
  "latency_ms": {
    "retrieval": 45,
    "llm": 287,
    "total": 332
  }
}
```

**Parameters:**
- `question` (required): Your question (1-2000 characters)
- `k` (optional): Number of source documents (1-20, default: 5)
- `namespace` (optional): Filter to specific namespace

### `/health` - System Status

**GET request:**
```bash
curl -H "x-api-token: your-secure-token-here" \
  http://localhost:7000/health
```

**Response:**
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

### `/metrics` - Prometheus Metrics

**GET request:**
```bash
curl -H "x-api-token: your-secure-token-here" \
  http://localhost:7000/metrics
```

**Response:** Prometheus-format metrics for monitoring
```prometheus
# HELP rag_search_latency_ms Search latency in milliseconds
# TYPE rag_search_latency_ms histogram
rag_search_latency_ms_bucket{le="50"} 234
rag_search_latency_ms_bucket{le="100"} 567
...
```

---

## 🎯 Usage Examples

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
client = RAGClient("http://localhost:7000", "your-secure-token-here")

# Search
results = client.search("timesheet submission", k=3)
for r in results["results"]:
    print(f"[{r['rank']}] {r['title']}: {r['score']:.2%}")

# Chat
answer = client.chat("How do I submit a timesheet?", k=3)
print(answer["answer"])
print(f"Sources: {len(answer['sources'])}")
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
const client = new RAGClient('http://localhost:7000', 'your-secure-token-here');

// Search
const results = await client.search('timesheet submission', 3);
results.results.forEach(r => {
  console.log(`[${r.rank}] ${r.title}: ${(r.score * 100).toFixed(1)}%`);
});

// Chat
const answer = await client.chat('How do I submit a timesheet?', 3);
console.log(answer.answer);
answer.sources.forEach((s, i) => {
  console.log(`[${i+1}] ${s.title}: ${s.url}`);
});
```

### cURL Examples
```bash
# Set token in environment for convenience
export TOKEN="your-secure-token-here"
export API="http://localhost:7000"

# Search
curl -H "x-api-token: $TOKEN" \
  "$API/search?q=timesheet&k=5"

# Chat (pretty-printed JSON)
curl -X POST -H "x-api-token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I submit a timesheet?", "k": 3}' \
  "$API/chat" | jq .

# Health check
curl -H "x-api-token: $TOKEN" "$API/health" | jq .

# Metrics
curl -H "x-api-token: $TOKEN" "$API/metrics"
```

---

## 🌐 Web UI Guide

### Login & Configuration
1. **API Token**: Enter your token from `.env` (default: `change-me`)
2. **API Base URL**: Leave as `http://localhost:7000` (can be changed)
3. **Results (k)**: Slider to adjust number of results (1-20)

### Search Tab
- **Input**: Enter your search query
- **Results**: Shows rank, title, URL, similarity score
- **Copy**: Click to copy URL or full result
- **Metadata**: Request ID, latency, namespace

### Chat Tab
- **Input**: Enter your question
- **Answer**: AI-generated answer with inline citations [n]
- **Sources**: List of grounded source documents
- **Metadata**: Latency breakdown (retrieval/LLM), model used, citation count

### Performance Features
- **Response Caching**: Repeated queries return in 5-20ms (cached)
- **Embedding Cache**: Query vectors cached for faster subsequent searches
- **Connection Pooling**: Batch embeddings optimized with HTTP session reuse

---

## ⚙️ Environment Configuration

### Required Variables
```bash
API_TOKEN=your-secure-token-here
```

### Optional Variables
```bash
# Ollama Configuration
LLM_BASE_URL=http://10.127.0.192:11434      # Ollama server address
EMBEDDING_MODEL=nomic-embed-text:latest      # Embedding model
LLM_MODEL=gpt-oss:20b                        # Chat model

# Server Configuration
API_HOST=0.0.0.0                             # Bind address
API_PORT=7000                                # Port
ENV=prod                                     # Environment (prod/dev)

# Cache Configuration
RESPONSE_CACHE_SIZE=1000                     # Max cached responses
RESPONSE_CACHE_TTL=3600                      # Cache TTL in seconds

# Logging
LOG_LEVEL=INFO                               # DEBUG/INFO/WARNING/ERROR
LOG_FILE=/path/to/logfile.log                # Optional file logging

# Rate Limiting
RATE_LIMIT_RPS=10                            # Requests per second limit
```

---

## 🔧 Troubleshooting

### "Connection refused" on startup
**Problem:** Ollama server not responding
```
ERROR: Failed to connect to Ollama at http://10.127.0.192:11434
```

**Solution:**
1. Verify Ollama is running: `curl http://10.127.0.192:11434/api/tags`
2. Update `LLM_BASE_URL` in `.env` to correct address
3. Check firewall/network connectivity

### "401 Unauthorized" errors
**Problem:** Invalid API token
```json
{"detail": "unauthorized"}
```

**Solution:**
1. Copy token from `.env`: `API_TOKEN=...`
2. In browser UI: Set the token in Config panel
3. In API calls: Add header: `-H "x-api-token: your-token"`

### "422 Validation Error"
**Problem:** Invalid query parameters
```json
{"detail": "Query too long (max 2000 chars)"}
```

**Solutions:**
- Keep queries/questions under 2000 characters
- Set `k` between 1-20
- Use valid namespace or leave blank

### Slow first query (2-5 seconds)
**This is normal:** First query warms up the embedding model
- Subsequent queries with caching: 5-20ms
- Cold queries: 50-150ms

### High memory usage
**Problem:** Large cache or model loading
```bash
# Clear response cache (restarts API)
# Edit .env: RESPONSE_CACHE_SIZE=100

# Or reduce embedding cache:
# Edit .env: EMBEDDING_MODEL=intfloat/multilingual-e5-base
```

### "Index not found" error
**Problem:** FAISS index files missing
```
❌ STARTUP FAILURE: Missing prebuilt index for namespace 'clockify-help'
```

**Solution:** This shouldn't happen with prebuilt image. If it does:
1. Check `index/faiss/clockify-help/` directory exists
2. Verify `index.faiss` and `meta.json` files present
3. File should be ~100MB+

---

## 📊 Performance Benchmarks

### Latency (measured on macOS M1, Ollama local)

| Operation | First | Cached | Cold Cache | Notes |
|-----------|-------|--------|-----------|-------|
| Search | 50ms | 8ms | 50ms | After warmup; 90% cached reduction |
| Chat | 350ms | N/A | 350ms | Includes LLM generation |
| Embedding (1) | 30ms | 1ms | 30ms | Single query; LRU cached |
| Embedding (8) | 200ms | - | 200ms | Batch with connection pooling |

### Resource Usage

| Resource | Typical | Max |
|----------|---------|-----|
| Memory | 500MB | 2GB (with large cache) |
| CPU | 10-30% | 100% (during embedding) |
| Network (Ollama) | 2-5 MB/s | 50 MB/s |

---

## 🔒 Security

### Authentication
- **Header-based**: `x-api-token` required on all requests
- **Constant-time comparison**: Uses `hmac.compare_digest()` (timing-attack resistant)
- **Production guard**: Won't start with default token in `ENV=prod`

### Input Validation
- Queries: 1-2000 characters, no injection attacks
- k parameter: Clamped to [1, 20]
- Namespaces: Validated against known list
- Citations: Fixed-width regex (no false positives)

### Data Privacy
- No query logging (only statistics)
- Responses cached locally, not persisted
- Secrets redacted in logs (tokens, API keys)

---

## 📝 Common Tasks

### Change the API Token
```bash
# In .env
API_TOKEN=your-new-secure-token

# Restart the server
# Re-enter token in browser UI
```

### Add More Documentation
Currently indexed: Clockify Help (https://clockify.me/help/*)

To add more sources:
1. Create new HTML/MD files in `docs/` directory
2. Run: `python -m src.ingest`
3. Restart server

### Monitor Performance
```bash
# Terminal 1: Watch logs
tail -f logs.txt

# Terminal 2: Check metrics
curl -H "x-api-token: $TOKEN" http://localhost:7000/metrics

# Terminal 3: Stress test
for i in {1..100}; do
  curl -s -H "x-api-token: $TOKEN" \
    "http://localhost:7000/search?q=test$i&k=5" | jq .count
done
```

### Deploy to Production
```bash
# 1. Set production environment
export ENV=prod
export API_TOKEN=your-very-secure-token-here

# 2. Use production docker image
docker build -f Dockerfile.prod -t rag-system:latest .
docker run -p 7000:7000 \
  -e API_TOKEN=$API_TOKEN \
  -e ENV=prod \
  rag-system:latest

# 3. Set up reverse proxy (nginx)
# See DEPLOY.md for full production guide
```

---

## 🆘 Getting Help

### Documentation Files
- **API_REFERENCE.md**: Complete API documentation
- **SETUP.md**: System architecture and detailed setup
- **INGESTION.md**: How to index new documents
- **README.md**: Project overview

### Logs
```bash
# View startup logs
tail -20 logs.txt

# Watch live logs
tail -f logs.txt

# View specific error
grep "ERROR" logs.txt
```

### Health Check
```bash
curl -H "x-api-token: your-token" http://localhost:7000/health | jq .
```

Response should show:
- `status: ok`
- `index_loaded: true`
- `embedding_model: nomic-embed-text:latest`
- `warnings: []`

---

## 📋 Checklist

Before production deployment:

- [ ] Clone repo: `git clone https://github.com/apet97/clrag.git`
- [ ] Create venv: `python3 -m venv .venv && source .venv/bin/activate`
- [ ] Install deps: `pip install -r requirements.txt`
- [ ] Config token: Edit `.env`, set `API_TOKEN`
- [ ] Start server: `python -m src.server`
- [ ] Test browser: Open `http://localhost:7000`
- [ ] Test search: Try a query in Search tab
- [ ] Test chat: Try a question in Chat tab
- [ ] Test API: `curl -H "x-api-token: ..." http://localhost:7000/search?q=test&k=5`
- [ ] Check health: `curl -H "x-api-token: ..." http://localhost:7000/health`
- [ ] Review logs: `tail logs.txt` (no errors)

---

## 🎉 You're Ready!

Your RAG chat system is now running.

- **Web UI**: http://localhost:7000
- **Search API**: `/search` endpoint
- **Chat API**: `/chat` endpoint
- **Docs**: Check `API_REFERENCE.md` for full API details

**Next steps:**
1. Try asking questions in the chat interface
2. Experiment with search queries
3. Integrate the API into your applications
4. Monitor performance with `/metrics` endpoint

Enjoy your production-grade RAG system! 🚀
