# RAG System - Copy-Paste Terminal Guide

**Get your RAG chat system running in 5 minutes with copy-paste commands.**

This guide is optimized for terminal newbies. Just copy each command block and paste into your terminal.

---

## 📋 Prerequisites

Before you start, make sure you have:

- ✅ Git installed
- ✅ Docker installed (or Python 3.11+)
- ✅ Ollama running (local or accessible)

---

## 🚀 Option 1: Docker (Recommended - 2 Minutes)

### Step 1: Clone Repository

\`\`\`bash
git clone https://github.com/apet97/clrag.git
cd clrag
\`\`\`

**Expected output:**
\`\`\`
Cloning into 'clrag'...
remote: Enumerating objects...
...
Done.
\`\`\`

---

### Step 2: Copy Environment File

\`\`\`bash
cp .env.docker .env
\`\`\`

**Expected output:**
\`\`\`
(no output = success)
\`\`\`

---

### Step 3: Build Docker Image

\`\`\`bash
docker build -t rag-system:latest .
\`\`\`

**Expected output:**
\`\`\`
Sending build context to Docker daemon  45.09MB
Step 1/8 : FROM python:3.11-slim
...
Successfully tagged rag-system:latest
\`\`\`

⏱️ **Takes:** 1-2 minutes (first time), cached after that

---

### Step 4: Start Services with Docker Compose

\`\`\`bash
docker-compose up -d
\`\`\`

**Expected output:**
\`\`\`
Creating network "clrag_rag-network" with driver "bridge"
Creating rag-ollama  ... done
Creating rag-system  ... done
\`\`\`

⏱️ **Takes:** 10-20 seconds

---

### Step 5: Wait and Verify

\`\`\`bash
sleep 10
curl -H "x-api-token: change-me" http://localhost:7000/health
\`\`\`

**Expected output:**
\`\`\`json
{"status":"ok","index_loaded":true,"namespaces":["clockify-help"],...}
\`\`\`

✅ **If you see this, you're running!**

---

### Step 6: Open in Browser

\`\`\`bash
# macOS
open http://localhost:7000

# Linux
xdg-open http://localhost:7000

# Windows (Command Prompt)
start http://localhost:7000
\`\`\`

Or manually open: **http://localhost:7000**

---

### Step 7: Use the Chat

1. **Set Token** (Config panel):
   - Enter: \`change-me\`

2. **Try Search** (Search tab):
   - Enter: "How do I submit a timesheet?"
   - See results!

3. **Try Chat** (Chat tab):
   - Enter: "How do I submit a timesheet?"
   - See AI answer with citations!

---

### Stop Services (When Done)

\`\`\`bash
docker-compose down
\`\`\`

---

## 🚀 Option 2: Native Python (5 Minutes)

### Step 1: Clone Repository

\`\`\`bash
git clone https://github.com/apet97/clrag.git
cd clrag
\`\`\`

---

### Step 2: Create Virtual Environment

\`\`\`bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (Command Prompt)
python -m venv .venv
.venv\Scripts\activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
\`\`\`

**Expected output:**
\`\`\`
(.venv) user@laptop:clrag$
\`\`\`

(Notice \`(.venv)\` at start of prompt)

---

### Step 3: Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

⏱️ **Takes:** 2-3 minutes

---

### Step 4: Configure .env

\`\`\`bash
cp .env.sample .env
\`\`\`

Edit \`.env\` and set:
\`\`\`
API_TOKEN=change-me
LLM_BASE_URL=http://localhost:11434
\`\`\`

---

### Step 5: Start Server

\`\`\`bash
python -m src.server
\`\`\`

**Expected output:**
\`\`\`
INFO | src.server:startup:... ✓ Ollama embedding model ready: dim=768
INFO | src.server:startup:... ✓ Response cache initialized
INFO | src.server:startup:... ✅ RAG System startup complete
\`\`\`

✅ **If you see this, you're running!**

---

### Step 6: Open Browser (New Terminal)

\`\`\`bash
# macOS
open http://localhost:7000

# Linux
xdg-open http://localhost:7000

# Windows (PowerShell)
Start-Process "http://localhost:7000"
\`\`\`

Or manually: **http://localhost:7000**

---

### Step 7: Stop Server

In terminal where server is running:

\`\`\`bash
Ctrl+C
\`\`\`

Then:
\`\`\`bash
deactivate
\`\`\`

---

## 🧪 Test Your Setup

### Test Health

\`\`\`bash
curl -H "x-api-token: change-me" http://localhost:7000/health
\`\`\`

### Test Search

\`\`\`bash
curl -H "x-api-token: change-me" \
  "http://localhost:7000/search?q=timesheet&k=3"
\`\`\`

### Test Chat

\`\`\`bash
curl -X POST -H "x-api-token: change-me" \
  -H "Content-Type: application/json" \
  -d '{"question":"How do I submit a timesheet?","k":3}' \
  http://localhost:7000/chat
\`\`\`

---

## 📊 Monitor & Logs

### Docker Logs

\`\`\`bash
docker-compose logs -f
\`\`\`

### Docker Status

\`\`\`bash
docker-compose ps
\`\`\`

---

## 🔗 Quick Commands

### Docker

\`\`\`bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Restart
docker-compose restart

# Rebuild
docker-compose up -d --build
\`\`\`

### Python

\`\`\`bash
# Activate
source .venv/bin/activate

# Install
pip install -r requirements.txt

# Start
python -m src.server

# Stop
Ctrl+C

# Deactivate
deactivate
\`\`\`

---

## 🌐 Access Points

| Resource | URL |
|----------|-----|
| Web UI | http://localhost:7000 |
| Search API | http://localhost:7000/search?q=... |
| Chat API | http://localhost:7000/chat |
| Health | http://localhost:7000/health |
| Metrics | http://localhost:7000/metrics |

---

## 🆘 Troubleshooting

### Docker not found

\`\`\`bash
# Install Docker Desktop or:
docker --version
\`\`\`

### Port 7000 in use

\`\`\`bash
# Use different port
docker run -p 8000:7000 rag-system:latest
# Visit: http://localhost:8000
\`\`\`

### Connection refused

\`\`\`bash
# Check if Ollama running
curl http://localhost:11434/api/tags
\`\`\`

### Out of memory

\`\`\`bash
# Increase Docker memory:
# Docker Desktop → Settings → Resources → Memory (4GB+)
# Then restart: docker-compose restart
\`\`\`

### Python version wrong

\`\`\`bash
python3 --version
# Should be 3.11 or higher
\`\`\`

---

## 📋 One-Liner Setup (Docker)

Copy-paste entire block:

\`\`\`bash
git clone https://github.com/apet97/clrag.git && cd clrag && \
cp .env.docker .env && \
docker build -t rag-system:latest . && \
docker-compose up -d && \
sleep 10 && \
echo "✅ Running at http://localhost:7000" && \
curl -H "x-api-token: change-me" http://localhost:7000/health
\`\`\`

---

## 📋 One-Liner Setup (Python)

\`\`\`bash
git clone https://github.com/apet97/clrag.git && cd clrag && \
python3 -m venv .venv && \
source .venv/bin/activate && \
pip install -r requirements.txt && \
cp .env.sample .env && \
echo "✅ Setup complete. Run: python -m src.server"
\`\`\`

---

## 🎉 You're All Set!

Your RAG chat system is running at: **http://localhost:7000**

Enjoy! 🚀

