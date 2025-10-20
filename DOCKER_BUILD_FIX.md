# Docker Build Fix - Index Not Found

Your error:
```
ERROR: failed to build: failed to solve: 
"/index/faiss/clockify-help": not found
```

## Quick Fix

The Dockerfile is looking for `index/faiss/clockify-help/` but your actual directory is `index/faiss/clockify/`

### Option 1: Rename Your Index (Recommended)

```bash
mv index/faiss/clockify index/faiss/clockify-help
```

Then build:
```bash
docker build -t rag-system:latest .
```

### Option 2: Update Dockerfile

Edit `Dockerfile` and change:

```dockerfile
# Line 25 - Change this:
COPY index/faiss/clockify-help/ index/faiss/clockify-help/

# To this:
COPY index/faiss/clockify/ index/faiss/clockify/
```

Then build:
```bash
docker build -t rag-system:latest .
```

### Option 3: Update docker-compose.yml

Edit `docker-compose.yml` and change NAMESPACES:

```yaml
environment:
  NAMESPACES: clockify  # Was: clockify-help
```

Then:
```bash
docker build -t rag-system:latest .
docker-compose up -d
```

## Recommended: Use Option 1

```bash
# Rename the index to match Dockerfile expectations
mv index/faiss/clockify index/faiss/clockify-help

# Build
docker build -t rag-system:latest .

# Run
docker-compose up -d

# Verify
curl -H "x-api-token: change-me" http://localhost:7000/health
```

Then open: http://localhost:7000

✅ Done!
