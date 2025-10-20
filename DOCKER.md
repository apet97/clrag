# RAG System - Complete Docker Launch Guide

**Deploy a production-grade RAG chat system using Docker in 2 minutes.**

This guide covers containerizing, building, and running the RAG system with Docker and Docker Compose.

---

## 🚀 Quick Start with Docker (2 Minutes)

### Prerequisites
- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)
- Ollama running locally or accessible via network

### Step 1: Clone Repository
```bash
git clone https://github.com/apet97/clrag.git
cd clrag
```

### Step 2: Build Docker Image
```bash
docker build -t rag-system:latest .
```

**Output should show:**
```
Step 1/8 : FROM python:3.11-slim
...
Step 8/8 : CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "7000"]
Successfully tagged rag-system:latest
```

### Step 3: Run Container with Docker Compose
```bash
docker-compose up -d
```

**Output:**
```
Creating rag-system ... done
```

### Step 4: Access the Chat UI
Open your browser:
```
http://localhost:7000
```

### Step 5: Verify Health
```bash
curl -H "x-api-token: change-me" http://localhost:7000/health | jq .
```

---

## 📦 Docker Image Details

### Base Image
```dockerfile
FROM python:3.11-slim
```

Why slim?
- **Size**: 130MB vs 920MB (full image)
- **Security**: Minimal attack surface
- **Speed**: Fast downloads and startup
- **Compatibility**: All dependencies included

### Image Contents
- Python 3.11 runtime
- System dependencies (gcc, make, etc.)
- Python packages from `requirements.txt`
- Prebuilt FAISS index (baked in)
- Source code

### Image Size
```
Repository          Tag      Size
rag-system          latest   ~450MB (includes FAISS index)
```

### Layers
```
Layer 1: Base Python 3.11-slim          (~130MB)
Layer 2: System dependencies            (~50MB)
Layer 3: Python packages                (~150MB)
Layer 4: Source code + index            (~120MB)
```

---

## 🐳 Docker Compose Setup

### Default `docker-compose.yml`
```yaml
version: '3.8'

services:
  rag:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "7000:7000"
    environment:
      API_TOKEN: change-me
      ENV: dev
      LLM_BASE_URL: http://host.docker.internal:11434  # Ollama on host
      LOG_LEVEL: INFO
    volumes:
      - ./logs:/app/logs  # Persist logs
    healthcheck:
      test: ["CMD", "curl", "-f", "-H", "x-api-token: change-me", "http://localhost:7000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped
```

### Quick Commands
```bash
# Start (background)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild image
docker-compose up -d --build

# Remove everything (careful!)
docker-compose down -v
```

---

## 🏗️ Dockerfile Architecture

### Production Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 7000

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD curl -f -H "x-api-token: change-me" http://localhost:7000/health || exit 1

# Run server
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "7000"]
```

### Multi-Stage Build (Optional)
For even smaller images:

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
EXPOSE 7000

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "7000"]
```

**Result: ~350MB image (40% smaller)**

---

## 🌍 Network Configuration

### Accessing Ollama from Docker

#### Option 1: Ollama on Host Machine (macOS/Linux)
```yaml
environment:
  LLM_BASE_URL: http://host.docker.internal:11434
```

#### Option 2: Ollama in Docker Network
```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama:/root/.ollama
    networks:
      - rag-network

  rag:
    build: .
    ports:
      - "7000:7000"
    environment:
      LLM_BASE_URL: http://ollama:11434
    networks:
      - rag-network
    depends_on:
      - ollama

volumes:
  ollama:

networks:
  rag-network:
    driver: bridge
```

#### Option 3: Remote Ollama Server
```yaml
environment:
  LLM_BASE_URL: http://192.168.1.100:11434
```

---

## 📊 Docker Compose Scenarios

### Scenario 1: Local Development
```yaml
version: '3.8'

services:
  rag:
    build: .
    ports:
      - "7000:7000"
    environment:
      API_TOKEN: dev-token
      ENV: dev
      LOG_LEVEL: DEBUG
      LLM_BASE_URL: http://host.docker.internal:11434
    volumes:
      - .:/app  # Live code reload
      - ./logs:/app/logs
```

