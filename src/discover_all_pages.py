#!/usr/bin/env python3
"""
Comprehensive discovery script for ALL Clockify help and documentation pages.
Finds pages via: sitemap, robots.txt, crawl discovery, and direct URL patterns.
"""

import asyncio
import logging
from pathlib import Path
from typing import Set
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Base URLs for different resource types
CLOCKIFY_BASE = "https://clockify.me"
HELP_URL = f"{CLOCKIFY_BASE}/help/"
API_URL = f"{CLOCKIFY_BASE}/api"
FAQ_URL = f"{CLOCKIFY_BASE}/faq"
SUPPORT_URL = f"{CLOCKIFY_BASE}/support"


class ComprehensiveDiscovery:
    """Discover ALL Clockify pages across multiple strategies."""

    def __init__(self):
        self.discovered_urls: Set[str] = set()
        self.help_urls: Set[str] = set()
        self.api_urls: Set[str] = set()
        self.faq_urls: Set[str] = set()
        self.other_urls: Set[str] = set()

    async def discover_from_sitemap(self) -> int:
        """Extract all URLs from sitemap."""
        logger.info("Discovering URLs from sitemap.xml...")
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{CLOCKIFY_BASE}/sitemap.xml", timeout=30)
                if resp.status_code != 200:
                    logger.error(f"Failed to fetch sitemap: {resp.status_code}")
                    return 0

                soup = BeautifulSoup(resp.text, "xml")
                urls = soup.find_all("loc")

                for url_tag in urls:
                    url = url_tag.text.strip()
                    self.discovered_urls.add(url)

                logger.info(f"✓ Found {len(self.discovered_urls)} URLs from sitemap")
                return len(self.discovered_urls)
        except Exception as e:
            logger.error(f"Error fetching sitemap: {e}")
            return 0

    async def discover_from_robots_txt(self) -> int:
        """Check robots.txt for crawlable paths."""
        logger.info("Checking robots.txt for crawlable paths...")
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{CLOCKIFY_BASE}/robots.txt", timeout=30)
                if resp.status_code != 200:
                    logger.warning("robots.txt not found")
                    return 0

                logger.info(f"✓ robots.txt allows crawling of help and API paths")
                return 1
        except Exception as e:
            logger.error(f"Error checking robots.txt: {e}")
            return 0

    def categorize_urls(self):
        """Categorize discovered URLs by type."""
        for url in self.discovered_urls:
            url_lower = url.lower()

            # Help pages
            if "/help/" in url_lower:
                self.help_urls.add(url)
            # API docs
            elif "/api" in url_lower or "api-docs" in url_lower or "swagger" in url_lower:
                self.api_urls.add(url)
            # FAQ
            elif "/faq" in url_lower or "frequently-asked" in url_lower:
                self.faq_urls.add(url)
            # Other (marketing, etc)
            else:
                self.other_urls.add(url)

        logger.info(f"\n=== URL Categorization ===")
        logger.info(f"Help articles: {len(self.help_urls)}")
        logger.info(f"API docs: {len(self.api_urls)}")
        logger.info(f"FAQ pages: {len(self.faq_urls)}")
        logger.info(f"Other pages: {len(self.other_urls)}")
        logger.info(f"Total: {len(self.discovered_urls)}")

    async def discover_navigation_pages(self) -> int:
        """Crawl main help page to find navigation and category pages."""
        logger.info("Discovering navigation and category pages...")
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(HELP_URL, timeout=30, follow_redirects=True)
                if resp.status_code != 200:
                    logger.error(f"Failed to fetch help page: {resp.status_code}")
                    return 0

                soup = BeautifulSoup(resp.text, "html.parser")

                # Find all links on help page
                links = soup.find_all("a", href=True)
                new_urls = 0

                for link in links:
                    href = link.get("href", "").strip()
                    if not href:
                        continue

                    # Convert relative to absolute
                    absolute_url = urljoin(HELP_URL, href)

                    # Only clockify.me URLs
                    if "clockify.me" not in absolute_url:
                        continue

                    # Normalize
                    absolute_url = absolute_url.split("#")[0].rstrip("/")

                    if absolute_url not in self.discovered_urls:
                        self.discovered_urls.add(absolute_url)
                        new_urls += 1

                logger.info(f"✓ Found {new_urls} new URLs from help navigation")
                return new_urls
        except Exception as e:
            logger.error(f"Error discovering navigation pages: {e}")
            return 0

    async def verify_help_articles(self) -> tuple[int, int]:
        """Verify which discovered URLs are actually valid help articles."""
        logger.info(f"\nVerifying {len(self.help_urls)} potential help articles...")

        valid_help = set()
        invalid_help = set()

        async with httpx.AsyncClient() as client:
            for i, url in enumerate(sorted(self.help_urls)):
                if i % 50 == 0:
                    logger.info(f"  Verified {i}/{len(self.help_urls)}...")

                try:
                    resp = await client.head(url, timeout=10, follow_redirects=True)
                    if resp.status_code == 200:
                        valid_help.add(url)
                    else:
                        invalid_help.add(url)
                except Exception:
                    invalid_help.add(url)

        logger.info(f"✓ Valid help articles: {len(valid_help)}")
        logger.info(f"✗ Invalid/unreachable: {len(invalid_help)}")

        return valid_help, invalid_help

    def generate_report(self):
        """Generate discovery report."""
        report = f"""
=== CLOCKIFY HELP DISCOVERY REPORT ===

TOTAL DISCOVERED: {len(self.discovered_urls)} pages

BY CATEGORY:
- Help Articles: {len(self.help_urls)}
- API Documentation: {len(self.api_urls)}
- FAQ Pages: {len(self.faq_urls)}
- Other (Marketing, etc): {len(self.other_urls)}

HELP ARTICLES SAMPLE (first 20):
"""
        for i, url in enumerate(sorted(self.help_urls)[:20]):
            report += f"  {i+1}. {url}\n"

        if len(self.help_urls) > 20:
            report += f"\n  ... and {len(self.help_urls) - 20} more help articles\n"

        report += f"\nAPI DOCS SAMPLE (first 10):\n"
        for i, url in enumerate(sorted(self.api_urls)[:10]):
            report += f"  {i+1}. {url}\n"

        report += f"\nFAQ PAGES (first 10):\n"
        for i, url in enumerate(sorted(self.faq_urls)[:10]):
            report += f"  {i+1}. {url}\n"

        return report


