from __future__ import annotations

import gzip

from seo_agents.extract.sitemap import analyze_sitemap_xml, parse_sitemap_xml

URLSET = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2099-01-01</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
"""


def test_parse_urlset() -> None:
    parsed = parse_sitemap_xml(URLSET)
    assert parsed["type"] == "urlset"
    assert parsed["urls"][0]["loc"] == "https://example.com/"
    assert parsed["urls"][0]["priority"] == "0.8"


def test_analyze_urlset_warns_future_and_deprecated_fields() -> None:
    analyzed = analyze_sitemap_xml(URLSET)
    messages = [item["message"] for item in analyzed["warnings"]]
    assert "lastmod is in the future" in messages
    assert any("priority/changefreq" in message for message in messages)


def test_parse_sitemap_index() -> None:
    xml = """<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <sitemap><loc>https://example.com/sitemap-posts.xml</loc></sitemap>
    </sitemapindex>"""
    parsed = parse_sitemap_xml(xml)
    assert parsed["type"] == "sitemapindex"
    assert parsed["sitemaps"][0]["loc"] == "https://example.com/sitemap-posts.xml"


def test_parse_gzip_sitemap() -> None:
    parsed = parse_sitemap_xml(gzip.compress(URLSET.encode("utf-8")))
    assert parsed["type"] == "urlset"
    assert parsed["urls"][0]["loc"] == "https://example.com/"


def test_invalid_sitemap_returns_error() -> None:
    parsed = parse_sitemap_xml("<not-closed>")
    assert parsed["type"] == "unknown"
    assert parsed["errors"]
