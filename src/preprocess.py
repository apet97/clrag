#!/usr/bin/env python3
"""HTML to Markdown extraction with namespace support, glossary tagging, and PII stripping."""

import json
import logging
import hashlib
import re
import argparse
from pathlib import Path
from urllib.parse import urljoin
from datetime import datetime
import trafilatura
from bs4 import BeautifulSoup
from readability import Document
from src.glossary import get_glossary

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_RAW_DIR = Path("data/raw")
DATA_CLEAN_DIR = Path("data/clean")


class HTMLCleaner:
    """Clean and extract HTML content."""

    NOISE_SELECTORS = [
        "nav", "footer", ".nav", ".navbar", ".header",
        ".cookie-consent", ".notification", ".sidebar",
        "script", "style", "[role='navigation']",
        ".edit-this-page", ".version-banner",
        ".social-share", ".related-articles",
        ".toc", "aside"
    ]

    # Regex patterns for PII detection and removal
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PHONE_PATTERN = r'\b(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
    SSN_PATTERN = r'\b\d{3}-\d{2}-\d{4}\b'

    @staticmethod
    def remove_noise(soup: BeautifulSoup) -> BeautifulSoup:
        """Remove navigation, ads, noise."""
        for selector in HTMLCleaner.NOISE_SELECTORS:
            for el in soup.select(selector):
                el.decompose()
        return soup

    @staticmethod
    def strip_pii(text: str) -> str:
        """Remove personally identifiable information (emails, phone numbers, SSN)."""
        text = re.sub(HTMLCleaner.EMAIL_PATTERN, "[EMAIL]", text)
        text = re.sub(HTMLCleaner.PHONE_PATTERN, "[PHONE]", text)
        text = re.sub(HTMLCleaner.SSN_PATTERN, "[SSN]", text)
        return text

    @staticmethod
    def extract_structure(soup: BeautifulSoup, base_url: str) -> tuple[str, dict]:
        """Extract structured markdown with metadata."""
        parts = []
        headings = {"h1": None, "h2": []}

        title = soup.title.string if soup.title else ""
        if soup.h1:
            title = soup.h1.get_text().strip() or title

        for tag in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "pre", "code", "table"]):
            if tag.name == "h1":
                text = tag.get_text().strip()
                if text:
                    parts.append(f"# {text}\n")
                    if not headings["h1"]:
                        headings["h1"] = text
            elif tag.name == "h2":
                text = tag.get_text().strip()
                if text:
                    parts.append(f"\n## {text}\n")
                    headings["h2"].append(text)
            elif tag.name == "h3":
                text = tag.get_text().strip()
                if text:
                    parts.append(f"\n### {text}\n")
            elif tag.name == "h4":
                text = tag.get_text().strip()
                if text:
                    parts.append(f"\n#### {text}\n")
            elif tag.name == "p":
                text = tag.get_text().strip()
                if text:
                    parts.append(f"{text}\n\n")
            elif tag.name == "li":
                parent = tag.parent.name
                indent = "  " * (len(tag.find_parents(["ul", "ol"])) - 1)
                prefix = "1. " if parent == "ol" else "- "
                text = tag.get_text().strip()
                if text:
                    parts.append(f"{indent}{prefix}{text}\n")
            elif tag.name == "pre":
                text = tag.get_text().strip()
                if text and len(text) > 10:
                    parts.append(f"\n```\n{text}\n```\n\n")
            elif tag.name == "table":
                try:
                    rows = tag.find_all("tr")
                    if rows:
                        parts.append("\n| ")
                        headers = rows[0].find_all(["th", "td"])
                        parts.append(" | ".join(h.get_text().strip() for h in headers))
                        parts.append(" |\n|")
                        parts.append("|".join(["---"] * len(headers)))
                        parts.append("|\n")
                        for row in rows[1:]:
                            cols = row.find_all(["td", "th"])
                            parts.append("| " + " | ".join(c.get_text().strip() for c in cols) + " |\n")
                except:
                    pass

        md = "".join(parts)
        md = re.sub(r"\n{3,}", "\n\n", md)
        md = re.sub(r" +", " ", md)

        # Fix URLs
        md = re.sub(
            r'\[([^\]]+)\]\(([^)]+)\)',
            lambda m: f"[{m.group(1)}]({urljoin(base_url, m.group(2))})" if m.group(2) else m.group(0),
            md
        )

        return md, {"title": title, "h1": headings["h1"], "h2": headings["h2"]}


