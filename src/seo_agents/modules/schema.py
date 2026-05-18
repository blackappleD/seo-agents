from __future__ import annotations

from seo_agents.extract.html import parse_html
from seo_agents.extract.schema import generate_schema, validate_schema
from seo_agents.fetch.render import render_page
from seo_agents.models import to_plain


def analyze_schema(url: str, *, render_mode: str = "auto") -> dict:
    snapshot = render_page(url, mode=render_mode)
    html = snapshot.rendered_html or snapshot.raw_html or ""
    parsed = parse_html(html, base_url=snapshot.final_url)
    findings = []
    for schema in parsed.schema:
        findings.extend(validate_schema(schema, {"url": snapshot.final_url}))
    opportunities = _schema_opportunities(parsed)
    return {
        "command": "schema",
        "target": url,
        "schema_count": len(parsed.schema),
        "schemas": parsed.schema,
        "findings": to_plain(findings),
        "opportunities": opportunities,
        "snapshot": to_plain(snapshot),
    }


def _schema_opportunities(parsed) -> list[dict]:  # type: ignore[no-untyped-def]
    existing = {
        item.get("@type")
        for item in parsed.schema
        if isinstance(item, dict) and item.get("@type")
    }
    opportunities: list[dict] = []
    if "WebPage" not in existing:
        opportunities.append(
            {
                "type": "WebPage",
                "schema": generate_schema(
                    "WebPage",
                    {"name": parsed.title, "description": parsed.meta_description},
                ),
            }
        )
    if parsed.h1 and "BreadcrumbList" not in existing:
        opportunities.append(
            {
                "type": "BreadcrumbList",
                "schema": generate_schema(
                    "BreadcrumbList",
                    {"items": [{"name": parsed.h1[0], "url": ""}]},
                ),
            }
        )
    return opportunities
