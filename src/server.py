#!/usr/bin/env python3
"""Advanced multi-corpus RAG server with hybrid search, reranking, and query rewrites."""

import json
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
import os
from datetime import datetime

import numpy as np
from fastapi import FastAPI, HTTPException
import uvicorn
import httpx
from pydantic import BaseModel
from dotenv import load_dotenv

try:
    import faiss
except ImportError:
    faiss = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

try:
    from whoosh.index import open_dir
    from whoosh.qparser import QueryParser
except ImportError:
    open_dir = None

from src.prompt import RAGPrompt
from src.rewrites import QueryRewriter
from src.rerank import rerank

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Config
MODEL_BASE_URL = os.getenv("MODEL_BASE_URL", "http://127.0.0.1:8000/v1")
MODEL_API_KEY = os.getenv("MODEL_API_KEY", "sk-local-or-empty")
MODEL_NAME = os.getenv("MODEL_NAME", "oss20b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-base")
QUERY_REWRITES = os.getenv("QUERY_REWRITES", "true").lower() == "true"
HYBRID_SEARCH = os.getenv("HYBRID_SEARCH", "true").lower() == "true"
PARENT_CHILD = os.getenv("PARENT_CHILD_INDEXING", "true").lower() == "true"
USE_CITATIONS = os.getenv("USE_CITATIONS", "true").lower() == "true"
MAX_CONTEXT = int(os.getenv("RETRIEVAL_MAX_CONTEXT_TOKENS", "4000"))
DEFAULT_K = int(os.getenv("RETRIEVAL_TOP_K", "5"))

INDEX_DIR = Path("index/faiss")

_embedder = None
_indexes: Dict[str, dict] = {}
_bm25_indexes: Dict[str, any] = {}


class SearchRequest(BaseModel):
    q: str
    k: Optional[int] = DEFAULT_K
    namespace: Optional[str] = None


class ChatRequest(BaseModel):
    question: str
    k: Optional[int] = DEFAULT_K
    namespace: Optional[str] = None
    allow_rewrites: Optional[bool] = True
    allow_rerank: Optional[bool] = True


def init_embedder():
    """Load embedder on startup."""
    global _embedder
    if _embedder is None:
        try:
            _embedder = SentenceTransformer(EMBEDDING_MODEL)
            _embedder.max_seq_length = 512
            logger.info(f"✓ Loaded embedder: {EMBEDDING_MODEL}")
        except Exception as e:
            logger.error(f"Failed to load embedder: {e}")
    return _embedder


def init_indexes():
    """Load all namespace indexes."""
    global _indexes, _bm25_indexes
    if _indexes:
        return

    for ns_dir in INDEX_DIR.glob("*/"):
        if ns_dir.name in ("hybrid",):
            continue

        ns = ns_dir.name
        index_file = ns_dir / "index.bin"
        meta_file = ns_dir / "meta.json"

        if index_file.exists() and meta_file.exists():
            try:
                index = faiss.read_index(str(index_file))
                with open(meta_file) as f:
                    meta = json.load(f)

                _indexes[ns] = {"index": index, "metadata": meta}
                logger.info(f"✓ Loaded index for {ns}: {index.ntotal} vectors")

                # Load BM25 if exists
                if HYBRID_SEARCH:
                    try:
                        bm25_dir = INDEX_DIR / "hybrid" / ns
                        if bm25_dir.exists():
                            bm25_ix = open_dir(str(bm25_dir))
                            _bm25_indexes[ns] = bm25_ix
                            logger.info(f"✓ Loaded BM25 for {ns}")
                    except Exception as e:
                        logger.debug(f"BM25 not available for {ns}: {e}")

            except Exception as e:
                logger.error(f"Failed to load index for {ns}: {e}")


def embed_query(text: str) -> np.ndarray:
    """Embed a query string with E5 prompt format."""
    embedder = init_embedder()
    if not embedder:
        raise HTTPException(status_code=503, detail="Embedder not loaded")
    # E5 format: prefix queries with "query: "
    query_with_prefix = f"query: {text.strip()}"
    emb = embedder.encode([query_with_prefix], convert_to_numpy=True).astype(np.float32)
    # L2-normalize to match index normalization
    emb = emb / (np.linalg.norm(emb, axis=1, keepdims=True) + 1e-12)
    return emb.astype(np.float32)


def vector_search(query_emb: np.ndarray, namespace: Optional[str], k: int) -> List[Dict[str, Any]]:
    """Search FAISS indexes."""
    if not _indexes:
        return []

    namespaces = [namespace] if namespace and namespace in _indexes else list(_indexes.keys())
    all_results = []

    for ns in namespaces:
        idx_data = _indexes.get(ns)
        if not idx_data:
            continue

        index = idx_data["index"]
        meta_chunks = idx_data["metadata"]["chunks"]

        # Search
        distances, indices = index.search(query_emb, min(k * 2, len(meta_chunks)))

        for i, idx in enumerate(indices[0]):
            if 0 <= idx < len(meta_chunks):
                chunk = meta_chunks[int(idx)]
                chunk["vector_score"] = float(distances[0][i])
                chunk["namespace"] = ns
                all_results.append(chunk)

    return sorted(all_results, key=lambda x: x.get("vector_score", 0), reverse=True)[:k]


