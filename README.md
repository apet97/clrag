# Advanced Multi-Corpus RAG Stack

Local, production-ready retrieval-augmented generation system for Clockify Help + LangChain docs. Zero cloud services, full control, state-of-the-art retrieval.

## Features

- **Multi-corpus support** (Clockify + LangChain with namespaces)
- **Advanced retrieval** (Vector search + BM25 hybrid, query rewrites, cross-encoder reranking)
- **Parent-child indexing** (Section-level context + focused chunks)
- **Inline citations** (Bracketed [1], [2] + sources list)
- **Local LLM** (OpenAI-compatible endpoint, oss20b or similar)
- **Async crawling** (robots.txt compliant, 1 req/sec, incremental updates)
- **Comprehensive pipeline** (HTML → Markdown → Parent-child chunks → FAISS + BM25 indexes)

## Quick Start

### Option 1: Company AI (Fastest - 2 min setup)
If you have access to `10.127.0.192:11434` (company AI):

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env
# .env.sample already configured for company AI - verify connection
curl http://10.127.0.192:11434/api/tags
# Then proceed to pipeline
make crawl preprocess chunk embed hybrid
make serve
```

**See [COMPANY_AI_SETUP.md](COMPANY_AI_SETUP.md) for full guide, models, IDE integration, and feedback.**

### Option 2: Local/External LLM (Standard setup)

```bash
# 1. Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env
# Edit .env: set MODEL_BASE_URL to your local/external LLM
# See STEP_BY_STEP_GUIDE.md for LLM setup options

# 2. Crawl + Process
make crawl preprocess chunk embed hybrid

# 3. Serve
make serve

# 4. Test (in another terminal)
curl 'http://localhost:7000/search?q=timesheet&namespace=clockify&k=5'
curl -X POST http://localhost:7000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question":"How do I create a project?","namespace":"clockify","k":5}'
```

## Architecture

### Pipeline
1. **Scrape** (src/scrape.py): Multi-domain async crawling with robots.txt, sitemaps, incremental state
2. **Preprocess** (src/preprocess.py): HTML → Markdown + frontmatter
3. **Chunk** (src/chunk.py): Parent-child nodes (sections + focused spans, 800-1200 tokens)
4. **Embed** (src/embed.py): Multi-namespace FAISS indexes (intfloat/multilingual-e5-base)
5. **Hybrid** (src/hybrid.py): BM25 indexes via whoosh
6. **Retrieve** (src/server.py): Vector + BM25 search, query rewrites, reranking

### Configuration (.env)
- `CRAWL_BASES`: URLs to crawl (comma-separated)
- `DOMAINS_WHITELIST`: Allowed domains
- `PARENT_CHILD_INDEXING`: Enable parent-child nodes (default: true)
- `HYBRID_SEARCH`: Vector + BM25 (default: true)
- `QUERY_REWRITES`: MultiQuery + HyDE (default: true)
- `USE_RERANKER`: Cross-encoder reranking (default: true)
- `MODEL_BASE_URL`, `MODEL_NAME`: Local LLM endpoint

### API Endpoints

**GET /health** – Status + loaded indexes
```bash
curl http://localhost:7000/health
```

**GET /search** – Multi-namespace search
```bash
curl 'http://localhost:7000/search?q=timesheet&namespace=clockify&k=5'
curl 'http://localhost:7000/search?q=retrievers&namespace=langchain&k=5'
```

**POST /chat** – Advanced RAG with citations
```bash
curl -X POST http://localhost:7000/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "How do I create a project?",
    "namespace": "clockify",
    "k": 5,
    "allow_rewrites": true,
    "allow_rerank": true
  }'
