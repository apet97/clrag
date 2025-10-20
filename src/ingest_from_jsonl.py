#!/usr/bin/env python3
"""
Ingest RAG-ready JSONL into FAISS index with metadata.
Designed for production-scale indexing with proper chunking and deduplication.
"""

import json
import logging
import hashlib
import numpy as np
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from tqdm import tqdm
import os
from dotenv import load_dotenv

load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Configuration
JSONL_PATH = Path(os.getenv("JSONL_PATH", "clockify-help/clockify_help.jsonl"))
INDEX_DIR = Path(os.getenv("INDEX_DIR", "index/faiss/clockify-improved"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "32"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text:latest")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")

INDEX_DIR.mkdir(parents=True, exist_ok=True)


def get_embedding(text: str) -> Optional[np.ndarray]:
    """Get embedding from Ollama."""
    import httpx

    try:
        client = httpx.Client(timeout=60.0)
        response = client.post(
            f"{LLM_BASE_URL}/api/embed",
            json={
                "model": EMBEDDING_MODEL,
                "input": text,
            },
        )
        response.raise_for_status()
        data = response.json()
        embedding = np.array(data["embeddings"][0], dtype=np.float32)
        # L2 normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        return embedding
    except Exception as e:
        logger.error(f"Embedding error: {e}")
        return None


def load_jsonl_records(jsonl_path: Path) -> List[Dict]:
    """Load records from JSONL file."""
    records = []
    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    record = json.loads(line)
                    records.append(record)
    except Exception as e:
        logger.error(f"Error loading JSONL: {e}")
    logger.info(f"Loaded {len(records)} records from {jsonl_path}")
    return records


def deduplicate_records(records: List[Dict]) -> Tuple[List[Dict], int]:
    """Deduplicate records by content hash."""
    seen = set()
    unique = []
    dupes = 0

    for rec in records:
        content_hash = hashlib.sha256(
            (rec["url"] + "\n" + rec["content"]).encode()
        ).hexdigest()

        if content_hash not in seen:
            seen.add(content_hash)
            rec["_hash"] = content_hash
            unique.append(rec)
        else:
            dupes += 1

    logger.info(f"Deduplicated: {dupes} duplicates removed, {len(unique)} unique records")
    return unique, dupes


def embed_batch(texts: List[str]) -> List[Optional[np.ndarray]]:
    """Get embeddings for a batch of texts."""
    embeddings = []
    for text in texts:
        emb = get_embedding(text)
        embeddings.append(emb)
    return embeddings


def build_index(records: List[Dict]) -> Dict:
    """Build FAISS index from records."""
    import faiss

    logger.info(f"Building FAISS index from {len(records)} records...")

    embeddings_list = []
    metadata_list = []

    # Process in batches
    for i in tqdm(range(0, len(records), BATCH_SIZE), desc="Embedding"):
        batch_records = records[i : i + BATCH_SIZE]
        batch_texts = [rec["content"][:2000] for rec in batch_records]  # Truncate to 2K
        batch_embeddings = embed_batch(batch_texts)

        for j, emb in enumerate(batch_embeddings):
            if emb is not None:
                embeddings_list.append(emb)
                metadata_list.append(batch_records[j])

    if not embeddings_list:
        logger.error("No embeddings generated!")
        return {}

    # Convert to numpy array
    embeddings_array = np.stack(embeddings_list, axis=0)
    logger.info(f"Embedding shape: {embeddings_array.shape}")

    # Create FAISS index (inner product for L2-normalized vectors)
    dimension = embeddings_array.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings_array)

    logger.info(f"Index built with {index.ntotal} vectors, dimension {dimension}")

    # Save index
    index_path = INDEX_DIR / "index.bin"
    faiss.write_index(index, str(index_path))
    logger.info(f"✓ Index saved: {index_path}")

    # Save metadata
    metadata_path = INDEX_DIR / "meta.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, indent=2, ensure_ascii=False)
    logger.info(f"✓ Metadata saved: {metadata_path}")

    # Save stats
    stats = {
        "total_records": len(records),
        "indexed_records": len(metadata_list),
        "dimension": dimension,
        "model": EMBEDDING_MODEL,
        "created_at": int(__import__("time").time()),
    }

    stats_path = INDEX_DIR / "stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    logger.info(f"✓ Stats saved: {stats_path}")

    return stats


def main():
    """Main ingestion pipeline."""
    logger.info(f"Starting JSONL ingestion from {JSONL_PATH}")

    # Load records
    records = load_jsonl_records(JSONL_PATH)
    if not records:
        logger.error("No records loaded!")
        return

    # Deduplicate
    records, dupes = deduplicate_records(records)

    # Build index
    stats = build_index(records)

    logger.info("=" * 60)
    logger.info("INGESTION COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Records indexed: {stats.get('indexed_records', 0)}")
    logger.info(f"Vector dimension: {stats.get('dimension', 0)}")
    logger.info(f"Index directory: {INDEX_DIR}")


if __name__ == "__main__":
    main()
