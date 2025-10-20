#!/usr/bin/env python3
"""
Surgical ingestion pipeline for Clockify Help (clockify.me/help only).
Allowlist: https://clockify.me/help/* only. Deny everything else.
Uses local Ollama embeddings. Builds FAISS index. Deterministic + normalized.
"""

import os
import json
import re
import hashlib
from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup
import numpy as np
import faiss
import requests
from loguru import logger

# Config
HELP_DIR = Path(os.getenv("HELP_DIR", "data/clockify_help"))
OLLAMA_BASE_URL = os.getenv("LLM_BASE_URL", "http://10.127.0.192:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text:latest")
NAMESPACE = "clockify-help"
INDEX_ROOT = Path("index/faiss") / NAMESPACE
CHUNK_TARGET_TOKENS = int(os.getenv("CHUNK_TARGET_TOKENS", "512"))
CHUNK_OVERLAP_TOKENS = int(os.getenv("CHUNK_OVERLAP_TOKENS", "64"))
ALLOWLIST_PREFIX = "https://clockify.me/help/"

logger.info(f"Ingestion config: HELP_DIR={HELP_DIR}, OLLAMA={OLLAMA_BASE_URL}, MODEL={EMBEDDING_MODEL}")
logger.info(f"Allowlist: {ALLOWLIST_PREFIX}*")


def extract_url_from_file(file_path: Path) -> Optional[str]:
    """
    Extract canonical URL from HTML/MD file.
    Priority: <link rel="canonical"> → <base href> → derive from filename.
    """
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(content, "html.parser")

        # Try canonical
        canonical = soup.find("link", rel="canonical")
        if canonical and canonical.get("href"):
            return canonical.get("href")

        # Try base href
        base = soup.find("base", href=True)
        if base:
            return base.get("href")

        # Derive from filename: "some-page.html" → "https://clockify.me/help/some-page"
        slug = file_path.stem
        derived_url = f"{ALLOWLIST_PREFIX}{slug}"
        return derived_url

    except Exception as e:
        logger.warning(f"Could not extract URL from {file_path}: {e}")
        return None


def validate_url(url: str) -> bool:
    """Enforce allowlist: only https://clockify.me/help/* URLs."""
    return url.startswith(ALLOWLIST_PREFIX)


