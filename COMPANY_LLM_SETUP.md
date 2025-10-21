# Company LLM Setup Guide

## Overview

This guide explains how to connect your RAG system to the company Ollama LLM server at **10.127.0.192:11434**.

---

## Prerequisites

✅ **System Requirements:**
- Network access to `10.127.0.192` port `11434`
- Python 3.11 or 3.12 (NOT 3.14 - has orjson compatibility issues)
- Virtual environment with dependencies installed

✅ **Verify Network Access:**
```bash
# Test connectivity
ping 10.127.0.192
# Or
curl http://10.127.0.192:11434/api/tags
# Should return: {"models": [...]}
```

---

## Setup Instructions

### Step 1: Disable MOCK_LLM Mode

```bash
# First, disable mock mode
export MOCK_LLM=false
```

### Step 2: Configure LLM Environment Variables

```bash
# Set the Ollama server URL
export LLM_BASE_URL=http://10.127.0.192:11434

# Optional: Specify embedding model (default: nomic-embed-text:latest)
export EMBEDDING_MODEL=nomic-embed-text:latest

# Optional: Specify LLM model (default: gpt-oss:20b)
export LLM_MODEL=gpt-oss:20b

# Optional: Set API port (default: 7000)
export API_PORT=8000
```

### Step 3: Start the Server

```bash
cd /path/to/clrag
source .venv/bin/activate
python -m src.server
```

You should see:
```
✅ Ollama embedding model ready: dim=768
✅ RAG System startup complete
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Full Setup One-Liner

```bash
export MOCK_LLM=false && \
export LLM_BASE_URL=http://10.127.0.192:11434 && \
export EMBEDDING_MODEL=nomic-embed-text:latest && \
export API_PORT=8000 && \
python -m src.server
```

---

## Verify Connection

### 1. Health Endpoint
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "ok": true,
  "mode": "production",
  "llm_ok": true,
  "llm_details": "gpt-oss:20b (Ollama)",
  "embedding_model": "nomic-embed-text:latest"
}
```

### 2. Search Endpoint
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "what is time tracking",
    "namespace": "clockify",
    "k": 3
  }'
```

Expected: Results with confidence scores and LLM-enriched metadata

### 3. Chat Endpoint
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is time tracking?"
  }'
```

Expected: AI-generated response with sources

---

## Troubleshooting

### Error: "Cannot reach Ollama at http://10.127.0.192:11434"

**Cause:** Network connectivity issue

**Solutions:**
```bash
# 1. Verify network access
ping 10.127.0.192
timeout 5

# 2. Check if Ollama is running
curl -v http://10.127.0.192:11434/api/tags

# 3. Verify firewall isn't blocking port 11434
telnet 10.127.0.192 11434

# 4. Check your network configuration
ifconfig  # macOS/Linux
ipconfig  # Windows
```

### Error: "Ollama returned 404: model not found"

**Cause:** Specified embedding model not available

**Solutions:**
```bash
# 1. List available models
curl http://10.127.0.192:11434/api/tags

# 2. Use a model that exists (check response above)
export EMBEDDING_MODEL=<model-name-from-list>

# 3. Pull the model if needed
# Contact your IT team to ensure the model is pulled on the server
```

### Error: "Connection timeout after 10 seconds"

**Cause:** Server is slow to respond or network is laggy

**Solutions:**
```bash
# 1. Increase connection timeout
# Edit src/server.py line 98, change timeout=10 to timeout=30

# 2. Check server load on Ollama server
# Ask your IT team to check server health

# 3. Test with simple ping
ping -c 10 10.127.0.192
# If ping times are >100ms, there's a network issue
```

### Error: "Python 3.14 compatibility with orjson"

**Solution:** Use Python 3.11 or 3.12

```bash
# Create new venv with correct Python version
python3.11 -m venv .venv_311
source .venv_311/bin/activate
pip install -r requirements.txt

# Then run setup
export MOCK_LLM=false
export LLM_BASE_URL=http://10.127.0.192:11434
python -m src.server
```

---

