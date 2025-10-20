#!/usr/bin/env python3
"""
Multi-namespace async web scraper for Clockify help + LangChain docs.
Respects robots.txt, rate limiting, and handles incremental crawls.
"""

import asyncio
import json
import hashlib
import logging
from pathlib import Path
from typing import Set, Optional, Dict, List
from urllib.parse import urlparse, urljoin
from datetime import datetime
import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration
CRAWL_BASES = os.getenv("CRAWL_BASES", "https://clockify.me/help/").split(",")
DOMAINS_WHITELIST = set(os.getenv("DOMAINS_WHITELIST", "clockify.me,docs.langchain.com").split(","))
CRAWL_CONCURRENCY = int(os.getenv("CRAWL_CONCURRENCY", "8"))  # Increased parallelism
CRAWL_DELAY_SEC = float(os.getenv("CRAWL_DELAY_SEC", "0.5"))  # Reduced delay for faster crawling
CRAWL_MAX_PAGES = int(os.getenv("CRAWL_MAX_PAGES", "2000"))  # Increased max pages to capture all help articles
CRAWL_TIMEOUT = int(os.getenv("CRAWL_TIMEOUT", "30"))
CRAWL_MAX_DEPTH = int(os.getenv("CRAWL_MAX_DEPTH", "5"))  # Crawl depth for deep resource discovery

DATA_RAW_DIR = Path("data/raw")
CRAWL_STATE = Path("data/.crawl_state.json")

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)


def get_namespace(url: str) -> Optional[str]:
    """Infer namespace from URL domain."""
    domain = urlparse(url).netloc.replace("www.", "")
    if "clockify" in domain:
        return "clockify"
    elif "langchain" in domain:
        return "langchain"
    return None


class RobotsChecker:
    """Check compliance with robots.txt per domain."""

    def __init__(self):
        self.rules_cache: Dict[str, Optional[str]] = {}

    async def fetch_robots(self, session: httpx.AsyncClient, domain: str) -> bool:
        """Fetch and cache robots.txt for a domain."""
        if domain in self.rules_cache:
            return self.rules_cache[domain] is not None

        try:
            robots_url = f"https://{domain}/robots.txt"
            resp = await session.get(robots_url, timeout=10.0)
            if resp.status_code == 200:
                self.rules_cache[domain] = resp.text
                logger.info(f"✓ Fetched robots.txt from {robots_url}")
                return True
        except Exception as e:
            logger.debug(f"Could not fetch robots.txt for {domain}: {e}")

        self.rules_cache[domain] = None
        return False

    def is_allowed(self, url: str) -> bool:
        """Check if URL is allowed by robots.txt."""
        domain = urlparse(url).netloc
        if domain not in self.rules_cache:
            return True

        rules = self.rules_cache.get(domain)
        if not rules:
            return True

        path = urlparse(url).path
        for line in rules.split("\n"):
            line = line.split("#")[0].strip()
            if not line:
                continue
            if line.lower().startswith("user-agent:") and "*" in line.lower():
                continue
            if line.lower().startswith("disallow:"):
                disallow = line.split(":", 1)[1].strip()
                if disallow == "/" or path.startswith(disallow):
                    return False
        return True


