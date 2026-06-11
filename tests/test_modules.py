from __future__ import annotations

from seo_agents.models import PageSnapshot
from seo_agents.modules import content as content_module
from seo_agents.modules import ecommerce as ecommerce_module
from seo_agents.modules import geo as geo_module
from seo_agents.modules import hreflang as hreflang_module
from seo_agents.modules import images as images_module
from seo_agents.modules import local as local_module
from seo_agents.modules import page as page_module
from seo_agents.modules import schema as schema_module
from seo_agents.modules import technical as technical_module

HTML = """
<html>
<head>
  <title>Short</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://example.com/">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization"}</script>
  <link rel="alternate" hreflang="en-US" href="https://example.com/">
  <link rel="alternate" hreflang="x-default" href="https://example.com/">
</head>
<body>
  <h1>1</h1>
  <p>Thin copy. Updated 2026-06-24. Contact us for privacy terms.</p>
  <p>Local service address: 1 Main Street. Phone +1 555 123 4567. Open Monday.</p>
  <p>Product price $19.99 in stock with shipping and return policy.</p>
  <img src="/hero.jpg">
</body>
</html>
"""


def fake_snapshot() -> PageSnapshot:
    return PageSnapshot(
        url="https://example.com/",
        final_url="https://example.com/",
        status_code=200,
        raw_html=HTML,
        rendered_html=None,
        is_spa=False,
        extracted_text="Thin copy.",
        headers={"Content-Type": "text/html"},
    )


def test_page_module_outputs_findings(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(page_module, "render_page", lambda url, mode="auto": fake_snapshot())
    result = page_module.analyze_page("https://example.com/")
    titles = [item["title"] for item in result["findings"]]
    assert "title 标签过短" in titles
    assert "H1 描述性不足" in titles
    assert result["score"] < 100


def test_technical_module_outputs_categories(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(technical_module, "render_page", lambda url, mode="auto": fake_snapshot())
    result = technical_module.analyze_technical("https://example.com/")
    assert result["technical_score"] <= 100
    assert {category["name"] for category in result["categories"]} >= {"Security", "Mobile"}


def test_schema_module_outputs_opportunities(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(schema_module, "render_page", lambda url, mode="auto": fake_snapshot())
    result = schema_module.analyze_schema("https://example.com/")
    assert result["schema_count"] == 1
    assert result["findings"]
    assert any(item["type"] == "WebPage" for item in result["opportunities"])


def test_images_module_outputs_summary(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(images_module, "render_page", lambda url, mode="auto": fake_snapshot())
    result = images_module.analyze_images("https://example.com/")
    assert result["summary"]["total"] == 1
    assert result["summary"]["missing_alt"] == 1
    assert result["findings"]


def test_content_module_outputs_quality_signals(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(content_module, "render_page", lambda url, mode="auto": fake_snapshot())
    result = content_module.analyze_content("https://example.com/")
    assert result["command"] == "content"
    assert result["summary"]["word_count"] > 0
    assert any(item["title"] == "内容偏薄" for item in result["findings"])


def test_hreflang_module_validates_tags(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(hreflang_module, "render_page", lambda url, mode="auto": fake_snapshot())
    result = hreflang_module.analyze_hreflang("https://example.com/")
    assert result["summary"]["hreflang_count"] == 2
    assert result["summary"]["has_self_reference"] is True


def test_local_module_detects_local_signals(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(local_module, "render_page", lambda url, mode="auto": fake_snapshot())
    result = local_module.analyze_local("https://example.com/")
    assert result["summary"]["phone_count"] == 1
    assert result["summary"]["has_address"] is True


def test_ecommerce_module_detects_product_gaps(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(ecommerce_module, "render_page", lambda url, mode="auto": fake_snapshot())
    result = ecommerce_module.analyze_ecommerce("https://example.com/")
    assert result["summary"]["has_price"] is True
    assert any(item["title"] == "缺少 Product schema" for item in result["findings"])


def test_geo_module_uses_offline_fetch_signals(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    class FakeFetch:
        status_code = 404
        content = ""
        error = None

    monkeypatch.setattr(geo_module, "render_page", lambda url, mode="auto": fake_snapshot())
    monkeypatch.setattr(geo_module, "fetch_url", lambda *args, **kwargs: FakeFetch())
    result = geo_module.analyze_geo("https://example.com/")
    assert result["command"] == "geo"
    assert result["summary"]["llms_txt_status"] == 404
    assert any(item["title"] == "未发现 llms.txt" for item in result["findings"])