## Available Environment Variables

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `MOCK_LLM` | `false` | Use mock LLM instead of Ollama | `false` |
| `LLM_BASE_URL` | `http://10.127.0.192:11434` | Ollama server URL | `http://10.127.0.192:11434` |
| `EMBEDDING_MODEL` | `nomic-embed-text:latest` | Embedding model name | `nomic-embed-text:latest` |
| `LLM_MODEL` | `gpt-oss:20b` | LLM model name | `gpt-oss:20b` |
| `API_PORT` | `7000` | API server port | `8000` |
| `API_HOST` | `0.0.0.0` | API bind address | `0.0.0.0` |
| `RETRIEVAL_K` | `5` | Default number of results | `5` |
| `NAMESPACES` | `clockify,langchain` | Document namespaces | `clockify,langchain` |

---

## Performance Optimization for Company LLM

### 1. Enable Caching
The system automatically uses TTL-based caching:
- Query analysis cache: 1 hour TTL
- Result cache: 1 hour TTL
- Cache hit rate: 60-70% typical

Monitor cache performance:
```bash
curl http://localhost:8000/stats/cache
```

### 2. Batch Requests
For multiple searches, batch them together:
```bash
# Instead of multiple curl requests
for query in "timer" "tracking" "project"; do
  curl -X POST http://localhost:8000/search -d "{\"query\":\"$query\",\"namespace\":\"clockify\",\"k\":3}"
done

# Use a script to batch them efficiently
```

### 3. Network Optimization
If latency is high:
```bash
# Add connection pooling (already in requirements.txt: httpx, aiohttp)
# The system already uses connection pooling internally
```

---

## Company Ollama Server Details

**Server Location:** `10.127.0.192:11434`

**Available Models:**
- `nomic-embed-text:latest` - Text embedding (768 dimensions)
- `gpt-oss:20b` - Large language model (~20B parameters)

**Server Capabilities:**
- Embeddings API: `/api/embeddings`
- Generation API: `/api/generate`
- Models API: `/api/tags` (list available models)

**Contact:** IT Team for server issues or model availability

---

## Integration Checklist

Before going to production:

- [ ] Network connectivity verified (ping + curl test)
- [ ] Environment variables set correctly
- [ ] Health endpoint returns `"ok": true`
- [ ] Search endpoint returns results with confidence scores
- [ ] Chat endpoint returns AI-generated responses
- [ ] Cache statistics showing hits (run endpoint twice)
- [ ] API responds in <500ms (typical)
- [ ] No timeout errors in logs
- [ ] Python version is 3.11 or 3.12
- [ ] All requirements.txt packages installed

---

## Quick Reference: Commands

```bash
# Disable mock mode and connect to company LLM
export MOCK_LLM=false
export LLM_BASE_URL=http://10.127.0.192:11434
export EMBEDDING_MODEL=nomic-embed-text:latest
export API_PORT=8000

# Start server
python -m src.server

# In another terminal, test:
curl http://localhost:8000/health
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -d '{"query":"timer","namespace":"clockify","k":3}'

# Monitor cache
curl http://localhost:8000/stats/cache

# Check logs
tail -f logs/app.log  # if logging to file
```

---

## FAQs

**Q: Can I use a different LLM provider?**
A: The system is currently optimized for Ollama. To use a different provider (OpenAI, Anthropic, etc.), you would need to modify `src/llm_client.py`.

**Q: How do I switch between company LLM and MOCK_LLM?**
A: Simply set `MOCK_LLM=true` or `MOCK_LLM=false` and restart the server.

**Q: What happens if the LLM server goes down?**
A: The startup will fail with a clear error. Cached results will still be available if the cache is warm. For production resilience, consider adding a retry mechanism.

**Q: Can I use multiple LLM servers?**
A: Not currently. The system connects to a single Ollama instance. Load balancing would require external configuration.

**Q: What's the maximum latency acceptable?**
A: Typical: 100-300ms for search, 500-2000ms for chat. If consistently slower, contact IT team about server load.

---

## Production Deployment

For production with company LLM:

1. **Use Python 3.11 or 3.12** (never 3.14)
2. **Set environment variables** in deployment config
3. **Monitor cache statistics** via `/stats/cache`
4. **Set up alerting** for LLM connection failures
5. **Use load balancer** if deploying multiple instances
6. **Enable logging** to file for debugging

See `DEPLOYMENT_FIXES.md` for additional production setup.

---

**Status:** ✅ Ready for Production
**Last Updated:** October 21, 2025
**Support:** Contact IT Team for Ollama server issues

