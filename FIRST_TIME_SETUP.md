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

## Quick Start (Recommended - 5 Minutes)

```bash
cd clrag

# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Point to your Ollama server (local or remote)
# For REMOTE Ollama (team server):
export LLM_BASE_URL=http://10.127.0.192:11434

# 4. Verify Ollama is reachable
curl $LLM_BASE_URL/api/tags

# 5. Build FAISS index from pre-cleaned data (uses data/clean/clockify/)
python -m src.ingest

# 6. Now Docker will work!
docker build -t rag-system:latest .
docker-compose up -d
```

**Time:** Step 5 takes 10-15 minutes to embed 102 pre-cleaned help pages

## Option 2: Skip Docker, Use Python Directly

```bash
cd clrag

# 1. Setup Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Set Ollama URL (local or remote)
export LLM_BASE_URL=http://10.127.0.192:11434

# 3. Build FAISS index (uses pre-cleaned data)
python -m src.ingest

# 4. Copy config and update Ollama URL
cp .env.sample .env
# Edit .env and set: LLM_BASE_URL=http://10.127.0.192:11434

# 5. Run server
python -m src.server

# 6. Open http://localhost:7000 in browser
```

## Data Sources and Ingestion

### Recommended: Use Pre-Cleaned Data (Fastest ✅)

The repository includes pre-cleaned, verified Clockify help pages in `data/clean/clockify/`:
- **102 verified help pages** (already curated for quality)
- **No web scraping needed** - data is ready to use
- **Just run ingest:** `python -m src.ingest`

### Alternative: Web Scrape + Ingest (Slower)

If you want fresh data from the web:

1. **Step 1: Scrape (src.scrape)** - COMPREHENSIVE COVERAGE
   - Crawls clockify.me/help and saves ALL pages to `data/raw/clockify/`
   - Time: 15-20 minutes to fetch 2000+ pages (comprehensive coverage)
   - Command: `python -m src.scrape`
   - ✅ **Smart link extraction:**
     - Main content links + Navigation menus
     - Breadcrumb paths + Sidebar links
     - Related articles + Resource sections
     - Sitemap alternates + Deep traversal
   - ✅ **Filters to ONLY help articles** (excludes marketing, non-English variants)
   - ✅ **8x parallel crawling** for speed
   - ✅ **Deep resource discovery** (crawl depth: 5 levels)

2. **Step 2: Ingest (src.ingest)**
   - Processes HTML and creates embeddings with Ollama
   - Time: 10-15 minutes to embed pages
   - Command: `python -m src.ingest`
   - Will automatically use `data/clean/clockify/` if it exists, else uses `data/raw/`

### How Ingest Works

The `src/ingest.py` script automatically:
1. Checks for `data/clean/clockify/` (pre-cleaned, verified data) ✅ **USE THIS**
2. Falls back to `data/raw/clockify/` (from web scrape) if clean data doesn't exist
3. Can override with `HELP_DIR` environment variable if needed

**For best results:** Use the pre-cleaned data in `data/clean/clockify/`

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
