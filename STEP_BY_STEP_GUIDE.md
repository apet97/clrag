# Advanced Multi-Corpus RAG Stack - Complete Step-by-Step Guide

**Complete guide to launching the production-ready RAG system locally**

---

## Table of Contents

1. [Initial Setup (First Time)](#initial-setup-first-time)
2. [Running the Full Pipeline](#running-the-full-pipeline)
3. [Testing the API](#testing-the-api)
4. [Local LLM Setup](#local-llm-setup)
5. [Using the API](#using-the-api)
6. [Docker Deployment](#docker-deployment)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Usage](#advanced-usage)

---

## Initial Setup (First Time)

### Step 1: Install Prerequisites

**On macOS:**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.9+
brew install python@3.9

# Install Git
brew install git

# Install Ollama (for local LLM)
brew install ollama

# (Optional) Install make for convenience
brew install make
```

**On Linux (Ubuntu/Debian):**
```bash
# Update package manager
sudo apt update
sudo apt upgrade -y

# Install Python 3.9+
sudo apt install -y python3.9 python3.9-venv python3-pip

# Install Git
sudo apt install -y git

# Install Ollama
curl https://ollama.ai/install.sh | sh

# (Optional) Install make
sudo apt install -y make
```

**On Windows (PowerShell as Administrator):**
```powershell
# Install Python 3.9+ from https://www.python.org/downloads/
# During installation, CHECK "Add Python to PATH"

# Install Git from https://git-scm.com/download/win

# Install Ollama from https://ollama.ai/download

# (Optional) Install make via chocolatey
choco install make
```

### Step 2: Clone Repository

```bash
# Navigate to your desired directory
cd ~/Projects  # or any directory you prefer

# Clone the repository
git clone https://github.com/apet97/clrag.git

# Enter the directory
cd clrag

# Verify structure
ls -la
# Should show: src/, data/, index/, Makefile, requirements.txt, README.md, etc.
```

### Step 3: Create Python Virtual Environment

```bash
# Create virtual environment
python3.9 -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate

# You should see (.venv) in your terminal prompt
```

### Step 4: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
python -c "import faiss; import httpx; print('✓ Dependencies installed')"
```

### Step 5: Configure Environment

```bash
# Copy example configuration
cp .env.sample .env

# Edit configuration (important!)
# On macOS/Linux:
nano .env

# On Windows:
# notepad .env

# Key configuration options to check/modify:
# CRAWL_BASES=https://clockify.me/help,https://python.langchain.com/docs
# DOMAINS_WHITELIST=clockify.me,langchain.com
# PARENT_CHILD_INDEXING=true
# HYBRID_SEARCH=true
# QUERY_REWRITES=true
# USE_RERANKER=true
# MODEL_BASE_URL=http://127.0.0.1:8000/v1
# MODEL_NAME=oss20b
# EMBEDDING_MODEL=intfloat/multilingual-e5-base
```

Example `.env` file:
```bash
# LLM Configuration (REQUIRED - must be running before pipeline)
MODEL_BASE_URL=http://127.0.0.1:8000/v1
MODEL_API_KEY=sk-local-or-empty
MODEL_NAME=oss20b
MODEL_MAX_TOKENS=1000
MODEL_TEMPERATURE=0.7

# Embedding Configuration
EMBEDDING_MODEL=intfloat/multilingual-e5-base
EMBEDDING_BATCH_SIZE=32
EMBEDDING_POOL_SIZE=4

# Crawling Configuration
CRAWL_BASES=https://clockify.me/help,https://python.langchain.com/docs
DOMAINS_WHITELIST=clockify.me,langchain.com
CRAWL_ALLOW_OVERRIDE=false

# Pipeline Features
PARENT_CHILD_INDEXING=true
HYBRID_SEARCH=true
QUERY_REWRITES=true
USE_RERANKER=true

# Logging
DEBUG=false
```

---

## Local LLM Setup

**IMPORTANT: Your local LLM must be running BEFORE you start the pipeline!**

### Option 0: Company AI (Internal - Fastest Setup)

If you have access to the company AI instance at `10.127.0.192:11434`:

```bash
# No setup needed! Just verify connection:
curl http://10.127.0.192:11434/api/tags

# Edit .env:
MODEL_BASE_URL=http://10.127.0.192:11434
MODEL_NAME=gpt-oss:20b

# Then proceed directly to "Running the Full Pipeline"
```

**See [COMPANY_AI_SETUP.md](COMPANY_AI_SETUP.md) for full details, model options, and feedback.**

---

### Option 1: Ollama (Recommended)

**Terminal 1 - Start Ollama:**
```bash
# Start Ollama service
ollama serve

# You should see:
# Listening on 127.0.0.1:11434
# Keep this terminal open!
```

**Terminal 2 - Pull and run a model:**
```bash
# Pull a model (oss20b recommended)
ollama pull oss20b

# Or pull alternatives:
ollama pull mistral       # Smaller, faster
ollama pull neural-chat   # Good balance
ollama pull orca-mini     # Very small

# Create OpenAI-compatible endpoint (if not auto-created)
# Ollama defaults to http://127.0.0.1:11434/v1
```

**Update .env for Ollama:**
```bash
MODEL_BASE_URL=http://127.0.0.1:11434/v1
MODEL_NAME=oss20b
```

### Option 2: vLLM (Faster inference)

```bash
# Install vLLM
pip install vllm

# Start server (Terminal 1)
python -m vllm.entrypoints.openai.api_server \
  --model TinyLlama-1.1B-Chat-v1.0 \
  --port 8000

# Update .env:
MODEL_BASE_URL=http://127.0.0.1:8000/v1
MODEL_NAME=TinyLlama-1.1B-Chat-v1.0
```

### Option 3: LM Studio (GUI)

1. Download from https://lmstudio.ai/
2. Load a model (e.g., oss20b)
3. Start OpenAI-compatible server (default: http://127.0.0.1:1234/v1)
4. Update .env:
```bash
MODEL_BASE_URL=http://127.0.0.1:1234/v1
```

---

## Running the Full Pipeline

### Quick Start (All-in-One)

**Terminal 2 - Run entire pipeline:**
```bash
# Activate virtual environment
source .venv/bin/activate

# Run full pipeline (crawl → preprocess → chunk → embed → hybrid)
# This may take 15-30 minutes on first run
make crawl preprocess chunk embed hybrid

# Expected output:
# [INFO] Crawling https://clockify.me/help ...
# [INFO] Scraped 300 articles
# [INFO] Preprocessing HTML to Markdown...
# [INFO] Creating parent-child chunks...
# [INFO] Building FAISS indexes...
# [INFO] Building BM25 indexes...
# [SUCCESS] Pipeline complete!
```

### Step-by-Step (Individual Steps)

**Step 1: Crawl articles**
```bash
source .venv/bin/activate
make crawl

# Expected output:
# [INFO] Starting crawl for 2 namespaces
# [INFO] Discovered 600+ URLs
# [INFO] Scraped 300+ articles
# Data saved to: data/raw/clockify/, data/raw/langchain/
```

**Step 2: Preprocess HTML to Markdown**
```bash
make preprocess

# Expected output:
# [INFO] Converting 300+ HTML files to Markdown
# [INFO] Extracting frontmatter (title, URL, section)
# Data saved to: data/clean/clockify/, data/clean/langchain/
```

**Step 3: Create parent-child chunks**
```bash
make chunk

# Expected output:
# [INFO] Creating parent-child nodes
# [INFO] Generated 2500+ chunks
# Data saved to: data/chunks/*.jsonl
```

**Step 4: Build FAISS vector indexes**
```bash
# IMPORTANT: Your local LLM must be running!
make embed

# Expected output:
# [INFO] Embedding 2500+ chunks with intfloat/multilingual-e5-base
# [INFO] Building FAISS indexes for 2 namespaces
# [INFO] Index size: ~100 MB per namespace
# Data saved to: index/faiss/
# This step takes 10-20 minutes depending on hardware
```

**Step 5: Build BM25 hybrid indexes**
```bash
make hybrid

# Expected output:
# [INFO] Building BM25 indexes via whoosh
# [INFO] Created indexes for 2 namespaces
# Data saved to: index/hybrid/
```

---

## Testing the API

### Terminal 3 - Start the Server

```bash
source .venv/bin/activate
make serve

# Expected output:
# [INFO] Starting Clockify RAG API server
# [INFO] Listening on http://0.0.0.0:7000
# [INFO] Health: HEALTHY
# [INFO] Loaded 2 namespaces: clockify, langchain

# Keep this terminal open!
```

### Testing Health Endpoint

**Terminal 4 - Test health:**
```bash
curl http://localhost:7000/health

# Expected response:
# {
#   "status": "healthy",
#   "namespaces": ["clockify", "langchain"],
#   "indexes_loaded": 2,
#   "vector_index_size_mb": 200,
#   "last_crawl": "2025-10-20T18:30:00Z"
# }
```

### Test Basic Search

```bash
# Search Clockify namespace
curl 'http://localhost:7000/search?q=timesheet&namespace=clockify&k=5'

# Expected response:
# {
#   "query": "timesheet",
#   "namespace": "clockify",
#   "results": [
#     {
#       "id": "chunk_123",
#       "title": "Timesheet",
#       "url": "https://clockify.me/help/...",
#       "content": "...",
#       "score": 0.95,
#       "source": "hybrid"  # Could be "vector", "bm25", or "hybrid"
#     }
#   ],
#   "count": 5,
#   "latency_ms": 45
# }
```

### Test Chat Endpoint

```bash
# Advanced RAG with citations
curl -X POST http://localhost:7000/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "How do I create a project in Clockify?",
    "namespace": "clockify",
    "k": 5,
    "allow_rewrites": true,
    "allow_rerank": true
  }'

# Expected response:
# {
#   "answer": "To create a project in Clockify [1], ...",
#   "sources": [
#     {
#       "id": "[1]",
#       "title": "Creating Projects",
#       "url": "https://clockify.me/help/...",
#       "namespace": "clockify"
#     }
#   ],
#   "latency_ms": 2500
# }
```

---

## Using the API

### Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:7000"

# 1. Search endpoint
response = requests.get(
    f"{BASE_URL}/search",
    params={
        "q": "timesheet",
        "namespace": "clockify",
        "k": 5
    }
)
results = response.json()
print(f"Found {results['count']} results")
for result in results['results']:
    print(f"- {result['title']}: {result['score']:.2f}")

# 2. Chat endpoint (with citations)
response = requests.post(
    f"{BASE_URL}/chat",
    json={
        "question": "How do I track time?",
        "namespace": "clockify",
        "k": 5,
        "allow_rewrites": True,
        "allow_rerank": True
    }
)
answer = response.json()
print(f"\nAnswer: {answer['answer']}")
print(f"Sources: {len(answer['sources'])} citations")
for source in answer['sources']:
    print(f"  [{source['id']}] {source['title']}")
```

### JavaScript/Node.js Example

```javascript
// search.js
const BASE_URL = 'http://localhost:7000';

// 1. Search
async function search(query, namespace) {
  const response = await fetch(
    `${BASE_URL}/search?q=${encodeURIComponent(query)}&namespace=${namespace}&k=5`
  );
  const data = await response.json();
  console.log(`Found ${data.count} results`);
  data.results.forEach(r => {
    console.log(`- ${r.title}: ${r.score.toFixed(2)}`);
  });
}

// 2. Chat
async function chat(question, namespace) {
  const response = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      question,
      namespace,
      k: 5,
      allow_rewrites: true,
      allow_rerank: true
    })
  });
  const data = await response.json();
  console.log(`Answer: ${data.answer}`);
  console.log(`Sources: ${data.sources.map(s => `[${s.id}] ${s.title}`).join(', ')}`);
}

// Usage
search('timesheet', 'clockify');
chat('How do I create a project?', 'clockify');
```

### cURL Examples

```bash
# Set base URL for convenience
export BASE="http://localhost:7000"

# 1. Health check
curl "$BASE/health" | jq

# 2. Simple search
curl "$BASE/search?q=timesheet&namespace=clockify&k=5" | jq

# 3. Search with reranking (slower, more accurate)
curl "$BASE/search?q=custom+fields&namespace=clockify&k=10&use_reranker=true" | jq

# 4. Chat with citations
curl -X POST "$BASE/chat" \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "What are the pricing tiers?",
    "namespace": "clockify",
    "k": 5
  }' | jq

# 5. Search LangChain namespace
curl "$BASE/search?q=retrievers&namespace=langchain&k=5" | jq
```

---

## Docker Deployment

### Build Docker Image

```bash
# Build image (from project root)
docker build -t clockify-rag:latest .

# Or use Docker Compose (simplest)
docker-compose build
```

### Run with Docker Compose

**Create docker-compose.override.yml for local setup:**
```yaml
version: '3.8'

services:
  api:
    environment:
      - MODEL_BASE_URL=http://host.docker.internal:8000/v1  # macOS/Windows
      # For Linux:
      # - MODEL_BASE_URL=http://localhost:8000/v1
    ports:
      - "7000:7000"
    volumes:
      - ./data:/app/data
      - ./index:/app/index
```

**Start services:**
```bash
# Terminal: Start Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f api

# Expected output:
# api_1  | [INFO] Starting API server on :7000
# api_1  | [INFO] Health: HEALTHY

# Test it
curl http://localhost:7000/health
```

**Stop services:**
```bash
docker-compose down
```

### Run with Docker (Manual)

```bash
# Run LLM container
docker run -d \
  --name ollama \
  -p 11434:11434 \
  ollama/ollama

# Run RAG API container
docker run -d \
  --name clockify-rag \
  -p 7000:7000 \
  -e MODEL_BASE_URL=http://ollama:11434/v1 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/index:/app/index \
  --link ollama \
  clockify-rag:latest

# Test
curl http://localhost:7000/health
```

---

## Monitoring & Debugging

### View Real-Time Logs

```bash
# Watch server logs
tail -f logs/api.log

# Search for errors
grep ERROR logs/api.log

# Search for slow queries (>1s)
grep "latency_ms.*[1-9][0-9][0-9][0-9]" logs/api.log

# Count queries by namespace
grep "SEARCH\|CHAT" logs/api.log | grep "namespace" | sort | uniq -c
```

### Monitor Performance

```bash
# Watch latency every 5 seconds
watch -n 5 'curl -s http://localhost:7000/health | jq .latency_stats'

# Test concurrent requests
for i in {1..10}; do
  curl -s "http://localhost:7000/search?q=test&namespace=clockify" &
done

# Measure search latency
time curl "http://localhost:7000/search?q=timesheet&namespace=clockify"
```

### Common Issues

**Issue: "Index not loaded"**
```bash
# Run pipeline again
make crawl preprocess chunk embed hybrid

# Or run individual step that failed
make embed  # if embedding failed
```

**Issue: "Cannot connect to LLM"**
```bash
# Check if LLM is running
curl http://127.0.0.1:8000/v1/models

# If not, start it:
ollama serve  # or vLLM, LM Studio, etc.
```

**Issue: "Out of memory" during embedding**
```bash
# Reduce batch size in .env
EMBEDDING_BATCH_SIZE=16  # Default is 32

# Then re-run embedding
make embed
```

**Issue: "Slow search latency"**
```bash
# Check what indexes are loaded
curl http://localhost:7000/health | jq '.indexes_loaded'

# If hybrid search is enabled, first search may be slower
# Subsequent queries use caching

# Try with fewer results
curl "http://localhost:7000/search?q=test&namespace=clockify&k=3"
```

---

## Advanced Usage

### Query Rewriting

The API automatically generates query rewrites to improve recall:

```bash
# With rewrites (default)
curl "http://localhost:7000/search?q=track+time&namespace=clockify&k=5&allow_rewrites=true"

# Disable rewrites (faster)
curl "http://localhost:7000/search?q=track+time&namespace=clockify&k=5&allow_rewrites=false"
```

### Cross-Encoder Reranking

Improves precision by re-scoring top candidates:

```bash
# With reranking (slower, more accurate)
curl "http://localhost:7000/search?q=custom+fields&namespace=clockify&k=10&use_reranker=true"

# Without reranking (faster)
curl "http://localhost:7000/search?q=custom+fields&namespace=clockify&k=10&use_reranker=false"
```

### Parent-Child Indexing

Retrieves child chunks with parent context:

```bash
# Details show parent-child info
curl "http://localhost:7000/search?q=timesheet&namespace=clockify&k=3&details=true" | jq '.results[].context'
```

### Hybrid Search

Combines vector search (semantic) + BM25 (lexical):

```bash
# View which search method matched each result
curl "http://localhost:7000/search?q=timesheet&namespace=clockify" | jq '.results[].source'
# Output: "vector", "bm25", or "hybrid"
```

### Incremental Crawling

Update indexes with new articles:

```bash
# Crawl only new/updated articles (respects ETags)
make crawl INCREMENTAL=true

# Re-process and re-index
make preprocess chunk embed hybrid
```

---

## Configuration Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_BASE_URL` | `http://127.0.0.1:8000/v1` | Local LLM OpenAI-compatible endpoint |
| `MODEL_NAME` | `oss20b` | Model name (must be loaded/available) |
| `EMBEDDING_MODEL` | `intfloat/multilingual-e5-base` | Embedding model |
| `CRAWL_BASES` | Clockify + LangChain | URLs to crawl (comma-separated) |
| `PARENT_CHILD_INDEXING` | `true` | Enable parent-child nodes |
| `HYBRID_SEARCH` | `true` | Combine vector + BM25 search |
| `QUERY_REWRITES` | `true` | Generate query rewrites |
| `USE_RERANKER` | `true` | Cross-encoder reranking |
| `DEBUG` | `false` | Verbose logging |

---

## Performance Expectations

| Operation | Time | Notes |
|-----------|------|-------|
| First crawl | 10-15 min | Depends on domain size + network |
| Preprocessing | 5-10 min | HTML → Markdown conversion |
| Chunking | 2-5 min | Creating parent-child nodes |
| Embedding | 10-20 min | Depends on embedding hardware + batch size |
| BM25 indexing | 2-5 min | Fast, lightweight |
| **Total first run** | **30-60 min** | One-time cost |
| Incremental crawl | 2-5 min | Only new/updated articles |
| Search latency | 50-100 ms | FAISS search (cached/warm) |
| Chat latency | 5-30 sec | LLM-dominated |

---

## Next Steps

1. ✅ Complete initial setup
2. ✅ Run full pipeline (crawl → embed)
3. ✅ Start API server
4. ✅ Test endpoints
5. 📖 Read README.md for architecture details
6. 📖 Read OPERATOR_GUIDE.md for tuning
7. 🚀 Deploy to production (Docker/Kubernetes)
8. 📊 Monitor via /health endpoint

---

## Support

**For issues:**
1. Check logs: `tail -f logs/api.log`
2. Verify LLM is running: `curl http://127.0.0.1:8000/v1/models`
3. Check health: `curl http://localhost:7000/health`
4. Open issue: https://github.com/apet97/clrag/issues

**Documentation:**
- README.md - Overview
- OPERATOR_GUIDE.md - Tuning & troubleshooting
- API_DOCUMENTATION.md - Endpoint reference
- DEPLOY_TO_GITHUB.md - GitHub deployment

---

**Last Updated:** October 20, 2025
**Status:** Production Ready
**Version:** Advanced Multi-Corpus RAG Stack 2.0