class MarkdownConverter:
    """Convert HTML files to markdown per namespace."""

    @staticmethod
    def process_file(html_file: Path) -> bool:
        """Process a single HTML file."""
        try:
            with open(html_file, "r", encoding="utf-8") as f:
                wrapper = json.load(f)

            html = wrapper["html"]
            meta = wrapper["meta"]
            url = meta["url"]
            namespace = meta.get("namespace")

            if not namespace:
                logger.warning(f"Skipping file without namespace: {html_file}")
                return False

            soup = BeautifulSoup(html, "html.parser")
            soup = HTMLCleaner.remove_noise(soup)

            md = trafilatura.extract(html, output_format="txt") or ""

            if len(md) < 100:
                md, headings = HTMLCleaner.extract_structure(soup, url)
            else:
                _, headings = HTMLCleaner.extract_structure(soup, url)

            if len(md) < 50:
                logger.warning(f"⊘ Insufficient content: {url}")
                return False

            # Strip PII from markdown
            md = HTMLCleaner.strip_pii(md)

            # Detect glossary entities
            glossary = get_glossary()
            entities = list(glossary.detect_terms(md))

            fm = {
                "url": url,
                "namespace": namespace,
                "title": headings.get("title") or "Untitled",
                "h1": headings.get("h1"),
                "h2": headings.get("h2", []),
                "fetched_at": meta.get("fetched_at"),
                "sha256_raw": meta.get("sha256", ""),
                "entities": entities,  # Detected glossary terms
            }

            ns_clean = DATA_CLEAN_DIR / namespace
            ns_clean.mkdir(parents=True, exist_ok=True)

            slug = html_file.stem
            output = ns_clean / f"{slug}.md"

            with open(output, "w", encoding="utf-8") as f:
                f.write(f"---\n{json.dumps(fm, indent=2)}\n---\n\n{md}")

            logger.info(f"✓ {namespace}/{slug}: {len(md)} chars, entities: {len(entities)}")
            return True

        except Exception as e:
            logger.error(f"✗ Error processing {html_file}: {e}")
            return False


def import_markdown_corpus(import_dir: str, namespace: str) -> int:
    """Import pre-extracted markdown files (e.g., from scraped/)."""
    import_path = Path(import_dir)
    if not import_path.exists():
        logger.error(f"Import directory not found: {import_dir}")
        return 0

    ns_clean = DATA_CLEAN_DIR / namespace
    ns_clean.mkdir(parents=True, exist_ok=True)

    count = 0
    for md_file in import_path.rglob("*.md"):
        try:
            raw_text = md_file.read_text(encoding="utf-8", errors="ignore")

            # Extract title from first H1 or filename
            title = ""
            for line in raw_text.splitlines():
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
            if not title:
                title = md_file.stem.replace("-", " ").title()

            # Build frontmatter
            fm = {
                "url": "",
                "namespace": namespace,
                "title": title,
                "h1": title,
                "h2": [],
                "fetched_at": datetime.utcnow().isoformat(),
                "sha256_raw": hashlib.sha256(raw_text.encode()).hexdigest(),
            }

            # Write with frontmatter
            out_file = ns_clean / f"{md_file.stem}.md"
            out_file.write_text(f"---\n{json.dumps(fm, indent=2)}\n---\n\n{raw_text}", encoding="utf-8")

            logger.info(f"✓ {namespace}/{md_file.stem}: {len(raw_text)} chars")
            count += 1

        except Exception as e:
            logger.error(f"✗ Failed to import {md_file}: {e}")

    logger.info(f"✓ Imported {count} markdown files into {namespace}")
    return count


async def main():
    """Process all raw HTML files."""
    logger.info(f"Starting preprocessing from {DATA_RAW_DIR}")

    total = 0
    success = 0

    for ns_dir in DATA_RAW_DIR.glob("*"):
        if ns_dir.is_dir():
            html_files = list(ns_dir.glob("*.html"))
            logger.info(f"Found {len(html_files)} files in {ns_dir.name}")

            for html_file in html_files:
                total += 1
                if MarkdownConverter.process_file(html_file):
                    success += 1

    logger.info(f"✓ Preprocessing complete: {success}/{total} successful")


if __name__ == "__main__":
    import asyncio

    parser = argparse.ArgumentParser(description="HTML → Markdown preprocessing with corpus import")
    parser.add_argument("--import-dir", type=str, default="", help="Directory to import markdown from")
    parser.add_argument("--namespace", type=str, default="", help="Namespace for imported docs")
    args = parser.parse_args()

    if args.import_dir and args.namespace:
        import_markdown_corpus(args.import_dir, args.namespace)
    else:
        asyncio.run(main())
