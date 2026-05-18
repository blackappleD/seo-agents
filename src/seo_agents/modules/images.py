from __future__ import annotations

from seo_agents.extract.html import parse_html
from seo_agents.extract.images import audit_images
from seo_agents.fetch.render import render_page
from seo_agents.models import to_plain


def analyze_images(url: str, *, render_mode: str = "auto") -> dict:
    snapshot = render_page(url, mode=render_mode)
    html = snapshot.rendered_html or snapshot.raw_html or ""
    parsed = parse_html(html, base_url=snapshot.final_url)
    audit = audit_images(parsed)
    return {
        "command": "images",
        "target": url,
        "summary": audit["summary"],
        "images": audit["images"],
        "findings": to_plain(audit["findings"]),
        "snapshot": to_plain(snapshot),
    }
