# Clockify RAG - Complete Step-by-Step Guide

**Get up and running with detailed instructions!**

---

## Table of Contents

1. [Initial Setup (First Time)](#initial-setup-first-time)
2. [Local Development](#local-development)
3. [Using the API](#using-the-api)
4. [Docker Deployment](#docker-deployment)
5. [Monitoring & Debugging](#monitoring--debugging)

---

## Initial Setup (First Time)

### Step 1: Install Prerequisites

**On macOS:**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11+
brew install python@3.11

# Install Git
brew install git

# Install Ollama
brew install ollama
```

**On Linux (Ubuntu/Debian):**
```bash
# Update package manager
sudo apt update
sudo apt upgrade

# Install Python 3.11+
sudo apt install python3.11 python3.11-venv python3-pip

# Install Git
sudo apt install git

# Install Ollama
curl https://ollama.ai/install.sh | sh
```

**On Windows:**
```powershell
# Install Python from https://www.python.org/downloads/
# Download Python 3.11+ installer
# During installation, CHECK "Add Python to PATH"

# Install Git from https://git-scm.com/download/win

# Install Ollama from https://ollama.ai/download
```

### Step 2: Clone the Repository

```bash
# Navigate to your desired directory
cd ~/Projects  # or any directory you prefer

# Clone the repository
git clone https://github.com/apet97/clrag.git

# Enter the directory
cd clrag

# Verify you're in the right place
ls -la
# Should show: src/, clockify-help/, index/, QUICK_START.md, etc.
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate
```

**You should see `(.venv)` in your terminal prompt**

### Step 4: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Verify installation
python -c "import faiss; import ollama; print('✓ All dependencies installed')"
```

### Step 5: Start Ollama Service

**Keep this running in a separate terminal!**

```bash
# Terminal 1: Start Ollama
ollama serve

# Wait for output like:
# "Listening on 127.0.0.1:11434"
```

### Step 6: Create Configuration File

```bash
# Copy the example configuration
cp .env.example .env

# On macOS/Linux, edit it:
nano .env

# On Windows, use Notepad:
# notepad .env

# For local setup, the defaults are fine
# Just verify these values:
# API_PORT=8000
# LLM_BASE_URL=http://localhost:11434
# EMBEDDING_MODEL=nomic-embed-text:latest
```

### Step 7: Build FAISS Index

**Run this once to build the searchable index:**

```bash
# Terminal 2: Build index
source .venv/bin/activate  # If not already activated
python -m src.ingest_from_jsonl

# Output should show:
# "Loaded 2221 records from clockify-help/clockify_help.jsonl"
# "Building FAISS index from 2221 records..."
# "Embedding:  [Progress bar]..."
# "✅ Index saved: index/faiss/clockify-improved/index.bin"
# "INGESTION COMPLETE"

# This takes 10-30 minutes depending on your hardware
```

---

## Local Development

### Step 1: Start the API Server

**Terminal 3: Start the API**

```bash
# Activate virtual environment (if not already)
source .venv/bin/activate

# Set the port (optional, defaults to 8000)
export API_PORT=8000

# Start the server
python -m src.server

# You should see:
# "Starting Clockify RAG API server..."
# "Listening on http://0.0.0.0:8000"
```

### Step 2: Verify Server is Running

**Terminal 4: Test the API**

```bash
# Check health
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "index_loaded": true, "articles_indexed": 300}
```

### Step 3: Perform Your First Search

```bash
# Search for something
curl "http://localhost:8000/search?q=how+do+i+track+time"

# Or use a more complex example
curl "http://localhost:8000/search?q=create+project&k=5"

# Expected response:
# {
#   "query": "how do i track time",
#   "results": [
#     {
#       "id": "doc_id",
#       "title": "Creating a Time Entry",
#       "url": "https://clockify.me/help/...",
#       "relevance_score": 0.95,
#       "content": "You can create a time entry using..."
#     }
#   ]
# }
```

### Step 4: Try Different Query Types

```bash
# How-to query
curl "http://localhost:8000/search?q=how+to+set+up+projects"

# Definition query
curl "http://localhost:8000/search?q=what+is+a+workspace"

# Comparison query
curl "http://localhost:8000/search?q=timer+vs+manual+entry"

# Factual query
curl "http://localhost:8000/search?q=clockify+pricing"

# General query
curl "http://localhost:8000/search?q=permissions"
```

### Step 5: Check Analytics

```bash
# Get search statistics
curl http://localhost:8000/analytics

# Expected response:
# {
#   "total_queries": 5,
#   "unique_queries": 5,
#   "zero_result_queries": 0,
#   "cache_hit_rate": 0.0,
#   "avg_latency_ms": 78.5,
#   "popular_queries": [...]
# }
```

### Step 6: Advanced Search Features

```bash
# Enable reranking (slower, more accurate)
curl "http://localhost:8000/search?q=track+time&rerank=true"

# Disable caching (get fresh results)
curl "http://localhost:8000/search?q=track+time&cache=false"

# Get more results
curl "http://localhost:8000/search?q=track+time&k=10"

# Get detailed matching info
curl "http://localhost:8000/search?q=track+time&details=true"
```

### Step 7: Stop the Server

```bash
# In Terminal 3 where the server is running:
# Press Ctrl+C

# Output should show:
# "Shutting down gracefully..."
# "Server stopped"
```

---

## Using the API

### Query Syntax Examples

**Simple Search:**
```bash
curl "http://localhost:8000/search?q=time+tracking"
```

**Multi-word Query:**
```bash
curl "http://localhost:8000/search?q=how+to+create+a+project"
```

**Special Characters (URL encoded):**
```bash
curl "http://localhost:8000/search?q=what%27s+the+difference"
```

### Using Python

```python
import requests

# Search
response = requests.get(
    "http://localhost:8000/search",
    params={"q": "track time", "k": 5}
)

results = response.json()
print(f"Found {len(results['results'])} results")

for result in results['results']:
    print(f"- {result['title']}")
    print(f"  Score: {result['relevance_score']:.2f}")
    print(f"  URL: {result['url']}\n")

# Get analytics
analytics = requests.get("http://localhost:8000/analytics").json()
print(f"Cache hit rate: {analytics['cache_hit_rate']:.1%}")
```

### Using JavaScript/Node.js

```javascript
// Search
fetch("http://localhost:8000/search?q=track+time")
  .then(res => res.json())
  .then(data => {
    console.log(`Found ${data.results.length} results`);
    data.results.forEach(r => {
      console.log(`- ${r.title}`);
      console.log(`  Score: ${r.relevance_score.toFixed(2)}`);
      console.log(`  URL: ${r.url}\n`);
    });
  });

// Get analytics
fetch("http://localhost:8000/analytics")
  .then(res => res.json())
  .then(data => {
    console.log(`Cache hit rate: ${(data.cache_hit_rate * 100).toFixed(1)}%`);
  });
```

---

## Docker Deployment

### Step 1: Install Docker

**macOS:**
```bash
brew install docker
brew install docker-compose
```

**Linux:**
```bash
sudo apt install docker.io docker-compose
```

**Windows:**
Download Docker Desktop from https://www.docker.com/products/docker-desktop

### Step 2: Build and Run

```bash
# Navigate to project directory
cd clrag

# Build the image
docker build -t clockify-rag:latest .

# Or use Docker Compose (simplest)
docker-compose up -d

# Check if running
docker ps

# View logs
docker-compose logs -f api
```

### Step 3: Access the API

```bash
# Same as before, but now on Docker
curl http://localhost:8000/health
curl "http://localhost:8000/search?q=track+time"
```

### Step 4: Stop Docker

```bash
# Stop the services
docker-compose down

# Or stop individual container
docker stop clockify-rag
```

---

## Monitoring & Debugging

### Check Logs

```bash
# View server logs in real-time
tail -f logs/api.log

# Search for errors
grep -i error logs/api.log

# Count log entries
wc -l logs/api.log
```

### Monitor Performance

```bash
# Watch cache hit rate change over time
watch -n 5 'curl -s http://localhost:8000/analytics | grep cache_hit_rate'

# Monitor latency
curl -w "@curl-format.txt" -o /dev/null http://localhost:8000/search?q=test

# Get full analytics
curl http://localhost:8000/analytics | python -m json.tool
```

### Troubleshooting

**Problem: "Connection refused" on port 8000**
```bash
# Check if server is running
curl http://localhost:8000/health

# If not, start it:
python -m src.server

# If port is in use, try different port:
export API_PORT=8001
python -m src.server
```

**Problem: "Cannot connect to Ollama"**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it:
ollama serve

# Check in .env that LLM_BASE_URL is correct
cat .env | grep LLM_BASE_URL
```

**Problem: "FAISS index not found"**
```bash
# Rebuild the index
python -m src.ingest_from_jsonl

# This will take 10-30 minutes
```

**Problem: No search results**
```bash
# Try simpler query
curl "http://localhost:8000/search?q=time"

# Check with analytics
curl http://localhost:8000/analytics

# Look for "zero_result_queries"
```

---

## Common Workflows

### Workflow 1: Development Session

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start server
source .venv/bin/activate
python -m src.server

# Terminal 3: Test queries
curl "http://localhost:8000/search?q=your+query"

# Terminal 4: Monitor
watch curl http://localhost:8000/analytics

# When done, Ctrl+C in Terminal 2 and Terminal 1
```

### Workflow 2: Testing Query Types

```bash
# Test each query type detection
curl "http://localhost:8000/search?q=how+do+i+track+time&details=true"    # how-to
curl "http://localhost:8000/search?q=what+is+a+project&details=true"     # definition
curl "http://localhost:8000/search?q=timer+vs+manual&details=true"       # comparison
curl "http://localhost:8000/search?q=does+clockify+have&details=true"    # factual
```

### Workflow 3: Performance Testing

```bash
# Test latency without cache
for i in {1..10}; do
  curl -w "Latency: %{time_total}s\n" -o /dev/null \
    "http://localhost:8000/search?q=track+time&cache=false"
done

# Test with cache (should be much faster)
for i in {1..10}; do
  curl -w "Latency: %{time_total}s\n" -o /dev/null \
    "http://localhost:8000/search?q=track+time&cache=true"
done
```

### Workflow 4: Load Testing

```bash
# Install Apache Bench
# macOS: brew install httpd
# Linux: sudo apt install apache2-utils

# Run load test
ab -n 1000 -c 10 "http://localhost:8000/search?q=track+time"

# Expected output shows:
# - Requests per second
# - Time per request
# - Success rate
```

---

## Production Deployment

### Option 1: Docker Compose

```bash
# Edit .env for production
nano .env

# Key changes:
# DEBUG=false
# API_HOST=0.0.0.0
# CACHE_SIZE=10000

# Deploy
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Option 2: Kubernetes

```bash
# Apply manifests
kubectl apply -f deployment.yaml

# Check deployment
kubectl get pods
kubectl get svc

# View logs
kubectl logs -f deployment/clockify-rag-api

# Port forward for testing
kubectl port-forward svc/clockify-rag-service 8000:80
```

### Option 3: Manual Server

```bash
# Create systemd service file
sudo nano /etc/systemd/system/clockify-rag.service

# Add content from PRODUCTION_DEPLOYMENT.md

# Enable and start
sudo systemctl enable clockify-rag
sudo systemctl start clockify-rag

# Check status
sudo systemctl status clockify-rag

# View logs
sudo journalctl -u clockify-rag -f
```

---

## Next Steps

1. ✅ Complete initial setup
2. ✅ Run local development server
3. ✅ Test basic searches
4. 📖 Read API_DOCUMENTATION.md for advanced features
5. 🚀 Deploy to production using your preferred method
6. 📊 Monitor analytics and optimize

---

## Help & Support

**Still stuck?**
1. Check QUICK_START.md for 5-minute version
2. Read API_DOCUMENTATION.md for endpoint details
3. See PRODUCTION_DEPLOYMENT.md for deployment help
4. Check logs: `tail -f logs/api.log`
5. Open issue on GitHub: https://github.com/apet97/clrag/issues

---

**Happy searching!** 🎉
