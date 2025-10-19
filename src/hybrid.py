#!/usr/bin/env python3
"""BM25 full-text search indexes for hybrid retrieval."""

import json
import logging
from pathlib import Path
import os
from dotenv import load_dotenv

try:
    from whoosh.fields import Schema, TEXT, ID, NUMERIC
    from whoosh.index import create_in, open_dir
    from whoosh.qparser import QueryParser
except ImportError:
    logging.warning("whoosh not installed; hybrid search disabled")
    Schema = None

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

CHUNKS_DIR = Path("data/chunks")
INDEX_DIR = Path("index/faiss")


class BM25Builder:
    """Build whoosh BM25 indexes per namespace."""

    def __init__(self):
        if not Schema:
            raise ImportError("whoosh required for hybrid search")

        self.schema = Schema(
            id=ID(stored=True, unique=True),
            text=TEXT(stored=True),
            title=TEXT(stored=True),
            namespace=TEXT(stored=True),
            url=TEXT(stored=True),
            node_type=TEXT(stored=True),
            tokens=NUMERIC(stored=True),
        )

    def build_index_for_namespace(self, namespace: str) -> bool:
        """Build BM25 index for namespace."""
        chunks_file = CHUNKS_DIR / f"{namespace}.jsonl"

        if not chunks_file.exists():
            logger.warning(f"Chunks not found: {chunks_file}")
            return False

        chunks = []
        with open(chunks_file, "r") as f:
            for line in f:
                if line.strip():
                    chunks.append(json.loads(line))

        if not chunks:
            return False

        logger.info(f"Building BM25 index for {namespace}: {len(chunks)} chunks")

        # Create index directory
        index_path = INDEX_DIR / "hybrid" / namespace
        index_path.mkdir(parents=True, exist_ok=True)

        # Create writer
        ix = create_in(str(index_path), self.schema)
        writer = ix.writer()

        for chunk in chunks:
            writer.add_document(
                id=str(chunk["id"]),
                text=chunk["text"],
                title=chunk["title"],
                namespace=namespace,
                url=chunk["url"],
                node_type=chunk.get("node_type", "child"),
                tokens=chunk["tokens"],
            )

        writer.commit()
        logger.info(f"✓ BM25 index built for {namespace}")
        return True


async def main():
    """Build BM25 indexes for all namespaces."""
    builder = BM25Builder()

    for chunks_file in CHUNKS_DIR.glob("*.jsonl"):
        namespace = chunks_file.stem
        if not namespace.startswith("."):
            builder.build_index_for_namespace(namespace)

    logger.info("✓ BM25 indexing complete!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
