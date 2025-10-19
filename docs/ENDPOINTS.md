# RAG API Endpoints & Deployment Modes

This document describes the three modes of LLM endpoint configuration and includes validation commands for each.

## Endpoints

### GET /health
Returns server status including index health and LLM endpoint availability.

**Response:**
```json
{
  "ok": true,
  "namespaces": ["clockify", "langchain"],
  "mode": "mock",
  "llm_api_type": "ollama",
  "llm_ok": null,
  "llm_details": null,
  "index_normalized": true,
  "index_normalized_by_ns": {"clockify": true, "langchain": true}
}
```

### GET /config
Returns effective configuration (non-secrets). In production, `llm_base_url` is hidden unless you provide the correct admin token.

**Response:**
```json
{
  "namespaces_env": ["clockify", "langchain"],
  "index_mode": "single",
  "embedding_model": "intfloat/multilingual-e5-base",
  "retrieval_k": 5,
  "llm_base_url": "http://10.127.0.192:11434",
  "llm_chat_path": "/api/chat",
  "llm_tags_path": "/api/tags",
  "llm_timeout_seconds": 30,
  "llm_api_type": "ollama",
  "streaming_enabled": false,
  "env": "dev",
  "mock_llm": false
}
```

**Production Security:** If `ENV=prod` and `llm_base_url` is hidden:
```bash
curl -H "x-admin-token: YOUR_ADMIN_TOKEN" http://localhost:7000/config
```

### GET /search?q={query}&k={k}&namespace={ns}
Retrieves relevant documents without LLM processing.

**Example:**
```bash
curl -H "x-api-token: change-me" \
  'http://localhost:7000/search?q=timesheet&k=5'
```

### POST /chat
Full RAG pipeline: retrieval → LLM generation → citations.

**Example:**
```bash
curl -X POST http://localhost:7000/chat \
  -H "Content-Type: application/json" \
  -H "x-api-token: change-me" \
  -d '{
    "question": "How do I create a project?",
    "k": 5,
    "namespace": null
  }'
```

---

## Deployment Modes

### Mode 1: Internal Ollama over HTTP (Company VPN)

**Use case:** Direct access to company Ollama on internal network.

**Configuration:**
```bash
export MOCK_LLM=false
export LLM_API_TYPE=ollama
export LLM_BASE_URL=http://10.127.0.192:11434
export LLM_CHAT_PATH=/api/chat
export LLM_TAGS_PATH=/api/tags
export LLM_MODEL=gpt-oss:20b
export LLM_TIMEOUT_SECONDS=30
export LLM_VERIFY_SSL=false
```

**Validation:**
```bash
# Test tags endpoint (health check)
curl http://10.127.0.192:11434/api/tags

# Test chat endpoint
curl -X POST http://10.127.0.192:11434/api/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-oss:20b",
    "messages": [{"role":"user","content":"ping"}],
    "stream": false
  }'
```

**Expected:** Tags endpoint returns JSON with `models` or `tags` array. Chat endpoint returns `200 OK` with message.

---

### Mode 2: Reverse-Proxied HTTPS (Company Proxy)

**Use case:** Company exposes Ollama through HTTPS reverse proxy with authentication.

**Configuration:**
```bash
export MOCK_LLM=false
export LLM_API_TYPE=ollama
export LLM_BASE_URL=https://ai.company.tld
export LLM_CHAT_PATH=/ollama/api/chat
export LLM_TAGS_PATH=/ollama/api/tags
export LLM_MODEL=gpt-oss:20b
export LLM_VERIFY_SSL=true  # Auto-detected for https://, but can override
```

**Important:** Ensure the reverse proxy properly exposes both `/ollama/api/chat` and `/ollama/api/tags` endpoints.

**Validation:**
```bash
LLM_BASE_URL="https://ai.company.tld"
LLM_CHAT_PATH="/ollama/api/chat"
LLM_TAGS_PATH="/ollama/api/tags"

# Test tags endpoint
curl ${LLM_BASE_URL}${LLM_TAGS_PATH}

# Test chat endpoint (same Bearer token if needed)
curl -X POST ${LLM_BASE_URL}${LLM_CHAT_PATH} \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-oss:20b",
    "messages": [{"role":"user","content":"ping"}],
    "stream": false
  }'
```

**Expected:** Same as Mode 1, but over HTTPS.

---

### Mode 3: Local Fallback Ollama

**Use case:** Work laptop has local Ollama running.

**Configuration:**
```bash
export MOCK_LLM=false
export LLM_API_TYPE=ollama
export LLM_BASE_URL=http://localhost:11434
export LLM_CHAT_PATH=/api/chat
export LLM_TAGS_PATH=/api/tags
export LLM_MODEL=gpt-oss:20b
```

**Validation:**
```bash
# Check if Ollama is running locally
curl http://localhost:11434/api/tags

# Test chat
curl -X POST http://localhost:11434/api/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-oss:20b",
    "messages": [{"role":"user","content":"test"}],
    "stream": false
  }'
```

