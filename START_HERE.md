# START HERE - Clockify RAG Stack Quick Reference

**Welcome!** You now have a complete, local RAG system for Clockify help pages. This file shows you exactly what to do next.

---

## The 60-Second Overview

1. **What it does:** Scrapes Clockify help pages, converts to markdown, chunks them, builds a vector index, and serves a RAG API.
2. **How it works:** Entirely local—no cloud services.
3. **What you get:** An API that can search and chat about Clockify help topics.
4. **Time to working system:** 10–25 minutes on first setup.

---

## The Exact Commands (Copy-Paste)

```bash
# Step 1: Setup (first time only, ~3-5 minutes)
make setup

# Step 2: Scrape, process, and index (~5-15 minutes)
make crawl preprocess embed

# Step 3: Start the API server (keep this running)
make serve
```

**Then in a new terminal:**

```bash
# Test that it works
curl http://localhost:7000/health

# See what's working
make test
```

**That's it!** You now have a running RAG API on `http://localhost:7000`.

---

## Optional: Add Chat with Local LLM

The `/chat` endpoint requires a local LLM. Pick one:

### Option A: Ollama (Recommended)
```bash
# Terminal 1: Download and run Ollama
ollama pull orca-mini
ollama serve

# Terminal 2: Run RAG server (see step 3 above)
make serve

# Terminal 3: Test chat
curl -X POST http://localhost:7000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question":"How do I create a project?","k":5}'
```

### Option B: vLLM
```bash
# Terminal 1:
pip install vllm
python -m vllm.entrypoints.openai.api_server --model TinyLlama-1.1B-Chat-v1.0

# Terminal 2: Run RAG server
make serve
```

### Option C: LM Studio
1. Download from https://lmstudio.ai/
2. Load a model (e.g., Orca Mini)
3. Start the server (runs on http://127.0.0.1:1234/v1 by default)
4. Edit `.env`: set `MODEL_BASE_URL=http://127.0.0.1:1234/v1`
5. Run `make serve`

---

## API Endpoints

Once the server is running, you can:

### Health Check
```bash
curl http://localhost:7000/health
```

### Search Help Pages
```bash
curl 'http://localhost:7000/search?q=timesheet&k=5'
```

### Chat (requires LLM)
```bash
curl -X POST http://localhost:7000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question":"How do I track time?","k":5}'
```

### Interactive Swagger Docs
Open `http://localhost:7000/docs` in your browser.

---

## File Organization

| File/Folder | Purpose |
|------------|---------|
| `QUICKSTART.md` | Step-by-step guide for new users |
| `OPERATOR_GUIDE.md` | Detailed operator manual with all options |
| `README.md` | Complete reference (setup, config, API, troubleshooting) |
| `MANIFEST.md` | Complete file inventory |
| `.env.sample` | Configuration template |
| `Makefile` | Automation (7 targets) |
| `src/` | Source code (7 Python modules) |
| `tests/` | E2E test suite |
| `data/` | Scraped pages and index (created at runtime) |

---

## Configuration (Optional)

All defaults work great! But if you want to customize:

```bash
cp .env.sample .env
# Edit .env in your editor
```

**Key options:**
- `CRAWL_CONCURRENCY=4` — Number of parallel crawlers (default: 4)
- `CRAWL_DELAY_SEC=1` — Rate limiting (default: 1 request/sec)
- `MODEL_BASE_URL=http://127.0.0.1:8000/v1` — LLM endpoint
- `CHUNK_TARGET_TOKENS=1000` — Chunk size (default: 1000)

---

## Common Questions

**Q: How long does setup take?**  
A: ~15-25 minutes total (setup 5 min + crawl 5 min + embed 5-15 min depending on CPU).

**Q: Can I run this on a Mac/Windows/Linux?**  
A: Yes, it works on all platforms. Just ensure Python 3.9+.

**Q: Do I need GPU?**  
A: No, but it helps. GPU will make embedding 5-10x faster.

**Q: Is my internet used after setup?**  
A: No, everything runs locally after the crawl. Incremental crawls need internet.

**Q: Can I customize the crawled content?**  
A: Yes. Edit `src/preprocess.py` to change HTML cleaning, chunking, etc.

**Q: How do I update the index with new pages?**  
A: Just run `make crawl preprocess embed` again. It's incremental!

**Q: Where does the data go?**  
A: `data/raw/` (HTML), `data/clean/` (Markdown), `data/chunks/` (chunks), `index/faiss/` (index).

---

## Troubleshooting

**"No HTML files scraped"**  
→ Check your internet. Verify Clockify isn't blocking you. See `OPERATOR_GUIDE.md`.

**"Index not loaded" error**  
→ Run the full pipeline first: `make setup && make crawl preprocess embed`

**LLM call fails**  
→ Make sure your LLM server is running (Ollama, vLLM, or LM Studio).

**Slow embeddings**  
→ Increase `EMBEDDING_BATCH_SIZE` in `.env` (e.g., 64 or 128).

See `README.md` or `OPERATOR_GUIDE.md` for more troubleshooting.

---

## What's Included

✅ **Web Scraper** — Async crawler with robots.txt compliance  
✅ **HTML Processing** — Converts to clean markdown  
✅ **Semantic Chunking** — Smart splitting with overlap  
✅ **FAISS Indexing** — Fast vector search  
✅ **FastAPI Server** — 3 endpoints (/health, /search, /chat)  
✅ **RAG Templates** — Domain-specific prompts  
✅ **E2E Tests** — Verify everything works  
✅ **Complete Docs** — 5 documentation files  
✅ **MIT License** — Open source  

---

## Next Steps

1. **Run the setup:**
   ```bash
   make setup
   ```

2. **Crawl and index:**
   ```bash
   make crawl preprocess embed
   ```

3. **Start the server:**
   ```bash
   make serve
   ```

4. **Test in another terminal:**
   ```bash
   curl http://localhost:7000/health
   make test
   ```

5. **Explore the docs:**
   - `README.md` — Full reference
   - `OPERATOR_GUIDE.md` — Detailed manual
   - `QUICKSTART.md` — Alternative quick start

---

## Support

- 📖 **Full docs:** `README.md`
- 🚀 **Quick start:** `QUICKSTART.md`
- 👤 **Operator manual:** `OPERATOR_GUIDE.md`
- 📋 **File manifest:** `MANIFEST.md`
- 💻 **Code docs:** Docstrings in `src/`

---

**Ready? Run:**
```bash
make setup && make crawl preprocess embed && make serve
```

**Then test in a new terminal:**
```bash
curl http://localhost:7000/health
```

Enjoy your local Clockify RAG system! 🚀
