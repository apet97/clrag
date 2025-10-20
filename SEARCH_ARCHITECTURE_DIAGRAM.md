# Search & Retrieval Architecture Diagram

## High-Level Search Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SEARCH REQUEST (/search)                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                    ┌──────────────────────────────────┐
                    │  1. AUTH & RATE LIMITING        │
                    │  - Token validation (HMAC)       │
                    │  - Per-IP throttling             │
                    └──────────────────────────────────┘
                                      │
                                      ▼
                    ┌──────────────────────────────────┐
                    │  2. RESPONSE CACHE CHECK        │
                    │  - LRU cache lookup              │
                    │  - MD5(query+k+ns) key           │
                    │  - TTL expiration (3600s)        │
                    └──────────────────────────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │ Hit? Return cached      │ Miss? Continue
                         │                         │
                    [80-90% latency saved]         ▼
                         │        ┌──────────────────────────────┐
                         │        │  3. QUERY EXPANSION          │
                         │        │  - Glossary synonym lookup   │
                         │        │  - Generate [q, syn1, syn2..] │
                         │        └──────────────────────────────┘
                         │                        │
                         │                        ▼
                         │        ┌──────────────────────────────┐
                         │        │  4. QUERY ENCODING           │
                         │        │  - Batch encode expansions   │
                         │        │  - Ollama /api/embeddings    │
                         │        │  - L2-normalize each vec     │
                         │        │  - LRU cache (512)           │
                         │        └──────────────────────────────┘
                         │                        │
                         │                        ▼
                         │        ┌──────────────────────────────┐
                         │        │  5. VECTOR AGGREGATION       │
                         │        │  - Mean of normalized vectors│
                         │        │  - Re-normalize result       │
                         │        │  - Verify norm ~1.0          │
                         │        └──────────────────────────────┘
                         │                        │
                         │                        ▼
                         │        ┌──────────────────────────────┐
                         │        │  6. MULTI-NAMESPACE SEARCH   │
                         │        │  - For each namespace:       │
                         │        │    * Search FAISS IndexFlatIP│
                         │        │    * Retrieve k*6 or k*3     │
                         │        │    * Score = cosine sim      │
                         │        └──────────────────────────────┘
                         │                        │
                         │                        ▼
                         │        ┌──────────────────────────────┐
                         │        │  7. RESULT FUSION (RRF)      │
                         │        │  - Merge multi-namespace     │
                         │        │  - RRF formula: 1/(C+rank)   │
                         │        │  - C=60.0 (configurable)     │
                         │        └──────────────────────────────┘
                         │                        │
                         │                        ▼
                         │        ┌──────────────────────────────┐
                         │        │  8. DEDUPLICATION            │
                         │        │  - Stable sort candidates    │
                         │        │  - Remove duplicate URLs     │
                         │        │  - Keep top-k unique URLs    │
                         │        └──────────────────────────────┘
                         │                        │
                         │                        ▼
                         │        ┌──────────────────────────────┐
                         │        │  9. OPTIONAL RERANKING       │
                         │        │  - Cross-encoder optional    │
                         │        │  - FlagEmbedding/bge-base    │
                         │        │  - Graceful fallback if N/A  │
                         │        │  - Update scores             │
                         │        └──────────────────────────────┘
                         │                        │
                         │                        ▼
                         │        ┌──────────────────────────────┐
                         │        │  10. CACHE RESPONSE          │
                         │        │  - Store in LRU cache        │
                         │        │  - TTL=3600s (default)       │
                         │        └──────────────────────────────┘
                         │                        │
                         └────────────┬───────────┘
                                      ▼
                    ┌──────────────────────────────────┐
                    │  RETURN SEARCH RESPONSE          │
                    │  - results: [...]                │
                    │  - request_id                    │
                    │  - latency_ms                    │
                    └──────────────────────────────────┘
```

---

## FAISS Index Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FAISS INDEX STRUCTURE                    │
└─────────────────────────────────────────────────────────────┘

Per-Namespace Index:
┌─────────────────┐
│   Namespace 1   │
│   (clockify)    │
├─────────────────┤
│  index.faiss    │  ← IndexFlatIP (brute force inner product)
│  meta.json      │  ← Metadata + chunk references
│  Vectors:       │
│  ┌───────────┐  │
│  │ [emb0]    │  │  L2-normalized embedding vectors
│  │ [emb1]    │  │  Dimension: 768 (E5-base default)
│  │ [emb2]    │  │  Count: N chunks
│  │ ...       │  │
│  │ [embN-1]  │  │
│  └───────────┘  │
│  Metadata:      │
│  ┌───────────┐  │
│  │ chunk_0:  │  │  id, url, title, headers, tokens
│  │ chunk_1:  │  │
│  │ chunk_2:  │  │
│  │ ...       │  │
│  │ chunk_N-1 │  │
│  └───────────┘  │
└─────────────────┘

┌─────────────────┐
│   Namespace 2   │
│  (langchain)    │
├─────────────────┤
│  index.faiss    │
│  meta.json      │
│  ... similar    │
└─────────────────┘

Multiple namespaces loaded in parallel:
_indexes = {
    "clockify": {"index": IndexFlatIP, "metas": [...], "dim": 768},
    "langchain": {"index": IndexFlatIP, "metas": [...], "dim": 768},
}
```

