# RAG v1: Baked FAISS Index Image
# Prebuilt index baked into Docker image for fast, reproducible deployments
# Includes: Python environment, dependencies, Ollama client, prebuilt FAISS index

FROM python:3.11-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/
COPY data/ data/

# Copy prebuilt FAISS index (CRITICAL for fast startup)
COPY index/faiss/clockify-help/ index/faiss/clockify-help/

# Set environment variables for prebuilt image
ENV NAMESPACES=clockify-help
ENV EMBEDDING_MODEL=nomic-embed-text:latest
ENV LLM_BASE_URL=http://ollama:11434
ENV API_HOST=0.0.0.0
ENV API_PORT=7000
ENV ENV=prod

# Default token - MUST be overridden in production!
ENV API_TOKEN=change-me

# Expose API port
EXPOSE 7000

# Health check: ensure index is loaded and API is responsive
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f -H "x-api-token: ${API_TOKEN}" http://localhost:7000/health || exit 1

# Startup: API server with prebuilt index validation
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "7000", "--log-level", "info"]
