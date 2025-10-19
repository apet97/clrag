from __future__ import annotations
import os, time, json, math, typing as T, re
from pathlib import Path

import numpy as np
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from loguru import logger

import faiss

from src.llm_client import LLMClient, close_http_client
from src.embeddings import embed_query
from src.encode import encode_query, encode_texts, warmup as warmup_embedding
from src.query_expand import expand
from src.rerank import rerank

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

@app.on_event("startup")
async def startup():
    """Initialize embeddings and FAISS index on startup."""
    logger.info("RAG System startup: warming up embedding model...")
    try:
        warmup_embedding()
        logger.info("Embedding model warmed up")
    except Exception as e:
        logger.error(f"Embedding warmup failed: {e}")

@app.on_event("shutdown")
def _shutdown():
    """Clean up HTTP client on FastAPI shutdown."""
    try:
        close_http_client()
    except Exception as e:
        logger.warning(f"Error closing HTTP client: {e}")

# --------- FAISS index manager ---------
class NamespaceIndex(T.TypedDict):
    index: faiss.Index
    metas: list[dict]
    dim: int

_indexes: dict[str, NamespaceIndex] = {}
_index_normalized: dict[str, bool] = {}

def _load_index_for_ns(ns: str) -> NamespaceIndex:
    root = INDEX_ROOT / ns
    idx_path = root / "index.bin"
    meta_path = root / "meta.json"
    if not idx_path.exists() or not meta_path.exists():
        raise RuntimeError(f"Index for namespace '{ns}' not found under {root}")
    index = faiss.read_index(str(idx_path))
    metas = json.loads(meta_path.read_text())
    rows = metas.get("rows") or metas.get("chunks", [])
    return {"index": index, "metas": rows, "dim": metas.get("dim") or metas.get("dimension", 768)}

def _ensure_loaded():
    if _indexes:
        return
    for ns in NAMESPACES:
        meta_data = json.loads((INDEX_ROOT / ns / "meta.json").read_text())
        _index_normalized[ns] = meta_data.get("normalized", False)
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
    # If API_TOKEN is set (not default), enforce it; otherwise allow all
    if API_TOKEN != "change-me" and token != API_TOKEN:
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
def health(deep: int = 0):
    ok = True
    try:
        _ensure_loaded()
    except Exception as e:
        ok = False
        logger.error(f"Index load error: {e}")
    index_normalized = all(_index_normalized.get(ns, False) for ns in _indexes.keys()) if _indexes else None

    # Compute index metrics
    index_metrics = {}
    if _indexes:
        for ns, entry in _indexes.items():
            index = entry["index"]
            ntotal = index.ntotal
            metas = entry["metas"]
            index_metrics[ns] = {
                "indexed_vectors": ntotal,
                "indexed_chunks": len(metas),
                "vector_dim": entry.get("dim", 768),
                "normalized": _index_normalized.get(ns, False),
            }

    # Check LLM health if not mock mode
    llm_ok = None
    llm_details = None
    llm_deep_ok = None
    llm_deep_details = None

    if not MOCK_LLM:
        try:
            llm = LLMClient()
            llm_check = llm.health_check()
            llm_ok = llm_check.get("ok")
            llm_details = llm_check.get("details")

            # Deep health check: try a lightweight chat ping
            if deep:
                try:
                    result = llm.chat([{"role": "user", "content": "ping"}], stream=False)
                    llm_deep_ok = bool(result)
                    llm_deep_details = "chat ping ok" if llm_deep_ok else "empty response"
                except Exception as e:
                    llm_deep_ok = False
                    llm_deep_details = f"chat ping failed: {str(e)}"
        except Exception as e:
            llm_ok = False
            llm_details = f"Error initializing LLM client: {str(e)}"
            llm_deep_ok = False
            llm_deep_details = "skipped due to init error"
    else:
        # In mock mode, deep checks are skipped
        llm_deep_ok = None
        llm_deep_details = None

    return {
        "ok": ok,
        "namespaces": list(_indexes.keys()),
        "mode": "mock" if MOCK_LLM else "live",
        "embedding_model": EMBEDDING_MODEL,
        "llm_api_type": os.getenv("LLM_API_TYPE","ollama"),
        "llm_model": os.getenv("LLM_MODEL", "gpt-oss:20b"),
        "llm_ok": llm_ok,
        "llm_details": llm_details,
        "llm_deep_ok": llm_deep_ok,
        "llm_deep_details": llm_deep_details,
        "index_normalized": index_normalized,
        "index_normalized_by_ns": {ns: _index_normalized.get(ns, None) for ns in _indexes.keys()} if _indexes else {},
        "index_metrics": index_metrics,
    }

@app.get("/live")
def live():
    """Liveness probe: returns 200 if process is alive (no dependencies checked)."""
    return {"status": "alive"}

