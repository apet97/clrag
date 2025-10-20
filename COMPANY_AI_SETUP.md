# Company AI Setup - Local AI Model Integration

**Clockify RAG System configured for internal company AI model**

This guide explains how to use the company AI model at `10.127.0.192:11434` (gpt-oss:20b) with the RAG system.

---

## 🚀 Quick Start (Company AI)

### Prerequisites
- ✅ VPN connection (required to access internal endpoint)
- ✅ RAG system installed locally
- ✅ Company AI endpoint running (verify via `curl http://10.127.0.192:11434/api/tags`)

### One-Liner Setup
```bash
# Copy company AI configuration
MODEL_BASE_URL="http://10.127.0.192:11434" \
MODEL_NAME="gpt-oss:20b" \
make crawl preprocess chunk embed hybrid
```

### Or Standard Setup
Edit `.env` and set:
```bash
MODEL_BASE_URL=http://10.127.0.192:11434
MODEL_NAME=gpt-oss:20b
MODEL_API_KEY=  # Leave empty - no API key needed
```

Then run:
```bash
source .venv/bin/activate
make crawl preprocess chunk embed hybrid
make serve
```

---

## 🔌 Available Models

Company AI hosts multiple models. Here are available options (as of latest sync):

### Recommended for RAG
| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| **gpt-oss:20b** | 13.7 GB | Medium | High | **RECOMMENDED** - Best balance |
| qwen2.5:32b | 19.8 GB | Slow | Very High | Accuracy critical tasks |
| deepseek-r1:70b | 42.5 GB | Very Slow | Excellent | Complex reasoning |
| gemma3:27b | 17.4 GB | Medium | High | Alternative to gpt-oss |

### Lightweight Options
| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| llama3.2:3b | 2.0 GB | Fast | Good | Quick tests, low resources |
| qwen2.5-coder:1.5b | 986 MB | Very Fast | Good | Code-focused queries |

### Specialized Models
| Model | Size | Purpose |
|-------|------|---------|
| llava:13b | 8.0 GB | Vision + text (image understanding) |
| mvkvl/sentiments:mistral | 4.1 GB | Sentiment analysis |
| nomic-embed-text:latest | 274 MB | Embeddings (used by default) |

---

## ✅ Verify Company AI Connection

### Test 1: Get Available Models
```bash
curl http://10.127.0.192:11434/api/tags | jq
```

Expected output: JSON list of available models

### Test 2: Send Test Message
```bash
curl -X POST http://10.127.0.192:11434/api/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-oss:20b",
    "messages": [{"role": "user", "content": "ping"}],
    "stream": false
  }' | jq .message.content
```

Expected output: `"pong"` or similar response

### Test 3: Check RAG System Health
```bash
# After starting the RAG system
curl http://localhost:7000/health | jq

# Should show: "status": "healthy"
```

---

## 🛠️ IDE Integration (Direct Connection)

If you want to use the company AI model directly in your IDE (without the RAG system):

### Connection Details
- **Endpoint**: `10.127.0.192:11434`
- **API Format**: Ollama-compatible
- **Authentication**: None (no API key needed)
- **Port**: 11434

### IDE Integration Examples

**VS Code with Continue.dev**
```json
{
  "models": [
    {
      "title": "Company GPT-OSS 20B",
      "provider": "ollama",
      "model": "gpt-oss:20b",
      "apiBase": "http://10.127.0.192:11434"
    }
  ]
}
```

**JetBrains IDEs with Ollama Plugin**
1. Install Ollama plugin
2. Settings → Ollama
3. Server URL: `http://10.127.0.192:11434`
4. Model: `gpt-oss:20b`

**Terminal Usage**
```bash
# Set as default
export OLLAMA_HOST=http://10.127.0.192:11434

# Run chat
ollama run gpt-oss:20b "Your question here"
```

---

## 📊 Performance Expectations

**⚠️ Important Notes:**
- This is a **Proof-of-Concept (PoC)** deployment
- Expect **moderate performance** and **occasional slowdowns**
- First request may take 20-30 seconds (model loading)
- Subsequent requests: 5-15 seconds depending on complexity

### Typical Latencies
| Operation | Time | Notes |
|-----------|------|-------|
| First request | 20-30s | Model initialization |
| Chat response | 5-15s | LLM generation |
| Search | 50-100ms | FAISS vector search |
| RAG pipeline | 10-25s | Search + LLM combined |

### Memory & Resource Usage
- Model loaded in VRAM: ~20-24GB (gpt-oss:20b)
- Shared system resource - performance may vary with other users
- Rate limiting: Not yet implemented (be respectful of shared resource)

---

## 🎯 Use Cases & Recommendations

### Good For
✅ Testing RAG functionality
✅ Development and experimentation
✅ Non-time-critical tasks
✅ Trying different prompts/queries
✅ Integration testing

### Not Recommended For
❌ Production high-traffic systems (use external API instead)
❌ Real-time chat applications
❌ Batch processing many requests
❌ Latency-sensitive applications

---

## 🔄 Model Selection

### Switch to Different Model
Edit `.env`:
```bash
MODEL_NAME=qwen2.5:32b  # Or any other available model
```

Restart the RAG system:
```bash
make serve
```

### Compare Model Performance
```bash
#!/bin/bash
for model in gpt-oss:20b qwen2.5:32b gemma3:27b; do
  echo "Testing: $model"
  time curl -X POST http://10.127.0.192:11434/api/chat \
    -H 'Content-Type: application/json' \
    -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"What is RAG?\"}],\"stream\":false}" \
    | jq -r .message.content
  echo "---"
done
```

