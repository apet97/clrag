# First Time Setup - Build FAISS Index

**If you're getting "index/faiss/clockify not found" error or "HELP_DIR does not exist" error:**

Fresh clones need to build the index for the first time. This is a 3-step process:

1. **Setup Python environment** - Install dependencies
2. **Crawl and ingest data** - Fetch Clockify help pages and build FAISS index (requires Ollama)
3. **Build Docker image** - Package everything for deployment

## Python Version

**Recommended: Python 3.11, 3.12, or 3.13**

All dependencies have pre-built wheels for these versions. If you have Python 3.14+, you may need to build from source, which requires a C compiler.

**Check your Python version:**
```bash
python3 --version
```

If you have 3.14+, consider using Python 3.13 instead (see Optional: Use Specific Python Version below).

## Quick Start (Recommended)

```bash
cd clrag

# 1. Create virtual environment (uses current Python)
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

# 5. Scrape Clockify Help (creates data/raw/)
python -m src.scrape

# 6. Build the FAISS index (this processes and embeds pages)
python -m src.ingest

# 7. Now Docker will work!
docker build -t rag-system:latest .
docker-compose up -d
```

**Note:** Steps 5-6 take 10-20 minutes total to crawl 200+ pages and embed them

## Option 2: Skip Docker, Use Python Directly

```bash
cd clrag

# 1. Setup Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Set Ollama URL (local or remote)
export LLM_BASE_URL=http://10.127.0.192:11434  # Your team's Ollama

# 3. Scrape Clockify Help
python -m src.scrape

# 4. Build FAISS index
python -m src.ingest

# 5. Copy config and update Ollama URL
cp .env.sample .env
# Edit .env and set: LLM_BASE_URL=http://10.127.0.192:11434

# 6. Run server
python -m src.server

# 7. Open http://localhost:7000 in browser
```

## Two-Step Process: Scrape → Ingest

The setup involves two separate scripts:

### Step 1: Scrape (src.scrape)
- **What it does:** Crawls clockify.me/help and saves pages to `data/raw/`
- **Time:** 5-10 minutes to fetch 200+ pages
- **Command:** `python -m src.scrape`
- **Output:** Raw HTML files in `data/raw/clockify/`

### Step 2: Ingest (src.ingest)
- **What it does:**
  - Processes HTML from `data/raw/`
  - Creates embeddings using Ollama's `nomic-embed-text` model
  - Builds FAISS index at `index/faiss/clockify/`
  - Creates metadata file `index/faiss/clockify/meta.json`
- **Time:** 5-10 minutes to process and embed pages
- **Command:** `python -m src.ingest`
- **Requires:** Ollama running with `nomic-embed-text` model available

### Remote Ollama Setup

If your team has Ollama hosted on a remote server:

```bash
# Set the remote Ollama URL before ingesting
export LLM_BASE_URL=http://10.127.0.192:11434

# Test connectivity
curl http://10.127.0.192:11434/api/tags

# Then run scrape and ingest
python -m src.scrape
python -m src.ingest
```

The URL will be saved in `.env` and persists across deployments.

### Why Two Steps?

1. **Scrape (src.scrape)** - Fetches content from the web
2. **Ingest (src.ingest)** - Processes and embeds with Ollama

This separation allows you to:
- Cache crawled data and re-ingest with different settings
- Skip scraping if you have cached data already

## After Index is Built

Once `index/faiss/clockify/` exists, you can use Docker:

```bash
# Now this will work!
docker build -t rag-system:latest .
docker-compose up -d

# Open http://localhost:7000
```

---

## Optional: Use Specific Python Version

If you have Python 3.14+ and want to use Python 3.13 instead:

```bash
# macOS with Homebrew
brew install python@3.13

# Then specify it when creating venv
python3.13 -m venv .venv
source .venv/bin/activate

# Or on older setups
/usr/local/bin/python3.13 -m venv .venv
source .venv/bin/activate
```

**Why?** Python 3.14+ doesn't have pre-built wheels for all packages, which requires C compiler and build tools. Python 3.11-3.13 are guaranteed to work.

## Troubleshooting

### "ModuleNotFoundError: No module named 'httpx'"
**Cause:** Virtual environment wasn't created or pip install failed

**Fix:**
```bash
# Delete old venv and start fresh
rm -rf .venv

# Create new venv with Python 3.13 (or current Python if 3.13 unavailable)
python3 -m venv .venv
source .venv/bin/activate

# Reinstall everything
pip install -r requirements.txt
```

### "pip install fails with 'Failed to build...'"
**Cause:** You're using Python 3.14+ (needs compiler) or missing build tools

**Fix:**
```bash
# Use Python 3.13 instead (see section above)
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick Summary

1. **First time?** → Run Python setup + `python -m src.scrape` + `python -m src.ingest`
2. **Index exists?** → Use Docker: `docker build ... && docker-compose up`

That's it! 🚀
