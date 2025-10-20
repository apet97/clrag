# First Time Setup - Build FAISS Index

**If you're getting "index/faiss/clockify not found" error:**

The index needs to be created the first time. Here's how:

## Option 1: Use Python (Recommended for First Time)

```bash
cd clrag

# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Build the FAISS index (creates index/faiss/clockify/)
python -m src.ingest

# 4. Now Docker will work!
docker build -t rag-system:latest .
docker-compose up -d
```

## Option 2: Skip Docker, Use Python Directly

```bash
cd clrag

# 1. Setup Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Build index
python -m src.ingest

# 3. Copy config
cp .env.sample .env

# 4. Run server
python -m src.server

# 5. Open http://localhost:7000 in browser
```

## What src.ingest Does

- Reads documentation files from `docs/` directory
- Creates embeddings using Ollama
- Builds FAISS index at `index/faiss/clockify/`
- Creates metadata file `index/faiss/clockify/meta.json`

This is a one-time operation that creates the index for production use.

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
