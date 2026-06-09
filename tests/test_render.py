from __future__ import annotations

from seo_agents.fetch.render import detect_spa_shell


def test_detect_spa_root_shell() -> None:
    assert detect_spa_shell('<html><body><div id="root"></div><script src="/app.js"></script></body></html>')


def test_detect_spa_next_shell() -> None:
    assert detect_spa_shell('<div id="__next"></div><script src="/_next/app.js"></script>')


def test_static_text_page_is_not_spa() -> None:
    html = "<html><body><main>" + "Useful visible copy. " * 120 + "</main></body></html>"
    assert detect_spa_shell(html) is False
