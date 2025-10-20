"""
RAG System Configuration with validated parameters.

Centralized configuration for all RAG components:
- Retrieval parameters (RRF fusion, oversampling)
- LLM generation (temperature, model)
- Performance tuning (cache sizes, timeouts)
- Security (token validation, rate limits)
"""

import os
import re
from dataclasses import dataclass
from typing import Optional
from loguru import logger


@dataclass
class RAGConfig:
    """Unified RAG configuration with validation."""

    # ===== RETRIEVAL =====
    # RRF (Reciprocal Rank Fusion) constant - higher = smoother scoring
    # From: S(d) = sum(1 / (k + rank_i(d))) where k is this constant
    RRF_CONSTANT: float = 60.0

    # Oversampling factors for pre-dedup retrieval
    # Retrieve k*factor docs before dedup to account for URL consolidation
    OVERSAMPLING_FACTOR_SMALL: int = 6  # For k <= 5
    OVERSAMPLING_FACTOR_LARGE: int = 3  # For k > 5

    # ===== LLM GENERATION =====
    TEMPERATURE_MIN: float = 0.0  # Deterministic
    TEMPERATURE_MAX: float = 2.0  # Maximum creativity
    TEMPERATURE_DEFAULT: float = 0.0  # Deterministic by default
    LLM_TIMEOUT_SECONDS: int = 30

    # ===== EMBEDDING =====
    EMBEDDING_TIMEOUT_SECONDS: int = 30
    EMBEDDING_CACHE_SIZE: int = 512  # LRU cache for encoded queries

    # ===== PERFORMANCE =====
    REQUEST_CACHE_MAX_SIZE: int = 1000  # Search response cache
    RATE_LIMIT_RPS: int = 10  # Per-IP requests per second
    RATE_LIMIT_WINDOW_SECONDS: int = 1

    # ===== SECURITY =====
    QUERY_MAX_LENGTH: int = 2000
    QUERY_MIN_LENGTH: int = 1
    NAMESPACE_MAX_LENGTH: int = 100
    K_MIN: int = 1
    K_MAX: int = 20
    K_DEFAULT: int = 5

    # ===== LOGGING =====
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")

    @staticmethod
    def validate_temperature(temp: float) -> float:
        """
        Validate and clamp temperature to valid range.

        Args:
            temp: Temperature value

        Returns:
            Clamped temperature value

        Raises:
            ValueError: If temperature is None or NaN
        """
        if temp is None:
            logger.warning("Temperature is None, using default")
            return RAGConfig.TEMPERATURE_DEFAULT

        try:
            temp_float = float(temp)
        except (ValueError, TypeError):
            logger.error(f"Invalid temperature type: {type(temp)}, using default")
            return RAGConfig.TEMPERATURE_DEFAULT

        if not (RAGConfig.TEMPERATURE_MIN <= temp_float <= RAGConfig.TEMPERATURE_MAX):
            logger.warning(
                f"Temperature {temp_float} out of range "
                f"[{RAGConfig.TEMPERATURE_MIN}, {RAGConfig.TEMPERATURE_MAX}], "
                f"clamping"
            )
            return max(RAGConfig.TEMPERATURE_MIN, min(temp_float, RAGConfig.TEMPERATURE_MAX))

        return temp_float

    @staticmethod
    def validate_k(k: Optional[int]) -> int:
        """
        Validate and clamp k to valid range.

        Args:
            k: Number of results to return

        Returns:
            Validated k value
        """
        if k is None:
            return RAGConfig.K_DEFAULT

        k_int = int(k)
        if not (RAGConfig.K_MIN <= k_int <= RAGConfig.K_MAX):
            logger.warning(
                f"k={k_int} out of range [{RAGConfig.K_MIN}, {RAGConfig.K_MAX}], "
                f"clamping"
            )
            return max(RAGConfig.K_MIN, min(k_int, RAGConfig.K_MAX))

        return k_int

    @staticmethod
    def validate_query(query: str) -> str:
        """
        Validate query text.

        Args:
            query: Query text to validate

        Returns:
            Validated query

        Raises:
            ValueError: If query is invalid
        """
        if not isinstance(query, str):
            raise ValueError(f"Query must be string, got {type(query)}")

        if len(query.strip()) < RAGConfig.QUERY_MIN_LENGTH:
            raise ValueError(f"Query too short (min {RAGConfig.QUERY_MIN_LENGTH} char)")

        if len(query) > RAGConfig.QUERY_MAX_LENGTH:
            raise ValueError(f"Query too long (max {RAGConfig.QUERY_MAX_LENGTH} chars)")

        # Block potential injection via regex escaping
        if re.search(r'[\\]', query):
            raise ValueError("Invalid characters in query (backslash not allowed)")

        return query

    @staticmethod
    def get_oversampling_factor(k: int) -> int:
        """
        Get oversampling factor based on k.

        Args:
            k: Number of final results requested

        Returns:
            Oversampling multiplier for pre-dedup retrieval
        """
        if k <= 5:
            return RAGConfig.OVERSAMPLING_FACTOR_SMALL
        else:
            return RAGConfig.OVERSAMPLING_FACTOR_LARGE


def redact_secrets(text: str) -> str:
    """
    Remove sensitive information from logs.

    Args:
        text: Text that may contain secrets

    Returns:
        Redacted text safe for logging
    """
    text = re.sub(r'Bearer\s+\S+', 'Bearer ***', text)
    text = re.sub(r'token["\']?\s*[=:]\s*["\']?\S+', 'token=***', text)
    text = re.sub(r'api[_-]?key["\']?\s*[=:]\s*["\']?\S+', 'api_key=***', text)
    text = re.sub(r'password["\']?\s*[=:]\s*["\']?\S+', 'password=***', text)
    return text


# Singleton instance
CONFIG = RAGConfig()
