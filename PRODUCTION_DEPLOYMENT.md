# Clockify RAG - Production Deployment Guide

**Version:** 2.0
**Date:** October 20, 2025
**Status:** Ready for Production

---

## Quick Start (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/apet97/clrag.git
cd clrag

# 2. Set up environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# 3. Start Ollama (embedding service)
ollama serve &

# 4. Build FAISS index (requires Ollama running)
python -m src.ingest_from_jsonl

# 5. Start API server
export API_PORT=8000
python -m src.server

# 6. Test
curl http://localhost:8000/health
curl "http://localhost:8000/search?q=track+time"
```

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                  CLIENT APPLICATIONS                     │
│         (Web, Mobile, Chat, Integration APIs)           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              API SERVER (src/server.py)                  │
│   • GET /search - Semantic search                        │
│   • POST /search/chat - Conversational                   │
│   • GET /analytics - Metrics                             │
│   • GET /health - Status check                           │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────────┐      ┌──────────────────┐
│  RETRIEVAL       │      │  CACHING LAYER   │
│  - Query prep    │      │  - LRU cache     │
│  - FAISS search  │      │  - 80-90% hit    │
│  - BM25 ranking  │      │  - TTL support   │
└────────┬─────────┘      └──────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│              FAISS INDEX (768-dim vectors)               │
│   • 2,221 chunks from 300 articles                       │
│   • L2-normalized embeddings                            │
│   • IndexFlatIP for fast search                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              OLLAMA SERVICE (Port 11434)                 │
│   • nomic-embed-text:latest model                        │
│   • Batch embedding (32 chunks/batch)                    │
│   • 768-dimensional output                               │
└─────────────────────────────────────────────────────────┘
```

---

## Installation

### Prerequisites

- Python 3.8+ (3.11+ recommended)
- 4 GB RAM minimum (8 GB recommended)
- 2 GB free disk space
- Ollama installed and running

### Step 1: Clone Repository

```bash
git clone https://github.com/apet97/clrag.git
cd clrag
```

### Step 2: Create Virtual Environment

```bash
# Unix/Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt

# Additional dependencies for enhanced features
pip install tldextract  # For advanced scraping
```

### Step 4: Install Ollama

**macOS/Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

**Windows:**
Download from https://ollama.ai

**Pull embedding model:**
```bash
ollama pull nomic-embed-text:latest
```

### Step 5: Build FAISS Index

```bash
# Ensure Ollama is running first
ollama serve &

# In another terminal
source .venv/bin/activate
python -m src.ingest_from_jsonl
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# API Server Configuration
API_PORT=8000
API_HOST=0.0.0.0
DEBUG=false

# Ollama Configuration
LLM_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=nomic-embed-text:latest

# Search Configuration
RETRIEVAL_K=5
CACHE_SIZE=1000
MIN_QUERY_LENGTH=2

# Data Paths
FAISS_INDEX_PATH=index/faiss/clockify-improved/index.bin
FAISS_METADATA_PATH=index/faiss/clockify-improved/meta.json
GLOSSARY_PATH=clockify-help/pages/help__getting-started__clockify-glossary.md

# Performance
MAX_WORKERS=4
BATCH_SIZE=32
```

### Configuration Profiles

**Development:**
```bash
DEBUG=true
API_HOST=127.0.0.1
CACHE_SIZE=100
```

**Production:**
```bash
DEBUG=false
API_HOST=0.0.0.0
CACHE_SIZE=10000
MAX_WORKERS=8
```

---

## Running the Server

### Local Development

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start API server
source .venv/bin/activate
python -m src.server
```

### Docker Deployment (Recommended)

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start server
CMD ["python", "-m", "src.server"]
```

**Docker Compose:**
```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: clockify-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_MODELS=/root/.ollama/models
    command: serve

  api:
    build: .
    container_name: clockify-api
    ports:
      - "8000:8000"
    environment:
      - LLM_BASE_URL=http://ollama:11434
      - API_PORT=8000
      - API_HOST=0.0.0.0
    depends_on:
      - ollama
    volumes:
      - ./index:/app/index
      - ./clockify-help:/app/clockify-help
    restart: unless-stopped

volumes:
  ollama_data:
```

**Run with Docker Compose:**
```bash
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop
docker-compose down
```

---

## Kubernetes Deployment

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: clockify-rag-api
  labels:
    app: clockify-rag

spec:
  replicas: 3
  selector:
    matchLabels:
      app: clockify-rag
  template:
    metadata:
      labels:
        app: clockify-rag
    spec:
      containers:
      - name: api
        image: your-registry/clockify-rag:latest
        ports:
        - containerPort: 8000
        env:
        - name: LLM_BASE_URL
          value: "http://ollama-service:11434"
        - name: API_PORT
          value: "8000"
        resources:
          requests:
            memory: "2Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: clockify-rag-service

spec:
  selector:
    app: clockify-rag
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

**Deploy:**
```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl logs -f deployment/clockify-rag-api
```

---

## Monitoring & Logging

### Health Monitoring

```bash
# Check system status
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "uptime_seconds": 3600,
#   "index_loaded": true,
#   "articles_indexed": 300,
#   "cache_hit_rate": 0.87
# }
```

### Performance Monitoring

```bash
# Get analytics
curl http://localhost:8000/analytics

# Monitor with watch (Linux/Mac)
watch curl http://localhost:8000/analytics
```

### Logging Setup

