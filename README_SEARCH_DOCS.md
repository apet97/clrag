# RAG Search & Retrieval Documentation Index

This directory contains comprehensive analysis of the search and retrieval implementation in the RAG system.

## Documents Overview

### 1. SEARCH_RETRIEVAL_ANALYSIS.md (Primary Technical Document)
**24KB | 800 lines | Deep Technical Analysis**

Complete deep-dive into the search implementation covering:
- Executive summary of the system architecture
- Query handling flow (7-step pipeline)
- FAISS index architecture and usage
- Hybrid retrieval mechanisms (dense + BM25)
- Ranking and reranking strategies
- Result deduplication and filtering
- Multi-layer caching system
- Current implementation strengths
- Detailed improvement recommendations (8 categories)
- Configuration tuning parameters
- System axioms documentation

**Best for:** Understanding the complete search pipeline, identifying improvement opportunities, and deep technical decisions.

---

### 2. SEARCH_ARCHITECTURE_DIAGRAM.md (Visual Reference)
**24KB | 434 lines | Diagrams & Visualizations**

Comprehensive ASCII diagrams and flow charts including:
- High-level search request pipeline (10 stages)
- FAISS index structure visualization
- Dense vs. Hybrid retrieval paths
- Multi-namespace result fusion (RRF)
- Caching strategy layers
- Score evolution through ranking stages
- Configuration sensitivity analysis matrix
- Query type detection enhancement proposal
- Phased improvement roadmap

**Best for:** Visual learners, architecture presentations, understanding data flow, and quick reference.

---

### 3. SEARCH_QUICK_REFERENCE.md (Operational Guide)
**8.4KB | 377 lines | Quick Lookup Reference**

Fast-access reference guide containing:
- Key files at a glance (11 components mapped)
- Step-by-step search request flow
- Critical configuration parameters with defaults
- Quick tuning guide for 3 scenarios (recall, precision, speed)
- Scoring explanation across 4 stages
- Caching behavior specifications
- Common issues and solutions
- Design axioms (8 principles)
- Health check API endpoints
- Debugging guide with code examples
- Complete environment variable reference
- Performance benchmarks and metrics
- Next steps recommendations

**Best for:** Operational teams, troubleshooting, configuration tuning, and maintenance.

---

### 4. SEARCH_IMPLEMENTATION_SUMMARY.txt (Executive Summary)
**Text format | Structured overview | Key findings**

High-level executive summary providing:
- Current state assessment (production-ready)
- 10-stage search pipeline breakdown
- Strengths and quality metrics
- Improvement opportunities categorized by timeline
- Configuration tuning recommendations
- Key metrics and axioms
- Component mapping
- Scoring flow example
- Next actions roadmap
- File locations (absolute paths)

**Best for:** Project managers, decision makers, and getting quick overview of the entire system.

---

## Quick Navigation

### For Different Roles

**Software Engineers:**
1. Start with SEARCH_QUICK_REFERENCE.md (15 min)
2. Read SEARCH_RETRIEVAL_ANALYSIS.md sections 1-5 (30 min)
3. Review improvement recommendations (section 8)

**DevOps/Operations:**
1. Read SEARCH_QUICK_REFERENCE.md completely
2. Focus on sections: Configuration, Debugging, Health Checks
3. Reference SEARCH_ARCHITECTURE_DIAGRAM.md for troubleshooting

**Product Managers:**
1. Read SEARCH_IMPLEMENTATION_SUMMARY.txt
2. Review improvement opportunities section
3. Understand improvement roadmap (PHASE 1-3)

**Data Scientists:**
1. Read sections 1-4 of SEARCH_RETRIEVAL_ANALYSIS.md
2. Review ranking mechanisms (section 4)
3. Study improvement recommendations (section 8.3 for Learning-to-Rank)

---

## Key Findings Summary

### Current State: Production-Ready
- Well-architected 10-stage pipeline
- Explicit design axioms (8 principles) guide all decisions
- 80-90% latency reduction through intelligent caching
- Multi-namespace support with RRF fusion
- Graceful fallbacks and comprehensive validation

### Search Pipeline (10 Stages)
1. Authentication & Rate Limiting
2. Response Cache Check
3. Query Expansion (glossary)
4. Query Encoding (Ollama)
5. Vector Aggregation
6. Multi-Namespace Retrieval (FAISS)
7. Result Fusion (RRF)
8. URL Deduplication
9. Optional Reranking
10. Response Caching

### Quick Win Improvements (+15-20% relevance in 1-2 weeks)
- Enable hybrid search by default
- Activate cross-encoder reranking
- Implement basic query type detection

---

## Configuration at a Glance

