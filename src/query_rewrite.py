"""Query expansion and rewriting using Clockify glossary."""
from __future__ import annotations
from typing import List
from src.ontologies.clockify_glossary import ALIASES, _norm


def expand(q: str, max_vars: int = 5) -> List[str]:
    """
    Expand query with controlled paraphrases based on glossary aliases.

    Examples:
        "How do I submit my timesheet?"
        → ["How do I submit my timesheet?", "How do I submit my timesheet? (timesheet)", ...]

        "What is billable rate?"
        → ["What is billable rate?", "What is bill rate?", ...]

    Args:
        q: Original query
        max_vars: Maximum variants to return

    Returns:
        List of query variants
    """
    ql = _norm(q)
    variants = [q]  # Start with original

    # Check if query mentions any glossary terms
    for canon, alts in ALIASES.items():
        # Check if any alias matches query
        hit = any(a in ql for a in alts + [canon])

        if hit:
            # Generate controlled paraphrases
            for alt in alts:
                if alt and alt not in ql:
                    # Add variant with term label
                    variants.append(q + f" ({canon})")
                    # Add variant with substitution
                    variant_sub = q
                    for a in alts:
                        if a in ql:
                            variant_sub = variant_sub.replace(a, canon)
                    if variant_sub != q:
                        variants.append(variant_sub)
                    break  # Only one expansion per canonical term

    # De-duplicate while preserving order, cap at max_vars
    seen = set()
    out = []
    for v in variants:
        if v not in seen:
            out.append(v)
            seen.add(v)
        if len(out) >= max_vars:
            break

    return out


def is_definitional(q: str) -> bool:
    """
    Detect if query is asking for a definition.

    Examples:
        "What is billable rate?" → True
        "How do I enable SSO?" → False
        "Define timesheet" → True
    """
    q_lower = q.lower()
    definitional_patterns = [
        "what is",
        "define",
        "meaning of",
        "glossary",
        "difference between",
        "what's",
        "what are",
    ]
    return any(pattern in q_lower for pattern in definitional_patterns)
