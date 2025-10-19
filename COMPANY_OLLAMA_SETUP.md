# Company Ollama Setup Guide

**For:** Deploying Clockify RAG with company-hosted Ollama
**Status:** ✅ Updated for HTTPS company endpoints

---

## What Changed

The LLM client now supports:
- ✅ Ollama API format (`/api/chat` endpoint)
- ✅ HTTPS connections (company servers)
- ✅ Self-signed SSL certificates
- ✅ Environment variable configuration
- ✅ Automatic fallback modes

---

## Critical Information to Get from IT

Before deploying, ask your IT team for these details:

### 1. Ollama Endpoint URL
```
Question: "What's the Ollama endpoint URL for gpt-oss20b?"
Expected: https://192.168.x.x:8080/api/chat
          or
          https://ollama-server.company.com/api/chat
```

### 2. Model Name Verification
```
Question: "Is the model name exactly 'gpt-oss20b'?"
Common variants:
  - gpt-oss20b
  - gpt-oss-20b
  - oss20b
```

### 3. Authentication (if needed)
```
Question: "Does the Ollama endpoint require authentication?"
If yes, ask about:
  - API key format
  - Header format (Bearer token, etc.)
  - Any special authentication requirements
```

### 4. SSL Certificate
```
Question: "Is the SSL certificate self-signed?"
If yes:
  - We already handle this in code (verify=False)
  - But let IT know if you get SSL errors
```

### 5. Rate Limiting
```
Question: "Are there any usage limits or rate limits?"
Examples:
  - Concurrent request limits
  - Requests per minute
  - Daily quota
```

---

## Work Laptop Configuration

### Step 1: Copy Configuration Template

```bash
# Copy the example config
cp .env.example .env
```

### Step 2: Edit .env with Company Details

```bash
# .env file
LLM_ENDPOINT=https://your-actual-company-ip/api/chat
LLM_MODEL=gpt-oss20b
LLM_API_TYPE=ollama
MOCK_LLM=false
FAISS_ENDPOINT=http://localhost:8888
API_PORT=8000
```

### Step 3: Test Connection Before Deploying

```bash
# Replace [company-ip] with actual IP from IT
curl -X POST https://[company-ip]/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-oss20b",
    "messages": [{"role": "user", "content": "Say hello"}],
    "stream": false
  }'

# Expected response:
# {
#   "message": {
#     "role": "assistant",
#     "content": "Hello!"
#   },
#   "model": "gpt-oss20b",
#   ...
# }
```

### Step 4: Verify with Python

```bash
# Activate venv
source .venv/bin/activate

# Test connection
python -c "
from src.llm.local_client import LocalLLMClient
client = LocalLLMClient(api_type='ollama')
print(f'Mock mode: {client.mock_mode}')
print(f'Endpoint: {client.endpoint}')
if client.test_connection():
    print('✅ Connection successful!')
else:
    print('❌ Connection failed!')
"
```

---

## API Request Format (Ollama vs OpenAI)

### Company Ollama API (what we use now)

```
POST https://[company-ip]/api/chat
Content-Type: application/json

{
  "model": "gpt-oss20b",
  "messages": [
    {"role": "system", "content": "You are helpful assistant"},
    {"role": "user", "content": "How do I track time?"}
  ],
  "stream": false,
  "temperature": 0.2
}

Response:
{
  "message": {
    "role": "assistant",
    "content": "To track time..."
  },
  "model": "gpt-oss20b"
}
```

### Personal PC OpenAI Format (what we built with)

```
POST http://localhost:8080/v1/chat/completions
Content-Type: application/json

{
  "model": "oss20b",
  "messages": [...],
  "max_tokens": 500,
  "temperature": 0.2,
  "top_p": 0.9,
  "stream": false
}

Response:
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "To track time..."
    }
  }]
}
```

---

## Troubleshooting

### Issue: "Cannot connect to LLM"

**Check 1: Is endpoint correct?**
```bash
# Verify the URL format
echo "Your endpoint: [copy from .env LLM_ENDPOINT]"

# Should be: https://[ip]/api/chat
# NOT: https://[ip]/v1/chat/completions (that's OpenAI format)
```