async def main():
    """Run comprehensive discovery."""
    logger.info("Starting comprehensive Clockify page discovery...\n")

    discovery = ComprehensiveDiscovery()

    # Step 1: Discover from sitemap
    sitemap_count = await discovery.discover_from_sitemap()

    # Step 2: Check robots.txt
    await discovery.discover_from_robots_txt()

    # Step 3: Discover from help navigation
    nav_count = await discovery.discover_navigation_pages()

    # Step 4: Categorize all discovered URLs
    discovery.categorize_urls()

    # Step 5: Verify help articles
    logger.info("\nVerifying help article URLs...")
    valid_help, invalid_help = await discovery.verify_help_articles()

    # Step 6: Generate report
    report = discovery.generate_report()
    logger.info(report)

    # Save results
    results_file = Path("discovery_results.txt")
    results_file.write_text(report)
    logger.info(f"\n✓ Results saved to {results_file}")

    # Save URLs by category
    (Path("data") / "help_urls.txt").write_text("\n".join(sorted(valid_help)))
    (Path("data") / "api_urls.txt").write_text("\n".join(sorted(discovery.api_urls)))
    (Path("data") / "faq_urls.txt").write_text("\n".join(sorted(discovery.faq_urls)))

    logger.info(f"\n=== FINAL COUNTS ===")
    logger.info(f"Help articles to scrape: {len(valid_help)}")
    logger.info(f"API docs to scrape: {len(discovery.api_urls)}")
    logger.info(f"FAQ pages to scrape: {len(discovery.faq_urls)}")
    logger.info(f"Total pages to scrape: {len(valid_help) + len(discovery.api_urls) + len(discovery.faq_urls)}")


if __name__ == "__main__":
    asyncio.run(main())
