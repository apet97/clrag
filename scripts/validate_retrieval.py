#!/usr/bin/env python3
"""Validate FAISS retrieval quality with realistic support queries."""

import json
import requests
import time
from pathlib import Path
from datetime import datetime

# Logging setup
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Test queries covering common support scenarios
TEST_QUERIES = [
    # Time Tracking
    ("How do I start tracking time?", "clockify"),
    ("What's the difference between timer and manual time entry?", "clockify"),
    ("Can I track time retroactively?", "clockify"),

    # Projects & Tasks
    ("How do I create a new project?", "clockify"),
    ("How do I delete a project?", "clockify"),
    ("Can I organize projects by client?", "clockify"),

    # Reports & Exports
    ("How do I generate a timesheet report?", "clockify"),
    ("How do I export my data to Excel?", "clockify"),
    ("Can I view reports by team member?", "clockify"),

    # Approvals & Workflows
    ("What are timesheet approvals?", "clockify"),
    ("How do I approve timesheets as a manager?", "clockify"),
    ("Can I set up approval workflows?", "clockify"),

    # Integrations
    ("What integrations does Clockify support?", "clockify"),
    ("Can Clockify integrate with Jira?", "clockify"),
    ("How do I sync with my calendar?", "clockify"),

    # Settings & Configuration
    ("How do I set my hourly rate?", "clockify"),
    ("What are tags and how do I use them?", "clockify"),
    ("Can I customize the time format?", "clockify"),

    # Mobile & Apps
    ("Can I track time on mobile?", "clockify"),
    ("Is there a Clockify desktop app?", "clockify"),
]

def validate_retrieval():
    """Run retrieval validation tests."""
    print("\n" + "="*80)
    print("CLOCKIFY RAG - RETRIEVAL VALIDATION")
    print("="*80 + "\n")

    results = {
        "timestamp": datetime.now().isoformat(),
        "queries_tested": len(TEST_QUERIES),
        "queries": [],
        "summary": {}
    }

    scores = []
    failed_queries = []
    successful_queries = 0

    for i, (query, namespace) in enumerate(TEST_QUERIES, 1):
        try:
            print(f"[{i:2d}/{len(TEST_QUERIES)}] Query: {query[:60]}...")

            # Call FAISS endpoint
            url = "http://localhost:8888/search"
            params = {"q": query, "namespace": namespace, "k": 5}

            start_time = time.time()
            response = requests.get(url, params=params, timeout=10)
            latency = time.time() - start_time

            if response.status_code != 200:
                print(f"  ❌ FAILED: HTTP {response.status_code}")
                failed_queries.append(query)
                continue

            data = response.json()
            result_count = data.get("count", 0)

            if result_count == 0:
                print(f"  ⚠️  No results returned")
                results["queries"].append({
                    "query": query,
                    "namespace": namespace,
                    "result_count": 0,
                    "top_scores": [],
                    "latency_ms": latency * 1000,
                    "status": "no_results"
                })
                failed_queries.append(query)
                continue

            # Extract top 3 results
            top_results = data.get("results", [])[:3]
            titles = [r.get("title", "Untitled") for r in top_results]
            scores_list = [r.get("vector_score", 0) for r in top_results]
            avg_score = sum(scores_list) / len(scores_list) if scores_list else 0

            scores.append(avg_score)
            successful_queries += 1

            # Print results
            print(f"  ✅ Found {result_count} results (avg score: {avg_score:.3f})")
            for j, (title, score) in enumerate(zip(titles, scores_list), 1):
                print(f"     {j}. {title[:70]} (score: {score:.3f})")
            print(f"     Latency: {latency*1000:.0f}ms\n")

            results["queries"].append({
                "query": query,
                "namespace": namespace,
                "result_count": result_count,
                "top_titles": titles,
                "top_scores": scores_list,
                "latency_ms": latency * 1000,
                "status": "success"
            })

        except requests.exceptions.ConnectionError:
            print(f"  ❌ FAILED: Cannot connect to localhost:8888")
            print(f"     Make sure the server is running: make serve\n")
            failed_queries.append(query)
            break
        except Exception as e:
            print(f"  ❌ FAILED: {str(e)}\n")
            failed_queries.append(query)

    # Calculate summary statistics
    results["summary"] = {
        "total_queries": len(TEST_QUERIES),
        "successful_queries": successful_queries,
        "failed_queries": len(failed_queries),
        "success_rate": (successful_queries / len(TEST_QUERIES) * 100) if TEST_QUERIES else 0,
        "average_score": sum(scores) / len(scores) if scores else 0,
        "queries_above_0_7": sum(1 for s in scores if s > 0.7),
        "queries_above_0_8": sum(1 for s in scores if s > 0.8),
        "min_score": min(scores) if scores else None,
        "max_score": max(scores) if scores else None,
    }

    # Print summary
    print("="*80)
    print("RETRIEVAL VALIDATION SUMMARY")
    print("="*80)
    print(f"Total Queries Tested:    {results['summary']['total_queries']}")
    print(f"Successful:              {results['summary']['successful_queries']} ✅")
    print(f"Failed:                  {results['summary']['failed_queries']} ❌")
    print(f"Success Rate:            {results['summary']['success_rate']:.1f}%")
    print(f"\nRelevance Scores:")
    print(f"  Average:               {results['summary']['average_score']:.3f}")
    print(f"  Min:                   {results['summary']['min_score']:.3f}")
    print(f"  Max:                   {results['summary']['max_score']:.3f}")
    print(f"  Queries > 0.7:         {results['summary']['queries_above_0_7']} 🎯")
    print(f"  Queries > 0.8:         {results['summary']['queries_above_0_8']} 🏆")

    if failed_queries:
        print(f"\nFailed Queries:")
        for query in failed_queries:
            print(f"  • {query}")

    # Save results
    results_file = LOG_DIR / "retrieval_test_results.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results saved to {results_file}")

    return results

if __name__ == "__main__":
    results = validate_retrieval()

    # Exit with appropriate code
    if results["summary"]["success_rate"] >= 90:
        print("\n🎉 Retrieval validation PASSED")
        exit(0)
    else:
        print("\n⚠️  Retrieval validation needs attention")
        exit(1)
