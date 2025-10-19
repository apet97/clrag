#!/usr/bin/env python3
"""Test LLM connection and basic functionality."""

import sys
import json
import time
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.llm.local_client import LocalLLMClient

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

# Test configurations
TESTS = [
    {
        "name": "Basic Connection",
        "system": "You are a helpful assistant.",
        "user": "Say 'Hello, I am working'",
        "expected_contains": ["hello", "working"],
    },
    {
        "name": "Math Question",
        "system": "You are a helpful math tutor.",
        "user": "What is 2+2?",
        "expected_contains": ["4"],
    },
    {
        "name": "Context with Timesheet",
        "system": "You are a Clockify support agent. Answer based only on the context provided.",
        "user": """Context: DCAA Compliant Timekeeping. Timesheets require manager approval.

Question: What is required for DCAA compliance?""",
        "expected_contains": ["timesheet", "manager", "approval"],
    },
]

def test_llm():
    """Run LLM connection tests."""
    print("\n" + "="*80)
    print("CLOCKIFY RAG - LLM CONNECTION TEST")
    print("="*80 + "\n")

    client = LocalLLMClient(
        base_url="http://localhost:8080/v1",
        model_name="oss20b"
    )

    results = {
        "timestamp": time.time(),
        "tests": [],
        "summary": {}
    }

    # Test connection first
    print("Checking LLM connection...")
    if not client.test_connection():
        print("\n❌ LLM is not responding. Make sure to start it:")
        print("   Ollama: ollama pull oss20b && ollama serve")
        print("   Or set MODEL_BASE_URL and start your LLM server")
        return results

    print("✅ LLM is responding\n")

    passed = 0
    failed = 0

    for i, test in enumerate(TESTS, 1):
        print(f"[Test {i}/{len(TESTS)}] {test['name']}")
        print(f"  System: {test['system'][:60]}...")
        print(f"  User:   {test['user'][:60]}...")

        start_time = time.time()
        response = client.generate(
            system_prompt=test["system"],
            user_prompt=test["user"],
            max_tokens=200,
            temperature=0.2,
        )
        latency = time.time() - start_time

        if response is None:
            print(f"  ❌ FAILED: No response from LLM")
            print(f"  Latency: {latency:.2f}s\n")
            results["tests"].append({
                "name": test["name"],
                "status": "failed",
                "latency_s": latency,
            })
            failed += 1
            continue

        # Check response quality
        response_lower = response.lower()
        expected_found = any(
            exp.lower() in response_lower for exp in test["expected_contains"]
        )

        if expected_found:
            print(f"  ✅ PASSED")
        else:
            print(f"  ⚠️  WARNING: Response doesn't contain expected content")
            print(f"     Expected one of: {test['expected_contains']}")

        print(f"  Response: {response[:100]}{'...' if len(response) > 100 else ''}")
        print(f"  Latency: {latency:.2f}s\n")

        results["tests"].append({
            "name": test["name"],
            "status": "passed" if expected_found else "passed_with_warning",
            "latency_s": latency,
            "response": response[:200],
        })

        if expected_found:
            passed += 1
        else:
            failed += 1

    # Summary
    print("="*80)
    print("LLM CONNECTION TEST SUMMARY")
    print("="*80)
    print(f"Tests Passed:         {passed}/{len(TESTS)} ✅")
    print(f"Tests Failed:         {failed}/{len(TESTS)} ❌")

    if results["tests"]:
        latencies = [t["latency_s"] for t in results["tests"]]
        print(f"Average Latency:      {sum(latencies)/len(latencies):.2f}s")
        print(f"Min Latency:          {min(latencies):.2f}s")
        print(f"Max Latency:          {max(latencies):.2f}s")

    results["summary"] = {
        "total_tests": len(TESTS),
        "passed": passed,
        "failed": failed,
        "success_rate": (passed / len(TESTS) * 100) if TESTS else 0,
    }

    # Save results
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    results_file = log_dir / "llm_connection_test.json"

    with open(results_file, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n✅ Results saved to {results_file}")

    return results

if __name__ == "__main__":
    results = test_llm()

    if results["summary"].get("success_rate", 0) >= 90:
        print("\n🎉 LLM connection test PASSED")
        exit(0)
    else:
        print("\n⚠️  LLM connection test needs attention")
        exit(1)
