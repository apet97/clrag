#!/usr/bin/env python3
"""
Comprehensive Clockify help article scraper based on ChatGPT recommendation.
Target: All 247 English help articles under /help (excluding /es, /pt, /de).
"""

import os
import re
import pathlib
import requests
import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup
try:
    from markdownify import markdownify as md
except ImportError:
    print("Installing markdownify...")
    os.system("pip install markdownify")
    from markdownify import markdownify as md

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE = "https://clockify.me"
ROOT = f"{BASE}/help/"
EXCLUDE = ("/help/es/", "/help/pt/", "/help/de/", "/help/fr/")
OUT = pathlib.Path("data/clean/clockify")
OUT.mkdir(parents=True, exist_ok=True)


def get(url):
    """Fetch URL with error handling."""
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.text
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None


def discover_urls():
    """Pull all article URLs from WordPress sitemaps."""
    logger.info("Discovering URLs from WordPress sitemaps...")

    sitemaps = []
    try:
        xml = get(f"{ROOT}wp-sitemap.xml")
        if not xml:
            logger.warning("wp-sitemap.xml not found, trying fallback...")
            xml = get(f"{BASE}/sitemap.xml")

        if xml:
            soup = BeautifulSoup(xml, "xml")
            for loc in soup.select("sitemap > loc"):
                u = loc.text
                if "/wp-sitemap-posts-" in u or "/wp-sitemap-pages-" in u:
                    sitemaps.append(u)
                    logger.debug(f"Found sitemap: {u}")
    except Exception as e:
        logger.error(f"Error discovering sitemaps: {e}")

    urls = set()
    for sm in sitemaps:
        try:
            sx_html = get(sm)
            if not sx_html:
                continue
            sx = BeautifulSoup(sx_html, "xml")
            for loc in sx.select("url > loc"):
                u = loc.text.strip()
                # Only help URLs, exclude non-English
                if u.startswith(ROOT) and not any(p in u for p in EXCLUDE):
                    urls.add(u)
        except Exception as e:
            logger.error(f"Error parsing sitemap {sm}: {e}")

    logger.info(f"✓ Discovered {len(urls)} English help articles")
    return urls


def safe_name(u: str) -> str:
    """Convert URL to safe filename."""
    p = urlparse(u).path.removeprefix("/").rstrip("/")
    # Sanitize: replace non-alphanumeric with dash
    p = re.sub(r"[^a-zA-Z0-9/_-]+", "-", p)
    # Replace path separators with double underscore
    filename = p.replace("/", "__") + ".md"
    return (OUT / filename).as_posix()


def extract_main(html: str, url: str) -> str:
    """Extract main content from HTML page."""
    s = BeautifulSoup(html, "lxml")

    # Remove unnecessary elements
    for tag in s.find_all(["script", "style", "nav", "footer", ".sidebar", ".navigation"]):
        tag.decompose()

    # Try multiple selectors for main content
    main_content = None
    for sel in ["article", "main", ".entry-content", ".post-content", "#content", ".page-content"]:
        n = s.select_one(sel)
        if n:
            main_content = str(n)
            break

    if not main_content:
        # Fallback to body
        main_content = str(s.body or s)

    # Convert to markdown
    markdown = md(main_content, heading_style="ATX")

    # Add metadata at top
    title = s.title.string if s.title else "Clockify Help"
    metadata = f"# {title}\n\n> Source: {url}\n\n"

    return metadata + markdown


def scrape_all():
    """Scrape all discovered help articles."""
    urls = discover_urls()

    if not urls:
        logger.error("No URLs discovered!")
        return 0

    logger.info(f"\nScraping {len(urls)} articles...")

    saved = 0
    failed = 0

    for i, u in enumerate(sorted(urls), 1):
        try:
            # Show progress
            if i % 25 == 0:
                logger.info(f"Progress: {i}/{len(urls)}...")

            html = get(u)
            if not html:
                failed += 1
                continue

            # Extract content
            mdown = extract_main(html, u)

            # Save file
            fp = safe_name(u)
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(mdown)

            saved += 1
            logger.debug(f"✓ {i}/{len(urls)}: {fp}")

        except Exception as e:
            logger.error(f"✗ {i}/{len(urls)}: {u} - {e}")
            failed += 1

    logger.info(f"\n{'='*60}")
    logger.info(f"SCRAPING COMPLETE")
    logger.info(f"{'='*60}")
    logger.info(f"Total URLs discovered: {len(urls)}")
    logger.info(f"Successfully saved: {saved}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Success rate: {100*saved//len(urls)}%")
    logger.info(f"Output directory: {OUT}")

    return saved


if __name__ == "__main__":
    import sys
    count = scrape_all()
    sys.exit(0 if count > 0 else 1)
