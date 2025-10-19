"""
Query expansion using domain glossary.

Expands queries with synonyms to improve recall during retrieval.
"""

import json
from pathlib import Path

from loguru import logger

_glossary = None


def _load_glossary() -> dict:
    """Load glossary from data/domain/glossary.json."""
    global _glossary
    if _glossary is None:
        path = Path("data/domain/glossary.json")
        if path.exists():
            try:
                _glossary = json.loads(path.read_text(encoding="utf-8"))
                logger.info(f"Loaded glossary with {len(_glossary)} terms")
            except Exception as e:
                logger.warning(f"Failed to load glossary: {e}")
                _glossary = {}
        else:
            logger.debug("No glossary found at data/domain/glossary.json")
            _glossary = {}
    return _glossary


def expand(q: str, max_expansions: int = 8) -> list[str]:
    """
    Expand query with synonyms from glossary.

    Args:
        q: Original query
        max_expansions: Maximum number of expansions to add

    Returns:
        List of queries: [original, synonym1, synonym2, ...]
    """
    glossary = _load_glossary()
    q_lower = q.lower()
    
    expansions = []
    for term, synonyms in glossary.items():
        if term in q_lower:
            for syn in synonyms:
                syn = syn.strip()
                if syn and syn not in expansions and syn != term:
                    expansions.append(syn)
                if len(expansions) >= max_expansions:
                    break
        if len(expansions) >= max_expansions:
            break
    
    # Return original + unique expansions
    result = [q] + expansions[:max_expansions]
    return result


if __name__ == "__main__":
    print("Testing query expansion...")
    queries = ["timesheet", "kiosk", "project budget", "what is sso"]
    for q in queries:
        expanded = expand(q)
        print(f"  '{q}' -> {expanded}")