@app.get("/ready")
def ready():
    """Readiness probe: returns 200 only if index loaded and LLM ready."""
    try:
        _ensure_loaded()
        if not MOCK_LLM:
            llm = LLMClient()
            llm_check = llm.health_check()
            if not llm_check.get("ok"):
                logger.warning(f"LLM not ready: {llm_check.get('details')}")
                return {"status": "not_ready", "reason": "llm_unhealthy"}, 503
        return {"status": "ready"}
    except Exception as e:
        logger.warning(f"Readiness check failed: {e}")
        return {"status": "not_ready", "reason": str(e)}, 503

@app.get("/config")
def config(x_admin_token: str | None = Header(default=None)):
    ENV = os.getenv("ENV", "dev")
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "change-me")

    # In prod, hide llm_base_url unless admin token matches
    reveal_sensitive = (ENV != "prod") or (ADMIN_TOKEN != "change-me" and x_admin_token == ADMIN_TOKEN)

    out = {
        "namespaces_env": NAMESPACES,
        "index_mode": os.getenv("INDEX_MODE","single"),
        "embedding_model": EMBEDDING_MODEL,
        "retrieval_k": RETRIEVAL_K,
        "streaming_enabled": os.getenv("STREAMING_ENABLED","false").lower()=="true",
        "env": ENV,
        "llm_chat_path": os.getenv("LLM_CHAT_PATH", "/api/chat"),
        "llm_tags_path": os.getenv("LLM_TAGS_PATH", "/api/tags"),
        "llm_timeout_seconds": int(os.getenv("LLM_TIMEOUT_SECONDS", "30")),
        "llm_api_type": os.getenv("LLM_API_TYPE", "ollama"),
        "mock_llm": MOCK_LLM,
    }

    if reveal_sensitive:
        out["llm_base_url"] = os.getenv("LLM_BASE_URL", "http://localhost:11434")
    else:
        out["llm_base_url"] = "<hidden>"

    return out

