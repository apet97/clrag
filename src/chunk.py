#!/usr/bin/env python3
"""Parent-child semantic chunking with token-based packing."""

import json
import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_CLEAN_DIR = Path("data/clean")
CHUNKS_DIR = Path("data/chunks")
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

PARENT_CHUNK_TOKENS = int(os.getenv("PARENT_CHUNK_TOKENS", "3500"))
PARENT_CHUNK_OVERLAP = int(os.getenv("PARENT_CHUNK_OVERLAP_TOKENS", "300"))
CHILD_CHUNK_TOKENS = int(os.getenv("CHILD_CHUNK_TOKENS", "1000"))
CHILD_CHUNK_OVERLAP = int(os.getenv("CHILD_CHUNK_OVERLAP_TOKENS", "150"))
CHILD_CHUNK_MIN = int(os.getenv("CHILD_CHUNK_MIN_TOKENS", "100"))


class TokenCounter:
    """Simple token estimation."""

    @staticmethod
    def count(text: str) -> int:
        """Estimate tokens: ~1 token per 4 chars."""
        return max(1, len(text.split()) + len(re.findall(r'\b\w+\b', text)))


class ParentChildChunker:
    """Create parent nodes (sections) and child nodes (chunks within sections)."""

    @staticmethod
    def split_by_headers(text: str) -> List[tuple[str, int]]:
        """Split by H2/H3 boundaries into sections."""
        sections = []
        current = []
        depth = 0

        for line in text.split("\n"):
            if re.match(r"^##\s", line):
                if current:
                    sections.append(("\n".join(current), depth))
                    current = []
                current.append(line)
                depth = 2
            elif re.match(r"^###\s", line):
                if depth >= 3 and current:
                    sections.append(("\n".join(current), 3))
                    current = []
                current.append(line)
                depth = 3
            else:
                current.append(line)

        if current:
            sections.append(("\n".join(current), depth))

        return sections

    @staticmethod
    def pack_by_tokens(text: str, target: int, overlap: int) -> List[str]:
        """Pack text into chunks of ~target tokens with overlap."""
        if TokenCounter.count(text) <= target:
            return [text]

        chunks = []
        words = text.split()
        current = []
        overlap_buf = []

        for i, word in enumerate(words):
            current.append(word)
            if TokenCounter.count(" ".join(current)) >= target:
                chunk_text = " ".join(current)
                chunks.append(chunk_text)

                # Overlap
                overlap_words = []
                for w in reversed(current):
                    overlap_words.insert(0, w)
                    if TokenCounter.count(" ".join(overlap_words)) >= overlap:
                        break

                current = overlap_words

        if current and TokenCounter.count(" ".join(current)) >= CHILD_CHUNK_MIN:
            chunks.append(" ".join(current))

        return chunks


class ChunkProcessor:
    """Process markdown files into parent-child chunks."""

    def __init__(self):
        self.chunk_id = 0
        self.parent_id = 0
        self.all_chunks = []

    def process_file(self, md_file: Path, namespace: str) -> List[Dict[str, Any]]:
        """Process a single markdown file."""
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
            if not match:
                logger.warning(f"⊘ Invalid frontmatter: {md_file}")
                return []

            try:
                fm = json.loads(match.group(1))
            except:
                logger.warning(f"⊘ Bad frontmatter: {md_file}")
                return []

            body = match.group(2).strip()
            url = fm.get("url", "")
            title = fm.get("title", "")
            headers = [fm.get("h1", "")] + fm.get("h2", [])
            headers = [h for h in headers if h]

            chunks = []

            # Split into parent sections
            sections = ParentChildChunker.split_by_headers(body)

            for sec_idx, (sec_text, _) in enumerate(sections):
                # Create parent node
                parent_tokens = TokenCounter.count(sec_text)
                parent = {
                    "id": self.parent_id,
                    "url": url,
                    "namespace": namespace,
                    "title": title,
                    "headers": headers,
                    "section_index": sec_idx,
                    "text": sec_text,
                    "tokens": parent_tokens,
                }

                parent_id = self.parent_id
                self.parent_id += 1
                chunks.append({**parent, "node_type": "parent"})

                # Create child chunks within section
                child_chunks = ParentChildChunker.pack_by_tokens(
                    sec_text, CHILD_CHUNK_TOKENS, CHILD_CHUNK_OVERLAP
                )

                for ch_idx, child_text in enumerate(child_chunks):
                    child_tokens = TokenCounter.count(child_text)
                    if child_tokens < CHILD_CHUNK_MIN:
                        continue

                    child = {
                        "id": self.chunk_id,
                        "parent_id": parent_id,
                        "url": url,
                        "namespace": namespace,
                        "title": title,
                        "headers": headers,
                        "section_index": sec_idx,
                        "chunk_index": ch_idx,
                        "text": child_text,
                        "tokens": child_tokens,
                        "node_type": "child",
                    }

                    chunks.append(child)
                    self.all_chunks.append(child)
                    self.chunk_id += 1

            logger.info(f"✓ {namespace}/{md_file.stem}: {len(chunks)} chunks")
            return chunks

        except Exception as e:
            logger.error(f"✗ Error processing {md_file}: {e}")
            return []

    def save_chunks(self, namespace: str):
        """Save chunks to JSONL per namespace."""
        ns_chunks = [c for c in self.all_chunks if c.get("namespace") == namespace]
        if not ns_chunks:
            return

        output_file = CHUNKS_DIR / f"{namespace}.jsonl"
        with open(output_file, "w", encoding="utf-8") as f:
            for chunk in ns_chunks:
                f.write(json.dumps(chunk) + "\n")

        logger.info(f"✓ Saved {len(ns_chunks)} chunks to {output_file}")


async def main():
    """Process all markdown files."""
    logger.info(f"Starting chunking from {DATA_CLEAN_DIR}")

    processor = ChunkProcessor()
    namespaces = set()

    for ns_dir in DATA_CLEAN_DIR.glob("*"):
        if ns_dir.is_dir():
            md_files = list(ns_dir.glob("*.md"))
            logger.info(f"Found {len(md_files)} files in {ns_dir.name}")

            for md_file in sorted(md_files):
                chunks = processor.process_file(md_file, ns_dir.name)
                namespaces.add(ns_dir.name)

    for ns in namespaces:
        processor.save_chunks(ns)

    logger.info(f"✓ Chunking complete: {len(processor.all_chunks)} total chunks")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