def extract_title_and_body(file_path: Path) -> tuple[str, str]:
    """Parse HTML/MD: extract title + clean body text."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(content, "html.parser")

        # Extract title
        title = "Unknown"
        if soup.title:
            title = soup.title.string or "Unknown"
        elif soup.find("h1"):
            title = soup.find("h1").get_text(strip=True) or "Unknown"

        # Extract body: remove script, style, nav, footer
        for tag in soup.find_all(["script", "style", "nav", "footer"]):
            tag.decompose()

        # Get main content or body
        main = soup.find("main") or soup.find("article") or soup.find("body")
        if main:
            body = main.get_text(separator="\n", strip=True)
        else:
            body = soup.get_text(separator="\n", strip=True)

        # Clean whitespace
        body = re.sub(r"\n\n+", "\n", body).strip()
        return title, body

    except Exception as e:
        logger.error(f"Could not parse {file_path}: {e}")
        return "Unknown", ""


def chunk_text(text: str, target_tokens: int = 512, overlap_tokens: int = 64) -> list[str]:
    """Split text into chunks. Rough tokenization: ~1 token per 4 chars."""
    if not text:
        return []

    chars_per_token = 4  # Rough estimate
    target_chars = target_tokens * chars_per_token
    overlap_chars = overlap_tokens * chars_per_token

    chunks = []
    pos = 0
    while pos < len(text):
        chunk = text[pos : pos + target_chars]
        chunks.append(chunk)
        pos += target_chars - overlap_chars

    return [c.strip() for c in chunks if c.strip()]


def embed_text(text: str, model: str) -> Optional[np.ndarray]:
    """Call Ollama /api/embeddings endpoint."""
    try:
        url = f"{OLLAMA_BASE_URL}/api/embeddings"
        payload = {"model": model, "prompt": text.strip()}
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            embedding = np.array(data.get("embedding"), dtype=np.float32)
            # L2 normalize
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
            return embedding
        else:
            logger.error(f"Ollama /api/embeddings failed: {resp.status_code} {resp.text[:200]}")
            return None
    except Exception as e:
        logger.error(f"Embedding request failed: {e}")
        return None


def ingest(help_dir: Path) -> int:
    """Main ingestion: walk HELP_DIR, extract, chunk, embed, index."""

    if not help_dir.exists():
        logger.error(f"HELP_DIR does not exist: {help_dir}")
        return 1

    logger.info(f"Scanning {help_dir} for .html, .htm, .md files...")

    # Collect all chunks
    all_chunks = []
    url_set = set()
    title_set = set()

    for file_path in sorted(help_dir.rglob("*")):
        if file_path.suffix.lower() not in [".html", ".htm", ".md"]:
            continue

        # Extract and validate URL
        url = extract_url_from_file(file_path)
        if not url or not validate_url(url):
            logger.warning(f"Skipped {file_path.name}: invalid or non-allowlisted URL: {url}")
            continue

        url_set.add(url)

        # Parse title + body
        title, body = extract_title_and_body(file_path)
        title_set.add(title)

        if not body:
            logger.warning(f"Skipped {file_path.name}: empty body")
            continue

        # Chunk
        chunks = chunk_text(body, CHUNK_TARGET_TOKENS, CHUNK_OVERLAP_TOKENS)
        logger.info(f"  {file_path.name} → {len(chunks)} chunks")

        for i, chunk_text_str in enumerate(chunks):
            chunk_id = hashlib.md5(f"{url}#{i}".encode()).hexdigest()
            all_chunks.append({
                "chunk_id": chunk_id,
                "url": url,
                "title": title,
                "text": chunk_text_str,
                "index": i,
            })

    logger.info(f"\n✓ Total unique URLs: {len(url_set)}")
    logger.info(f"✓ Total unique titles: {len(title_set)}")
    logger.info(f"✓ Total chunks: {len(all_chunks)}")

    # Sample URLs
    logger.info("\nSample URLs (first 10):")
    for url in sorted(url_set)[:10]:
        logger.info(f"  {url}")

    if not all_chunks:
        logger.error("No chunks to index. Exiting.")
        return 1

    # Embed all chunks
    logger.info(f"\nEmbedding {len(all_chunks)} chunks via Ollama {EMBEDDING_MODEL}...")
    embeddings = []
    for i, chunk in enumerate(all_chunks):
        if i % 10 == 0:
            logger.info(f"  {i}/{len(all_chunks)}...")
        embedding = embed_text(chunk["text"], EMBEDDING_MODEL)
        if embedding is None:
            logger.error(f"Failed to embed chunk {i}. Exiting.")
            return 1
        embeddings.append(embedding)

    embeddings_array = np.array(embeddings, dtype=np.float32)
    logger.info(f"✓ Embeddings shape: {embeddings_array.shape}")

    # Build FAISS index
    logger.info("\nBuilding FAISS IndexFlatIP...")
    dim = embeddings_array.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings_array)
    logger.info(f"✓ Index built: {index.ntotal} vectors, dim={dim}")

    # Write index and metadata
    INDEX_ROOT.mkdir(parents=True, exist_ok=True)

    index_path = INDEX_ROOT / "index.faiss"
    faiss.write_index(index, str(index_path))
    logger.info(f"✓ Index written: {index_path}")

    meta_data = {
        "model": EMBEDDING_MODEL,
        "dimension": int(dim),
        "dim": int(dim),
        "num_vectors": index.ntotal,
        "normalized": True,
        "chunks": [
            {
                "id": i,
                "chunk_id": chunk["chunk_id"],
                "url": chunk["url"],
                "title": chunk["title"],
                "index": chunk["index"],
            }
            for i, chunk in enumerate(all_chunks)
        ],
    }

    meta_path = INDEX_ROOT / "meta.json"
    with open(meta_path, "w") as f:
        json.dump(meta_data, f, indent=2)
    logger.info(f"✓ Metadata written: {meta_path}")

    logger.info(f"\n{'='*80}")
    logger.info("INGESTION COMPLETE")
    logger.info(f"{'='*80}")
    logger.info(f"Namespace: {NAMESPACE}")
    logger.info(f"URLs indexed: {len(url_set)}")
    logger.info(f"Total chunks: {len(all_chunks)}")
    logger.info(f"Vector dimension: {dim}")
    logger.info(f"Index location: {INDEX_ROOT}")
    logger.info(f"\nRun: make serve")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(ingest(HELP_DIR))