---

## 📈 Feedback & Monitoring

### Collecting Feedback for PoC Evaluation

Please provide feedback on the company AI using this template:

**Date**: ___________
**Model Used**: ___________
**Task**: ___________ (e.g., search, chat, coding)

#### Feedback Questions (Rate 1-5, 1=Poor, 5=Excellent)

**Performance**
- Speed: ☐1 ☐2 ☐3 ☐4 ☐5
- Reliability: ☐1 ☐2 ☐3 ☐4 ☐5
- Stability: ☐1 ☐2 ☐3 ☐4 ☐5

**Quality**
- Answer Accuracy: ☐1 ☐2 ☐3 ☐4 ☐5
- Answer Usefulness: ☐1 ☐2 ☐3 ☐4 ☐5
- Relevance: ☐1 ☐2 ☐3 ☐4 ☐5

**Overall Experience**
- Would Use Again: ☐1 ☐2 ☐3 ☐4 ☐5
- Recommendation: ☐1 ☐2 ☐3 ☐4 ☐5
- Overall Satisfaction: ☐1 ☐2 ☐3 ☐4 ☐5

**Comments/Issues**:
```
[Your feedback here]
```

**Send feedback to**: [Internal feedback channel TBD]

### Monitoring Usage

Track your usage to help identify patterns:

```bash
#!/bin/bash
# Monitor queries to company AI
echo "Company AI Usage Summary"
echo "======================================="
curl -s http://10.127.0.192:11434/api/tags | jq '.models | length'
echo "Total models available"

# Log request to a file for feedback
echo "[$(date)] Query to gpt-oss:20b via RAG" >> ~/.config/company-ai-usage.log
```

---

## 🔐 Security & Best Practices

### What's Safe to Test
✅ Internal company data
✅ Clockify help articles
✅ Development code
✅ Internal documentation
✅ Test data

### What's NOT Safe to Test
❌ Production credentials
❌ Customer personal data
❌ Payment information
❌ Sensitive business secrets
❌ External API keys

**Note**: The PoC is specifically designed for testing - be mindful but feel free to experiment!

---

## 🆘 Troubleshooting

### Connection Refused
```bash
# Check if endpoint is accessible
curl -v http://10.127.0.192:11434/api/tags

# Verify VPN connection
ping 10.127.0.192
```

### Model Not Available
```bash
# List all available models
curl http://10.127.0.192:11434/api/tags | jq '.models[].name'

# Pull a model if missing
# (Note: May not work on shared instance - ask admin)
ollama pull gpt-oss:20b
```

### Slow Response Times
```bash
# Check if model is loaded
curl http://10.127.0.192:11434/api/tags | jq '.models[] | select(.name=="gpt-oss:20b")'

# Test with smaller model
MODEL_NAME=llama3.2:3b make serve
```

### "Out of Memory" Errors
- The shared instance has memory constraints
- Try smaller model: `llama3.2:3b` or `qwen2.5-coder:1.5b`
- Contact admin if persistent

---

## 📚 Additional Resources

- **RAG Setup**: See [STEP_BY_STEP_GUIDE.md](STEP_BY_STEP_GUIDE.md)
- **API Reference**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Local Ollama Setup**: See [STEP_BY_STEP_GUIDE.md - Local LLM Setup](STEP_BY_STEP_GUIDE.md#local-llm-setup)
- **Company AI Web UI**: https://ai.coingdevelopment.com (VPN required, "Continue with Cake ID")

---

## 📝 Configuration Reference

### Complete `.env` for Company AI
```bash
# ==== COMPANY AI CONFIGURATION ====
MODEL_BASE_URL=http://10.127.0.192:11434
MODEL_API_KEY=
MODEL_NAME=gpt-oss:20b
MODEL_MAX_TOKENS=1000
MODEL_TEMPERATURE=0.7

# ==== EMBEDDING CONFIGURATION ====
# Can use company embedding or external
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_BATCH_SIZE=32
EMBEDDING_POOL_SIZE=4

# ==== CRAWLING (Optional - customize for your use) ====
CRAWL_BASES=https://clockify.me/help,https://python.langchain.com/docs
DOMAINS_WHITELIST=clockify.me,langchain.com
CRAWL_ALLOW_OVERRIDE=false

# ==== PIPELINE FEATURES ====
PARENT_CHILD_INDEXING=true
HYBRID_SEARCH=true
QUERY_REWRITES=true
USE_RERANKER=true

# ==== LOGGING ====
DEBUG=false
```

---

## ✅ Checklist: Company AI Setup

- ☐ VPN connection verified
- ☐ `.env` updated with company AI endpoint
- ☐ Connection test passed: `curl http://10.127.0.192:11434/api/tags`
- ☐ RAG system started: `make serve`
- ☐ Health check passed: `curl http://localhost:7000/health`
- ☐ First search test successful
- ☐ Ready to provide feedback

---

## 🎉 You're Ready!

Your RAG system is now configured for the company AI model.

**Next Steps:**
1. Run the RAG pipeline: `make crawl preprocess chunk embed hybrid`
2. Start the server: `make serve`
3. Test searches and chat
4. Provide feedback on performance and usefulness

**Questions?** Contact [admin/support] or check [internal documentation]

---

**Last Updated**: October 20, 2025
**Status**: PoC Active
**Endpoint**: http://10.127.0.192:11434
**Recommended Model**: gpt-oss:20b
**Web UI**: https://ai.coingdevelopment.com (VPN required)
