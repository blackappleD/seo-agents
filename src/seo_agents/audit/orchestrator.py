from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

from seo_agents.audit.scoring import SEVERITY_PENALTIES, score_findings, weighted_health_score
from seo_agents.fetch.crawler import discover_urls
from seo_agents.modules.content import analyze_content
from seo_agents.modules.ecommerce import analyze_ecommerce
from seo_agents.modules.external import offline_placeholder
from seo_agents.modules.geo import analyze_geo
from seo_agents.modules.hreflang import analyze_hreflang
from seo_agents.modules.images import analyze_images
from seo_agents.modules.local import analyze_local
from seo_agents.modules.page import analyze_page
from seo_agents.modules.schema import analyze_schema
from seo_agents.modules.technical import analyze_technical
from seo_agents.reports.markdown import (
    action_plan_markdown,
    audit_report_markdown,
    findings_markdown,
)


def run_audit(url: str, *, max_pages: int = 20, output_dir: str | None = None) -> dict:
    pages = discover_urls(url, max_pages=max_pages)
    if not pages:
        pages = [url]

    page_results = [analyze_page(page) for page in pages]
    technical_results = [analyze_technical(page) for page in pages[: min(len(pages), 5)]]
    content_results = [analyze_content(page) for page in pages[: min(len(pages), 5)]]
    schema_results = [analyze_schema(page) for page in pages[: min(len(pages), 5)]]
    image_results = [analyze_images(page) for page in pages[: min(len(pages), 5)]]
    geo_results = [analyze_geo(page) for page in pages[:1]]
    hreflang_results = [analyze_hreflang(page) for page in pages[: min(len(pages), 5)]]
    local_results = [analyze_local(page) for page in pages[:1]]
    ecommerce_results = [analyze_ecommerce(page) for page in pages[:1]]
    external_results = {
        provider: offline_placeholder(provider)
        for provider in ["google", "backlinks", "dataforseo", "firecrawl"]
    }

    categories = _build_categories(
        page_results,
        technical_results,
        content_results,
        schema_results,
        image_results,
        geo_results,
        hreflang_results,
        local_results,
        ecommerce_results,
        external_results,
    )
    all_findings = [finding for category in categories for finding in category["findings"]]
    top_findings = sorted(
        all_findings,
        key=lambda item: SEVERITY_PENALTIES.get(item.get("severity"), 0),
        reverse=True,
    )[:10]
    quick_wins = [
        item for item in all_findings if item.get("severity") in {"Medium", "Low"} and item not in top_findings
    ][:10]
    health_score = weighted_health_score(categories)
    audit_data = {
        "target": url,
        "summary": {
            "health_score": health_score,
            "business_type": _detect_business_type(page_results),
            "top_findings": top_findings,
            "quick_wins": quick_wins,
        },
        "categories": categories,
        "action_plan": _action_plan(top_findings, quick_wins),
        "artifacts": {
            "findings_dir": "findings/",
            "screenshots_dir": "screenshots/",
        },
        "pages_analyzed": pages,
        "raw_results": {
            "page": page_results,
            "technical": technical_results,
            "content": content_results,
            "schema": schema_results,
            "images": image_results,
            "geo": geo_results,
            "hreflang": hreflang_results,
            "local": local_results,
            "ecommerce": ecommerce_results,
            "external": external_results,
        },
    }
    artifact_dir = Path(output_dir or _default_output_dir(url))
    audit_data["artifacts"]["output_dir"] = str(artifact_dir)
    _write_artifacts(audit_data, str(artifact_dir))
    return audit_data


def _build_categories(
    page_results: list[dict],
    technical_results: list[dict],
    content_results: list[dict],
    schema_results: list[dict],
    image_results: list[dict],
    geo_results: list[dict],
    hreflang_results: list[dict],
    local_results: list[dict],
    ecommerce_results: list[dict],
    external_results: dict[str, dict],
) -> list[dict]:
    page_findings = [finding for result in page_results for finding in result["findings"]]
    technical_findings = [
        finding for result in technical_results for finding in result.get("findings", [])
    ]
    content_module_findings = [
        finding for result in content_results for finding in result.get("findings", [])
    ]
    schema_findings = [finding for result in schema_results for finding in result.get("findings", [])]
    image_findings = [finding for result in image_results for finding in result.get("findings", [])]
    geo_findings = [finding for result in geo_results for finding in result.get("findings", [])]
    hreflang_findings = [
        finding for result in hreflang_results for finding in result.get("findings", [])
    ]
    local_findings = [finding for result in local_results for finding in result.get("findings", [])]
    ecommerce_findings = [
        finding for result in ecommerce_results for finding in result.get("findings", [])
    ]
    external_findings = [
        {
            "title": f"{provider} 未配置" if not result.get("configured") else f"{provider} 已配置但未接入",
            "severity": "Info",
            "category": "External Data",
            "description": result["message"],
            "recommendation": "需要真实外部数据时，再配置凭据并接入 provider 客户端。",
            "evidence": {
                "status": result["status"],
                "mode": result["mode"],
                "configured": result.get("configured", False),
                "config_dir": result["config_dir"],
                "config": result.get("config", {}),
            },
            "affected_urls": [],
            "effort": None,
            "impact": None,
        }
        for provider, result in external_results.items()
    ]
    content_findings = [
        item for item in page_findings if item.get("category") == "Content Quality"
    ] + content_module_findings
    on_page_findings = [
        item
        for item in page_findings
        if item.get("category") in {"On-Page SEO", "Indexability", "Links", "Social Metadata"}
    ]
    structured_findings = [
        item
        for item in [*page_findings, *technical_findings, *schema_findings]
        if item.get("category") in {"Schema", "Structured Data"}
    ]
    performance_findings = [
        item
        for item in technical_findings
        if item.get("category") in {"Core Web Vitals", "JavaScript Rendering"}
    ]
    ai_findings = _ai_search_findings(page_results, schema_results) + geo_findings

    return [
        _category("Technical SEO", technical_findings),
        _category("Content Quality", content_findings),
        _category("On-Page SEO", on_page_findings),
        _category("Schema / Structured Data", structured_findings),
        _category("Performance / CWV", performance_findings),
        _category("AI Search Readiness", ai_findings),
        _category("Images", image_findings),
        _category("Hreflang / International SEO", hreflang_findings),
        _category("Local SEO", local_findings),
        _category("Ecommerce SEO", ecommerce_findings),
        _category("External Data Sources", external_findings),
    ]