def bm25_search(query: str, namespace: Optional[str], k: int) -> List[Dict[str, Any]]:
    """Search using BM25."""
    if not HYBRID_SEARCH or not _bm25_indexes:
        return []

    results = []
    namespaces = [namespace] if namespace and namespace in _bm25_indexes else list(_bm25_indexes.keys())

    for ns in namespaces:
        try:
            ix = _bm25_indexes.get(ns)
            if not ix:
                continue

            searcher = ix.searcher()
            parser = QueryParser("text", ix.schema)
            parsed_q = parser.parse(query)

            hits = searcher.search(parsed_q, limit=k * 2)
            for hit in hits:
                results.append({
                    "id": int(hit["id"]),
                    "text": hit["text"],
                    "title": hit["title"],
                    "url": hit["url"],
                    "namespace": ns,
                    "node_type": hit.get("node_type", "child"),
                    "bm25_score": hit.score,
                })

            searcher.close()
        except Exception as e:
            logger.debug(f"BM25 search error for {ns}: {e}")

    return results[:k]


def hybrid_search(query: str, query_emb: np.ndarray, namespace: Optional[str], k: int) -> List[Dict[str, Any]]:
    """Hybrid search: combine vector and BM25."""
    vector_results = vector_search(query_emb, namespace, k * 2)
    bm25_results = bm25_search(query, namespace, k * 2)

    # Dedupe and combine
    seen = set()
    combined = []
    for r in vector_results + bm25_results:
        key = (r.get("id"), r.get("url"))
        if key not in seen:
            combined.append(r)
            seen.add(key)

    return combined[:k]


app = FastAPI(
    title="Multi-Corpus RAG Assistant",
    description="Clockify + LangChain advanced retrieval",
    version="2.0.0"
)


@app.on_event("startup")
async def startup():
    """Initialize on startup."""
    init_embedder()
    init_indexes()
    logger.info("✓ Server ready")


@app.get("/health")
async def health():
    """Health check."""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "indexes_loaded": len(_indexes),
        "namespaces": list(_indexes.keys()),
    }


@app.get("/search")
async def search(q: str, k: int = DEFAULT_K, namespace: Optional[str] = None):
    """Search across corpora."""
    if not q or len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Query too short")

    k = min(k, 20)

    try:
        query_emb = embed_query(q)

        if HYBRID_SEARCH:
            results = hybrid_search(q, query_emb, namespace, k)
        else:
            results = vector_search(query_emb, namespace, k)

        return {
            "query": q,
            "count": len(results),
            "results": results[:k],
        }

    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail="Search failed")


@app.post("/chat")
async def chat(req: ChatRequest):
    """Chat with advanced retrieval."""
    if not req.question or len(req.question.strip()) < 2:
        raise HTTPException(status_code=400, detail="Question too short")

    try:
        # Rewrite query if enabled
        queries = [req.question]
        if req.allow_rewrites and QUERY_REWRITES:
            queries = QueryRewriter.rewrite(req.question)
            logger.info(f"Generated {len(queries)} query rewrites")

        # Search with all rewrites
        all_chunks = []
        for q in queries:
            q_emb = embed_query(q)
            if HYBRID_SEARCH:
                chunks = hybrid_search(q, q_emb, req.namespace, req.k or DEFAULT_K)
            else:
                chunks = vector_search(q_emb, req.namespace, req.k or DEFAULT_K)
            all_chunks.extend(chunks)

        # Dedupe
        seen = set()
        unique_chunks = []
        for c in all_chunks:
            key = (c.get("url"), c.get("id"))
            if key not in seen:
                unique_chunks.append(c)
                seen.add(key)

        # Rerank if enabled
        if req.allow_rerank:
            unique_chunks = rerank(req.question, unique_chunks, req.k or DEFAULT_K)

        # Build prompt
        msgs, sources = RAGPrompt.build_messages(req.question, unique_chunks[:DEFAULT_K])

        # Call LLM
        answer = await call_llm(msgs)

        # Format response
        result = RAGPrompt.format_response(answer or "Unable to generate response", sources, USE_CITATIONS)

        return result

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Chat failed")


async def call_llm(messages: List[Dict[str, str]]) -> Optional[str]:
    """Call local LLM."""
    try:
        url = f"{MODEL_BASE_URL}/chat/completions"
        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.2,  # Factual Q&A: very low entropy
            "top_p": 0.9,  # Allow some diversity but stay focused
        }
        headers = {
            "Authorization": f"Bearer {MODEL_API_KEY}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"LLM error: {resp.status_code}")
                return None

    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return None


@app.get("/")
async def root():
    """API info."""
    return {
        "name": "Multi-Corpus RAG Assistant",
        "version": "2.0.0",
        "features": {
            "vector_search": True,
            "hybrid_search": HYBRID_SEARCH,
            "query_rewrites": QUERY_REWRITES,
            "reranking": True,
            "parent_child": PARENT_CHILD,
            "citations": USE_CITATIONS,
        },
        "endpoints": {
            "health": "GET /health",
            "search": "GET /search?q=...&namespace=...&k=5",
            "chat": "POST /chat",
        },
        "docs": "/docs",
    }


def main():
    """Run server."""
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "7000"))

    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(
        "src.server:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()
