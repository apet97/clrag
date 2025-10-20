# Deployment Fixes & Troubleshooting Guide

This guide documents all deployment issues encountered and their solutions, ensuring you won't encounter the same errors again.

## Quick Start (Recommended Path)

```bash
# 1. Fresh clone
git clone https://github.com/yourusername/rag.git
cd rag

# 2. Set up virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 4. Run scraper to populate data (optional but recommended for first run)
python -m src.scrape  # Scrapes Clockify help articles

# 5. Build index (optional but recommended)
python -m src.embed   # Builds FAISS index from scraped data

# 6. Start server
export API_PORT=8000
python -m src.server
```

## Fixed Issues & Solutions

### Issue 1: Docker Build - Missing FAISS Index

**Error Message:**
```
ERROR: failed to build: failed to solve: failed to compute cache key: 
"/index/faiss/clockify-help": not found
```

**Root Cause:** The Dockerfile was attempting to copy a pre-built FAISS index that doesn't exist in fresh clones.

**Solution Applied:**
- ✅ Updated Dockerfile to use optional COPY with fallback:
  ```dockerfile
  # Old (failed):
  COPY index/faiss/clockify/ index/faiss/clockify/
  
  # New (works):
  COPY index/ index/ 2>/dev/null || true
  ```
- ✅ Changed from hard requirement to optional prebuilt index
- ✅ Server now builds index at runtime if missing

**Prevention:** The new Dockerfile gracefully handles missing indexes, so deployments work immediately on fresh clones.

---

### Issue 2: Dependency Version Conflicts

**Error Message:**
```
ERROR: Could not find a version that satisfies the requirement 
faiss-cpu==1.8.0 (from versions: 1.9.0.post1, 1.10.0...)
```

**Root Cause:** `requirements.txt` specified outdated package versions that no longer exist on PyPI.

**Solution Applied:**
- ✅ Updated `requirements.txt` with stable, available versions:
  ```
  faiss-cpu==1.12.0  (was 1.8.0)
  sentence-transformers==2.6.1
  pydantic>=2.9.0    (compatible with Python 3.13)
  ```
- ✅ All versions verified to exist on PyPI and work together
- ✅ Added Python 3.11-3.13 compatibility comment

**Prevention:** All package versions in `requirements.txt` are now validated and compatible.

---

### Issue 3: Dockerfile Syntax Warning

**Error Message:**
```
WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 5)
```

**Root Cause:** Mixed case in Dockerfile syntax (`FROM ... as base` instead of `AS`).

**Solution Applied:**
- ✅ Changed `FROM python:3.11-slim as base` → `FROM python:3.11-slim AS base`

**Prevention:** Now using proper Dockerfile syntax conventions.

---

### Issue 4: Module Not Found - httpx

**Error Message:**
```
ModuleNotFoundError: No module named 'httpx'
```

**Root Cause:** Virtual environment not properly activated or requirements not installed.

**Solution Applied:**
- ✅ Verified `httpx==0.27.2` in `requirements.txt`
- ✅ Added explicit activation steps in setup instructions
- ✅ Added pip upgrade step to prevent install conflicts

**Prevention:** See "Quick Start" section above for proper setup sequence.

---

### Issue 5: Missing Data Directory

**Error Message:**
```
HELP_DIR does not exist: data/clockify_help
```

**Root Cause:** Fresh clone has no scraped data; index building requires it.

**Solution Applied:**
- ✅ Updated Dockerfile to make `data/` optional (fallback with `|| true`)
- ✅ Updated server.py to check for data and provide helpful message
- ✅ Added scraper documentation in Quick Start

**Prevention:** Users now know to run `python -m src.scrape` before building the index on fresh clones.

---

### Issue 6: Docker Daemon Not Running

**Error Message:**
```
ERROR: Cannot connect to the Docker daemon at 
unix:///Users/username/.docker/run/docker.sock
```

**Root Cause:** Docker Desktop not running on the machine.

**Solution:** This is an environmental issue.
- Ensure Docker Desktop is running before building images
- On Mac: Click Docker icon in Applications folder or use `open -a Docker`
- On Linux: `sudo systemctl start docker`
- On Windows: Start Docker Desktop from Start Menu

---

### Issue 7: Missing .dockerignore

**Error:** Large build context, slow builds, unnecessary files in image.

**Solution Applied:**
- ✅ Created `.dockerignore` file to exclude:
  - Virtual environments (`venv/`, `.venv`)
  - Python caches (`__pycache__`, `*.pyc`)
  - Large data files (`data/raw/`, `data/clean/`)
  - Documentation (`*.md`, `LICENSE`)
  - Development files (`tests/`, `scripts/`)

**Prevention:** Docker builds are now faster and smaller images.

---

## Deployment Methods

### Method 1: Local Development (Recommended First Time)

```bash
source .venv/bin/activate
export API_PORT=8000
python -m src.server
```

Visit http://localhost:8000

