from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from seo_agents.audit import orchestrator

ROOT = Path(__file__).resolve().parents[1]
PROVIDER_ENV_KEYS = [
    "GOOGLE_APPLICATION_CREDENTIALS",
    "GOOGLE_API_KEY",
    "GA4_PROPERTY_ID",
    "GSC_PROPERTY",
    "MOZ_API_KEY",
    "BING_WEBMASTER_API_KEY",
    "DATAFORSEO_USERNAME",
    "DATAFORSEO_PASSWORD",
    "FIRECRAWL_API_KEY",
]


def test_run_audit_writes_contract(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    page_result = {
        "findings": [
            {
                "title": "Missing meta description",
                "severity": "Medium",
                "category": "On-Page SEO",
                "description": "Missing.",
                "recommendation": "Add it.",
                "evidence": {},
                "affected_urls": ["https://example.com/"],
                "effort": None,
                "impact": None,
            }
        ],
        "summary": {"final_url": "https://example.com/"},
        "parsed": {"schema": [], "word_count": 100, "text": "pricing platform"},
    }
    technical_result = {
        "findings": [],
        "categories": [],
    }
    schema_result = {
        "findings": [],
        "opportunities": [{"type": "WebPage", "schema": {"@type": "WebPage"}}],
        "snapshot": {"final_url": "https://example.com/"},
    }
    image_result = {"findings": []}
    module_result = {"findings": []}
    monkeypatch.setattr(orchestrator, "discover_urls", lambda url, max_pages=20: ["https://example.com/"])
    monkeypatch.setattr(orchestrator, "analyze_page", lambda url: page_result)
    monkeypatch.setattr(orchestrator, "analyze_technical", lambda url: technical_result)
    monkeypatch.setattr(orchestrator, "analyze_content", lambda url: module_result)
    monkeypatch.setattr(orchestrator, "analyze_schema", lambda url: schema_result)
    monkeypatch.setattr(orchestrator, "analyze_images", lambda url: image_result)
    monkeypatch.setattr(orchestrator, "analyze_geo", lambda url: module_result)
    monkeypatch.setattr(orchestrator, "analyze_hreflang", lambda url: module_result)
    monkeypatch.setattr(orchestrator, "analyze_local", lambda url: module_result)
    monkeypatch.setattr(orchestrator, "analyze_ecommerce", lambda url: module_result)
    for key in PROVIDER_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)

    output_dir = ROOT / ".test-artifacts" / f"example.com-audit-{uuid4().hex}"
    monkeypatch.setenv("SEO_AGENTS_CONFIG_DIR", str(output_dir / "config"))
    monkeypatch.setenv("SEO_AGENTS_CLAUDE_SETTINGS", str(output_dir / "settings.json"))
    result = orchestrator.run_audit("https://example.com/", output_dir=str(output_dir))
    assert result["summary"]["health_score"] < 100
    assert result["summary"]["business_type"] == "saas"
    assert (output_dir / "FULL-AUDIT-REPORT.md").exists()
    data_path = output_dir / "audit-data.json"
    assert data_path.exists()
    saved = json.loads(data_path.read_text(encoding="utf-8"))
    assert saved["action_plan"]["phases"][0]["name"] == "Phase 1: 关键修复"
    assert saved["categories"]
    assert "external" in saved["raw_results"]
    external_category = next(item for item in saved["categories"] if item["name"] == "External Data Sources")
    assert any("未配置" in item["title"] for item in external_category["findings"])
    assert all(item["evidence"]["mode"] == "offline-placeholder" for item in external_category["findings"])
