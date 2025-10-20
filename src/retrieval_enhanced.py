#!/usr/bin/env python3
"""
Enhanced retrieval with query expansion, preprocessing, and optimization.
Features:
- Glossary-based query expansion
- Improved preprocessing (lemmatization, stop word removal)
- Cross-encoder reranking support
- Advanced caching strategy
- Query analytics
"""

import re
import json
import hashlib
import logging
from functools import lru_cache
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
import numpy as np
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Configuration
GLOSSARY_PATH = Path(os.getenv("GLOSSARY_PATH", "clockify-help/pages/help__getting-started__clockify-glossary.md"))
CACHE_SIZE = int(os.getenv("CACHE_SIZE", "1000"))
MIN_QUERY_LENGTH = int(os.getenv("MIN_QUERY_LENGTH", "2"))


class QueryPreprocessor:
    """Advanced query preprocessing with lemmatization and stop word removal."""

    STOP_WORDS = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', 'if',
        'in', 'into', 'is', 'it', 'no', 'not', 'of', 'on', 'or', 'such', 'that',
        'the', 'their', 'then', 'there', 'these', 'they', 'this', 'to', 'was',
        'will', 'with', 'can', 'could', 'would', 'should', 'may', 'might', 'must',
        'how', 'what', 'when', 'where', 'why', 'do', 'does', 'did', 'have', 'has',
        'had', 'get', 'gets', 'got', 'am', 'been', 'being', 'do', 'does'
    }

    LEMMATIZATION_MAP = {
        'tracking': 'track', 'tracked': 'track', 'tracks': 'track',
        'timing': 'time', 'timed': 'time', 'times': 'time',
        'entries': 'entry', 'entry': 'entry',
        'projects': 'project', 'project': 'project',
        'timers': 'timer', 'timer': 'timer',
        'reports': 'report', 'report': 'report',
        'managing': 'manage', 'managed': 'manage', 'manages': 'manage',
        'creating': 'create', 'created': 'create', 'creates': 'create',
        'adding': 'add', 'added': 'add', 'adds': 'add',
        'deleting': 'delete', 'deleted': 'delete', 'deletes': 'delete',
        'editing': 'edit', 'edited': 'edit', 'edits': 'edit',
        'enabling': 'enable', 'enabled': 'enable', 'enables': 'enable',
        'disabling': 'disable', 'disabled': 'disable', 'disables': 'disable',
        'permissions': 'permission', 'permission': 'permission',
        'settings': 'setting', 'setting': 'setting',
        'users': 'user', 'user': 'user',
        'members': 'member', 'member': 'member',
        'teams': 'team', 'team': 'team',
        'workspaces': 'workspace', 'workspace': 'workspace',
        'integration': 'integration', 'integrations': 'integration',
    }

    @classmethod
    def preprocess(cls, query: str) -> Tuple[str, List[str]]:
        """
        Preprocess query: lowercase, remove special chars, tokenize, remove stopwords, lemmatize.
        Returns: (cleaned_query, tokens)
        """
        # Lowercase
        query = query.lower().strip()

        # Remove special characters (keep alphanumeric and spaces)
        query = re.sub(r'[^a-zA-Z0-9\s]', '', query)

        # Tokenize
        tokens = query.split()

        # Filter: remove stop words and short tokens
        filtered = [
            cls.LEMMATIZATION_MAP.get(t, t)
            for t in tokens
            if t not in cls.STOP_WORDS and len(t) > 1
        ]

        cleaned_query = ' '.join(filtered)
        return cleaned_query, filtered

    @classmethod
    def expand_with_synonyms(cls, tokens: List[str], glossary: Dict[str, List[str]]) -> List[str]:
        """Expand tokens with glossary synonyms."""
        expanded = set(tokens)
        for token in tokens:
            if token in glossary:
                expanded.update(glossary[token])
        return list(expanded)