**Expected:** Same as Mode 1, but on localhost.

---

## Mock Mode (Development)

**Use case:** Instant testing without real LLM endpoint.

**Configuration:**
```bash
export MOCK_LLM=true
```

**Note:** All other LLM variables are ignored. Responses are template-based and instant (0ms latency).

**Validation:**
```bash
curl http://localhost:7000/health
# Returns: {"ok": true, "llm_ok": null, "mode": "mock", ...}

curl http://localhost:7000/chat \
  -H 'Content-Type: application/json' \
  -d '{"question": "test?", "k": 5}'
# Returns instantly with template response
```

---

## Troubleshooting

### Error: "404 on /api/tags - endpoint not exposed (UI-only URL?)"

**Cause:** LLM endpoint is a web UI URL without API exposure.

**Solutions:**
1. Ensure you have the raw Ollama port (e.g., :11434), not a web UI URL
2. Check that the reverse proxy exposes `/api/chat` and `/api/tags` paths
3. Use local Ollama: `LLM_BASE_URL=http://localhost:11434`

---

### Error: "403 on /api/tags - forbidden (check auth, VPN, firewall)"

**Cause:** Authentication or network access issue.

**Solutions:**
1. Verify VPN connection for company endpoints
2. Check firewall rules
3. If behind proxy, ensure `LLM_BASE_URL` includes proxy URL
4. Verify credentials if endpoint requires authentication

---

### Error: "HTTP 500 on /api/tags"

**Cause:** Ollama/LLM server error.

**Solutions:**
1. Check server logs: `docker logs <ollama-container>`
2. Verify model is loaded: `curl http://<server>/api/tags`
3. Restart Ollama service
4. Check disk space and memory

---

## Deep Health Check

`GET /health?deep=1` performs a lightweight chat ping in addition to the `/api/tags` endpoint check.

**Example:**
```bash
curl 'http://localhost:7000/health?deep=1' | python -m json.tool
```

**Response fields (in addition to basic health):**
- `llm_deep_ok`: boolean or null (null in mock mode)
- `llm_deep_details`: diagnostic string ("chat ping ok", "empty response", or error message)

---

## Streaming

Enable Ollama SSE aggregation (optional, off by default):

```bash
export STREAMING_ENABLED=true
```

**Notes:**
- `/chat` request parameter `stream` is still accepted; when `STREAMING_ENABLED=false`, streaming requests fall back to non-streaming.
- When enabled and the request body includes `"stream": true`, the server aggregates Ollama SSE chunks into a single response.
- Streaming is automatically disabled if the endpoint returns an error.

---

## Security

- **SSL/TLS:** Auto-detected for `https://` base URLs (defaults to `LLM_VERIFY_SSL=true`). Can be overridden with `LLM_VERIFY_SSL`.
- **Admin Token:** In `ENV=prod`, use `x-admin-token: YOUR_ADMIN_TOKEN` header on `/config` to reveal `llm_base_url`.
- **Deprecated:** `LLM_TIMEOUT` alias is supported but logs a warning; use `LLM_TIMEOUT_SECONDS` instead.

---

## Full Integration Test

```bash
#!/bin/bash
set -e

echo "Testing RAG API..."

# Check health
echo "1. Checking health..."
curl http://localhost:7000/health | python -m json.tool

# Check config
echo "2. Checking config..."
curl http://localhost:7000/config | python -m json.tool

# Deep health
echo "3. Testing deep health..."
curl 'http://localhost:7000/health?deep=1' | python -m json.tool

# Search endpoint
echo "4. Testing search..."
curl -H "x-api-token: change-me" \
  'http://localhost:7000/search?q=timesheet&k=3' | python -m json.tool

# Chat endpoint
echo "5. Testing chat..."
curl -X POST http://localhost:7000/chat \
  -H "Content-Type: application/json" \
  -H "x-api-token: change-me" \
  -d '{"question":"How do I track time?","k":3}' | python -m json.tool

echo "✅ All endpoints working!"
```

---

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `MOCK_LLM` | `false` | Use mock responses (instant) |
| `LLM_API_TYPE` | `ollama` | API type: `ollama` or `openai` |
| `LLM_BASE_URL` | `http://10.127.0.192:11434` | Base URL of LLM server |
| `LLM_CHAT_PATH` | `/api/chat` | Path to chat endpoint |
| `LLM_TAGS_PATH` | `/api/tags` | Path to models/tags endpoint |
| `LLM_MODEL` | `gpt-oss20b` | Model name to use |
| `LLM_TIMEOUT_SECONDS` | `30` | Request timeout |
| `LLM_VERIFY_SSL` | `false` | Verify SSL certificates |
| `LLM_RETRIES` | `3` | Retry attempts on failure |
| `LLM_BACKOFF` | `0.75` | Backoff multiplier for retries |

---

**Last Updated:** 2025-10-19
