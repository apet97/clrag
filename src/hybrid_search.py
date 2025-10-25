"""
Hybrid Search: Semantic + Keyword Matching

Combines vector similarity search with BM25 keyword matching
for superior recall and relevance.
"""

import math
from typing import List, Dict, Tuple
from loguru import logger
from collections import Counter

def compute_bm25_score(doc_tokens: List[str], query_tokens: List[str],
                       doc_length: int, avg_doc_length: float,
                       k1: float = 1.5, b: float = 0.75) -> float:
    """
    Compute BM25 score for a document given a query.

    BM25 is a probabilistic relevance framework used in information retrieval.
    It considers:
    - Term frequency in document
    - Inverse document frequency
    - Document length normalization

    Args:
        doc_tokens: Tokenized document
        query_tokens: Tokenized query
        doc_length: Length of document (word count)
        avg_doc_length: Average document length in corpus
        k1: Term frequency saturation parameter (default 1.5)
        b: Length normalization parameter (default 0.75)

    Returns:
        BM25 score
    """
    doc_freq = Counter(doc_tokens)
    score = 0.0

    # Estimate IDF (simplified - would normally use corpus-wide stats)
    idf = {}
    for token in query_tokens:
        # Simple IDF approximation
        idf[token] = math.log(1 + (doc_freq.get(token, 0) + 0.5) / (0.5 + 1))

    # Calculate BM25 for each query term
    for token in query_tokens:
        if token in doc_freq:
            freq = doc_freq[token]
            norm_length = 1 - b + b * (doc_length / (avg_doc_length + 1))
            bm25_component = idf[token] * (freq * (k1 + 1)) / (freq + k1 * norm_length)
            score += bm25_component

    return score

def keyword_match_score(text: str, query: str) -> float:
    """
    Simple keyword matching score.

    Rewards exact matches and phrase matches.

    Args:
        text: Text to match against (title + content)
        query: Query string

    Returns:
        Score between 0 and 1
    """
    text_lower = text.lower()
    query_lower = query.lower()

    # Exact phrase match (highest weight)
    if query_lower in text_lower:
        return 1.0

    # Word matches
    query_words = query_lower.split()
    text_words = set(text_lower.split())

    if not query_words:
        return 0.0

    match_ratio = len([w for w in query_words if w in text_words]) / len(query_words)
    return match_ratio

def entity_match_score(text: str, entities: List[str]) -> float:
    """
    Score based on presence of query entities in text.

    Args:
        text: Text to check
        entities: List of entities from query analysis

    Returns:
        Score between 0 and 1
    """
    if not entities:
        return 0.0

    text_lower = text.lower()
    matches = sum(1 for entity in entities if entity.lower() in text_lower)
    return min(1.0, matches / len(entities))

def hybrid_search_score(result: Dict, query: str, entities: List[str],
                       semantic_weight: float = 0.70,
                       keyword_weight: float = 0.30) -> Dict:
    """
    Compute hybrid score combining semantic and keyword matching.

    Args:
        result: Search result dict with 'semantic_score', 'title', 'content'
        query: Original query
        entities: Extracted entities from query
        semantic_weight: Weight for semantic similarity (0-1)
        keyword_weight: Weight for keyword matching (0-1)

    Returns:
        Updated result dict with hybrid_score added
    """
    # Get semantic score (already computed by FAISS)
    semantic = result.get('semantic_score', result.get('score', 0.0))

    # Compute keyword score
    combined_text = f"{result.get('title', '')} {result.get('content', '')}"
    keyword_score = keyword_match_score(combined_text, query)

    # Bonus for entity matches
    entity_score = entity_match_score(combined_text, entities)
    keyword_score = 0.7 * keyword_score + 0.3 * entity_score

    # Normalize scores to 0-1 range if needed
    semantic_normalized = min(1.0, max(0.0, semantic))
    keyword_normalized = min(1.0, max(0.0, keyword_score))

    # Combine scores
    hybrid_score = (semantic_weight * semantic_normalized +
                   keyword_weight * keyword_normalized)

    result['hybrid_score'] = hybrid_score
    result['semantic_score'] = semantic_normalized
    result['keyword_score'] = keyword_normalized
    result['entity_score'] = entity_score

    return result

