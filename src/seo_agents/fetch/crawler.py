from __future__ import annotations

from collections import deque
from urllib.parse import urlparse

from seo_agents.extract.html import parse_html
from seo_agents.fetch.render import render_page
from seo_agents.security.url_safety import validate_url_strict


def discover_urls(seed_url: str, *, max_pages: int = 20) -> list[str]:
    seed, _ = validate_url_strict(seed_url)
    seed_host = urlparse(seed).netloc.lower()
    queue: deque[str] = deque([seed])
    seen: set[str] = set()
    ordered: list[str] = []

    while queue and len(ordered) < max_pages:
        current = queue.popleft()
        if current in seen:
            continue
        seen.add(current)
        ordered.append(current)
        snapshot = render_page(current, mode="never")
        if snapshot.error:
            continue
        parsed = parse_html(snapshot.raw_html or "", base_url=snapshot.final_url)
        for link in parsed.links.get("internal", []):
            href = link.get("href")
            if not href:
                continue
            try:
                safe_href, _ = validate_url_strict(href)
            except Exception:
                continue
            if urlparse(safe_href).netloc.lower() == seed_host and safe_href not in seen:
                queue.append(safe_href)
    return ordered
