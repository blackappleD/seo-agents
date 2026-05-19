from __future__ import annotations

import re

from seo_agents.extract.html import parse_html
from seo_agents.fetch.render import render_page
from seo_agents.models import Finding, finding, score_from_findings, to_plain

PHONE_RE = re.compile(r"(\+?\d[\d\s().-]{7,}\d)")
ADDRESS_RE = re.compile(r"\b(street|st\.|road|rd\.|avenue|ave\.|suite|floor|地址|路|街|号)\b", re.I)


def analyze_local(url: str, *, render_mode: str = "auto") -> dict:
    snapshot = render_page(url, mode=render_mode)
    html = snapshot.rendered_html or snapshot.raw_html or ""
    parsed = parse_html(html, base_url=snapshot.final_url)
    text = parsed.text
    lower_text = text.lower()
    schema_types = _schema_types(parsed.schema)
    phones = _extract_phones(text)
    has_address = bool(ADDRESS_RE.search(text))
    has_hours = any(word in lower_text for word in ["hours", "open", "营业", "时间", "mon", "monday"])
    has_gbp = "google.com/maps" in html.lower() or "google.com/business" in html.lower()
    findings: list[Finding] = []

    if not ("LocalBusiness" in schema_types or has_address or phones):
        findings.append(
            finding(
                "NAP 信号不足",
                "Medium",
                "Local SEO",
                "页面没有明显 Name/Address/Phone 本地商家信号。",
                "在本地业务页面展示名称、地址、电话，并保持与主要引用源一致。",
                evidence={"phones": phones[:3], "has_address": has_address},
                affected_urls=[snapshot.final_url],
            )
        )

    if "LocalBusiness" not in schema_types:
        findings.append(
            finding(
                "缺少 LocalBusiness schema",
                "Medium",
                "Local SEO",
                "页面未发现 LocalBusiness 结构化数据。",
                "为本地门店或服务区域页面添加与可见内容一致的 LocalBusiness schema。",
                evidence={"schema_types": schema_types},
                affected_urls=[snapshot.final_url],
            )
        )

    if not has_hours:
        findings.append(
            finding(
                "缺少营业时间或服务时间",
                "Low",
                "Local SEO",
                "页面没有明显营业时间、服务时间或可预约时间。",
                "补充营业时间、服务区域或预约方式。",
                evidence={"has_hours": has_hours},
                affected_urls=[snapshot.final_url],
            )
        )

    if not has_gbp:
        findings.append(
            finding(
                "未发现 Google Business Profile 或地图入口",
                "Info",
                "Local SEO",
                "页面没有明显 Google Maps/GBP 链接或嵌入。",
                "如果业务依赖本地搜索，可添加门店地图入口或 GBP 链接。",
                evidence={"has_gbp_link": False},
                affected_urls=[snapshot.final_url],
            )
        )

    return {
        "command": "local",
        "target": url,
        "score": score_from_findings(findings),
        "summary": {
            "final_url": snapshot.final_url,
            "phone_count": len(phones),
            "has_address": has_address,
            "has_hours": has_hours,
            "has_gbp_link": has_gbp,
            "schema_types": schema_types,
        },
        "findings": to_plain(findings),
        "snapshot": to_plain(snapshot),
    }


def _schema_types(schemas: list[dict]) -> list[str]:
    types: list[str] = []
    for schema in schemas:
        schema_type = schema.get("@type")
        if isinstance(schema_type, list):
            types.extend(str(item) for item in schema_type)
        elif schema_type:
            types.append(str(schema_type))
    return types


def _extract_phones(text: str) -> list[str]:
    phones: list[str] = []
    for candidate in PHONE_RE.findall(text):
        digits = re.sub(r"\D", "", candidate)
        if len(digits) < 10:
            continue
        phones.append(candidate.strip())
    return phones
