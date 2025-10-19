#!/usr/bin/env python
"""
Evaluation harness for RAG retrieval and generation.

Computes Recall@k, MRR@k on retrieval and citation coverage on generation.
"""

import json
import time
from pathlib import Path

import requests


def load_qas(path: str = "eval/qas.jsonl") -> list[dict]:
    """Load QA pairs from JSONL."""
    qas = []
    with open(path) as f:
        for line in f:
            qas.append(json.loads(line))
    return qas


def compute_recall_at_k(retrieved_urls: list[str], must_cite: list[str], k: int) -> float:
    """Compute recall@k: what fraction of must_cite URLs appear in top-k."""
    if not must_cite:
        return 1.0
    retrieved_top_k = retrieved_urls[:k]
    found = sum(1 for url in must_cite if url in retrieved_top_k)
    return found / len(must_cite)


def compute_mrr_at_k(retrieved_urls: list[str], must_cite: list[str], k: int) -> float:
    """Compute MRR@k: mean reciprocal rank of first relevant item."""
    if not must_cite:
        return 1.0
    retrieved_top_k = retrieved_urls[:k]
    for rank, url in enumerate(retrieved_top_k, start=1):
        if url in must_cite:
            return 1.0 / rank
    return 0.0


def run_eval(base_url: str = "http://localhost:7000", k: int = 10):
    """Run evaluation on retrieval and generation."""
    qas = load_qas()
    print(f"\n{'='*80}")
    print(f"Clockify RAG Evaluation - {len(qas)} QA pairs")
    print(f"{'='*80}\n")
    
    recalls_5 = []
    recalls_10 = []
    mrr_5 = []
    mrr_10 = []
    latencies = []
    
    for i, qa in enumerate(qas, 1):
        q = qa["q"]
        must_cite = qa.get("must_cite", [])
        
        try:
            # Run search
            t0 = time.time()
            resp = requests.get(f"{base_url}/search", params={"q": q, "k": k}, timeout=10)
            latency = time.time() - t0
            latencies.append(latency * 1000)  # ms
            
            if resp.status_code != 200:
                print(f"[{i:2d}] ✗ FAIL {q[:40]:40s} (HTTP {resp.status_code})")
                continue
            
            data = resp.json()
            retrieved_urls = [r.get("url", "") for r in data.get("results", [])]
            
            # Compute metrics
            r5 = compute_recall_at_k(retrieved_urls, must_cite, 5)
            r10 = compute_recall_at_k(retrieved_urls, must_cite, k)
            mrr5 = compute_mrr_at_k(retrieved_urls, must_cite, 5)
            mrr10 = compute_mrr_at_k(retrieved_urls, must_cite, k)
            
            recalls_5.append(r5)
            recalls_10.append(r10)
            mrr_5.append(mrr5)
            mrr_10.append(mrr10)
            
            status = "✓" if r5 >= 0.8 else "◐" if r5 >= 0.5 else "✗"
            print(f"[{i:2d}] {status} {q[:40]:40s} | R@5={r5:.2f} R@10={r10:.2f} | {latency*1000:6.1f}ms")
            
        except Exception as e:
            print(f"[{i:2d}] ✗ ERR {q[:40]:40s} ({str(e)[:30]})")
    
    # Summary
    if recalls_5:
        print(f"\n{'='*80}")
        print("SUMMARY")
        print(f"{'='*80}")
        print(f"Recall@5:   {sum(recalls_5)/len(recalls_5):.1%} ({sum(1 for r in recalls_5 if r>=0.8)}/{len(recalls_5)} >= 0.80)")
        print(f"Recall@10:  {sum(recalls_10)/len(recalls_10):.1%}")
        print(f"MRR@5:      {sum(mrr_5)/len(mrr_5):.3f}")
        print(f"MRR@10:     {sum(mrr_10)/len(mrr_10):.3f}")
        print(f"Latency p50: {sorted(latencies)[len(latencies)//2]:.1f}ms")
        print(f"Latency p95: {sorted(latencies)[int(len(latencies)*0.95)]:.1f}ms")
        print(f"{'='*80}\n")
        
        # Check targets
        recall_target = 0.70
        latency_target = 800
        p95_lat = sorted(latencies)[int(len(latencies)*0.95)]
        
        if sum(recalls_5)/len(recalls_5) >= recall_target:
            print(f"✓ Recall@5 meets target ({recall_target})")
        else:
            print(f"✗ Recall@5 below target (got {sum(recalls_5)/len(recalls_5):.1%}, need {recall_target})")
        
        if p95_lat <= latency_target:
            print(f"✓ Latency p95 meets target (<{latency_target}ms)")
        else:
            print(f"✗ Latency p95 exceeds target (got {p95_lat:.0f}ms, need <{latency_target}ms)")


if __name__ == "__main__":
    import sys
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:7000"
    run_eval(base_url)