**Usage:**
```bash
docker-compose up --build
# Code changes auto-reload (if using auto-reload server)
```

### Scenario 2: Production Single Node
```yaml
version: '3.8'

services:
  rag:
    image: rag-system:latest
    restart: always
    ports:
      - "7000:7000"
    environment:
      API_TOKEN: ${API_TOKEN}  # From .env file
      ENV: prod
      LOG_LEVEL: INFO
      LLM_BASE_URL: http://ollama:11434
      RESPONSE_CACHE_SIZE: 2000
      RATE_LIMIT_RPS: 20
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    healthcheck:
      test: ["CMD", "curl", "-f", "-H", "x-api-token: $API_TOKEN", "http://localhost:7000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - rag-network
    depends_on:
      ollama:
        condition: service_healthy

  ollama:
    image: ollama/ollama:latest
    restart: always
    volumes:
      - ollama_data:/root/.ollama
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - rag-network

volumes:
  ollama_data:

networks:
  rag-network:
    driver: bridge
```

### Scenario 3: Production with Reverse Proxy
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - rag
    networks:
      - rag-network

  rag:
    image: rag-system:latest
    restart: always
    environment:
      API_TOKEN: ${API_TOKEN}
      ENV: prod
      LLM_BASE_URL: http://ollama:11434
    volumes:
      - ./logs:/app/logs
    networks:
      - rag-network
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    restart: always
    volumes:
      - ollama_data:/root/.ollama
    networks:
      - rag-network

volumes:
  ollama_data:

networks:
  rag-network:
    driver: bridge
```

---

## 🔧 Common Docker Commands

### Building
```bash
# Build image
docker build -t rag-system:latest .

# Build with custom name/tag
docker build -t mycompany/rag-system:v1.0 .

# Build without cache
docker build --no-cache -t rag-system:latest .

# Build specific dockerfile
docker build -f Dockerfile.prod -t rag-system:prod .
```

### Running
```bash
# Run container
docker run -p 7000:7000 -e API_TOKEN=mytoken rag-system:latest

# Run with name
docker run --name rag-app -p 7000:7000 rag-system:latest

# Run with environment file
docker run --env-file .env -p 7000:7000 rag-system:latest

# Run interactive (for debugging)
docker run -it rag-system:latest bash

# Run with volume mount
docker run -v ./logs:/app/logs -p 7000:7000 rag-system:latest

# Run with resource limits
docker run --memory="2g" --cpus="2" -p 7000:7000 rag-system:latest
```

### Inspection
```bash
# List images
docker images | grep rag

# View image details
docker inspect rag-system:latest

# View image layers
docker history rag-system:latest

# List running containers
docker ps | grep rag

# View container logs
docker logs -f container_id

# View resource usage
docker stats container_id

# Exec command in running container
docker exec container_id curl http://localhost:7000/health
```

### Cleanup
```bash
# Stop container
docker stop container_id

# Remove container
docker rm container_id

# Remove image
docker rmi rag-system:latest

# Remove unused resources
docker system prune

# Remove everything (careful!)
docker system prune -a
```

---

## 🚢 Docker Compose vs Plain Docker

### Use Docker Compose When:
- Running multiple services (RAG + Ollama)
- Need environment variables management
- Want to persist volumes
- Need health checks
- Scaling to multiple containers

### Use Plain Docker When:
- Simple single-service setup
- Integrated into orchestration platform (Kubernetes)
- Container already on remote registry
- Running adhoc containers

### Comparison

| Feature | Docker | Docker Compose |
|---------|--------|----------------|
| Services | 1 command per service | 1 `docker-compose up` |
| Environment | `-e` flags | `.env` file or YAML |
| Volumes | `-v` flags | YAML configuration |
| Networks | Manual creation | Auto-created |
| Health checks | Manual testing | Built-in |
| Scaling | Manual management | `docker-compose scale` |
| Restart policy | Flags | YAML |

---

## 🌐 Environment Variables in Docker

### From `.env` File
```bash
# Create .env
echo "API_TOKEN=your-secure-token" > .env
echo "LOG_LEVEL=INFO" >> .env

