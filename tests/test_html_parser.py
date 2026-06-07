from __future__ import annotations

from seo_agents.extract.html import parse_html

SAMPLE_HTML = """
<!doctype html>
<html>
  <head>
    <title>Example SEO Page</title>
    <meta name="description" content="A practical page for SEO parser tests.">
    <meta name="robots" content="index,follow">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta property="og:title" content="OG title">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="canonical" href="/canonical">
    <link rel="alternate" hreflang="en-us" href="/en-us/">
    <script type="application/ld+json">
      {"@context":"https://schema.org","@graph":[
        {"@type":"Organization","name":"Acme","url":"https://example.com"},
        {"@type":"WebPage","name":"Example SEO Page","url":"https://example.com/canonical"}
      ]}
    </script>
  </head>
  <body>
    <h1>Main heading</h1>
    <h2>Section heading</h2>
    <h3>Nested heading</h3>
    <p>This parser extracts visible words and ignores script text.</p>
    <a href="/internal">Internal link</a>
    <a href="https://other.example/path" rel="nofollow"></a>
    <img src="/hero.jpg" alt="Hero" width="1200" height="600">
    <img data-src="/lazy.jpg" class="lazyload">
  </body>
</html>
"""


def test_parse_html_core_fields() -> None:
    parsed = parse_html(SAMPLE_HTML, base_url="https://example.com/page")
    assert parsed.title == "Example SEO Page"
    assert parsed.meta_description == "A practical page for SEO parser tests."
    assert parsed.meta_robots == "index,follow"
    assert parsed.viewport == "width=device-width, initial-scale=1"
    assert parsed.canonical == "https://example.com/canonical"
    assert parsed.h1 == ["Main heading"]
    assert parsed.h2 == ["Section heading"]
    assert parsed.h3 == ["Nested heading"]
    assert parsed.open_graph["og:title"] == "OG title"
    assert parsed.twitter_card["twitter:card"] == "summary_large_image"
    assert parsed.hreflang == [{"hreflang": "en-us", "href": "https://example.com/en-us/"}]


def test_parse_html_links_images_and_schema() -> None:
    parsed = parse_html(SAMPLE_HTML, base_url="https://example.com/page")
    assert len(parsed.links["internal"]) == 1
    assert len(parsed.links["external"]) == 1
    assert parsed.links["external"][0]["text"] == ""
    assert parsed.images[0]["cls_risk"] is False
    assert parsed.images[1]["is_lazy"] is True
    assert parsed.images[1]["cls_risk"] is True
    assert [item["@type"] for item in parsed.schema] == ["Organization", "WebPage"]
    assert parsed.word_count > 5


def test_parse_invalid_json_ld_reports_error() -> None:
    parsed = parse_html(
        '<script type="application/ld+json">{"@type": "Thing",}</script>',
        base_url="https://example.com",
    )
    assert parsed.schema[0]["error"].startswith("Invalid JSON-LD")
