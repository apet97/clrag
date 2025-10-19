# Work Laptop Deployment Guide

**For:** Deploying Clockify RAG from personal PC to work laptop
**Status:** ✅ Ready for deployment
**LLM Requirement:** gpt-oss20b running on work laptop (via Ollama or similar)

---

## Quick Start (5 minutes)

### For Company Ollama Setup (Most Important!)

```bash
# On Work Laptop:

# 1. Before you start: Get Ollama endpoint from IT
#    Ask: "What's the Ollama endpoint URL for gpt-oss20b?"
#    You'll get something like: https://192.168.x.x:8080/api/chat

# 2. Copy project from personal PC
scp -r user@personal-pc:~/project/clockify-rag ./

# 3. Enter project directory
cd clockify-rag

# 4. Setup environment
python -m venv .venv
source .venv/bin/activate  # on macOS/Linux
# or: .venv\Scripts\activate  (on Windows)

# 5. Install dependencies
pip install -r requirements.txt

# 6. Create .env file with company Ollama settings
# Copy .env.example to .env and update:
cp .env.example .env

# Edit .env with your company details:
# LLM_ENDPOINT=https://your-company-ip/api/chat
# LLM_API_TYPE=ollama
# MOCK_LLM=false

# 7. Start FAISS server
python -m src.embed &

# 8. Test company Ollama connection first!
curl -X POST https://[company-ip]/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-oss20b",
    "messages": [{"role": "user", "content": "say hello"}],
    "stream": false
  }'

# 9. Run end-to-end test
python scripts/test_llm_connection.py

# 10. Start API server
export API_PORT=8000
python -m src.server

# 11. Test with real company LLM
curl 'http://localhost:8000/search?q=how%20to%20create%20project&namespace=clockify&k=5'
```

---

## Prerequisites Checklist

### Hardware/Environment
- [ ] Work laptop with at least 8GB RAM
- [ ] 5GB free disk space (indexes + models)
- [ ] Python 3.9+ installed
- [ ] Git (for version control)

### Software Requirements
- [ ] Ollama installed (or vLLM/LM Studio)
- [ ] oss20b model available locally
- [ ] Git/SSH access to copy files
- [ ] Terminal/Command Prompt access

### Knowledge
- [ ] Basic Python/CLI knowledge
- [ ] Understanding of environment variables
- [ ] Port availability (8000, 8080, 8888)

---

## File Transfer

### Option 1: Direct Copy (SCP/SFTP)
```bash
# From work laptop, copy from personal PC
scp -r user@personal-pc:/path/to/clockify-rag ~/clockify-rag

# Or copy specific directories
scp -r user@personal-pc:~/clockify-rag/src ~/clockify-rag/src
scp -r user@personal-pc:~/clockify-rag/index ~/clockify-rag/index
scp -r user@personal-pc:~/clockify-rag/data ~/clockify-rag/data
```

### Option 2: Git Clone
```bash
# If project is in git repository
git clone <repo-url> clockify-rag
cd clockify-rag
git checkout main  # or appropriate branch
```

### Option 3: USB Drive
```bash
# On personal PC
tar -czf clockify-rag.tar.gz clockify-rag/
# Copy to USB, transfer to work laptop

# On work laptop
tar -xzf clockify-rag.tar.gz
cd clockify-rag
```

### Important Files to Transfer
```
✅ MUST TRANSFER:
  src/               - Core source code
  index/             - FAISS indexes (4MB)
  data/              - Chunk data
  scripts/           - Test and utility scripts
  requirements.txt   - Python dependencies
  README.md          - Documentation

⚠️  OPTIONAL (can recreate):
  logs/              - Test results (can be regenerated)
  .git/              - Git history (if not using git)

❌ DON'T TRANSFER:
  .venv/             - Recreate on work laptop
  __pycache__/       - Will be regenerated
  *.pyc              - Will be regenerated
```

---

## Work Laptop Setup

### Step 1: Prepare Environment

```bash
# Navigate to project directory
cd clockify-rag

# Verify project structure
ls -la
# Should show: src/, index/, data/, scripts/, requirements.txt, README.md

# Check Python version
python --version
# Should be 3.9+

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate      # macOS/Linux
# or: .venv\Scripts\activate   # Windows PowerShell
# or: .venv\Scripts\activate.bat # Windows CMD
```

### Step 2: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installations
python -c "import faiss; print('✅ FAISS installed')"
python -c "import httpx; print('✅ httpx installed')"
python -c "import sentence_transformers; print('✅ Transformers installed')"
```

### Step 3: Start FAISS Indexes

```bash
# Terminal 1: Start FAISS embedding server
python -m src.embed

# Expected output:
# ✅ FAISS server started on :8888
# ✅ Loading indexes...
# ✅ clockify: 438 chunks loaded
# ✅ langchain: 758 chunks loaded
```

### Step 4: Start LLM Server

```bash
# Terminal 2: Start Ollama with oss20b model
ollama pull oss20b    # Download model (first time only)
ollama serve

