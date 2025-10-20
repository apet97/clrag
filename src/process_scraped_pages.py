#!/usr/bin/env python3
"""
Process scraped Clockify help pages: convert HTML to clean markdown, deduplicate, and validate.
"""

import json
import logging
import hashlib
from pathlib import Path
from bs4 import BeautifulSoup
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = Path("data/raw/clockify")
CLEAN_DIR = Path("data/clean/clockify")
CLEAN_DIR.mkdir(parents=True, exist_ok=True)


def extract_content_from_html(html_content: str, url: str) -> tuple[str, str, str]:
    """Extract title, description, and body from HTML."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract title
    title = "Clockify Help"
    if soup.find("title"):
        title = soup.find("title").get_text(strip=True)
    elif soup.find("h1"):
        title = soup.find("h1").get_text(strip=True)

    # Extract description/meta
    description = ""
    if soup.find("meta", attrs={"name": "description"}):
        description = soup.find("meta", attrs={"name": "description"}).get("content", "")

    # Extract main content
    # Remove script, style, nav, footer
    for tag in soup.find_all(["script", "style", "nav", "footer", "noscript"]):
        tag.decompose()

    # Get main content
    main = soup.find("main") or soup.find("article") or soup.find("body")
    if main:
        # Remove navigation elements
        for nav_elem in main.find_all(["nav", ".sidebar", ".navigation"]):
            nav_elem.decompose()

        # Get text
        body = main.get_text(separator="\n", strip=True)
    else:
        body = soup.get_text(separator="\n", strip=True)

    # Clean whitespace
    body = re.sub(r"\n\n+", "\n", body).strip()

    return title, description, body


def process_html_file(html_path: Path) -> dict:
    """Process single HTML file into markdown."""
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        html = content.get("html", "")
        meta = content.get("meta", {})
        url = meta.get("url", "")

        # Skip non-English URLs
        if any(lang in url.lower() for lang in ["/help/de", "/help/es", "/help/fr", "/help/pt"]):
            logger.info(f"⊘ Skipping non-English: {url}")
            return None

        # Extract content
        title, description, body = extract_content_from_html(html, url)

        # Skip if body is too short or empty
        if len(body) < 100:
            logger.warning(f"⊘ Too short ({len(body)} chars): {url}")
            return None

        # Create markdown
        markdown = f"# {title}\n\n"
        if description:
            markdown += f"> {description}\n\n"
        markdown += f"**Source:** {url}\n\n"
        markdown += body

        # Create hash for deduplication
        content_hash = hashlib.sha256(body.encode()).hexdigest()

        return {
            "title": title,
            "url": url,
            "description": description,
            "content_hash": content_hash,
            "body_length": len(body),
            "markdown": markdown,
            "file_path": html_path,
        }

    except Exception as e:
        logger.error(f"✗ Failed to process {html_path}: {e}")
        return None


async def main():
    """Process all scraped HTML files."""
    logger.info(f"Processing HTML files from {RAW_DIR}...")

    html_files = list(RAW_DIR.glob("*.html"))
    logger.info(f"Found {len(html_files)} HTML files")

    processed = []
    seen_hashes = set()
    duplicates = 0

    for i, html_file in enumerate(sorted(html_files)):
        if i % 20 == 0:
            logger.info(f"Processing {i}/{len(html_files)}...")

        result = process_html_file(html_file)

        if result is None:
            continue

        # Check for duplicates
        if result["content_hash"] in seen_hashes:
            logger.debug(f"⊘ Duplicate content: {result['url']}")
            duplicates += 1
            continue

        seen_hashes.add(result["content_hash"])
        processed.append(result)

    logger.info(f"\n=== PROCESSING RESULTS ===")
    logger.info(f"Total HTML files processed: {len(html_files)}")
    logger.info(f"Valid articles extracted: {len(processed)}")
    logger.info(f"Duplicates removed: {duplicates}")
    logger.info(f"Final unique articles: {len(processed)}")

    # Save as markdown files
    logger.info(f"\nSaving to {CLEAN_DIR}...")
    for result in processed:
        # Create safe filename from title
        safe_title = re.sub(r"[^\w\s-]", "", result["title"]).strip()
        safe_title = re.sub(r"[-\s]+", "-", safe_title).lower()
        filename = f"{safe_title}.md"

        filepath = CLEAN_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result["markdown"])

        logger.debug(f"✓ Saved: {filepath}")

    logger.info(f"\n✓ Saved {len(processed)} clean markdown files to {CLEAN_DIR}")

    # Save metadata
    metadata = {
        "total_original": len(html_files),
        "total_processed": len(processed),
        "duplicates_removed": duplicates,
        "articles": [
            {
                "title": r["title"],
                "url": r["url"],
                "file": (CLEAN_DIR / f"{re.sub(r'[^\\w\\s-]', '', r['title']).strip().replace(' ', '-').lower()}.md").name,
                "size": r["body_length"],
            }
            for r in processed
        ]
    }

    metadata_file = Path("CLOCKIFY_HELP_INGESTION_METADATA.json")
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"✓ Metadata saved to {metadata_file}")

    return len(processed)


if __name__ == "__main__":
    import asyncio
    count = asyncio.run(main())
    logger.info(f"\nReady to ingest {count} articles!")