---

## Dense vs. Hybrid Retrieval Paths

```
                          QUERY
                            │
                ┌───────────┬┴────────────┐
                │           │             │
                ▼           ▼             ▼
        ┌──────────────┐  DENSE-ONLY    HYBRID
        │ Encoded      │    PATH         PATH
        │ Query Vec    │    │            │
        │ (L2-norm)    │    │            ▼
        └──────────────┘    │      ┌───────────┐
                │            │      │ BM25 Index│
                │            │      │ tokenize  │
                │            ▼      │ score     │
                │      ┌──────────┐ └───────────┘
                │      │ FAISS    │      │
                │      │ IndexFlatIP   │
                │      │ search(q, k)│ │
                │      │ D, I ← ← ← ┘  │
                │      │ (distances,   │
                │      │  indices)     │
                │      └──────────┘    │
                │            │         │
                ▼            ▼         ▼
        ┌────────────────────────────────────┐
        │  DENSE RESULTS      BM25 RESULTS   │
        │  (from FAISS)       (from BM25)    │
        │  k_dense=40         k_bm25=40      │
        └────────────────────────────────────┘
                        │
                        ▼
        ┌────────────────────────────────────┐
        │  LATE FUSION (Min-Max Normalize)   │
        │  Combine scores:                   │
        │  α*norm(dense) + (1-α)*norm(bm25) │
        │  α = 0.6 (default)                 │
        └────────────────────────────────────┘
                        │
                        ▼
        ┌────────────────────────────────────┐
        │  FIELD BOOSTING                    │
        │  +0.08 if title matches            │
        │  +0.05 if section matches          │
        │  +0.10 if glossary doc             │
        └────────────────────────────────────┘
```

---

## Multi-Namespace Result Fusion

```
              ENCODED QUERY VECTOR
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
    ┌─────────┐   ┌─────────┐   ┌─────────┐
    │Namespace│   │Namespace│   │Namespace│
    │clockify │   │langchain│   │  wiki   │
    └─────────┘   └─────────┘   └─────────┘
         │              │              │
    FAISS search   FAISS search   FAISS search
    k*6 results   k*6 results    k*6 results
         │              │              │
         ▼              ▼              ▼
    ┌─────────────────────────────────────────┐
    │ RECIPROCAL RANK FUSION (RRF)            │
    │                                         │
    │ For each result from all namespaces:   │
    │ score = Σ (1 / (C + rank_i))           │
    │ where C = 60.0 (RRF constant)          │
    │                                         │
    │ Example:                                │
    │ - Result appears at rank 1 in NS1      │
    │   and rank 2 in NS2:                   │
    │   score = 1/(60+1) + 1/(60+2)          │
    │        = 1/61 + 1/62 ≈ 0.0163 + 0.0161│
    │        ≈ 0.0324                        │
    └─────────────────────────────────────────┘
         │
         ▼
    ┌─────────────────────────────────────────┐
    │ SORT BY FUSED SCORE                     │
    │ Return top-k merged results             │
    └─────────────────────────────────────────┘
```

---

## Caching Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                      CACHING LAYERS                         │
└─────────────────────────────────────────────────────────────┘

LAYER 1: RESPONSE CACHE (LRU)
┌──────────────────────────────────────────┐
│ LRUResponseCache                         │
│ max_size: 1000 entries                   │
│ default_ttl: 3600 seconds                │
│                                          │
│ Key: MD5(query + k + namespace)          │
│ Value: Full /search response             │
│                                          │
│ Hit rate: 80-90% for repeated queries    │
│ Thread-safe: Lock-based sync             │
│                                          │
│ Eviction: LRU when over capacity         │
│ Expiration: TTL-based removal            │
└──────────────────────────────────────────┘
              Cache Hit? [Yes]──────────────► Return immediately
                    │
                   [No]
                    ▼

LAYER 2: EMBEDDING CACHE (LRU)
┌──────────────────────────────────────────┐
│ @lru_cache(maxsize=512)                 │
│ _encode_cached(text: str)               │
│                                          │
│ Caches: Ollama embedding calls           │
│ Indexed by: Query text                   │
│ Returns: Tuple (hashable)                │
│                                          │
│ Benefit: Avoid redundant Ollama calls    │
│ for repeated query expansions            │
└──────────────────────────────────────────┘
         Used during query expansion
