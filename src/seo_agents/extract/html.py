from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urljoin, urlparse

from seo_agents.models import ParsedPage


class SEOHTMLParser(HTMLParser):
    def __init__(self, base_url: str | None = None) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.result = ParsedPage()
        self._current_tag: str | None = None
        self._current_heading: str | None = None
        self._heading_text: list[str] = []
        self._title_text: list[str] = []
        self._anchor: dict[str, Any] | None = None
        self._script_type: str | None = None
        self._script_text: list[str] = []
        self._json_ld_blocks: list[str] = []
        self._skip_visible_depth = 0
        self._visible_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs_map = _attrs_to_dict(attrs)
        self._current_tag = tag

        if tag in {"script", "style", "noscript", "template"}:
            self._skip_visible_depth += 1

        if tag == "title":
            self._title_text = []
        elif tag == "meta":
            self._handle_meta(attrs_map)
        elif tag == "link":
            self._handle_link(attrs_map)
        elif tag in {"h1", "h2", "h3"}:
            self._current_heading = tag
            self._heading_text = []
        elif tag == "img":
            self.result.images.append(self._normalize_image(attrs_map))
        elif tag == "a":
            href = attrs_map.get("href")
            self._anchor = {
                "href": urljoin(self.base_url or "", href) if href else "",
                "rel": attrs_map.get("rel", ""),
                "text": "",
            }
        elif tag == "script":
            self._script_type = attrs_map.get("type", "").lower()
            self._script_text = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "template"} and self._skip_visible_depth:
            self._skip_visible_depth -= 1
        if tag == "title":
            title = _clean_text(" ".join(self._title_text))
            self.result.title = title or None
        elif tag in {"h1", "h2", "h3"} and self._current_heading == tag:
            text = _clean_text(" ".join(self._heading_text))
            if text:
                getattr(self.result, tag).append(text)
            self._current_heading = None
            self._heading_text = []
        elif tag == "a" and self._anchor is not None:
            self._anchor["text"] = _clean_text(self._anchor.get("text", ""))
            self._store_anchor(self._anchor)
            self._anchor = None
        elif tag == "script":
            if self._script_type and "ld+json" in self._script_type:
                block = "\n".join(self._script_text).strip()
                if block:
                    self._json_ld_blocks.append(block)
            self._script_type = None
            self._script_text = []
        self._current_tag = None

    def handle_data(self, data: str) -> None:
        if not data:
            return
        if self._current_tag == "title":
            self._title_text.append(data)
        if self._current_heading:
            self._heading_text.append(data)
        if self._anchor is not None:
            self._anchor["text"] = f"{self._anchor.get('text', '')} {data}"
        if self._script_type and "ld+json" in self._script_type:
            self._script_text.append(data)
        if self._skip_visible_depth == 0:
            stripped = _clean_text(data)
            if stripped:
                self._visible_text.append(stripped)

    def close(self) -> None:
        super().close()
        self.result.schema = parse_json_ld_blocks(self._json_ld_blocks)
        self.result.text = _clean_text(" ".join(self._visible_text))
        self.result.word_count = len(re.findall(r"\b\w+\b", self.result.text, flags=re.UNICODE))

    def _handle_meta(self, attrs: dict[str, str]) -> None:
        name = attrs.get("name", "").lower()
        prop = attrs.get("property", "").lower()
        content = attrs.get("content", "").strip()
        if not content:
            return
        if name == "description":
            self.result.meta_description = content
        elif name == "robots":
            self.result.meta_robots = content
        elif name == "viewport":
            self.result.viewport = content
        elif prop.startswith("og:"):
            self.result.open_graph[prop] = content
        elif name.startswith("twitter:"):
            self.result.twitter_card[name] = content

    def _handle_link(self, attrs: dict[str, str]) -> None:
        rel = attrs.get("rel", "").lower()
        href = attrs.get("href", "")
        if not href:
            return
        absolute = urljoin(self.base_url or "", href)
        rel_tokens = {token.strip() for token in rel.split() if token.strip()}
        if "canonical" in rel_tokens:
            self.result.canonical = absolute
        if "alternate" in rel_tokens and attrs.get("hreflang"):
            self.result.hreflang.append(
                {"hreflang": attrs.get("hreflang", ""), "href": absolute}
            )

    def _normalize_image(self, attrs: dict[str, str]) -> dict[str, Any]:
        src = attrs.get("src") or attrs.get("data-src") or attrs.get("data-original") or ""
        lazy_attrs = ["data-src", "data-srcset", "data-lazy-src", "data-original", "data-echo"]
        classes = attrs.get("class", "")
        is_lazy = (
            attrs.get("loading", "").lower() == "lazy"
            or any(attrs.get(key) for key in lazy_attrs)
            or "lazy" in classes.lower()
            or "perfmatters" in " ".join(attrs.keys()).lower()
            or "ewww" in " ".join(attrs.keys()).lower()
        )
        width = attrs.get("width")
        height = attrs.get("height")
        return {
            "src": urljoin(self.base_url or "", src) if src else "",
            "alt": attrs.get("alt"),
            "width": width,
            "height": height,
            "loading": attrs.get("loading"),
            "srcset": attrs.get("srcset") or attrs.get("data-srcset"),
            "sizes": attrs.get("sizes"),
            "is_lazy": is_lazy,
            "cls_risk": not bool(width and height),
        }

    def _store_anchor(self, anchor: dict[str, Any]) -> None:
        href = anchor.get("href") or ""
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            return
        base_host = urlparse(self.base_url or "").netloc.lower()
        link_host = urlparse(href).netloc.lower()
        bucket = "internal" if not link_host or link_host == base_host else "external"
        self.result.links[bucket].append(anchor)


def parse_html(html: str, base_url: str | None = None) -> ParsedPage:
    parser = SEOHTMLParser(base_url)
    parser.feed(html or "")
    parser.close()
    return parser.result


def parse_json_ld_blocks(blocks: list[str]) -> list[dict[str, Any]]:
    parsed_items: list[dict[str, Any]] = []
    for block in blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError as exc:
            parsed_items.append({"error": f"Invalid JSON-LD: {exc}", "raw": block[:500]})
            continue
        parsed_items.extend(_expand_json_ld(data))
    return parsed_items


def _expand_json_ld(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        items: list[dict[str, Any]] = []
        for item in data:
            items.extend(_expand_json_ld(item))
        return items
    if not isinstance(data, dict):
        return [{"error": "JSON-LD block is not an object", "value": data}]
    graph = data.get("@graph")
    if isinstance(graph, list):
        return [item for item in graph if isinstance(item, dict)]
    return [data]


def _attrs_to_dict(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, value in attrs:
        if key:
            result[key.lower()] = value or ""
    return result


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()
