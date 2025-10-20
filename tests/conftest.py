"""Pytest configuration and fixtures for RAG tests."""

import time
import pytest


@pytest.fixture(autouse=True)
def reset_rate_limiter_state():
    """Reset rate limiter state between tests to avoid 429 errors."""
    # Delay to ensure rate limiter window has passed (min_interval=0.1, so sleep a bit more)
    time.sleep(0.12)
    yield