```

Response includes answer with inline [1] citations + sources list.

**GET /docs** – Swagger UI

## Advanced Features

### Query Rewriting (MultiQuery)
Generates 3 diverse rewrites of the query to capture different phrasings, improving recall.

### Hybrid Search
Combines vector search (semantic) + BM25 (lexical) via reciprocal rank fusion for better relevance.

### Cross-Encoder Reranking
BAAI/bge-reranker-base re-scores top-50 candidates for better precision.

### Parent-Child Indexing
Retrieves child chunks (focused), expands to parent sections (context), balancing specificity and breadth.

### Inline Citations
Answers include [1], [2] brackets tied to numbered sources with namespace + URL.

## File Structure

```
.env.sample                   # Config template
requirements.txt             # Dependencies
Makefile                     # Automation
src/
  scrape.py                  # Multi-namespace crawler
  preprocess.py              # HTML → Markdown
  chunk.py                   # Parent-child chunking
  embed.py                   # FAISS indexing
  hybrid.py                  # BM25 indexing
  rewrites.py                # Query rewriting
  rerank.py                  # Cross-encoder reranking
  prompt.py                  # RAG templates
  server.py                  # FastAPI server
tests/
  test_pipeline.py           # E2E tests
data/
  raw/{clockify,langchain}/  # Scraped HTML
  clean/{clockify,langchain}/# Markdown
  chunks/                    # *.jsonl per namespace
index/faiss/
  {clockify,langchain}/      # FAISS indexes + meta
  hybrid/{clockify,langchain}/# BM25 indexes
```

## Makefile Targets

- `make setup` – Create venv, install deps
- `make crawl` – Scrape Clockify + LangChain
- `make preprocess` – HTML → Markdown
- `make chunk` – Create parent-child chunks
- `make embed` – Build FAISS indexes
- `make hybrid` – Build BM25 indexes
- `make serve` – Start API on :7000
- `make test` – Run E2E tests
- `make clean` – Remove venv, data, indexes

## Requirements

- Python 3.9+
- 8 GB RAM (4+ GB for embeddings)
- ~2 GB disk
- Local LLM running on MODEL_BASE_URL (Ollama, vLLM, LM Studio)

## Local LLM Setup

### Ollama (Recommended)
```bash
ollama pull orca-mini
ollama serve  # Runs on http://127.0.0.1:11434/v1
# In .env: MODEL_BASE_URL=http://127.0.0.1:11434/v1
```

### vLLM
```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server --model TinyLlama-1.1B-Chat-v1.0
# Default: http://127.0.0.1:8000/v1
```

### LM Studio
Download from https://lmstudio.ai/, load model, start server (default port 1234).

## Performance

- **First setup**: 15-30 min (depends on crawl size + embedding hardware)
- **Incremental crawl**: 2-5 min
- **Search latency**: <100 ms (FAISS)
- **Chat latency**: 5-30 sec (LLM-dominated)
- **Index size**: ~100 MB per namespace
- **Memory**: ~2 GB at runtime (index + embedder)

## Compliance & Security

- Respects robots.txt by default (override with CRAWL_ALLOW_OVERRIDE=true for internal use)
- Rate-limited to 1 req/sec per domain
- No external API calls; all local
- User-Agent: "Clockify-Internal-RAG/1.0"
- Incremental crawling via ETag/Last-Modified

## Troubleshooting

**"No HTML files scraped"**
→ Check internet, verify CRAWL_BASES in .env, check if domain blocks requests.

**"Index not loaded"**
→ Run full pipeline: `make crawl preprocess chunk embed hybrid`

**LLM connection error**
→ Ensure LLM running on MODEL_BASE_URL. Test: `curl http://127.0.0.1:8000/v1/models`

**Slow embeddings**
→ Increase EMBEDDING_BATCH_SIZE in .env (e.g., 64). Use GPU if available.

**OOM errors**
→ Reduce EMBEDDING_BATCH_SIZE, or use smaller embedding model.

## Next Steps

1. Read QUICKSTART.md for step-by-step walkthrough
2. Read OPERATOR_GUIDE.md for tuning and troubleshooting
3. Customize in .env: chunk sizes, reranker, rewrite methods
4. Deploy with Docker/nginx for production
5. Monitor via /health endpoint and logs

## License

MIT

---

See QUICKSTART.md to get started immediately.
