from __future__ import annotations

from urllib.parse import urlparse, urlunparse

from seo_agents.extract.sitemap import analyze_sitemap_xml
from seo_agents.fetch.http import fetch_bytes, fetch_url
from seo_agents.security.url_safety import validate_url_strict


def analyze_sitemap(url: str, *, max_nested: int = 10) -> dict:
    normalized, _ = validate_url_strict(url)
    origin = _origin(normalized)
    discovered = _discover_sitemap_urls(origin)
    analyzed: list[dict] = []
    seen: set[str] = set()
    queue = list(discovered)

    while queue and len(analyzed) < max_nested:
        sitemap_url = queue.pop(0)
        if sitemap_url in seen:
            continue
        seen.add(sitemap_url)
        result = fetch_bytes(sitemap_url, max_bytes=10_000_000)
        if result["error"] or result["content"] is None:
            analyzed.append({"url": sitemap_url, "error": result["error"], "type": "unknown"})
            continue
        parsed = analyze_sitemap_xml(result["content"])
        parsed["url"] = sitemap_url
        analyzed.append(parsed)
        if parsed.get("type") == "sitemapindex":
            for item in parsed.get("sitemaps", [])[:max_nested]:
                loc = item.get("loc")
                if loc and loc not in seen:
                    queue.append(loc)

    return {
        "command": "sitemap",
        "target": url,
        "discovered": discovered,
        "sitemaps": analyzed,
        "summary": {
            "sitemaps_checked": len(analyzed),
            "urls_found": sum(len(item.get("urls", [])) for item in analyzed),
            "errors": sum(1 for item in analyzed if item.get("error") or item.get("errors")),
            "warnings": sum(len(item.get("warnings", [])) for item in analyzed),
        },
    }


def _discover_sitemap_urls(origin: str) -> list[str]:
    candidates: list[str] = []
    robots_url = f"{origin}/robots.txt"
    robots = fetch_url(robots_url, timeout=10, max_bytes=500_000)
    if robots.content:
        for line in robots.content.splitlines():
            key, sep, value = line.partition(":")
            if sep and key.strip().lower() == "sitemap":
                sitemap_url = value.strip()
                if sitemap_url:
                    candidates.append(sitemap_url)
    candidates.append(f"{origin}/sitemap.xml")

    unique: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        try:
            safe_candidate = validate_url_strict(candidate)[0]
        except Exception:
            continue
        if safe_candidate not in seen:
            seen.add(safe_candidate)
            unique.append(safe_candidate)
    return unique


def _origin(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))
