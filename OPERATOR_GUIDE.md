# OPERATOR_GUIDE - Advanced Configuration & Troubleshooting

Production operations for multi-corpus RAG system.

## Configuration Tuning

### Retrieval Quality

**Vector-only search:**
```env
HYBRID_SEARCH=false
USE_RERANKER=true        # Cross-encoder for precision
RETRIEVAL_TOP_K=5
```

**Balanced (recommended):**
```env
HYBRID_SEARCH=true       # Vector + BM25
USE_RERANKER=true        # Cross-encoder reranking
QUERY_REWRITES=true      # MultiQuery variants
RETRIEVAL_TOP_K=5
```

**Recall-focused (comprehensive):**
```env
HYBRID_SEARCH=true
USE_RERANKER=true
QUERY_REWRITES=true      # 3+ query variants
REWRITE_COUNT=5
RETRIEVAL_TOP_K=10       # Return more candidates
```

### Performance Tuning

**For CPU-only systems:**
```env
EMBEDDING_BATCH_SIZE=16  # Lower = less memory
RERANKER_BATCH_SIZE=8
PARENT_CHUNK_TOKENS=2000 # Smaller parents
CHILD_CHUNK_TOKENS=600   # Smaller children
```

**For GPU systems:**
```env
EMBEDDING_BATCH_SIZE=64
RERANKER_BATCH_SIZE=32
PARENT_CHUNK_TOKENS=5000
CHILD_CHUNK_TOKENS=1200
```

**Low-memory (4 GB RAM):**
```env
EMBEDDING_BATCH_SIZE=8
USE_RERANKER=false
HYBRID_SEARCH=false
```

### Chunking Strategy

**Focused retrieval (narrow documents):**
```env
CHILD_CHUNK_TOKENS=600
CHILD_CHUNK_OVERLAP_TOKENS=75
```

**Broad context (large docs):**
```env
PARENT_CHUNK_TOKENS=5000
CHILD_CHUNK_TOKENS=1500
CHILD_CHUNK_OVERLAP_TOKENS=200
```

## Incremental Operations

### Partial Recrawl

Refresh only Clockify help (skip LangChain):

```bash
# Edit .env temporarily
CRAWL_BASES=https://clockify.me/help/
make crawl

# Edit back
CRAWL_BASES=https://clockify.me/help/,https://docs.langchain.com
```

### Rebuild Single Namespace

```bash
# Reprocess + re-index only Clockify
python -m src.preprocess
# Deletes data/chunks/clockify.jsonl
python -m src.chunk
python -m src.embed
python -m src.hybrid

# Restart server
# make serve
```

### Cache Warmup

Pre-load indexes on server startup:

```bash
# Add to src/server.py startup:
# for ns in _indexes:
#     _indexes[ns]["index"].ntotal  # Touch index
```

## Monitoring

### Health Metrics

```bash
# Index status
curl http://localhost:7000/health | jq

# Expected:
# {
#   "status": "ok",
#   "indexes_loaded": 2,
#   "namespaces": ["clockify", "langchain"]
# }
```

### Query Performance

Log query latency (edit src/server.py):

```python
import time
start = time.time()
# ... retrieval code ...
logger.info(f"Query '{q}' took {time.time() - start:.2f}s")
```

### Index Size

```bash
du -sh index/faiss/{clockify,langchain}
# Expected: ~50-100 MB each
```

## Troubleshooting

### Issue: Slow searches

**Diagnosis:**
```bash
curl 'http://localhost:7000/search?q=test' --verbose  # Check latency
```

**Solutions:**
1. Disable reranking: `USE_RERANKER=false`
2. Disable hybrid: `HYBRID_SEARCH=false`
3. Reduce RETRIEVAL_TOP_K
4. Rebuild with smaller chunk size

### Issue: Low retrieval quality

**Diagnosis:**
```bash
# Search for known terms that should match
curl 'http://localhost:7000/search?q=timesheet&namespace=clockify'
# Should return >3 relevant results
```

**Solutions:**
1. Enable query rewrites: `QUERY_REWRITES=true`
2. Enable reranking: `USE_RERANKER=true`
3. Increase RETRIEVAL_TOP_K (retrieve more, rerank)
4. Re-embed with better model (e.g., BAAI/bge-large-en)

### Issue: "No indexes loaded"

**Diagnosis:**
```bash
ls -la index/faiss/clockify/index.bin index/faiss/langchain/index.bin
# Should exist and be >1 MB
```

**Solution:**
```bash
make clean
make crawl preprocess chunk embed hybrid
make serve
```

### Issue: OOM during embedding