# Docker Compose reads .env automatically
docker-compose up
```

### From Command Line
```bash
docker run -e API_TOKEN=mytoken -e LOG_LEVEL=DEBUG rag-system:latest
```

### In docker-compose.yml
```yaml
environment:
  - API_TOKEN=production-token
  - LLM_BASE_URL=http://ollama:11434
  - LOG_LEVEL=INFO
```

### Full Environment Reference
```dockerfile
# Required
API_TOKEN=your-secure-token

# Network
LLM_BASE_URL=http://ollama:11434
EMBEDDING_MODEL=nomic-embed-text:latest
LLM_MODEL=gpt-oss:20b

# Server
API_HOST=0.0.0.0
API_PORT=7000
ENV=prod

# Cache
RESPONSE_CACHE_SIZE=1000
RESPONSE_CACHE_TTL=3600

# Rate Limiting
RATE_LIMIT_RPS=10

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/rag.log

# Namespaces
NAMESPACES=clockify-help
```

---

## 📈 Performance Tuning in Docker

### Resource Limits
```yaml
services:
  rag:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

### Memory Optimization
```yaml
environment:
  RESPONSE_CACHE_SIZE: 500    # Smaller cache
  PYTHON_OPTIMIZE: 2          # Python optimization level
```

### CPU Optimization
```bash
# High performance mode
docker run --cpus="4" --memory="4g" rag-system:latest
```

### Network Optimization
```yaml
# Enable host network mode (Linux only)
network_mode: host

# Or use bridge network
networks:
  - rag-network
```

---

## 🆘 Troubleshooting Docker

### "Docker daemon not running"
```bash
# Start Docker Desktop or daemon
docker --version  # Verify Docker is running

# Linux: Start Docker service
sudo systemctl start docker
```

### "Port 7000 already in use"
```bash
# Use different port
docker run -p 8000:7000 rag-system:latest

# Or find and stop existing container
docker ps | grep 7000
docker stop container_id
```

### "Connection refused to Ollama"
```yaml
# Check if Ollama is accessible
environment:
  LLM_BASE_URL: http://host.docker.internal:11434  # macOS/Windows
  # Or for Linux:
  LLM_BASE_URL: http://172.17.0.1:11434
```

### "Out of memory"
```bash
# Increase Docker memory limit
docker run --memory="4g" -p 7000:7000 rag-system:latest

# Docker Desktop: Settings → Resources → Memory
```

### "Build context too large"
```bash
# Create .dockerignore
cat > .dockerignore <<EOF
.git
__pycache__
.venv
.pytest_cache
*.pyc
EOF

docker build -t rag-system:latest .
```

### "Container exits immediately"
```bash
# View logs
docker logs -f container_id

# Run interactively
docker run -it rag-system:latest bash

# Check health
docker inspect container_id | jq '.State.Health'
```

### "Cannot find image"
```bash
# Pull image if from registry
docker pull myregistry/rag-system:latest

# Or build locally
docker build -t rag-system:latest .

# List images
docker images | grep rag
```

---

## 🔐 Security in Docker

### API Token Security
```bash
# Use secrets (Docker Swarm/Kubernetes)
# Or environment file with restricted permissions
chmod 600 .env
docker-compose up --env-file .env
```

### Image Security
```bash
# Scan for vulnerabilities
docker scan rag-system:latest

# Use minimal base images
FROM python:3.11-slim  # Good
# FROM ubuntu:20.04    # Bad - bloated

# Don't run as root
RUN useradd -m appuser
USER appuser
```

### Network Security
```yaml
# Use bridge network (isolated)
networks:
  - rag-network

# Don't expose unnecessary ports
ports:
  - "7000:7000"  # Good
# ports:
#   - "22:22"    # Bad - SSH exposed
```

---

## 📝 Production Deployment Checklist

- [ ] Build image: `docker build -t rag-system:v1.0 .`
- [ ] Set secure token: `API_TOKEN=your-very-secure-token`
- [ ] Set ENV: `ENV=prod`
- [ ] Configure Ollama: `LLM_BASE_URL=http://ollama:11434`
- [ ] Increase cache: `RESPONSE_CACHE_SIZE=2000`
- [ ] Set up volumes: `./logs:/app/logs`
- [ ] Enable health checks
- [ ] Set resource limits
- [ ] Test health endpoint: `/health`
- [ ] Set up monitoring: `/metrics` endpoint
- [ ] Configure logging: `LOG_LEVEL=INFO`
- [ ] Set up restart policy: `restart: always`
- [ ] Test failure recovery
- [ ] Document deployment
- [ ] Set up backups

