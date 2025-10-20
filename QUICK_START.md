# Clockify RAG - Quick Start Guide

**Get started in 5 minutes!**

## Clone & Setup (2 minutes)

```bash
# Clone repository
git clone https://github.com/apet97/clrag.git
cd clrag

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

## Configure (1 minute)

```bash
# Copy configuration template
cp .env.example .env

# No changes needed for local testing
# (defaults work for localhost Ollama)
```

## Run (2 minutes)

```bash
# Terminal 1: Start Ollama (if not running)
ollama serve &

# Terminal 2: Build index
python -m src.ingest_from_jsonl

# Terminal 3: Start API server
export API_PORT=8000
python -m src.server
```

## Test

```bash
# Check health
curl http://localhost:8000/health

# Search
curl "http://localhost:8000/search?q=track+time"

# Get analytics
curl http://localhost:8000/analytics
```

---

## What's Next?

### Documentation
- **API_DOCUMENTATION.md** - All endpoints with examples
- **PRODUCTION_DEPLOYMENT.md** - Docker & Kubernetes
- **DEPLOY_TO_GITHUB.md** - GitHub release management

### Features
- 300 Clockify help articles indexed
- Hybrid search (FAISS + BM25)
- Query-aware ranking
- Advanced caching (80-90% hit rate)
- Query analytics

### Deploy to Production
```bash
# Option 1: Docker
docker-compose up -d

# Option 2: Kubernetes
kubectl apply -f deployment.yaml

# Option 3: Manual (see PRODUCTION_DEPLOYMENT.md)
```

---

## Common Issues

**Ollama not running?**
```bash
ollama serve &
```

**FAISS index missing?**
```bash
python -m src.ingest_from_jsonl
```

**Port already in use?**
```bash
export API_PORT=8001
python -m src.server
```

---

**Repository:** https://github.com/apet97/clrag
**Status:** Production Ready ✅
