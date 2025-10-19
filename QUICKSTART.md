# QUICKSTART - Multi-Corpus RAG in 10 Minutes

Complete setup for Clockify + LangChain dual-corpus retrieval system.

## Prerequisites

- Python 3.9+
- 8 GB RAM
- ~2 GB disk
- Internet (for initial crawl only)

## Step 1: Clone & Setup (3 min)

```bash
cd /path/to/rag
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Configure (1 min)

```bash
cp .env.sample .env
nano .env  # or open in editor

# Critical: Set local LLM endpoint
# MODEL_BASE_URL=http://127.0.0.1:8000/v1  (vLLM default)
# or
# MODEL_BASE_URL=http://127.0.0.1:11434/v1  (Ollama)
# or leave default if using LM Studio on 1234
```

## Step 3: Crawl (5-15 min, first time only)

Scrape Clockify Help + LangChain docs, respecting robots.txt.

```bash
make crawl

# Watch progress in terminal
# Expected: ~50-100 pages per corpus
# Files: data/raw/clockify/*.html + data/raw/langchain/*.html
```

## Step 4: Process (2 min)

Extract markdown, create parent-child chunks.

```bash
make preprocess chunk
```

Expected output:
- `data/clean/{clockify,langchain}/*.md` (markdown with frontmatter)
- `data/chunks/{clockify.jsonl,langchain.jsonl}` (parent-child chunks)

## Step 5: Index (5-10 min, depends on CPU/GPU)

Build FAISS vector indexes + BM25 full-text indexes.

```bash
make embed hybrid
```

Expected output:
- `index/faiss/{clockify,langchain}/{index.bin,meta.json}` (FAISS)
- `index/faiss/hybrid/{clockify,langchain}/` (BM25)

## Step 6: Start Server

```bash
make serve

# Output:
# Uvicorn running on http://0.0.0.0:7000
# [Press Ctrl+C to stop]
```

**Keep this terminal open!** Open new terminal for testing.

## Step 7: Test in New Terminal

### Health Check
```bash
curl http://localhost:7000/health

# Expected:
# {"status":"ok","timestamp":"...","indexes_loaded":2,"namespaces":["clockify","langchain"]}
```

### Search Clockify
```bash
curl 'http://localhost:7000/search?q=timesheet&namespace=clockify&k=5'

# Returns 5 Clockify help chunks about timesheets
```

### Search LangChain
```bash
curl 'http://localhost:7000/search?q=retrievers&namespace=langchain&k=5'

# Returns 5 LangChain doc chunks about retrievers
```

### Chat with LLM (requires local LLM running!)

**IMPORTANT:** Start your local LLM FIRST:

**Ollama:**
```bash
# Terminal A: Start Ollama
ollama pull orca-mini
ollama serve

# Terminal B: Your test terminal (keep running)
# Continue below...
```

**vLLM:**
```bash
# Terminal A: Start vLLM
python -m vllm.entrypoints.openai.api_server --model TinyLlama-1.1B-Chat-v1.0

# Terminal B: Continue below
```

**LM Studio:**
Open LM Studio app, load model, start server. It runs on port 1234 by default.

Now test chat:
```bash
curl -X POST http://localhost:7000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question":"How do I create a project?","namespace":"clockify","k":5}'

# Expected: Answer with inline [1] citations + sources list
```

### Swagger UI

Open in browser: `http://localhost:7000/docs`

## Full End-to-End Command

```bash
# One-liner for impatient users (after setup)
source .venv/bin/activate && make crawl preprocess chunk embed hybrid && make serve
```

## What Just Happened?

1. **Scraped** 50-100 pages from each corpus
2. **Extracted** clean markdown with structure preserved
3. **Chunked** into parent sections + focused child nodes (parent-child indexing)
4. **Embedded** each chunk with multilingual E5 model
5. **Indexed** with FAISS (vector) + Whoosh (BM25)
6. **Served** multi-corpus RAG API with hybrid search, query rewrites, reranking

## Incremental Updates

To refresh index with new pages:

```bash
make crawl preprocess chunk embed hybrid
```

Only fetches changed pages (via ETag/Last-Modified).

## Customization

Edit `.env` before running pipeline:

- `PARENT_CHUNK_TOKENS=3500` – Section size
- `CHILD_CHUNK_TOKENS=1000` – Chunk size
- `QUERY_REWRITES=true` – Enable query variants
- `USE_RERANKER=true` – Enable cross-encoder
- `HYBRID_SEARCH=true` – Enable BM25

Then restart: `make crawl ... && make serve`

## Local LLM Options

### Ollama (Easiest)
```bash
ollama pull orca-mini
ollama serve
# Set in .env: MODEL_BASE_URL=http://127.0.0.1:11434/v1
```

### vLLM (Faster GPU)
```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server --model TinyLlama-1.1B-Chat-v1.0
# Runs on http://127.0.0.1:8000/v1 (default)
```

### LM Studio (GUI)
1. Download https://lmstudio.ai/
2. Load model (e.g., Orca Mini)
3. Start local server
4. Set in .env: `MODEL_BASE_URL=http://127.0.0.1:1234/v1`

## Troubleshooting

### "Index not loaded" error
→ `make embed hybrid` didn't finish. Re-run it.

### "No HTML files" scraped
→ Check internet. Verify CRAWL_BASES in .env. Check if domain blocks you.

### Slow embedding
→ Increase `EMBEDDING_BATCH_SIZE` in .env (e.g., 64). Use GPU if available.

### Chat returns error
→ Ensure local LLM is running. Test: `curl http://127.0.0.1:8000/v1/models`

### Out of memory
→ Reduce `EMBEDDING_BATCH_SIZE`. Use smaller embedding model.

## Next

- Full docs: `README.md`
- Ops guide: `OPERATOR_GUIDE.md`
- API docs: `http://localhost:7000/docs` (live Swagger)

---

**You're ready!** 🚀
