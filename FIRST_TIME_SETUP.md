# First Time Setup - Build FAISS Index

**If you're getting "index/faiss/clockify not found" error or "HELP_DIR does not exist" error:**

Fresh clones need to build the index for the first time. This is a 3-step process:

1. **Setup Python environment** - Install dependencies
2. **Crawl and ingest data** - Fetch Clockify help pages and build FAISS index (requires Ollama)
3. **Build Docker image** - Package everything for deployment

## Quick Start (Recommended)

```bash
cd clrag

# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Point to your Ollama server (local or remote)
# For LOCAL Ollama:
export LLM_BASE_URL=http://localhost:11434

# OR for REMOTE Ollama (team server):
export LLM_BASE_URL=http://10.127.0.192:11434  # Replace with your team's IP

# 4. Verify Ollama is reachable
curl $LLM_BASE_URL/api/tags

# 5. Build the FAISS index (this fetches clockify.me/help pages)
python -m src.ingest

# 6. Now Docker will work!
docker build -t rag-system:latest .
docker-compose up -d
```

**Note:** Step 5 takes 5-15 minutes to crawl and embed ~200 pages from clockify.me/help

## Option 2: Skip Docker, Use Python Directly

```bash
cd clrag

# 1. Setup Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Set Ollama URL (local or remote)
export LLM_BASE_URL=http://10.127.0.192:11434  # Your team's Ollama

# 3. Build index
python -m src.ingest

# 4. Copy config and update Ollama URL
cp .env.sample .env
# Edit .env and set: LLM_BASE_URL=http://10.127.0.192:11434

# 5. Run server
python -m src.server

# 6. Open http://localhost:7000 in browser
```

## What src.ingest Does

The ingestion process requires pre-crawled HTML/markdown files in `data/clockify_help/`:

1. **Reads files** from `data/clockify_help/` (HTML/markdown files)
2. **Creates embeddings** using Ollama's `nomic-embed-text` model
3. **Builds FAISS index** at `index/faiss/clockify/`
4. **Creates metadata** in `index/faiss/clockify/meta.json`

**NOTE:** Fresh clones don't include pre-crawled HTML files. You must either:
- **Option A:** Run the web crawler first to populate `data/clockify_help/`
- **Option B:** Use pre-built index if available (check if `index/faiss/clockify/` already exists)

### Option A: Crawl Data First (Recommended)

```bash
# Set Ollama URL (local or team server)
export LLM_BASE_URL=http://10.127.0.192:11434

# Verify connection
curl $LLM_BASE_URL/api/tags

# Run ingestion (crawls clockify.me/help and builds index)
python -m src.ingest
```

This will:
1. Fetch pages from `https://clockify.me/help/*`
2. Save HTML to `data/clockify_help/`
3. Create FAISS index using remote Ollama
4. Takes 5-15 minutes depending on internet speed

### Remote Ollama Setup

If your team has Ollama hosted on a remote server:

```bash
# Set the remote Ollama URL
export LLM_BASE_URL=http://10.127.0.192:11434

# Test connectivity
curl http://10.127.0.192:11434/api/tags

# Then proceed with ingestion
python -m src.ingest
```

The URL will be saved in the Docker configuration, so it persists across deployments.

## After Index is Built

Once `index/faiss/clockify/` exists, you can use Docker:

```bash
# Now this will work!
docker build -t rag-system:latest .
docker-compose up -d

# Open http://localhost:7000
```

---

## Quick Summary

1. **First time?** → Run Python setup + `python -m src.ingest`
2. **Index exists?** → Use Docker: `docker build ... && docker-compose up`

That's it! 🚀