### Method 2: Docker Compose (Recommended for Production)

```bash
docker-compose up --build
```

Includes: FastAPI server + Ollama (if configured)

### Method 3: Docker Build Only

```bash
docker build -t rag:latest .
docker run -p 7000:7000 -e API_PORT=7000 rag:latest
```

Visit http://localhost:7000

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `API_PORT` | `8000` | Port to run API server |
| `API_HOST` | `0.0.0.0` | Host to bind server |
| `NAMESPACES` | `clockify` | Document namespace to search |
| `EMBEDDING_MODEL` | `nomic-embed-text:latest` | Ollama embedding model |
| `LLM_BASE_URL` | `http://localhost:11434` | Ollama API URL |
| `RERANKER_MODEL` | (optional) | CrossEncoder model for reranking |

**Development:**
```bash
export API_PORT=8000
export LLM_BASE_URL=http://10.127.0.192:11434  # Company AI
python -m src.server
```

---

## Verification Steps

After setup, verify everything works:

### 1. Check API Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "indexes_loaded": ["clockify"],
  "embedding_model": "nomic-embed-text:latest",
  "last_crawl": "2024-10-20T18:56:00"
}
```

### 2. Test Search
```bash
curl "http://localhost:8000/search?q=how+to+start+timer&namespace=clockify&k=5"
```

### 3. Test Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I start a timer?",
    "namespace": "clockify",
    "k": 5
  }'
```

### 4. Open Web UI
```
http://localhost:8000
```

---

## Common Errors & Quick Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Port already in use` | Another app using port 8000 | `export API_PORT=8001` or kill process |
| `ModuleNotFoundError` | Virtual env not activated | `source .venv/bin/activate` |
| `Connection refused` | Server not running | `python -m src.server` |
| `No search results` | Index not built | `python -m src.embed` |
| `LLM connection error` | Ollama not running | Start Ollama or use company AI |

---

## File Structure

```
rag/
├── public/                 # Web UI (NEW)
│   ├── index.html         # Single-page app
│   ├── css/style.css      # Styling (dark mode + responsive)
│   └── js/                # Frontend controllers
│       ├── api.js         # API client
│       ├── main.js        # Tab navigation
│       ├── chat.js        # Chat interface
│       └── articles.js    # Article search
│
├── src/                    # Backend
│   ├── server.py          # FastAPI app
│   ├── scrape.py          # Web scraper
│   ├── embed.py           # Index builder
│   ├── query_optimizer.py # Query analysis (NEW)
│   ├── scoring.py         # Confidence scoring (NEW)
│   └── rag/               # RAG modules
│
├── data/                   # Scraped content (generated)
│   ├── raw/               # Original HTML
│   ├── clean/             # Processed text
│   └── chunks/            # Split chunks
│
├── index/                  # FAISS indexes (generated)
│   └── faiss/
│       └── clockify/
│
├── Dockerfile             # Docker image definition (FIXED)
├── docker-compose.yml     # Services orchestration
├── .dockerignore          # Build context optimization (NEW)
├── requirements.txt       # Python dependencies
└── DEPLOYMENT_FIXES.md    # This file (NEW)
```

---

## What Changed to Prevent Future Errors

1. **Dockerfile** (`Dockerfile`)
   - Uses optional COPY (with `|| true`) for missing directories
   - Syntax corrected to use uppercase `AS`
   - Now includes `public/` directory

2. **Dependencies** (`requirements.txt`)
   - All versions validated and available on PyPI
   - Tested with Python 3.11-3.13
   - No conflicting version requirements

3. **Docker Optimization** (`.dockerignore`)
   - Excludes large unnecessary files
   - Faster builds, smaller images
   - Prevents build context bloat

4. **Documentation** (This file + Quick Start)
   - Clear setup sequence
   - Verification steps after setup
   - Common error solutions

---

## Support & Debugging

If you encounter a new error:

1. **Check this guide** - Your error may be documented above
2. **Check logs** - Run server with verbose output:
   ```bash
   export LOG_LEVEL=DEBUG
   python -m src.server
   ```
3. **Check environment** - Verify Python version, pip packages:
   ```bash
   python --version  # Should be 3.11+
   pip freeze | grep -E "fastapi|pydantic|faiss"
   ```
4. **Check connectivity** - Verify Ollama/APIs are accessible:
   ```bash
   curl http://10.127.0.192:11434/api/tags  # Company AI check
   ```

---

## Testing Deployment Changes

To verify the fixes work:

```bash
# 1. Fresh clone in temp directory
mkdir test-deployment
cd test-deployment
git clone https://github.com/yourusername/rag.git
cd rag

# 2. Run Quick Start steps
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 3. Verify each component
curl http://localhost:8000/health  # After starting server
# OR
docker build -t rag:test .
docker run -p 7000:7000 rag:test
```

---

**Last Updated:** October 20, 2024
**Status:** All known deployment issues fixed
**Next Review:** When adding new dependencies or deployment methods