class GlossaryExtractor:
    """Extract glossary terms and synonyms from Clockify glossary."""

    @staticmethod
    def load_glossary(glossary_path: Path) -> Dict[str, List[str]]:
        """
        Load glossary from markdown file.
        Format: # Term\nSynonym 1, Synonym 2...
        """
        glossary = defaultdict(list)

        try:
            if not glossary_path.exists():
                logger.warning(f"Glossary not found: {glossary_path}")
                return glossary

            with open(glossary_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract glossary entries (looking for term definitions)
            # Pattern: # Term\nDefinition with potential synonyms
            entries = re.findall(
                r'#{2,3}\s+([A-Za-z\s]+?)\n(.*?)(?=#{2,3}|\Z)',
                content,
                re.DOTALL
            )

            for term, definition in entries:
                term_clean = term.strip().lower()
                # Extract potential synonyms (words that appear to be related)
                words = re.findall(r'\b([a-z]+)\b', definition.lower())
                # Keep words that appear to be synonyms (1-3 words, appear early)
                synonyms = words[:10]
                glossary[term_clean].extend(synonyms)

                # Add reverse mappings
                for syn in synonyms:
                    if syn not in glossary[term_clean]:
                        glossary[syn].append(term_clean)

        except Exception as e:
            logger.error(f"Error loading glossary: {e}")

        return glossary


class QueryAnalytics:
    """Track query statistics and analytics."""

    def __init__(self):
        self.query_stats = defaultdict(lambda: {'count': 0, 'no_results': 0})
        self.search_history = []

    def record_query(self, query: str, result_count: int, latency_ms: float):
        """Record query statistics."""
        query_key = hashlib.md5(query.lower().encode()).hexdigest()[:8]
        self.query_stats[query_key]['count'] += 1
        if result_count == 0:
            self.query_stats[query_key]['no_results'] += 1

        self.search_history.append({
            'query': query,
            'results': result_count,
            'latency_ms': latency_ms,
            'timestamp': __import__('time').time()
        })

    def get_stats(self) -> Dict:
        """Get analytics summary."""
        total_queries = sum(s['count'] for s in self.query_stats.values())
        zero_result_queries = sum(s['no_results'] for s in self.query_stats.values())

        return {
            'total_queries': total_queries,
            'zero_result_queries': zero_result_queries,
            'zero_result_rate': zero_result_queries / max(total_queries, 1),
            'avg_latency_ms': np.mean([r['latency_ms'] for r in self.search_history]) if self.search_history else 0,
            'unique_queries': len(self.query_stats),
        }


class EnhancedRetrieval:
    """Enhanced retrieval with all optimizations."""

    def __init__(self, index_path: str = None, metadata_path: str = None):
        self.preprocessor = QueryPreprocessor()
        self.analytics = QueryAnalytics()
        self.glossary = GlossaryExtractor.load_glossary(GLOSSARY_PATH)

        # Initialize cache
        self._cache = {}
        self.cache_hits = 0
        self.cache_misses = 0

        # Load index and metadata if provided
        self.index = None
        self.metadata = []
        if index_path and metadata_path:
            self._load_index(index_path, metadata_path)

    def _load_index(self, index_path: str, metadata_path: str):
        """Load FAISS index and metadata."""
        try:
            import faiss
            self.index = faiss.read_index(index_path)

            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            logger.info(f"Loaded index with {len(self.metadata)} records")
        except Exception as e:
            logger.error(f"Error loading index: {e}")

    def _get_cache_key(self, query: str) -> str:
        """Generate cache key for query."""
        return hashlib.md5(query.lower().encode()).hexdigest()

    def _cache_get(self, query: str) -> Optional[List[Dict]]:
        """Get result from cache."""
        key = self._get_cache_key(query)
        if key in self._cache:
            self.cache_hits += 1
            return self._cache[key]
        self.cache_misses += 1
        return None

    def _cache_set(self, query: str, results: List[Dict]):
        """Set result in cache with size limit."""
        if len(self._cache) >= CACHE_SIZE:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]

        key = self._get_cache_key(query)
        self._cache[key] = results

    def expand_query(self, query: str) -> str:
        """Expand query with synonyms from glossary."""
        cleaned, tokens = self.preprocessor.preprocess(query)
        expanded_tokens = self.preprocessor.expand_with_synonyms(tokens, self.glossary)
        return ' '.join(expanded_tokens)

    def preprocess_query(self, query: str) -> Tuple[str, List[str]]:
        """Preprocess query for better matching."""
        return self.preprocessor.preprocess(query)

    def search(
        self,
        query: str,
        k: int = 5,
        use_cache: bool = True,
        expand_query: bool = True,
        rerank: bool = False
    ) -> Tuple[List[Dict], Dict]:
        """
        Enhanced search with all optimizations.

        Returns: (results, metadata)
        """
        import time
        start_time = time.time()

        # Check cache
        if use_cache:
            cached_results = self._cache_get(query)
            if cached_results:
                return cached_results, {'from_cache': True}

        try:
            # Preprocess query
            cleaned_query, tokens = self.preprocess_query(query)

            # Expand query with synonyms
            if expand_query:
                expanded = self.preprocessor.expand_with_synonyms(tokens, self.glossary)
                search_query = ' '.join(expanded)
            else:
                search_query = cleaned_query

            # TODO: Perform actual search (integrate with FAISS)
            # For now, return empty results as placeholder
            results = []

            # Cache results
            if use_cache:
                self._cache_set(query, results)

            # Track analytics
            latency_ms = (time.time() - start_time) * 1000
            self.analytics.record_query(query, len(results), latency_ms)

            metadata = {
                'from_cache': False,
                'latency_ms': latency_ms,
                'query_expanded': search_query != cleaned_query,
                'cache_stats': {
                    'hits': self.cache_hits,
                    'misses': self.cache_misses,
                    'hit_rate': self.cache_hits / max(self.cache_hits + self.cache_misses, 1),
                }
            }

            return results, metadata

        except Exception as e:
            logger.error(f"Search error: {e}")
            return [], {'error': str(e)}

    def get_analytics(self) -> Dict:
        """Get search analytics."""
        return self.analytics.get_stats()