```

---

## Score Evolution Through Pipeline

```
Document retrieval and scoring at each stage:

Stage 1: Dense Retrieval
────────────────────────
Doc A: score = 0.85 (cosine similarity, normalized vecs)
Doc B: score = 0.78
Doc C: score = 0.72

Stage 2: BM25 Scoring (if hybrid)
──────────────────────────────────
Doc A: bm25_score = 0.90 (keyword match)
Doc B: bm25_score = 0.45
Doc C: bm25_score = 0.92

Stage 3: Fusion & Field Boosting
─────────────────────────────────
Doc A: base = 0.6*0.85 + 0.4*norm(0.90) = 0.51 + 0.36 = 0.87
       + 0.08 (title match) = 0.95
       + 0.10 (glossary) = 1.05

Doc B: base = 0.6*0.78 + 0.4*norm(0.45) = 0.47 + 0.18 = 0.65
       + 0.05 (section match) = 0.70

Doc C: base = 0.6*0.72 + 0.4*norm(0.92) = 0.43 + 0.37 = 0.80
       (no boosts) = 0.80

Ranking before rerank: A(1.05) > C(0.80) > B(0.70)

Stage 4: Optional Reranking
──────────────────────────
Cross-encoder re-scores:
Doc A: 0.92
Doc C: 0.85
Doc B: 0.78

Final Ranking: A(0.92) > C(0.85) > B(0.78)
```

---

## Configuration Sensitivity Analysis

```
Parameter               Default    Impact on      Impact on
                                   Relevance      Speed
─────────────────────────────────────────────────────────
RETRIEVAL_K            5           Higher k→      Slower
                                   broader      response
                                   results

HYBRID_ALPHA           0.6         0.7→semantic   Similar
                                   0.4→keyword   (both cached)

K_DENSE               40           More dense     Retrieval
K_BM25                40           candidates→   slower
                                   better recall

RESPONSE_CACHE_TTL    3600s        Larger TTL→    Hit rate
                                   stale results ↑

RESPONSE_CACHE_SIZE   1000         Larger→       More memory
                                   more hits

EMBEDDING_BATCH_SIZE  32           Larger batch→  Pool efficiency
                                   better Ollama throughput
                                   utilization

QUERY_EXPANSION_      on           Expansion→    +encoder
(glossary)                         recall ↑      time
```

---

## Query Type Detection (Potential Enhancement)

```
Current State: Basic synonym expansion

Recommended Enhancement:
┌──────────────────────────────────────────────────────┐
│ Query Type Detection Module                          │
├──────────────────────────────────────────────────────┤
│                                                      │
│ Input: "How do I enable SSO?"                       │
│                                                      │
│ ┌──────────────────────────────────────────────┐    │
│ │ Pattern Matching                             │    │
│ │ - "What is X?" → Definitional               │    │
│ │ - "How do I X?" → Procedural                │    │
│ │ - "Why X?" → Causal                         │    │
│ │ - "When/Where X?" → Situational             │    │
│ └──────────────────────────────────────────────┘    │
│ → Type: PROCEDURAL                                  │
│                                                      │
│ ┌──────────────────────────────────────────────┐    │
│ │ Adaptive Settings                            │    │
│ │ - Procedural: alpha=0.7 (semantic weight)    │    │
│ │ - Definitional: alpha=0.5 (balanced)         │    │
│ │ - Skip reranking for procedural              │    │
│ └──────────────────────────────────────────────┘    │
│                                                      │
│ Output: Tuned retrieval parameters                  │
│         based on query type                         │
└──────────────────────────────────────────────────────┘
```

---

## Improvement Roadmap (Phased)

```
PHASE 1: Quick Wins (1-2 weeks)
┌─────────────────────────────────────────────────┐
│ • Enable hybrid search by default                │
│ • Activate cross-encoder reranking in pipeline  │
│ • Add query type detection (basic)              │
│ Estimated impact: +15-20% relevance            │
└─────────────────────────────────────────────────┘
                    ▼

PHASE 2: Medium-term (1 month)
┌─────────────────────────────────────────────────┐
│ • Implement Learning-to-Rank (LambdaMART)      │
│ • Add hierarchical chunking (parent/child)      │
│ • Distributed caching (Redis)                   │
│ • Parallel namespace retrieval (threading)      │
│ Estimated impact: +25-35% relevance, 30% speed │
└─────────────────────────────────────────────────┘
                    ▼

PHASE 3: Advanced (2+ months)
┌─────────────────────────────────────────────────┐
│ • Approximate indices (HNSW/IVF)               │
│ • Feedback loop & online learning              │
│ • Named Entity Recognition                     │
│ • Multi-intent query splitting                 │
│ • Personalization framework                    │
│ Estimated impact: +40-50% relevance            │
└─────────────────────────────────────────────────┘
```