---

## 📚 Docker Best Practices

### 1. Use .dockerignore
```
.git
.gitignore
.env
.venv
__pycache__
.pytest_cache
*.pyc
logs/
data/
```

### 2. Multi-stage Builds
```dockerfile
# Reduces final image size by 40%
FROM python:3.11-slim as builder
# ... build steps ...

FROM python:3.11-slim
COPY --from=builder /build /app
```

### 3. Minimize Layers
```dockerfile
# Bad - multiple layers
RUN apt-get update
RUN apt-get install package1
RUN apt-get install package2

# Good - single layer
RUN apt-get update && apt-get install -y package1 package2
```

### 4. Use Specific Tags
```bash
# Bad - unpredictable
docker build -t rag-system .

# Good - versioned
docker build -t rag-system:v1.2.3 .
docker build -t rag-system:latest .
```

### 5. Health Checks
```dockerfile
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:7000/health || exit 1
```

### 6. Volume Mounts
```yaml
volumes:
  - ./logs:/app/logs          # Host path : Container path
  - ./data:/app/data
  - ollama:/root/.ollama      # Named volume
```

---

## 🚀 Advanced Scenarios

### Scenario: Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rag-system
  template:
    metadata:
      labels:
        app: rag-system
    spec:
      containers:
      - name: rag
        image: rag-system:v1.0
        ports:
        - containerPort: 7000
        env:
        - name: API_TOKEN
          valueFrom:
            secretKeyRef:
              name: rag-secrets
              key: api-token
        - name: LLM_BASE_URL
          value: "http://ollama:11434"
        livenessProbe:
          httpGet:
            path: /health
            port: 7000
          initialDelaySeconds: 10
          periodSeconds: 10
        resources:
          requests:
            memory: "500Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2"
```

### Scenario: CI/CD Pipeline
```yaml
# GitHub Actions example
name: Build and Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Build Docker image
        run: docker build -t rag-system:${{ github.sha }} .

      - name: Push to registry
        run: |
          docker tag rag-system:${{ github.sha }} myregistry/rag-system:latest
          docker push myregistry/rag-system:latest
```

### Scenario: Local Development with Hot Reload
```yaml
version: '3.8'

services:
  rag:
    build: .
    ports:
      - "7000:7000"
    volumes:
      - .:/app  # Mount entire directory
      - /app/__pycache__  # Exclude cache
    environment:
      PYTHONUNBUFFERED: 1
    command: uvicorn src.server:app --host 0.0.0.0 --reload
```

---

## 📞 Getting Help

### Useful Commands
```bash
# View detailed logs
docker logs -f container_id --tail 100

# Inspect container
docker inspect container_id | jq .

# Check resource usage
docker stats container_id

# Enter running container
docker exec -it container_id bash

# Health status
docker inspect --format='{{.State.Health.Status}}' container_id
```

### Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `docker: command not found` | Install Docker |
| `permission denied` | Use `sudo` or add user to docker group |
| `port already in use` | Use different port: `-p 8000:7000` |
| `out of memory` | Increase Docker memory limit |
| `connection refused` | Check if Ollama is running and accessible |
| `image not found` | Build image: `docker build -t rag-system .` |

---

## 🎉 You're Ready!

Your RAG system is now containerized and ready for deployment.

**Next Steps:**
1. Build image: `docker build -t rag-system:latest .`
2. Run with compose: `docker-compose up -d`
3. Access UI: `http://localhost:7000`
4. Check health: `curl -H "x-api-token: change-me" http://localhost:7000/health`
5. Deploy to production with your orchestration platform

**Documentation:**
- **LAUNCH.md** - Quick start guide
- **API_REFERENCE.md** - API documentation
- **SETUP.md** - Architecture and setup
- **DOCKER.md** - This Docker guide

Happy containerizing! 🐳