# Expected output:
# serving on 127.0.0.1:8080
# [Model] oss20b ready

# Verify LLM is running
curl http://localhost:8080/v1/models
# Should return: {"object":"list","data":[{"id":"oss20b",...}]}
```

### Step 5: Verify Setup

```bash
# Terminal 3: Activate venv and verify components
source .venv/bin/activate

# Check FAISS server
curl http://localhost:8888/health
# Expected: {"status":"ok","indexes_loaded":2,...}

# Check LLM server
curl http://localhost:8080/v1/models
# Expected: model list returned

# Run LLM connection test
python scripts/test_llm_connection.py
# Expected: ✅ All 3 tests pass
```

### Step 6: Start API Server

```bash
# Terminal 3 (after verification): Start FastAPI server
export API_PORT=8000
python -m src.server

# Expected output:
# 🚀 Starting Clockify RAG API Server
# Server running on http://0.0.0.0:8000
# Production mode: REAL LLM ENABLED
```

### Step 7: Test End-to-End

```bash
# Terminal 4: Test the full pipeline
source .venv/bin/activate

# Test 1: Retrieval
curl 'http://localhost:8000/search?q=how%20do%20I%20create%20a%20project&namespace=clockify&k=3'

# Test 2: RAG Pipeline (requires LLM running)
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "How do I create a project?",
    "namespace": "clockify",
    "k": 3
  }'

# Test 3: System Health
curl http://localhost:8000/health
```

---

## Configuration

### Environment Variables

```bash
# Create .env file (or export variables)
export FAISS_HOST=localhost
export FAISS_PORT=8888
export LLM_BASE_URL=http://localhost:8080/v1
export LLM_MODEL=oss20b
export API_PORT=8000
export LOG_LEVEL=INFO
export MOCK_LLM=false  # CRITICAL: Use real LLM on work laptop!
```

### Configuration File

```bash
# src/config.py (or .env file)
# Default values for work laptop:

FAISS_HOST = "localhost"
FAISS_PORT = 8888
FAISS_ENDPOINT = "http://localhost:8888"

LLM_BASE_URL = "http://localhost:8080/v1"
LLM_MODEL = "oss20b"
LLM_TIMEOUT = 60
LLM_MAX_RETRIES = 3

API_HOST = "0.0.0.0"
API_PORT = 8000
API_WORKERS = 4

LOG_LEVEL = "INFO"
MOCK_LLM = False  # Use real LLM!
```

---

## Deployment Checklist

```
PRE-DEPLOYMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Project files transferred
✅ Python 3.9+ available
✅ 5GB+ free disk space
✅ Ports 8000, 8080, 8888 available
✅ Git access for updates

SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Virtual environment created
✅ Dependencies installed
✅ FAISS indexes verified
✅ Ollama + oss20b running

CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ MOCK_LLM = false
✅ LLM_BASE_URL = http://localhost:8080/v1
✅ FAISS_ENDPOINT = http://localhost:8888
✅ API_PORT = 8000

TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ FAISS health check: curl http://localhost:8888/health
✅ LLM health check: curl http://localhost:8080/v1/models
✅ LLM connection test: python scripts/test_llm_connection.py
✅ Retrieval test: curl http://localhost:8000/search?q=test
✅ RAG end-to-end: curl -X POST http://localhost:8000/chat

DEPLOYMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ API server running
✅ All tests passing
✅ Logs configured
✅ Monitoring setup (optional)
```

---

## Troubleshooting

### Issue: "Cannot connect to FAISS server"

**Solution:**
```bash
# Check if FAISS is running
curl http://localhost:8888/health

# If not, start it
python -m src.embed &

# Or check if port is in use
lsof -i :8888  # macOS/Linux
netstat -ano | findstr :8888  # Windows

# Kill process using port if needed
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Issue: "Cannot connect to LLM"

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:8080/v1/models

# If not, start Ollama
ollama serve

# Verify model is available
ollama list

# Download model if needed
ollama pull oss20b

# Check Ollama logs
# macOS: ~/. ollama/logs
# Linux: ~/.ollama/logs
# Windows: %USERPROFILE%\.ollama\logs
```

### Issue: "Port already in use"

**Solution:**
```bash
# Find what's using the port
lsof -i :8000  # FAISS port
lsof -i :8080  # LLM port
lsof -i :8888  # API port

# Kill the process
kill -9 <PID>

# Or use different port
export API_PORT=9000
python -m src.server
```

### Issue: "Out of memory" error

**Solution:**
```bash
# Reduce batch size
export BATCH_SIZE=4  # Default is 32

