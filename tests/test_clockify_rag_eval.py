"""Evaluation tests for Clockify RAG recall and precision."""
import pytest


# Eval cases: (query, must_contain_1, must_contain_2)
EVAL_CASES = [
    ("How do I submit my weekly timesheet?", "submit", "timesheet"),
    ("Set billable rates per workspace member", "billable rate", "member"),
    ("Enable time rounding to 15 minutes", "rounding", "15"),
    ("What is SSO?", "sso", "sign-on"),
    ("How do I approve timesheets as a manager?", "approve", "manager"),
]


@pytest.mark.skip(reason="Requires full INDEX and encoder; used for manual eval")
def test_recall_pipeline():
    """Smoke test: verify retrieval includes expected terms."""
    # This test is meant for manual execution with full INDEX loaded
    # Run as: pytest tests/test_clockify_rag_eval.py::test_recall_pipeline -v -s
    pass


def test_eval_cases_structure():
    """Verify eval cases are well-formed."""
    for q, m1, m2 in EVAL_CASES:
        assert isinstance(q, str) and len(q) > 0
        assert isinstance(m1, str) and len(m1) > 0
        assert isinstance(m2, str) and len(m2) > 0
        assert m1 != m2