def apply_diversity_penalty(results: List[Dict], diversity_weight: float = 0.15) -> List[Dict]:
    """
    Apply diversity penalty to avoid redundant results.

    Penalizes results that are very similar to already-selected results.

    Args:
        results: List of results (assumed sorted by relevance)
        diversity_weight: Weight for diversity penalty (0-1)

    Returns:
        Results with diversity_penalty and adjusted_score fields added
    """
    if not results:
        return results

    processed = []
    seen_content_hashes = set()

    for i, result in enumerate(results):
        # Create simple content hash for diversity
        content_hash = hash(result.get('content', '')[:100])

        # Calculate diversity score
        if content_hash in seen_content_hashes:
            # Penalize if similar content already in results
            diversity_penalty = diversity_weight
        else:
            diversity_penalty = 0.0
            seen_content_hashes.add(content_hash)

        # Apply penalty to score
        original_score = result.get('hybrid_score', result.get('score', 0.0))
        adjusted_score = original_score * (1 - diversity_penalty)

        result['diversity_penalty'] = diversity_penalty
        result['adjusted_score'] = adjusted_score

        processed.append(result)

    # Re-sort by adjusted score
    processed.sort(key=lambda x: x.get('adjusted_score', 0), reverse=True)

    return processed

def rank_hybrid_results(results: List[Dict], query: str, entities: List[str],
                       apply_diversity: bool = True) -> List[Dict]:
    """
    Complete hybrid ranking pipeline.

    Applies semantic scoring, keyword matching, entity matching, and diversity.

    Args:
        results: Initial search results
        query: Original query
        entities: Extracted query entities
        apply_diversity: Whether to apply diversity penalty

    Returns:
        Ranked results with hybrid scores
    """
    logger.debug(f"Hybrid ranking: {len(results)} results, {len(entities)} entities")

    # Apply hybrid scoring to each result
    scored_results = [
        hybrid_search_score(r, query, entities) for r in results
    ]

    # Sort by hybrid score
    scored_results.sort(key=lambda x: x.get('hybrid_score', 0), reverse=True)

    # Apply diversity penalty if requested
    if apply_diversity and len(scored_results) > 1:
        scored_results = apply_diversity_penalty(scored_results)

    return scored_results

def create_hybrid_result(result: Dict) -> Dict:
    """
    Format hybrid result for API response.

    Args:
        result: Internal result dict

    Returns:
        Formatted result with clean field names
    """
    return {
        'title': result.get('title', ''),
        'content': result.get('content', '')[:300],  # Truncate content
        'url': result.get('url', ''),
        'namespace': result.get('namespace', ''),
        'confidence': int(result.get('adjusted_score', result.get('hybrid_score', 0)) * 100),
        'level': 'high' if result.get('adjusted_score', 0) > 0.7 else 'medium' if result.get('adjusted_score', 0) > 0.4 else 'low',
        'emoji': '🟢' if result.get('adjusted_score', 0) > 0.7 else '🟡' if result.get('adjusted_score', 0) > 0.4 else '🔴',
        'factors': {
            'semantic_similarity': round(result.get('semantic_score', 0), 3),
            'keyword_match': round(result.get('keyword_score', 0), 3),
            'entity_alignment': round(result.get('entity_score', 0), 3),
            'diversity_bonus': round(1 - result.get('diversity_penalty', 0), 3),
        },
        'explanation': _generate_explanation(result),
    }

def _generate_explanation(result: Dict) -> str:
    """Generate human-readable explanation of ranking."""
    factors = []

    if result.get('semantic_score', 0) > 0.7:
        factors.append("strong semantic match")
    if result.get('keyword_score', 0) > 0.6:
        factors.append("keyword match")
    if result.get('entity_score', 0) > 0.5:
        factors.append("entity alignment")

    if factors:
        return f"Ranked high due to {', '.join(factors)}"
    return "Relevant result"