# Or allocate more swap
# Check current: free -h (Linux) or System Info (macOS)
# Consider upgrading RAM or running on machine with more memory
```

### Issue: "LLM responses are slow"

**Solution:**
```bash
# This is normal for first request (~30-60s)
# Subsequent requests should be faster

# For faster inference:
# Option 1: Use smaller model (TinyLlama)
ollama pull tinyllama
export LLM_MODEL=tinyllama

# Option 2: Use GPU if available
# Configure Ollama to use GPU (see Ollama docs)

# Option 3: Use vLLM instead (faster inference)
python -m vllm.entrypoints.openai.api_server --model oss20b
```

---

## Differences: Personal PC vs Work Laptop

| Feature | Personal PC | Work Laptop |
|---------|------------|------------|
| Mock LLM | ✅ Enabled | ❌ Disabled |
| Real LLM | ❌ Not running | ✅ Running |
| Test Queries | 25 retrieval tests | Full RAG pipeline |
| FAISS Server | ✅ Running | ✅ Running |
| API Server | ✅ Running | ✅ Running |
| Response Mode | Mock (instant) | Real (1-30s) |

---

## Testing Commands

```bash
# On work laptop after setup:

# 1. Test retrieval (instant, no LLM needed)
python scripts/validate_retrieval_enhanced.py

# 2. Test LLM connection (with real gpt-oss20b)
python scripts/test_llm_connection.py

# 3. Run full RAG pipeline tests
python scripts/test_rag_pipeline.py

# 4. Test all APIs
python scripts/test_api.py

# 5. Interactive demo
python scripts/demo_rag.py

# 6. Full end-to-end test suite
python scripts/run_all_tests.py
```

---

## Production Deployment

### Option 1: Direct Deployment

```bash
# Start all services
screen -S faiss python -m src.embed
screen -S llm ollama serve
screen -S api python -m src.server

# Test
curl http://localhost:8000/health

# Access from other machines
# Replace localhost with machine IP
curl http://<laptop-ip>:8000/search?q=test
```

### Option 2: Docker Deployment

```bash
# Create Dockerfile (already provided in project)
docker build -t clockify-rag .

# Run container
docker run \
  -p 8000:8000 \
  -e LLM_BASE_URL=http://host.docker.internal:8080/v1 \
  clockify-rag

# Access
curl http://localhost:8000/health
```

### Option 3: systemd Service (Linux)

```bash
# Create /etc/systemd/system/clockify-rag.service
[Unit]
Description=Clockify RAG Service
After=network.target

[Service]
Type=simple
User=<username>
WorkingDirectory=/home/<username>/clockify-rag
Environment="PATH=/home/<username>/clockify-rag/.venv/bin"
ExecStart=/home/<username>/clockify-rag/.venv/bin/python -m src.server
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable clockify-rag
sudo systemctl start clockify-rag
sudo systemctl status clockify-rag
```

---

## Performance Metrics

Expected performance on work laptop with oss20b:

| Operation | Latency | Notes |
|-----------|---------|-------|
| Retrieval | 17-45ms | FAISS search |
| LLM (first) | 30-60s | Model loading + inference |
| LLM (cached) | 2-5s | Warm model inference |
| Total RAG | 2-5s | Retrieval + answer (cached) |
| API Response | <1s | Health/search endpoints |

---

## Support & Debugging

### Enable Debug Logging

```bash
# In .env or command line
export LOG_LEVEL=DEBUG

# This will show:
# - LLM requests/responses
# - FAISS search details
# - API request/response times
# - Mock mode status
```

### Check Logs

```bash
# API logs
tail -f logs/api.log

# LLM logs (Ollama)
tail -f ~/.ollama/logs/server.log

# FAISS logs
tail -f logs/faiss.log
```

### Get Help

```bash
# Check documentation
cat README.md
cat CRITICAL_FIXES.md
cat ARCHITECTURE_MAPPING.md

# Run in verbose mode
python scripts/test_llm_connection.py --verbose

# Check system info
python -c "import platform; print(platform.platform())"
python -c "import psutil; print(f'RAM: {psutil.virtual_memory().total / 1e9:.0f}GB')"
```

---

## Summary

| Phase | PC | Laptop | Command |
|-------|---|--------|---------|
| **Build** | ✅ | - | `python scripts/validate_retrieval_enhanced.py` |
| **Test Mock** | ✅ | - | `python scripts/test_llm_modes.py` |
| **Transfer** | ✅ | - | `scp -r ... clockify-rag ~/` |
| **Setup** | - | ✅ | `pip install -r requirements.txt` |
| **Start LLM** | - | ✅ | `ollama serve` |
| **Test LLM** | - | ✅ | `python scripts/test_llm_connection.py` |
| **Deploy** | - | ✅ | `python -m src.server` |

---

**Status:** ✅ **Ready for Deployment**

Your Clockify RAG system is fully built and tested on personal PC. Follow this guide to deploy on work laptop with full LLM capabilities in ~30 minutes.