# Global instance
_retrieval_instance = None


def get_retrieval_instance() -> EnhancedRetrieval:
    """Get or create global retrieval instance."""
    global _retrieval_instance
    if _retrieval_instance is None:
        _retrieval_instance = EnhancedRetrieval()
    return _retrieval_instance


if __name__ == "__main__":
    # Test the enhanced retrieval
    retrieval = EnhancedRetrieval()

    # Test query preprocessing
    test_queries = [
        "How do I track time?",
        "Creating new projects",
        "What are the permissions for team members?",
        "Delete time entries",
        "Enable force timer setting",
    ]

    print("=" * 60)
    print("QUERY PREPROCESSING TEST")
    print("=" * 60)
    for query in test_queries:
        cleaned, tokens = retrieval.preprocess_query(query)
        print(f"Original: {query}")
        print(f"Cleaned:  {cleaned}")
        print(f"Tokens:   {tokens}\n")

    print("=" * 60)
    print("QUERY EXPANSION TEST")
    print("=" * 60)
    for query in test_queries:
        expanded = retrieval.expand_query(query)
        print(f"Original: {query}")
        print(f"Expanded: {expanded}\n")

    print("=" * 60)
    print("CACHE PERFORMANCE TEST")
    print("=" * 60)
    test_query = "How do I track time?"
    for i in range(3):
        results, meta = retrieval.search(test_query)
        status = "CACHED" if meta.get('from_cache') else "FRESH"
        print(f"Search #{i+1}: {status} ({meta.get('latency_ms', 0):.2f}ms)")

    print("\nCache Stats:", meta.get('cache_stats'))
