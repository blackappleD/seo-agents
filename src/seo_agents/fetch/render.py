from __future__ import annotations

import re
import time

from seo_agents.extract.html import parse_html
from seo_agents.fetch.http import fetch_url
from seo_agents.models import PageSnapshot
from seo_agents.security.url_safety import URLSafetyError, validate_url_strict


def detect_spa_shell(html: str | None) -> bool:
    if not html:
        return False
    shell_patterns = [
        r"<div[^>]+id=['\"]root['\"][^>]*>\s*</div>",
        r"<div[^>]+id=['\"]__next['\"]",
        r"<div[^>]+id=['\"]app['\"][^>]*>\s*</div>",
        r"<div[^>]+id=['\"]__nuxt['\"]",
        r"data-svelte-h=",
        r"<astro-island\b",
    ]
    if any(re.search(pattern, html, re.I | re.S) for pattern in shell_patterns):
        return True
    parsed = parse_html(html)
    return parsed.word_count < 80 and bool(re.search(r"<script\b", html, re.I))


def render_page(url: str, *, mode: str = "auto", timeout: int = 15) -> PageSnapshot:
    if mode not in {"never", "auto", "always"}:
        raise ValueError("mode must be one of: never, auto, always")

    started = time.perf_counter()
    fetch_result = fetch_url(url, timeout=timeout)
    raw_html = fetch_result.content
    is_spa = detect_spa_shell(raw_html)
    console_errors: list[str] = []
    rendered_html: str | None = None
    render_engine = "raw"
    mode_used = "raw"

    should_render = mode == "always" or (mode == "auto" and is_spa)
    if should_render and fetch_result.error is None:
        rendered_html, console_errors = _render_with_playwright(fetch_result.final_url, timeout=timeout)
        if rendered_html:
            render_engine = "playwright-chromium"
            mode_used = "rendered"
        elif mode == "always":
            console_errors.append("Playwright 渲染不可用；已返回 raw HTML 降级结果")

    effective_html = rendered_html or raw_html
    parsed_text = parse_html(effective_html or "", base_url=fetch_result.final_url).text if effective_html else None
    render_ms = int((time.perf_counter() - started) * 1000)
    return PageSnapshot(
        url=url,
        final_url=fetch_result.final_url,
        status_code=fetch_result.status_code,
        raw_html=raw_html,
        rendered_html=rendered_html,
        is_spa=is_spa,
        extracted_text=parsed_text,
        headers=fetch_result.headers,
        console_errors=console_errors,
        redirect_chain=fetch_result.redirect_chain,
        render_engine=render_engine,
        render_ms=render_ms,
        mode_used=mode_used,
        error=fetch_result.error,
    )


def _render_with_playwright(url: str, *, timeout: int) -> tuple[str | None, list[str]]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None, ["未安装 Playwright"]

    console_errors: list[str] = []
    try:
        safe_url, _ = validate_url_strict(url)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()

            def route_handler(route, request):  # type: ignore[no-untyped-def]
                try:
                    validate_url_strict(request.url)
                except URLSafetyError:
                    route.abort()
                    return
                route.continue_()

            page.route("**/*", route_handler)
            page.on(
                "console",
                lambda message: console_errors.append(message.text)
                if message.type == "error"
                else None,
            )
            page.goto(safe_url, wait_until="networkidle", timeout=timeout * 1000)
            html = page.content()
            browser.close()
            return html, console_errors
    except Exception as exc:  # pragma: no cover - requires browser runtime
        console_errors.append(str(exc))
        return None, console_errors
