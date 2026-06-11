from __future__ import annotations

from itertools import count
from pathlib import Path
from uuid import uuid4

from seo_agents.models import PageSnapshot
from seo_agents.modules import drift

ROOT = Path(__file__).resolve().parents[1]

HTML_A = """
<html>
<head>
  <title>Original title</title>
  <meta name="description" content="A">
  <link rel="canonical" href="https://example.com/a">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","name":"A","url":"https://example.com/a"}</script>
</head>
<body><h1>Original H1</h1><p>Body A</p></body>
</html>
"""

HTML_B = """
<html>
<head>
  <title>New title</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="https://other.example/b">
</head>
<body><p>Body B</p></body>
</html>
"""


def make_snapshot(html: str, status_code: int = 200) -> PageSnapshot:
    return PageSnapshot(
        url="https://example.com/a",
        final_url="https://example.com/a",
        status_code=status_code,
        raw_html=html,
        rendered_html=None,
        is_spa=False,
        extracted_text=None,
        headers={},
    )


def test_drift_baseline_compare_and_history(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    calls = count()

    def fake_render(url: str, mode: str = "auto") -> PageSnapshot:
        return make_snapshot(HTML_A if next(calls) == 0 else HTML_B, status_code=404)

    monkeypatch.setattr(drift, "render_page", fake_render)
    artifact_dir = ROOT / ".test-artifacts"
    artifact_dir.mkdir(exist_ok=True)
    db_path = artifact_dir / f"baselines-{uuid4().hex}.db"

    baseline = drift.create_baseline("https://example.com/a", db_path=db_path)
    assert baseline["status"] == "已建立基线"

    compared = drift.compare_to_baseline("https://example.com/a", db_path=db_path)
    titles = {item["title"] for item in compared["changes"]}
    assert "新增 noindex" in titles
    assert "canonical 发生变化" in titles
    assert "H1 消失" in titles
    assert any(item["severity"] == "Critical" for item in compared["changes"])

    history = drift.history("https://example.com/a", db_path=db_path)
    assert history["items"]
