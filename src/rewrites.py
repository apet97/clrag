#!/usr/bin/env python3
"""Query rewriting for advanced retrieval (MultiQuery, HyDE)."""

import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

REWRITE_COUNT = int(os.getenv("REWRITE_COUNT", "3"))
REWRITE_METHODS = os.getenv("REWRITE_METHODS", "multiquery,hyde").split(",")


class QueryRewriter:
    """Generate diverse query rewrites."""

    @staticmethod
    def multiquery_rewrite(query: str) -> list[str]:
        """Generate 3 diverse rewrites of the query."""
        rewrites = [query]

        # Heuristic rewrites (no LLM needed)
        if "?" not in query:
            rewrites.append(f"What is {query.lower()}?")

        # Synonyms and variations
        if "create" in query.lower():
            rewrites.append(query.replace("create", "set up").lower())
        if "how" in query.lower():
            rewrites.append("Tips for " + query.replace("how to ", "").lower())

        return rewrites[:REWRITE_COUNT]

    @staticmethod
    def hyde_prompt_generate(query: str) -> str:
        """Generate hypothetical ideal answer for HyDE."""
        return f"A well-written document that would answer the question '{query}'."

    @staticmethod
    def rewrite(query: str) -> list[str]:
        """Generate rewrites using enabled methods."""
        rewrites = [query]

        if "multiquery" in REWRITE_METHODS:
            rewrites.extend(QueryRewriter.multiquery_rewrite(query))

        # Remove duplicates
        rewrites = list(dict.fromkeys(rewrites))[:REWRITE_COUNT]
        return rewrites