```bash
# Default Values
RETRIEVAL_K=5                       # Results per query
HYBRID_ALPHA=0.6                    # Dense weight (0-1)
RESPONSE_CACHE_SIZE=1000            # LRU entries
RESPONSE_CACHE_TTL=3600             # Cache time (seconds)

# Quick Tuning Profiles
# For Recall:    RETRIEVAL_K=10, HYBRID_ALPHA=0.5
# For Precision: RETRIEVAL_K=3, HYBRID_ALPHA=0.7, ENABLE_RERANKING=true
# For Speed:     RETRIEVAL_K=3, RESPONSE_CACHE_SIZE=2000, ENABLE_RERANKING=false
```

---

## File Locations (Absolute Paths)

### Documentation
- `/Users/15x/Downloads/rag/SEARCH_RETRIEVAL_ANALYSIS.md`
- `/Users/15x/Downloads/rag/SEARCH_ARCHITECTURE_DIAGRAM.md`
- `/Users/15x/Downloads/rag/SEARCH_QUICK_REFERENCE.md`
- `/Users/15x/Downloads/rag/SEARCH_IMPLEMENTATION_SUMMARY.txt`

### Core Implementation
- `/Users/15x/Downloads/rag/src/server.py` (main API, lines 378-462)
- `/Users/15x/Downloads/rag/src/encode.py` (embeddings)
- `/Users/15x/Downloads/rag/src/embed.py` (FAISS indexing)
- `/Users/15x/Downloads/rag/src/ingest.py` (data ingestion)
- `/Users/15x/Downloads/rag/src/retrieval_hybrid.py` (hybrid search)
- `/Users/15x/Downloads/rag/src/rerank.py` (reranking)
- `/Users/15x/Downloads/rag/src/cache.py` (caching)
- `/Users/15x/Downloads/rag/src/query_expand.py` (query expansion)

---

## System Axioms (8 Principles)

| # | Axiom | Description |
|---|-------|-------------|
| 0 | Security | Tokens, rate limits, injection prevention |
| 1 | Deterministic | Reproducible results, seeded randomness |
| 2 | Grounded | Return URLs, chunk IDs, metadata |
| 3 | Normalized | L2-normalize all vectors consistently |
| 4 | Expanded | Query expansion via glossary synonyms |
| 5 | Graceful | Reranking optional, never blocks retrieval |
| 7 | Fast | Caching 80-90% latency reduction, p95<800ms |
| 9 | Offline | No external dependencies, local embeddings |

---

## Performance Benchmarks

### Typical Latencies
- Cache hit: 1-5ms (80-90% of requests)
- Cold query: 200-400ms (full pipeline)
- FAISS search: 5-20ms (k=12)
- Reranking: 50-100ms
- Ollama encoding: 100-150ms

### Complexity
- Index space: O(n) - linear with chunks
- Search: O(n*d) for flat indices
- Search: O(log n) for approximate indices (future)

---

## Improvement Timeline

**Phase 1 (1-2 weeks): Quick Wins (+15-20% relevance)**
- Enable hybrid search
- Activate reranking
- Query type detection

**Phase 2 (1 month): Medium-term (+25-35% relevance, 30% speed)**
- Learning-to-Rank
- Hierarchical chunking
- Redis caching
- Parallel retrieval

**Phase 3 (2+ months): Advanced (+40-50% relevance)**
- Approximate indices (HNSW/IVF)
- Feedback loops
- NER integration
- Personalization

---

## Common Operations

### Check Health
```bash
curl http://localhost:7000/health
curl http://localhost:7000/health?deep=1
```

### Test Search
```bash
curl -H "x-api-token: YOUR_TOKEN" \
  "http://localhost:7000/search?q=timesheet&k=5"
```

### Verify Embeddings
```python
from src.encode import encode_query
import numpy as np

vec = encode_query("test")
norm = np.linalg.norm(vec)
print(f"Norm: {norm:.6f}")  # Should be ~1.0
```

### Monitor Cache
```python
from src.cache import get_cache

cache = get_cache()
stats = cache.stats()
print(f"Hit rate: {stats['hit_rate_pct']}%")
```

---

## Recommendation

**Start here based on your role:**

- **First time?** Read SEARCH_QUICK_REFERENCE.md (15 min)
- **Need deep understanding?** Read SEARCH_RETRIEVAL_ANALYSIS.md (60 min)
- **Visual learner?** Study SEARCH_ARCHITECTURE_DIAGRAM.md (20 min)
- **Executive overview?** Read SEARCH_IMPLEMENTATION_SUMMARY.txt (10 min)

---

## Questions?

Refer to the appropriate document section:
- **"How does search work?"** → SEARCH_ARCHITECTURE_DIAGRAM.md
- **"How do I configure this?"** → SEARCH_QUICK_REFERENCE.md (Configuration section)
- **"How can we improve?"** → SEARCH_RETRIEVAL_ANALYSIS.md (Section 8+)
- **"What should we do next?"** → SEARCH_IMPLEMENTATION_SUMMARY.txt (Next Actions)

---

*Documentation generated: October 20, 2025*
*RAG System Version: Production-ready*
*Search Implementation Status: Excellent*
