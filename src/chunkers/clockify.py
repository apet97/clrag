"""HTML-aware chunking for Clockify help pages."""
from __future__ import annotations
from bs4 import BeautifulSoup
from itertools import pairwise


def parse_clockify_html(html: str, url: str, title: str, breadcrumb: str = "") -> list[tuple[dict, dict]]:
    """
    Parse Clockify HTML into semantic chunks based on h2/h3 sections.

    Args:
        html: HTML string
        url: Page URL
        title: Page title
        breadcrumb: Breadcrumb navigation text

    Returns:
        List of (chunk_doc, metadata) tuples
    """
    soup = BeautifulSoup(html, "html.parser")

    # Extract h2/h3 headers
    heads = soup.select("h2, h3")

    if not heads:
        # Fallback: treat entire page as one chunk
        text = soup.get_text(" ", strip=True)
        return [(
            {"text": text},
            {"url": url, "title": title, "breadcrumb": breadcrumb, "section": title, "anchor": None}
        )]

    chunks = []

    # Process each h2/h3 and subsequent content until next h2/h3
    for h, nxt in pairwise(heads + [soup.new_tag("div")]):
        block = []
        for el in h.next_siblings:
            if el == nxt:
                break
            if getattr(el, "name", None) not in {"script", "style"}:
                if hasattr(el, "get_text"):
                    block.append(el.get_text(" ", strip=True))
                else:
                    block.append(str(el).strip())

        section_title = h.get_text(" ", strip=True)
        section_text = " ".join([section_title] + block).strip()
        anchor = h.get("id")

        meta = {
            "url": url,
            "title": title,
            "breadcrumb": breadcrumb,
            "section": section_title,
            "anchor": anchor,
            "type": "help"
        }

        chunks.append(({"text": section_text}, meta))

    return chunks