**Logging Configuration:**
```python
# In src/server.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('logs/api.log'),
        logging.StreamHandler()
    ]
)
```

**View Logs:**
```bash
# Real-time logs
tail -f logs/api.log

# Search logs
grep "error" logs/api.log
grep "search" logs/api.log | head -20
```

---

## Performance Tuning

### FAISS Index Optimization

```python
# Use optimized index configuration
import faiss

# For production: use HNSW with GPU acceleration (if available)
index = faiss.IndexHNSWFlat(768, 32)
index.add(embeddings)

# Or use GPU FAISS
index = faiss.GpuIndexFlatIP(res, 768)
```

### Caching Optimization

```bash
# Increase cache size for high-traffic scenarios
export CACHE_SIZE=50000

# Monitor cache performance
curl http://localhost:8000/analytics | grep cache_hit_rate
```

### Database Connection Pooling

```python
# For future database integration
from sqlalchemy import create_engine
engine = create_engine(
    'postgresql://user:pass@host/db',
    pool_size=20,
    max_overflow=40,
    pool_recycle=3600
)
```

---

## Scaling Strategies

### Horizontal Scaling (Multiple Instances)

**Load Balancer Configuration (Nginx):**
```nginx
upstream api_backend {
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}

server {
    listen 80;
    location / {
        proxy_pass http://api_backend;
    }
}
```

**Start Multiple Instances:**
```bash
# Terminal 1
API_PORT=8001 python -m src.server

# Terminal 2
API_PORT=8002 python -m src.server

# Terminal 3
API_PORT=8003 python -m src.server

# Terminal 4: Run Nginx
nginx -c /path/to/nginx.conf
```

### Vertical Scaling (More Resources)

```bash
# Increase worker processes
export MAX_WORKERS=16

# Increase cache
export CACHE_SIZE=100000

# Use high-performance embedding batching
export BATCH_SIZE=64
```

---

## Backup & Recovery

### Backup Strategy

```bash
# Backup FAISS index
tar -czf backups/faiss_index_$(date +%Y%m%d).tar.gz index/

# Backup scraped articles
tar -czf backups/articles_$(date +%Y%m%d).tar.gz clockify-help/

# Backup complete system
tar -czf backups/full_backup_$(date +%Y%m%d).tar.gz \
  index/ clockify-help/ src/ requirements.txt
```

### Restore from Backup

```bash
# Restore FAISS index
tar -xzf backups/faiss_index_20251020.tar.gz

# Restart server
python -m src.server
```

---

## Security

### API Security

```bash
# Add authentication (future)
# Use environment variables for secrets
export API_KEY=your_secret_key

# Enable HTTPS (production)
# Use SSL certificates
openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365
```

### Input Validation

```python
# Validate query input
MIN_QUERY_LENGTH = 2
MAX_QUERY_LENGTH = 500

if len(query) < MIN_QUERY_LENGTH or len(query) > MAX_QUERY_LENGTH:
    return error_response("Invalid query length")
```

### Rate Limiting

```bash
# Install rate limiter
pip install flask-limiter

# Configure in src/server.py
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/search')
@limiter.limit("100 per minute")
def search():
    ...
```

---

## Troubleshooting

### Index Not Found

```
Error: FileNotFoundError: index/faiss/clockify-improved/index.bin
```

**Solution:**
```bash
python -m src.ingest_from_jsonl
```

### Ollama Connection Error

```
Error: [Errno 61] Connection refused
```

**Solution:**
```bash
ollama serve &
# Wait 5 seconds for service to start
python -m src.server
```

### Out of Memory

```
Error: MemoryError
```

**Solution:**
```bash
# Reduce batch size
export BATCH_SIZE=8

# Reduce cache size
export CACHE_SIZE=1000

# Or allocate more memory
# Increase system swap or VM memory
```

### Slow Search Performance

```
Latency: 500ms+
```

**Solution:**
```bash
# Check cache hit rate
curl http://localhost:8000/analytics | grep cache_hit_rate

# Clear and rebuild cache
rm -rf .cache
python -m src.server

# Enable query caching
# curl http://localhost:8000/search?q=test&cache=true
```

---

## Maintenance

### Regular Tasks

```bash
# Daily: Monitor logs
tail -f logs/api.log

# Weekly: Check analytics
curl http://localhost:8000/analytics

# Monthly: Reindex if articles updated
python -m src.ingest_from_jsonl

# Quarterly: Backup system
tar -czf backups/backup_q4.tar.gz .
```

### Updates

```bash
# Pull latest code
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Restart server
systemctl restart clockify-rag-api
```

---

## Systemd Service (Linux)

**File: `/etc/systemd/system/clockify-rag.service`**
```ini
[Unit]
Description=Clockify RAG API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/clockify-rag
ExecStart=/opt/clockify-rag/.venv/bin/python -m src.server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable & Start:**
```bash
sudo systemctl enable clockify-rag
sudo systemctl start clockify-rag
sudo systemctl status clockify-rag
```

---

## Support & Troubleshooting

- **Documentation**: See README.md and API_DOCUMENTATION.md
- **Issues**: https://github.com/apet97/clrag/issues
- **Health Check**: `curl http://localhost:8000/health`
- **Analytics**: `curl http://localhost:8000/analytics`

---

**Last Updated:** October 20, 2025
**Status:** Production Ready
**Tested On:** macOS 12+, Ubuntu 20.04+, Docker, Kubernetes