class MultiNamespaceScraper:
    """Async scraper for multiple corpora with namespacing."""

    def __init__(self):
        self.bases = [base.strip() for base in CRAWL_BASES]
        self.robots = RobotsChecker()
        self.visited_urls: Set[str] = set()
        self.queue: asyncio.Queue = asyncio.Queue()
        self.last_request_time_per_domain: Dict[str, float] = {}
        self.session: Optional[httpx.AsyncClient] = None
        self.state = self._load_state()
        self.namespace_dirs = {}

    def _load_state(self) -> dict:
        """Load previous crawl state."""
        if CRAWL_STATE.exists():
            try:
                with open(CRAWL_STATE) as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load crawl state: {e}")
        return {}

    def _save_state(self):
        """Save crawl state."""
        with open(CRAWL_STATE, "w") as f:
            json.dump(self.state, f, indent=2)

    def _is_help_article(self, url: str) -> bool:
        """Check if URL is an actual help article (not marketing, language variant, etc)."""
        parsed = urlparse(url)
        path = parsed.path.lower()

        # For clockify.me: only accept /help/* paths (exclude non-English variants)
        if "clockify.me" in parsed.netloc:
            # Must be under /help/
            if not path.startswith("/help/"):
                return False

            # Exclude language-specific paths like /help/fr/, /help/es/, etc
            path_parts = path.split("/")
            if len(path_parts) > 2:
                lang_part = path_parts[2]
                # Exclude 2-letter language codes at start of path
                if len(lang_part) == 2 and lang_part.isalpha() and lang_part not in ["en"]:
                    return False
                # Exclude paths that are just language codes
                if lang_part in ["fr", "es", "de", "pt", "ja", "zh", "ru", "ar", "hi"]:
                    return False

            # Exclude common non-help pages
            excluded_patterns = [
                "/help/customers",
                "/help/partners",
                "/help/start",
                "/help/index",
                "/help/$",  # homepage
                "/help?",  # query strings
            ]
            if any(pattern in path for pattern in excluded_patterns):
                return False

            return True

        return True  # For other domains, accept as-is

    def _normalize_url(self, url: str) -> Optional[str]:
        """Normalize URL and check domain."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.replace("www.", "")

            # Check domain whitelist
            if not any(domain.endswith(allowed) for allowed in DOMAINS_WHITELIST):
                return None

            # Check if it's an actual help article
            if not self._is_help_article(url):
                return None

            # Remove fragments and querystrings (except tracking)
            if "?" in url:
                url = url.split("?")[0]
            if "#" in url:
                url = url.split("#")[0]

            url = url.rstrip("/")
            return url
        except Exception:
            return None

    def _get_slug(self, url: str, namespace: str) -> str:
        """Get slug for filename from URL."""
        path = urlparse(url).path
        slug = path.replace("/", "_").strip("_") or "index"
        return slug

    async def _rate_limit(self, domain: str):
        """Rate limit per domain."""
        if domain not in self.last_request_time_per_domain:
            self.last_request_time_per_domain[domain] = 0

        elapsed = asyncio.get_event_loop().time() - self.last_request_time_per_domain[domain]
        if elapsed < CRAWL_DELAY_SEC:
            await asyncio.sleep(CRAWL_DELAY_SEC - elapsed)

        self.last_request_time_per_domain[domain] = asyncio.get_event_loop().time()

    async def _fetch_page(self, url: str) -> Optional[tuple[str, dict]]:
        """Fetch a single page."""
        domain = urlparse(url).netloc
        namespace = get_namespace(url)

        if not self.robots.is_allowed(url):
            logger.debug(f"✗ Blocked by robots.txt: {url}")
            return None

        await self._rate_limit(domain)

        try:
            headers = {
                "User-Agent": "Clockify-Internal-RAG/1.0",
                "Accept-Encoding": "gzip, deflate"
            }

            # Conditional headers for incremental crawling
            state_key = url
            if state_key in self.state and self.state[state_key].get("etag"):
                headers["If-None-Match"] = self.state[state_key]["etag"]
            if state_key in self.state and self.state[state_key].get("last_modified"):
                headers["If-Modified-Since"] = self.state[state_key]["last_modified"]

            logger.info(f"→ Fetching: {url}")
            resp = await self.session.get(url, headers=headers, timeout=CRAWL_TIMEOUT, follow_redirects=True)

            if resp.status_code == 304:
                logger.debug(f"⊘ Not modified (304): {url}")
                return None

            if resp.status_code != 200:
                logger.warning(f"✗ HTTP {resp.status_code}: {url}")
                return None

            meta = {
                "url": url,
                "namespace": namespace,
                "fetched_at": datetime.utcnow().isoformat(),
                "status": resp.status_code,
                "etag": resp.headers.get("etag", ""),
                "last_modified": resp.headers.get("last-modified", ""),
                "sha256": hashlib.sha256(resp.content).hexdigest(),
            }

            self.state[state_key] = {
                "etag": meta["etag"],
                "last_modified": meta["last_modified"],
                "sha256": meta["sha256"],
                "fetched_at": meta["fetched_at"],
            }

            logger.info(f"✓ Fetched {len(resp.content)} bytes: {url}")
            return (resp.text, meta)

        except Exception as e:
            logger.error(f"✗ Error fetching {url}: {e}")
            return None

    def _extract_links(self, html: str, base_url: str) -> Set[str]:
        """Extract ALL internal links from HTML (comprehensive resource discovery)."""
        links = set()
        try:
            soup = BeautifulSoup(html, "html.parser")

            # Extract from <a> tags (main content links)
            for link in soup.find_all("a", href=True):
                href = link["href"]
                absolute_url = urljoin(base_url, href)
                normalized = self._normalize_url(absolute_url)
                if normalized and normalized not in self.visited_urls:
                    links.add(normalized)

            # Extract from sitemap links (if present)
            for sitemap in soup.find_all("link", {"rel": "alternate", "hreflang": True}):
                href = sitemap.get("href")
                if href:
                    absolute_url = urljoin(base_url, href)
                    normalized = self._normalize_url(absolute_url)
                    if normalized and normalized not in self.visited_urls:
                        links.add(normalized)

            # Extract from breadcrumb navigation
            for breadcrumb in soup.find_all("li", {"class": lambda x: x and "breadcrumb" in x.lower()}):
                for a in breadcrumb.find_all("a", href=True):
                    href = a["href"]
                    absolute_url = urljoin(base_url, href)
                    normalized = self._normalize_url(absolute_url)
                    if normalized and normalized not in self.visited_urls:
                        links.add(normalized)

            # Extract from navigation menus and sidebars
            for nav in soup.find_all(["nav", "aside"]):
                for a in nav.find_all("a", href=True):
                    href = a["href"]
                    absolute_url = urljoin(base_url, href)
                    normalized = self._normalize_url(absolute_url)
                    if normalized and normalized not in self.visited_urls:
                        links.add(normalized)

            # Extract from related articles/links sections
            for section in soup.find_all(["section", "div"], {"class": lambda x: x and any(p in x.lower() for p in ["related", "articles", "links", "resources", "help"])}):
                for a in section.find_all("a", href=True):
                    href = a["href"]
                    absolute_url = urljoin(base_url, href)
                    normalized = self._normalize_url(absolute_url)
                    if normalized and normalized not in self.visited_urls:
                        links.add(normalized)

        except Exception as e:
            logger.debug(f"Error extracting links: {e}")
        return links

    async def _save_page(self, html: str, meta: dict):
        """Save fetched HTML with metadata."""
        namespace = meta.get("namespace")
        if not namespace:
            logger.warning(f"Skipping URL without namespace: {meta['url']}")
            return

        ns_dir = DATA_RAW_DIR / namespace
        ns_dir.mkdir(parents=True, exist_ok=True)

        slug = self._get_slug(meta["url"], namespace)
        filepath = ns_dir / f"{slug}.html"

        try:
            wrapper = {
                "meta": {
                    "url": meta["url"],
                    "namespace": namespace,
                    "fetched_at": meta["fetched_at"],
                    "sha256": meta["sha256"],
                },
                "html": html
            }

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(json.dumps(wrapper, indent=2))

            logger.info(f"✓ Saved: {filepath}")
        except Exception as e:
            logger.error(f"✗ Failed to save {filepath}: {e}")

    async def _worker(self):
        """Worker coroutine for crawling queue."""
        while True:
            url = await self.queue.get()
            try:
                if url in self.visited_urls or len(self.visited_urls) >= CRAWL_MAX_PAGES:
                    continue

                self.visited_urls.add(url)
                result = await self._fetch_page(url)

                if result:
                    html, meta = result
                    await self._save_page(html, meta)

                    # Extract and queue new links
                    new_links = self._extract_links(html, url)
                    for link in new_links:
                        if len(self.visited_urls) < CRAWL_MAX_PAGES:
                            await self.queue.put(link)

            except Exception as e:
                logger.error(f"Worker error: {e}")
            finally:
                self.queue.task_done()

    async def run(self):
        """Run the scraper."""
        logger.info(f"Starting multi-namespace scraper from: {self.bases}")

        async with httpx.AsyncClient() as session:
            self.session = session

            # Fetch robots.txt for each domain
            domains = set(urlparse(base).netloc for base in self.bases)
            for domain in domains:
                await self.robots.fetch_robots(session, domain)

            # Seed queue with base URLs and try sitemaps
            for base in self.bases:
                await self.queue.put(base)

                # Try sitemap
                domain = urlparse(base).netloc
                sitemap_url = f"https://{domain}/sitemap.xml"
                try:
                    resp = await session.get(sitemap_url, timeout=10.0)
                    if resp.status_code == 200:
                        soup = BeautifulSoup(resp.text, "xml")
                        for loc in soup.find_all("loc"):
                            url = self._normalize_url(loc.text)
                            if url:
                                await self.queue.put(url)
                        logger.info(f"✓ Loaded sitemap from {sitemap_url}")
                except Exception as e:
                    logger.debug(f"Sitemap not available for {domain}: {e}")

            # Create workers
            workers = [asyncio.create_task(self._worker()) for _ in range(CRAWL_CONCURRENCY)]

            # Wait for queue to empty
            await self.queue.join()

            # Cancel workers
            for w in workers:
                w.cancel()

            # Save state
            self._save_state()

            logger.info(f"✓ Crawl complete. Visited {len(self.visited_urls)} pages.")
            logger.info(f"  Clockify: {len(list((DATA_RAW_DIR / 'clockify').glob('*.html')))} pages")
            logger.info(f"  LangChain: {len(list((DATA_RAW_DIR / 'langchain').glob('*.html')))} pages")


async def main():
    """Main entry point."""
    scraper = MultiNamespaceScraper()
    await scraper.run()


if __name__ == "__main__":
    asyncio.run(main())
