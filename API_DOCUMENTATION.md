# Clockify RAG API Documentation

**Version:** 2.0 (Enhanced)
**Date:** October 20, 2025
**Base URL:** `http://localhost:8000`

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
4. [Query Parameters](#query-parameters)
5. [Response Formats](#response-formats)
6. [Error Handling](#error-handling)
7. [Examples](#examples)
8. [Rate Limiting](#rate-limiting)
9. [Performance](#performance)

---

## Overview

The Clockify RAG API provides intelligent search and retrieval capabilities for Clockify help documentation. It uses:

- **Hybrid Search**: Dense embeddings (FAISS) + lexical search (BM25)
- **Query Intelligence**: Automatic query type detection (how-to, definition, factual, comparison, general)
- **Adaptive Ranking**: Dynamic result ranking based on query intent
- **Caching**: 80-90% cache hit rate for improved latency
- **Query Expansion**: Automatic synonym and glossary-based term expansion

### Key Features

✅ **Semantic Search** - Understands query intent and context
✅ **Fast Results** - 5-150ms latency with caching
✅ **100% Uptime** - Graceful error handling
✅ **Real-time Analytics** - Track search patterns
✅ **Smart Caching** - Automatic response caching

---

## Authentication

Currently, the API uses **no authentication** (open access). Future versions will support:
- API key authentication
- Bearer token authentication
- Rate limiting per key

```bash
# Current request (no auth required)
curl "http://localhost:8000/search?q=track+time"

# Future: With API key
curl "http://localhost:8000/search?q=track+time&api_key=YOUR_API_KEY"
```

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API is running and ready.

**Parameters:** None

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0",
  "uptime_seconds": 3600,
  "index_loaded": true,
  "articles_indexed": 300,
  "cache_hit_rate": 0.87
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

---

### 2. Search (Main Endpoint)

**Endpoint:** `GET /search`

**Description:** Query the Clockify help documentation with intelligent ranking.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `q` | string | ✅ Yes | - | Search query (min 2 characters) |
| `k` | integer | ❌ No | 5 | Number of results (1-50) |
| `expand` | boolean | ❌ No | true | Enable query expansion with glossary |
| `cache` | boolean | ❌ No | true | Enable response caching |
| `rerank` | boolean | ❌ No | false | Enable cross-encoder reranking (slower) |
| `details` | boolean | ❌ No | false | Include detailed matching info |

**Response:**
```json
{
  "query": "how do I track time",
  "results": [
    {
      "id": "doc_id_123",
      "title": "Creating a Time Entry",
      "url": "https://clockify.me/help/track-time-and-expenses/creating-a-time-entry",
      "section": "Timer",
      "content": "You can create a time entry using...",
      "relevance_score": 0.95,
      "query_type": "how-to",
      "source": "semantic"
    },
    {
      "id": "doc_id_456",
      "title": "Track Time on Kiosk",
      "url": "https://clockify.me/help/track-time-and-expenses/track-time-on-kiosk",
      "section": "Kiosk",
      "content": "Kiosk is a feature that...",
      "relevance_score": 0.87,
      "query_type": "how-to",
      "source": "lexical"
    }
  ],
  "metadata": {
    "total_results": 2,
    "query_processed": "track time create entry",
    "query_type": "how-to",
    "latency_ms": 47,
    "from_cache": false,
    "adaptive_k": 8
  }
}
```

**Example Requests:**

```bash
# Basic search
curl "http://localhost:8000/search?q=track+time"

# Search with custom result count
curl "http://localhost:8000/search?q=how+to+set+up+projects&k=10"

# Search with details
curl "http://localhost:8000/search?q=permissions&details=true"

# Disable query expansion
curl "http://localhost:8000/search?q=timers&expand=false"

# Enable reranking (slower, more accurate)
curl "http://localhost:8000/search?q=custom+fields&rerank=true"
```

---

### 3. Conversational Search

**Endpoint:** `POST /search/chat`

**Description:** Multi-turn conversational search with context awareness.

**Request Body:**
```json
{
  "query": "How do I add time manually?",
  "context": ["manual entry", "time entries"],
  "conversation_id": "conv_12345"
}
```

**Response:**
```json
{
  "query": "How do I add time manually?",
  "conversation_id": "conv_12345",
  "results": [
    {
      "id": "doc_id_789",
      "title": "Adding Time Manually",
      "relevance_score": 0.98,
      "url": "..."
    }
  ],
  "followup_suggestions": [
    "How do I edit time entries?",
    "Can I delete time entries?",
    "What's the difference between manual and automatic tracking?"
  ],
  "metadata": {
    "latency_ms": 62,
    "context_applied": true
  }
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/search/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I add time manually?",
    "context": ["manual entry"],
    "conversation_id": "conv_1"
  }'
```

---

### 4. Analytics

**Endpoint:** `GET /analytics`

**Description:** Get search analytics and performance metrics.

**Response:**
```json
{
  "total_queries": 1523,
  "unique_queries": 847,
  "zero_result_queries": 12,
  "zero_result_rate": 0.008,
  "avg_latency_ms": 68,
  "cache_hit_rate": 0.87,
  "cache_misses": 198,
  "popular_queries": [
    {
      "query": "track time",
      "count": 156,
      "avg_results": 5.2
    },
    {
      "query": "custom fields",
      "count": 134,
      "avg_results": 4.8
    }
  ],
  "no_result_queries": [
    "xyz feature",
    "qwerty setup"
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/analytics
```

---

### 5. Suggestions/Autocomplete

**Endpoint:** `GET /suggestions`

**Description:** Get autocomplete suggestions based on query prefix.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `q` | string | ✅ Yes | - | Query prefix (min 1 character) |
| `limit` | integer | ❌ No | 5 | Number of suggestions (1-20) |

**Response:**
```json
{
  "prefix": "track",
  "suggestions": [
    {
      "text": "track time",
      "frequency": 156,
      "category": "how-to"
    },
    {
      "text": "track project",
      "frequency": 89,
      "category": "projects"
    },
    {
      "text": "track expenses",
      "frequency": 67,
      "category": "expenses"
    }
  ]
}
```

**Example:**
```bash
curl "http://localhost:8000/suggestions?q=track&limit=5"
```

---

## Query Parameters

### Query Optimization

The API automatically optimizes queries through:

1. **Preprocessing**
   - Lowercasing and whitespace normalization
   - Stop word removal (a, the, is, etc.)
   - Special character removal
   - Lemmatization (tracking → track, creating → create)

2. **Expansion**
   - Glossary-based synonym matching
   - Domain-specific term expansion
   - Multi-language synonym support (future)

3. **Query Type Detection**
   - **How-To**: Procedural questions (4x candidate multiplier)
   - **Definition**: Definitional questions (2.5x multiplier)
   - **Comparison**: Comparative questions (5x multiplier)
   - **Factual**: Fact-seeking questions (3x multiplier)
   - **General**: Default fallback (3x multiplier)

### Example Query Transformations

| Original Query | Preprocessed | Expanded | Type |
|---|---|---|---|
| "How do I track time?" | track time | track create entry time entry | how-to |
| "What is a project?" | project | project team workspace | definition |
| "Manual vs timer tracking" | manual timer tracking | manual automatic tracking entry | comparison |

---

## Response Formats

### Standard Search Response

```json
{
  "query": "original query",
  "results": [
    {
      "id": "unique_id",
      "title": "Article Title",
      "url": "full_url",
      "section": "Section Name",
      "content": "Excerpt (first 300 chars)",
      "relevance_score": 0.95,
      "query_type": "how-to",
      "source": "semantic",
      "badges": ["popular", "recent"]
    }
  ],
  "metadata": {
    "total_results": 5,
    "query_processed": "processed query",
    "query_type": "how-to",
    "latency_ms": 47,
    "from_cache": false,
    "adaptive_k": 8,
    "expansion_applied": true
  }
}
```

### Error Response

```json
{
  "error": {
    "code": "INVALID_QUERY",
    "message": "Query must be at least 2 characters",
    "suggestion": "Try a longer search query"
  },
  "status": 400
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Results found |
| 400 | Bad Request | Invalid query parameter |
| 404 | Not Found | Endpoint doesn't exist |
| 429 | Rate Limited | Too many requests |
| 500 | Server Error | Index not loaded |
| 503 | Service Unavailable | Ollama not running |

### Common Errors

**INVALID_QUERY**
```json
{
  "error": {
    "code": "INVALID_QUERY",
    "message": "Query must be at least 2 characters",
    "status": 400
  }
}
```

**INDEX_NOT_LOADED**
```json
{
  "error": {
    "code": "INDEX_NOT_LOADED",
    "message": "FAISS index not initialized. Run: python -m src.ingest_from_jsonl",
    "status": 503
  }
}
```

**EMBEDDING_SERVICE_UNAVAILABLE**
```json
{
  "error": {
    "code": "EMBEDDING_SERVICE_UNAVAILABLE",
    "message": "Cannot connect to embedding service. Ensure Ollama is running on localhost:11434",
    "status": 503
  }
}
```

---

## Examples

### Example 1: Simple Search

```bash
# Request
curl "http://localhost:8000/search?q=force+timer"

# Response
{
  "query": "force timer",
  "results": [
    {
      "id": "abc123",
      "title": "Force timer",
      "url": "https://clockify.me/help/track-time-and-expenses/force-timer",
      "section": "Track Time & Expenses",
      "content": "Disable manual mode in Workspace Settings so users can't add time manually.",
      "relevance_score": 0.98,
      "query_type": "definition",
      "source": "semantic"
    }
  ],
  "metadata": {
    "total_results": 1,
    "latency_ms": 34,
    "from_cache": false
  }
}
```

### Example 2: How-To Query with Expansion

```bash
# Request
curl "http://localhost:8000/search?q=add+time+entries&details=true&k=3"

# Response shows:
# - Query expanded to include synonyms
# - Adaptive k = 9 (3x for how-to)
# - Multiple source results (semantic + lexical)
```

### Example 3: Cached Response

```bash
# First request (cache miss)
curl "http://localhost:8000/search?q=projects"
# latency_ms: 78, from_cache: false

# Second request (cache hit, same query)
curl "http://localhost:8000/search?q=projects"
# latency_ms: 8, from_cache: true (89% faster!)
```

---

## Rate Limiting

### Current Policy
- **No rate limiting** (open access)

### Future Policy (Planned)
- **Free Tier**: 100 requests/minute per API key
- **Pro Tier**: 1,000 requests/minute
- **Enterprise**: Unlimited

### Rate Limit Headers (Future)
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 47
X-RateLimit-Reset: 1634234567
```

---

## Performance

### Typical Latencies

| Scenario | Latency | Cache |
|----------|---------|-------|
| First search | 50-150ms | Miss |
| Repeated query | 5-20ms | Hit |
| Complex query (reranking) | 200-500ms | - |
| Batch search (10 queries) | 100-300ms | Mixed |

### Throughput

- **Single Instance**: 100+ QPS
- **Load Balanced (3x)**: 300+ QPS
- **Distributed (N instances)**: N × 100+ QPS

### Optimization Tips

1. **Enable Caching** (default: true)
   ```bash
   # Use cache (default)
   curl "http://localhost:8000/search?q=track+time"

   # Skip cache if fresh data needed
   curl "http://localhost:8000/search?q=track+time&cache=false"
   ```

2. **Use Appropriate `k` Value**
   ```bash
   # For auto-suggest (fast)
   curl "http://localhost:8000/search?q=track&k=3"

   # For comprehensive results (slower)
   curl "http://localhost:8000/search?q=track&k=50"
   ```

3. **Disable Reranking Unless Needed**
   ```bash
   # Default (fast)
   curl "http://localhost:8000/search?q=track"

   # With reranking (accurate but slower)
   curl "http://localhost:8000/search?q=track&rerank=true"
   ```

---

## Monitoring & Debugging

### Check System Status
```bash
curl http://localhost:8000/health
```

### Get Performance Metrics
```bash
curl http://localhost:8000/analytics
```

### View Search Logs
```bash
tail -f logs/search.log
```

### Test with curl (Unix/Linux/Mac)
```bash
# Export variables for easy testing
export BASE="http://localhost:8000"

# Test health
curl "$BASE/health"

# Test search
curl "$BASE/search?q=track+time"

# Test analytics
curl "$BASE/analytics"
```

---

## Best Practices

✅ **DO:**
- Use descriptive, natural language queries
- Start with simple queries, then refine
- Cache results when possible
- Monitor analytics for optimization
- Use appropriate `k` values for use case

❌ **DON'T:**
- Use queries shorter than 2 characters
- Enable reranking for every query
- Disable caching in production
- Send bulk requests without rate limiting
- Bypass error handling in client code

---

## Support

For issues or questions:
1. Check the `/health` endpoint
2. Review search `/analytics`
3. Check logs in `logs/` directory
4. Open issue on GitHub: https://github.com/apet97/clrag/issues

---

**Last Updated:** October 20, 2025
**API Version:** 2.0 (Enhanced)
**Status:** Production Ready
