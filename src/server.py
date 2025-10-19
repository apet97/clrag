from __future__ import annotations
import os, time, json, math, typing as T
from pathlib import Path

import numpy as np
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from loguru import logger

from sentence_transformers import SentenceTransformer
import faiss

from src.llm_client import LLMClient

API_TOKEN = os.getenv("API_TOKEN", "change-me")
HOST = os.getenv("API_HOST", "0.0.0.0")
PORT = int(os.getenv("API_PORT", "7000"))
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "5"))
NAMESPACES = [s.strip() for s in os.getenv("NAMESPACES","clockify,langchain").split(",") if s.strip()]

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-base")
INDEX_MODE = os.getenv("INDEX_MODE", "single")
INDEX_ROOT = Path("index/faiss")

MOCK_LLM = os.getenv("MOCK_LLM", "false").lower() == "true"

app = FastAPI(default_response_class=ORJSONResponse)

# --------- Embedding loader ---------
_embedder = None
def get_embedder():
    global _embedder
    if _embedder is None:
        logger.info(f"Loading embedder: {EMBEDDING_MODEL}")
        _embedder = SentenceTransformer(EMBEDDING_MODEL)
        _embedder.max_seq_length = 512
    return _embedder

def embed_query(text: str) -> np.ndarray:
    q = f"query: {text.strip()}"
    v = get_embedder().encode([q], convert_to_numpy=True).astype(np.float32)
    v /= (np.linalg.norm(v, axis=1, keepdims=True) + 1e-12)
    return v

# --------- FAISS index manager ---------
class NamespaceIndex(T.TypedDict):
    index: faiss.Index
    metas: list[dict]
    dim: int

_indexes: dict[str, NamespaceIndex] = {}

def _load_index_for_ns(ns: str) -> NamespaceIndex:
    root = INDEX_ROOT / ns
    idx_path = root / "index.bin"
    meta_path = root / "meta.json"
    if not idx_path.exists() or not meta_path.exists():
        raise RuntimeError(f"Index for namespace '{ns}' not found under {root}")
    index = faiss.read_index(str(idx_path))
    metas = json.loads(meta_path.read_text())
    return {"index": index, "metas": metas["rows"], "dim": metas["dim"]}

def _ensure_loaded():
    if _indexes:
        return
    for ns in NAMESPACES:
        _indexes[ns] = _load_index_for_ns(ns)
    logger.info(f"Loaded namespaces: {list(_indexes.keys())}")

# --------- Retrieval ---------
def search_ns(ns: str, qvec: np.ndarray, k: int) -> list[dict]:
    entry = _indexes[ns]
    D, I = entry["index"].search(qvec, k)
    res = []
    for rank, (idx, score) in enumerate(zip(I[0].tolist(), D[0].tolist()), start=1):
        if idx < 0:
            continue
        meta = entry["metas"][idx]
        res.append({
            "namespace": ns,
            "score": float(score),
            "rank": rank,
            **meta
        })
    return res

def fuse_results(by_ns: dict[str, list[dict]], k: int) -> list[dict]:
    scores: dict[tuple, float] = {}
    payloads: dict[tuple, dict] = {}
    C = 60.0
    for ns, lst in by_ns.items():
        for r, item in enumerate(lst, start=1):
            key = (item.get("url",""), item.get("chunk_id", item.get("id", r)))
            scores[key] = scores.get(key, 0.0) + 1.0/(C + r)
            payloads[key] = item
    merged = sorted(payloads.values(), key=lambda x: scores[(x.get("url",""), x.get("chunk_id", x.get("id", 0)))], reverse=True)
    return merged[:k]

# --------- Models ---------
class SearchResponse(BaseModel):
    results: list[dict]

class ChatRequest(BaseModel):
    question: str
    k: int | None = None
    namespace: str | None = None

class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]
    latency_ms: dict
    meta: dict

# --------- Auth/limits ---------
def require_token(token: str | None):
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="unauthorized")

_last_req: dict[str, float] = {}
def rate_limit(ip: str, min_interval: float = 0.25):
    now = time.time()
    t = _last_req.get(ip, 0.0)
    if now - t < min_interval:
        raise HTTPException(status_code=429, detail="rate_limited")
    _last_req[ip] = now

# --------- Routes ---------
@app.get("/health")
def health():
    ok = True
    try:
        _ensure_loaded()
    except Exception as e:
        ok = False
        logger.error(f"Index load error: {e}")
    return {
        "ok": ok,
        "namespaces": list(_indexes.keys()),
        "mode": "mock" if MOCK_LLM else "live",
        "llm_api_type": os.getenv("LLM_API_TYPE","ollama"),
    }

@app.get("/config")
def config():
    return {
        "namespaces_env": NAMESPACES,
        "index_mode": os.getenv("INDEX_MODE","single"),
        "embedding_model": EMBEDDING_MODEL,
        "retrieval_k": RETRIEVAL_K,
    }

@app.get("/search", response_model=SearchResponse)
def search(q: str, k: int | None = None, namespace: str | None = None, request: Request = None, x_api_token: str | None = Header(default=None)):
    require_token(x_api_token)
    rate_limit(request.client.host if request and request.client else "unknown")

    _ensure_loaded()
    k = k or RETRIEVAL_K
    ns_list = [namespace] if namespace in _indexes else list(_indexes.keys())
    qvec = embed_query(q)
    per_ns = {ns: search_ns(ns, qvec, k) for ns in ns_list}
    results = fuse_results(per_ns, k) if len(ns_list) > 1 else per_ns[ns_list[0]]
    return {"results": results}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, request: Request, x_api_token: str | None = Header(default=None)):
    require_token(x_api_token)
    rate_limit(request.client.host if request and request.client else "unknown")

    _ensure_loaded()
    k = req.k or RETRIEVAL_K
    ns_list = [req.namespace] if req.namespace in _indexes else list(_indexes.keys())

    t0 = time.time()
    qvec = embed_query(req.question)
    per_ns = {ns: search_ns(ns, qvec, k) for ns in ns_list}
    hits = fuse_results(per_ns, k) if len(ns_list) > 1 else per_ns[ns_list[0]]
    t_retr = int((time.time() - t0) * 1000)

    # Build context and citations
    sources = []
    context_blocks = []
    for i, h in enumerate(hits, start=1):
        title = h.get("title") or h.get("url") or f"chunk-{i}"
        url = h.get("url", "")
        text = h.get("text", "")[:1800]
        sources.append({"title": title, "url": url, "namespace": h.get("namespace"), "score": h.get("score", 0.0)})
        context_blocks.append(f"[{i}] {title}\n{url}\n{text}")

    sys_prompt = (
        "Answer only from the provided context. If the answer is not present, say it is not covered in documentation.\n"
        "Add bracketed citations like [1], [2]. Then include a 'Sources' list with URLs."
    )
    user_prompt = f"Context:\n\n" + "\n\n".join(context_blocks) + f"\n\nQuestion: {req.question}\n\nAnswer:"
    messages = [{"role":"system","content":sys_prompt},{"role":"user","content":user_prompt}]

    t1 = time.time()
    answer = LLMClient().chat(messages, max_tokens=800, temperature=0.2, stream=False)
    t_llm = int((time.time() - t1) * 1000)

    return {
        "answer": answer,
        "sources": sources,
        "latency_ms": {"retrieval": t_retr, "llm": t_llm, "total": int((time.time()-t0)*1000)},
        "meta": {"model": os.getenv("LLM_MODEL","gpt-oss20b"), "namespaces_used": ns_list, "k": k, "api_type": os.getenv("LLM_API_TYPE","ollama")},
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