**Check 2: Test with curl first**
```bash
# This should work if endpoint is correct
curl -X POST https://[company-ip]/api/chat \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-oss20b","messages":[{"role":"user","content":"test"}],"stream":false}'
```

**Check 3: Network connectivity**
```bash
# Can you reach the server?
ping [company-ip]
telnet [company-ip] 8080  # Or whatever port

# If fails: check VPN, firewall, network connectivity
```

### Issue: "SSL: CERTIFICATE_VERIFY_FAILED"

**Our code already handles this** with `verify=False` in httpx calls.

If you still get errors:
```
1. Confirm it's a self-signed certificate issue with IT
2. They may need to configure something on their end
3. Or provide a certificate file to install
```

### Issue: "Unexpected response format"

This means Ollama API format is different than expected.

**Get the actual response:**
```bash
# See what Ollama actually returns
curl -X POST https://[company-ip]/api/chat \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-oss20b","messages":[{"role":"user","content":"test"}],"stream":false}' \
  | python -m json.tool
```

**Then tell us:**
- Copy the actual response
- We can update the parsing code

### Issue: "Authentication failed"

If Ollama requires an API key:
```
1. Ask IT for the API key format
2. Ask if it's a Bearer token, API key header, etc.
3. Tell us, we can add authentication support

Example we can add:
headers = {
  "Authorization": f"Bearer {os.getenv('OLLAMA_API_KEY')}"
}
```

### Issue: "Rate limit exceeded"

Company may have usage limits:
```
1. Ask IT about request limits
2. We can adjust retry strategy
3. Or add request batching/queuing
```

---

## Environment Variables Reference

| Variable | Value | Example |
|----------|-------|---------|
| `LLM_ENDPOINT` | Company Ollama URL | `https://192.168.1.100:8080/api/chat` |
| `LLM_MODEL` | Model name | `gpt-oss20b` |
| `LLM_API_TYPE` | "ollama" or "openai" | `ollama` |
| `MOCK_LLM` | false (to use real LLM) | `false` |
| `FAISS_ENDPOINT` | Local FAISS server | `http://localhost:8888` |
| `API_PORT` | API server port | `8000` |
| `LLM_TIMEOUT` | Request timeout (sec) | `60` |
| `LLM_MAX_RETRIES` | Retry attempts | `3` |

---

## Deployment Checklist for Company Setup

```
PRE-DEPLOYMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Got Ollama endpoint URL from IT
✅ Got model name from IT
✅ Tested curl connection to endpoint
✅ Confirmed SSL certificate handling (if self-signed)
✅ Asked about authentication requirements
✅ Asked about rate limiting

CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Copied .env.example to .env
✅ Updated LLM_ENDPOINT with company URL
✅ Set LLM_API_TYPE=ollama
✅ Set MOCK_LLM=false
✅ Verified endpoint format: https://[ip]/api/chat

TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Curl test passes
✅ Python connection test passes
✅ FAISS server running
✅ test_llm_connection.py passes all 3 tests

DEPLOYMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Start services (FAISS, API server)
✅ Run full test suite
✅ Deploy to production
✅ Monitor for errors
```

---

## Support

If you hit issues with company Ollama setup:

1. **Check .env.example** for configuration options
2. **Run curl test** to verify endpoint works
3. **Check troubleshooting section** above
4. **Share error message** - we can debug and fix

Key files:
- `.env.example` - Configuration template
- `WORK_LAPTOP_DEPLOYMENT.md` - Deployment steps
- `src/llm/local_client.py` - LLM client code (handles both formats)

---

## Summary

| Component | Personal PC | Work Laptop |
|-----------|------------|------------|
| Mode | Mock (dev) | Real LLM (prod) |
| Endpoint | Local HTTP | Company HTTPS |
| API Type | OpenAI format | Ollama format |
| Code | Fully tested | Same code |
| Config | In .env.example | In .env |

✅ **System supports both automatically** - just update .env!