def _category(name: str, findings: list[dict]) -> dict:
    return {
        "name": name,
        "score": score_findings(findings),
        "what_works": [] if findings else ["MVP 检查中未发现阻断性问题。"],
        "findings": findings,
    }


def _ai_search_findings(page_results: list[dict], schema_results: list[dict]) -> list[dict]:
    findings: list[dict] = []
    first = page_results[0] if page_results else {}
    parsed = first.get("parsed", {})
    if not parsed.get("schema"):
        findings.append(
            {
                "title": "Entity schema is missing",
                "severity": "Medium",
                "category": "AI Search Readiness",
                "description": "AI answer engines 更容易理解清晰的组织和页面实体。",
                "recommendation": "添加基于可见内容的 Organization/WebSite/WebPage schema。",
                "evidence": {"schema_count": 0},
                "affected_urls": [first.get("summary", {}).get("final_url", "")],
                "effort": None,
                "impact": None,
            }
        )
    if parsed.get("word_count", 0) < 500:
        findings.append(
            {
                "title": "Limited citation-ready text",
                "severity": "Low",
                "category": "AI Search Readiness",
                "description": "MVP 检查发现可用于段落级引用的可见文本偏少。",
                "recommendation": "在合适位置添加简洁定义、事实、示例和 FAQ 式段落。",
                "evidence": {"word_count": parsed.get("word_count", 0)},
                "affected_urls": [first.get("summary", {}).get("final_url", "")],
                "effort": None,
                "impact": None,
            }
        )
    for result in schema_results:
        for item in result.get("opportunities", []):
            if item.get("type") == "WebPage":
                findings.append(
                    {
                        "title": "WebPage schema opportunity",
                        "severity": "Info",
                        "category": "AI Search Readiness",
                        "description": "已生成 WebPage schema 草稿。",
                        "recommendation": "仅在它与可见内容一致时，审阅并添加该 schema。",
                        "evidence": {"schema": item.get("schema")},
                        "affected_urls": [result.get("snapshot", {}).get("final_url", "")],
                        "effort": None,
                        "impact": None,
                    }
                )
                break
    return findings


def _detect_business_type(page_results: list[dict]) -> str:
    schema_types = set()
    text = ""
    if page_results:
        parsed = page_results[0].get("parsed", {})
        text = parsed.get("text", "").lower()
        for schema in parsed.get("schema", []):
            schema_type = schema.get("@type")
            if isinstance(schema_type, list):
                schema_types.update(schema_type)
            elif schema_type:
                schema_types.add(schema_type)
    if "Product" in schema_types or any(word in text for word in ["cart", "checkout", "sku"]):
        return "ecommerce"
    if "LocalBusiness" in schema_types or any(word in text for word in ["address", "hours", "near me"]):
        return "local"
    if {"Article", "BlogPosting"} & schema_types:
        return "publisher"
    if any(word in text for word in ["pricing", "demo", "saas", "platform"]):
        return "saas"
    if "agency" in text:
        return "agency"
    return "other"


def _action_plan(top_findings: list[dict], quick_wins: list[dict]) -> dict:
    critical = [item for item in top_findings if item.get("severity") in {"Critical", "High"}]
    high_impact = [item for item in top_findings if item.get("severity") == "Medium"]
    return {
        "phases": [
            {"name": "Phase 1: 关键修复", "timeframe": "第 1 周", "items": critical},
            {
                "name": "Phase 2: 高影响改进",
                "timeframe": "第 2-3 周",
                "items": high_impact,
            },
            {"name": "Phase 3: 内容与权威", "timeframe": "第 2 个月", "items": quick_wins},
            {"name": "Phase 4: 监控与迭代", "timeframe": "持续", "items": []},
        ]
    }


def _write_artifacts(audit_data: dict, output_dir: str) -> Path:
    root = Path(output_dir)
    findings_dir = root / "findings"
    screenshots_dir = root / "screenshots"
    findings_dir.mkdir(parents=True, exist_ok=True)
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    (root / "audit-data.json").write_text(
        json.dumps(audit_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (root / "FULL-AUDIT-REPORT.md").write_text(audit_report_markdown(audit_data), encoding="utf-8")
    (root / "ACTION-PLAN.md").write_text(action_plan_markdown(audit_data), encoding="utf-8")
    for category in audit_data["categories"]:
        filename = category["name"].lower().replace(" / ", "-").replace(" ", "-")
        (findings_dir / f"{filename}.md").write_text(
            findings_markdown(category["name"], category["findings"]),
            encoding="utf-8",
        )
    return root


def _default_output_dir(url: str) -> str:
    host = urlparse(url).netloc or urlparse(url).path or "site"
    safe = "".join(char if char.isalnum() or char in {"-", "."} else "-" for char in host)
    return f"{safe}-audit"
