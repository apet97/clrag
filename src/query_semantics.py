"""
Advanced Query Processing: Semantic Expansion & Synonym Detection

This module implements:
1. Semantic query expansion using embeddings
2. Synonym/related term detection
3. Typo handling and spell correction
4. Multi-form query generation for better recall
"""

import os
from typing import List, Dict, Tuple, Set
from loguru import logger
import re
from functools import lru_cache

# Common synonyms and related terms for time tracking domain
DOMAIN_SYNONYMS = {
    "timer": ["stopwatch", "time tracker", "clock", "timing", "countdown"],
    "tracking": ["monitoring", "recording", "logging", "tracking time", "time recording"],
    "project": ["task", "job", "assignment", "work", "engagement"],
    "billable": ["chargeable", "invoiceable", "paid", "billable time", "billable hours"],
    "time entry": ["time log", "entry", "log", "time record", "activity record"],
    "client": ["customer", "account", "organization", "company"],
    "rate": ["hourly rate", "price", "cost", "billing rate", "rate per hour"],
    "report": ["reporting", "analytics", "analysis", "metrics", "dashboard"],
    "approval": ["approving", "approve", "authorization", "review", "sign-off"],
    "dashboard": ["interface", "UI", "screen", "view", "workspace"],
    "team": ["group", "department", "members", "staff", "colleagues"],
    "workspace": ["account", "organization", "workspace", "project space", "environment"],
}

# Typo patterns and corrections for common mistakes
TYPO_PATTERNS = {
    r"\btiem\b": "time",
    r"\btracking\b": "tracking",  # correctly spelled
    r"\btrak\b": "tracking",
    r"\bprojet\b": "project",
    r"\bptoject\b": "project",
    r"\bclient\b": "client",
    r"\bclinet\b": "client",
    r"\bapproval\b": "approval",
    r"\bapprove\b": "approve",
    r"\breport\b": "report",
    r"\breport\b": "report",
}

@lru_cache(maxsize=512)
def get_synonyms(term: str) -> List[str]:
    """
    Get synonyms for a term from domain knowledge base.

    Args:
        term: Query term to expand

    Returns:
        List of related terms and synonyms
    """
    term_lower = term.lower().strip()

    # Direct match
    if term_lower in DOMAIN_SYNONYMS:
        return DOMAIN_SYNONYMS[term_lower]

    # Partial match (e.g., "billing" could match "billable")
    for key, values in DOMAIN_SYNONYMS.items():
        if term_lower in key or key in term_lower:
            return values

    return []

def correct_typos(query: str) -> Tuple[str, bool]:
    """
    Attempt to correct common typos in query.

    Args:
        query: Original query

    Returns:
        Tuple of (corrected_query, was_corrected)
    """
    corrected = query
    was_corrected = False

    for pattern, replacement in TYPO_PATTERNS.items():
        if re.search(pattern, corrected, re.IGNORECASE):
            corrected = re.sub(pattern, replacement, corrected, flags=re.IGNORECASE)
            was_corrected = True
            logger.debug(f"Typo correction: '{query}' -> '{corrected}'")

    return corrected, was_corrected

def expand_query_with_synonyms(query: str, max_synonyms: int = 3) -> List[str]:
    """
    Expand query with synonyms and related terms.

    Args:
        query: Original query string
        max_synonyms: Maximum number of synonyms per term

    Returns:
        List of expanded query variations
    """
    terms = query.lower().split()
    expansions = [query]  # Keep original

    # For each term, try to find synonyms
    for term in terms:
        synonyms = get_synonyms(term)
        if synonyms:
            # Create variations by replacing term with synonyms
            for syn in synonyms[:max_synonyms]:
                expanded = query.replace(term, syn, 1)
                if expanded not in expansions:
                    expansions.append(expanded)

    return expansions[:5]  # Limit to 5 variations

def enhance_query_for_semantic_search(query: str, max_variations: int = 3) -> Dict[str, any]:
    """
    Comprehensive query enhancement combining typo correction and semantic expansion.

    Args:
        query: Original query
        max_variations: Max variations to generate

    Returns:
        Dict with original, corrected, and expanded queries
    """
    # Step 1: Correct typos
    corrected, was_corrected = correct_typos(query)

    # Step 2: Expand with synonyms
    base_query = corrected if was_corrected else query
    expansions = expand_query_with_synonyms(base_query, max_synonyms=2)

    # Step 3: Add ngrams and partial matches
    words = query.split()
    additional_forms = []

    # Add bigrams for multi-word concepts
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i+1]}"
        if len(bigram) > 5:  # Meaningful length
            additional_forms.append(bigram)

    all_variations = [corrected] + expansions + additional_forms
    all_variations = list(dict.fromkeys(all_variations))[:max_variations]  # Deduplicate

    return {
        "original": query,
        "corrected": corrected,
        "was_corrected": was_corrected,
        "base_query": base_query,
        "variations": all_variations,
        "primary_query": all_variations[0] if all_variations else query,
    }

def should_use_fuzzy_matching(query: str, typo_threshold: float = 0.3) -> bool:
    """
    Determine if query likely has typos and should use fuzzy matching.

    Args:
        query: Query to check
        typo_threshold: Confidence threshold for typo detection

    Returns:
        Boolean indicating if fuzzy matching should be used
    """
    corrected, was_corrected = correct_typos(query)

    if was_corrected:
        return True

    # Check for unusual character patterns
    if re.search(r'[^a-zA-Z0-9\s\-]', query):
        return True

    # Check for very short query (more likely typo)
    if len(query) < 4 and len(query.split()) == 1:
        return True

    return False

def get_query_variants_for_search(query: str) -> Dict[str, any]:
    """
    Get all variants of a query for comprehensive search coverage.
    Combines typo correction, synonyms, and fuzzy matching flags.

    Args:
        query: Input query

    Returns:
        Dict with different query variants and search parameters
    """
    enhanced = enhance_query_for_semantic_search(query)
    fuzzy = should_use_fuzzy_matching(query)

    return {
        "original_query": query,
        "primary_search_query": enhanced["primary_query"],
        "all_variations": enhanced["variations"],
        "should_use_fuzzy": fuzzy,
        "typo_detected": enhanced["was_corrected"],
        "original_unchanged": not enhanced["was_corrected"] and len(enhanced["variations"]) == 1,
        "synonyms_used": len(enhanced["variations"]) > 1,
    }