**Solutions:**
1. Reduce `EMBEDDING_BATCH_SIZE` in .env
2. Use smaller model: `EMBEDDING_MODEL=all-MiniLM-L6-v2`
3. Embed one namespace at a time:
   ```bash
   # Edit .env: only include one CRAWL_BASE
   make crawl preprocess chunk embed
   # Repeat for other namespace
   ```

### Issue: Crawl hangs or times out

**Diagnosis:**
```bash
# Check if domain is blocking
curl -I -H "User-Agent: Clockify-Internal-RAG/1.0" https://clockify.me/help/
# Should return 200
```

**Solutions:**
1. Increase `CRAWL_TIMEOUT` in .env (default 30s)
2. Reduce `CRAWL_CONCURRENCY` (default 4)
3. Increase `CRAWL_DELAY_SEC` (default 1)
4. Manually add robots.txt permissions in .env (internal use only)

### Issue: LLM connection refused

**Diagnosis:**
```bash
curl http://127.0.0.1:8000/v1/models
# Should return {"object":"list","data":[...]}
```

**Solutions:**
1. Start LLM server (Ollama/vLLM/LM Studio)
2. Verify `MODEL_BASE_URL` in .env matches running server
3. Check firewall/port access:
   ```bash
   netstat -an | grep 8000  # or your port
   ```

## Advanced Operations

### Custom Embeddings

Replace `EMBEDDING_MODEL`:

```env
# Smaller & faster
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Larger & better quality
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2

# Rerank models
RERANKER_MODEL=BAAI/bge-reranker-large
```

Then rebuild:
```bash
make clean && make crawl preprocess chunk embed hybrid
```

### Custom Chunk Boundaries

For specialized corpora, edit src/chunk.py:

```python
# Add custom split logic for LangChain docs
if "langchain" in url:
    sections = custom_split_langchain(text)
```

### Batch Reindexing

Index multiple large corpora:

```bash
# Add to .env
CRAWL_BASES=https://clockify.me/help/

make crawl preprocess chunk embed hybrid
mv data/chunks/clockify.jsonl data/chunks/_clockify.bak
mv index/faiss/clockify index/faiss/_clockify.bak

# Now do LangChain
# CRAWL_BASES=https://docs.langchain.com
# make crawl preprocess chunk embed hybrid

# Merge later if needed
```

### Exporting Results

Export search results for analysis:

```python
import json
from src.server import vector_search, embed_query

query = "How to create a project?"
q_emb = embed_query(query)
results = vector_search(q_emb, "clockify", k=10)

with open("export.jsonl", "w") as f:
    for r in results:
        f.write(json.dumps(r) + "\n")
```

## Performance Benchmarks

Expected performance on standard hardware (8 GB RAM, 4-core CPU):

| Operation | Time |
|-----------|------|
| Crawl (50 pages) | 5-10 min |
| Preprocess | 1-2 min |
| Chunking | 10-30 sec |
| Embedding (1000 chunks, CPU) | 10-20 min |
| Embedding (GPU) | 1-3 min |
| Search latency | <100 ms |
| Chat latency | 5-30 sec (LLM-dominated) |

## Compliance & Audit

### Rate Limiting
- Default: 1 req/sec per domain (configurable: `CRAWL_DELAY_SEC`)
- Respects robots.txt by default
- Override only for internal approved use: `CRAWL_ALLOW_OVERRIDE=true`

### Audit Logging

Enable detailed logs:

```env
LOG_LEVEL=DEBUG
DEBUG=true
```

Check logs:
```bash
# Tail crawl logs
python -m src.scrape 2>&1 | tee crawl.log

# Tail server logs
make serve 2>&1 | tee server.log
```

### Data Retention

Crawl state persists in `data/.crawl_state.json` for incremental updates. Clean if needed:

```bash
rm data/.crawl_state.json
# Next crawl will be full re-crawl
```

## Disaster Recovery

### Full Reset

```bash
make clean
make crawl preprocess chunk embed hybrid
make serve
```

### Partial Reset (keep data, rebuild index)

```bash
rm -rf index/faiss data/chunks/*.jsonl
make chunk embed hybrid
make serve
```

### Backup & Restore

```bash
# Backup indexes
tar czf backup-$(date +%s).tar.gz index/ data/chunks/

# Restore
tar xzf backup-*.tar.gz
make serve
```

## Support & Resources

- **README.md**: Full system architecture
- **QUICKSTART.md**: Getting started
- **Makefile**: `make help` for all targets
- **src/{module}.py**: Docstrings for detailed implementation

---

Contact: See README.md for support channels.