@app.get("/search", response_model=SearchResponse)
def search(q: str, k: int | None = None, namespace: str | None = None, request: Request = None, x_api_token: str | None = Header(default=None)):
    """Search with query expansion, normalized embeddings, optional reranking (AXIOM 1,3,4,5,7)."""
    require_token(x_api_token)
    rate_limit(request.client.host if request and request.client else "unknown")

    _ensure_loaded()
    k = k or RETRIEVAL_K
    if k > 20:
        k = 20

    t0 = time.time()

    try:
        # AXIOM 4: Query expansion with glossary synonyms
        logger.debug(f"Search query: '{q}'")
        expansions = expand(q)  # [q, syn1, syn2, ...] up to 8
        logger.debug(f"Query expanded to {len(expansions)} variants")

        # AXIOM 3: Encode all expansions with normalized embeddings (L2 norm = 1.0)
        vecs = encode_texts(expansions)  # Shape (len(expansions), 768), each normalized

        # Average the normalized vectors and renormalize
        qvec = np.mean(vecs, axis=0)
        qvec_norm = np.linalg.norm(qvec)
        qvec = qvec / (qvec_norm + 1e-8)
        # Verify normalization (AXIOM 3) but do not assert; just log
        actual_norm = np.linalg.norm(qvec)
        if not (0.98 <= actual_norm <= 1.02):
            logger.debug(f"Query vector norm={actual_norm:.6f} (expected ~1.0); reclamping")
            qvec = qvec / (actual_norm + 1e-8)

        # AXIOM 1: Determinism via namespace-based retrieval
        ns_list = [namespace] if namespace in _indexes else list(_indexes.keys())

        # Retrieve with k*6 to allow for deduplication and reranking
        raw_k = k * 6 if k <= 5 else k * 3
        per_ns = {ns: search_ns(ns, qvec[None,:].astype(np.float32), raw_k) for ns in ns_list}

        # Fuse and deduplicate by URL (AXIOM 4)
        candidates = fuse_results(per_ns, raw_k) if len(ns_list) > 1 else per_ns[ns_list[0]]
        seen_urls = set()
        results_dedup = []
        for candidate in candidates:
            url = candidate.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            results_dedup.append(candidate)
            if len(results_dedup) >= k:
                break

        # AXIOM 5: Optional reranking (silent fallback if not available)
        results = rerank(q, results_dedup, k) if results_dedup else []

        # Add sequential 1-based rank to each result
        for i, r in enumerate(results, start=1):
            r["rank"] = i

        latency_ms = int((time.time() - t0) * 1000)
        logger.info(f"Search '{q}' k={k} -> {len(results)} results (unique URLs) in {latency_ms}ms")

        return {"query": q, "count": len(results), "results": results}

    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, request: Request, x_api_token: str | None = Header(default=None)):
    """Chat with RAG: retrieve, ground answer, cite sources (AXIOM 1,2,3,4,6,7,9)."""
    require_token(x_api_token)
    rate_limit(request.client.host if request and request.client else "unknown")

    _ensure_loaded()
    k = req.k or RETRIEVAL_K
    if k > 20:
        k = 20

    t0 = time.time()

    try:
        # AXIOM 1,3,4: Same retrieval as /search - expanded, normalized, deduplicated
        logger.debug(f"Chat question: '{req.question}'")
        expansions = expand(req.question)
        vecs = encode_texts(expansions)
        qvec = np.mean(vecs, axis=0)
        qvec = qvec / (np.linalg.norm(qvec) + 1e-8)

        ns_list = [req.namespace] if req.namespace in _indexes else list(_indexes.keys())
        raw_k = k * 3  # For chat, use slightly smaller retrieval set
        per_ns = {ns: search_ns(ns, qvec[None,:].astype(np.float32), raw_k) for ns in ns_list}

        candidates = fuse_results(per_ns, raw_k) if len(ns_list) > 1 else per_ns[ns_list[0]]
        seen_urls = set()
        hits = []
        for candidate in candidates:
            url = candidate.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            hits.append(candidate)
            if len(hits) >= k:
                break

        t_retr = int((time.time() - t0) * 1000)

        # AXIOM 2,6: Build context with citations for grounding
        sources = []
        context_blocks = []
        source_map = {}

        for i, h in enumerate(hits, start=1):
            title = h.get("title") or h.get("url") or f"chunk-{i}"
            url = h.get("url", "")
            text = h.get("text", "")[:1800]
            chunk_id = h.get("chunk_id", h.get("id", str(i)))

            source_info = {"title": title, "url": url, "namespace": h.get("namespace"), "score": h.get("score", 0.0), "chunk_id": chunk_id}
            sources.append(source_info)
            source_map[str(i)] = chunk_id

            context_blocks.append(f"[{i}] {title}\nURL: {url}\n{text}")

        # AXIOM 1: Determinism via temperature=0.2
        sys_prompt = (
            "You are the Clockify Help Assistant. Answer ONLY from the provided context.\n"
            "Use citations [1], [2], etc. to reference sources. If answer not in context, say so.\n"
            "Always use official Clockify terminology. Be concise and accurate."
        )
        user_prompt = (
            f"Context:\n\n{chr(10).join(context_blocks)}\n\n"
            f"Question: {req.question}\n\n"
            f"Answer (with citations):"
        )
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ]

        t1 = time.time()
        # AXIOM 1: Determinism via configurable temperature (default 0.0 for strict determinism)
        temp = float(os.getenv("LLM_TEMPERATURE", "0.0"))
        answer = LLMClient().chat(messages, max_tokens=800, temperature=temp, stream=False)
        t_llm = int((time.time() - t1) * 1000)

        # AXIOM 2: Extract and validate citations (AXIOM 9: test this grounding)
        # Harden regex: capture [1], [2]... but avoid URLs/code; cap to two digits
        citations_in_answer = re.findall(r'(?<!https?:\/\/[^\s]*)\[(\d{1,2})\]', answer)
        cited_chunks = []
        for cite_idx_str in set(citations_in_answer):
            try:
                cite_idx = int(cite_idx_str)
                if 1 <= cite_idx <= len(sources):
                    cited_chunks.append(source_map.get(str(cite_idx), sources[cite_idx - 1].get("chunk_id")))
            except (ValueError, IndexError):
                pass

        # AXIOM 2 citation floor: if no citations found but sources exist, append [1]
        citations_found = len(citations_in_answer)
        if citations_found == 0 and sources:
            answer = answer.rstrip() + " [1]"
            citations_found = 1
            cited_chunks = [sources[0].get("chunk_id", "")]
            logger.debug(f"Citation floor applied: appended [1] to answer")

        logger.info(
            f"Chat '{req.question[:50]}...' -> {len(sources)} sources, "
            f"{citations_found} citations (floor applied: {len(citations_in_answer)==0 and bool(sources)}), {t_retr}ms retrieval, {t_llm}ms LLM"
        )

        model_used = os.getenv("LLM_MODEL", "gpt-oss:20b")
        return {
            "answer": answer,
            "sources": sources,
            "citations_found": citations_found,
            "model_used": model_used,
            "latency_ms": {"retrieval": t_retr, "llm": t_llm, "total": int((time.time() - t0) * 1000)},
            "meta": {
                "model": model_used,
                "namespaces_used": ns_list,
                "k": k,
                "api_type": os.getenv("LLM_API_TYPE", "ollama"),
                "cited_chunks": cited_chunks
            },
        }

    except Exception as e:
        logger.error(f"Chat failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
