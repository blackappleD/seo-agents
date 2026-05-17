from __future__ import annotations

import gzip
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any


def parse_sitemap_xml(content: bytes | str) -> dict[str, Any]:
    errors: list[str] = []
    if isinstance(content, str):
        raw = content.encode("utf-8")
    else:
        raw = content
    if raw.startswith(b"\x1f\x8b"):
        try:
            raw = gzip.decompress(raw)
        except OSError as exc:
            return {"type": "unknown", "urls": [], "sitemaps": [], "errors": [str(exc)]}

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        return {"type": "unknown", "urls": [], "sitemaps": [], "errors": [str(exc)]}

    root_name = _local_name(root.tag)
    if root_name == "sitemapindex":
        return {
            "type": "sitemapindex",
            "urls": [],
            "sitemaps": [_parse_sitemap_entry(node) for node in root if _local_name(node.tag) == "sitemap"],
            "errors": errors,
        }
    if root_name == "urlset":
        return {
            "type": "urlset",
            "urls": [_parse_url_entry(node) for node in root if _local_name(node.tag) == "url"],
            "sitemaps": [],
            "errors": errors,
        }
    errors.append(f"Unsupported root element: {root_name}")
    return {"type": "unknown", "urls": [], "sitemaps": [], "errors": errors}


def analyze_sitemap_xml(content: bytes | str) -> dict[str, Any]:
    parsed = parse_sitemap_xml(content)
    warnings: list[dict[str, Any]] = []
    urls = parsed.get("urls", [])
    sitemaps = parsed.get("sitemaps", [])
    if len(urls) > 50_000:
        warnings.append({"severity": "High", "message": "Sitemap contains more than 50,000 URLs"})
    now = datetime.now(timezone.utc)
    for item in [*urls, *sitemaps]:
        lastmod = item.get("lastmod")
        if lastmod and _parse_datetime(lastmod) and _parse_datetime(lastmod) > now:
            warnings.append(
                {
                    "severity": "Medium",
                    "message": "lastmod is in the future",
                    "loc": item.get("loc"),
                    "lastmod": lastmod,
                }
            )
    deprecated_count = sum(1 for item in urls if item.get("priority") or item.get("changefreq"))
    if deprecated_count:
        warnings.append(
            {
                "severity": "Info",
                "message": "priority/changefreq are present but no longer important ranking signals",
                "count": deprecated_count,
            }
        )
    parsed["warnings"] = warnings
    parsed["counts"] = {"urls": len(urls), "sitemaps": len(sitemaps)}
    return parsed


def _parse_sitemap_entry(node: ET.Element) -> dict[str, str | None]:
    return {
        "loc": _child_text(node, "loc"),
        "lastmod": _child_text(node, "lastmod"),
    }


def _parse_url_entry(node: ET.Element) -> dict[str, str | None]:
    return {
        "loc": _child_text(node, "loc"),
        "lastmod": _child_text(node, "lastmod"),
        "changefreq": _child_text(node, "changefreq"),
        "priority": _child_text(node, "priority"),
    }


def _child_text(node: ET.Element, name: str) -> str | None:
    for child in node:
        if _local_name(child.tag) == name:
            return (child.text or "").strip() or None
    return None


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _parse_datetime(value: str) -> datetime | None:
    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        try:
            parsed = datetime.strptime(value.strip(), "%Y-%m-%d")
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed
