from __future__ import annotations

from urllib.parse import urlparse

from seo_agents.extract.html import parse_html
from seo_agents.extract.schema import validate_schema
from seo_agents.fetch.render import render_page
from seo_agents.models import AuditCategory, Finding, finding, score_from_findings, to_plain


def analyze_technical(url: str, *, render_mode: str = "auto") -> dict:
    snapshot = render_page(url, mode=render_mode)
    html = snapshot.rendered_html or snapshot.raw_html or ""
    parsed = parse_html(html, base_url=snapshot.final_url)

    categories = [
        _crawlability(snapshot),
        _indexability(snapshot.final_url, parsed.meta_robots, parsed.canonical),
        _security(snapshot.final_url, snapshot.headers),
        _url_structure(snapshot.final_url, snapshot.redirect_chain),
        _mobile(parsed.viewport, snapshot.final_url),
        _structured_data(parsed.schema, snapshot.final_url),
        _javascript(snapshot),
        _core_web_vitals(snapshot.final_url),
        _indexnow(snapshot.final_url),
    ]
    score = round(sum(category.score for category in categories) / len(categories))
    return {
        "command": "technical",
        "target": url,
        "technical_score": score,
        "categories": to_plain(categories),
        "findings": to_plain([finding for category in categories for finding in category.findings]),
        "snapshot": to_plain(snapshot),
    }


def _category(name: str, findings: list[Finding], what_works: list[str] | None = None) -> AuditCategory:
    score = score_from_findings(findings)
    severities = {finding.severity for finding in findings}
    status = "fail" if severities & {"Critical", "High"} else "warn" if findings else "pass"
    return AuditCategory(name=name, score=score, findings=findings, what_works=what_works or [], status=status)


def _crawlability(snapshot) -> AuditCategory:  # type: ignore[no-untyped-def]
    findings: list[Finding] = []
    if snapshot.error:
        findings.append(
            finding(
                "抓取失败",
                "Critical",
                "Crawlability",
                snapshot.error,
                "确保页面公网可访问，且允许 crawler 抓取。",
                evidence={"url": snapshot.url},
                affected_urls=[snapshot.url],
            )
        )
    elif snapshot.status_code and snapshot.status_code >= 400:
        findings.append(
            finding(
                "crawler 收到错误状态码",
                "High",
                "Crawlability",
                f"HTTP 状态码为 {snapshot.status_code}。",
                "可索引页面应返回 200，或明确重定向到目标页面。",
                evidence={"status_code": snapshot.status_code},
                affected_urls=[snapshot.final_url],
            )
        )
    return _category("Crawlability", findings, ["页面返回了可抓取响应。"] if not findings else [])


def _indexability(final_url: str, robots: str | None, canonical: str | None) -> AuditCategory:
    findings: list[Finding] = []
    if robots and "noindex" in robots.lower():
        findings.append(
            finding(
                "Meta robots 包含 noindex",
                "Critical",
                "Indexability",
                "页面指示搜索引擎不要索引。",
                "如果页面需要参与排名，移除 noindex。",
                evidence={"robots": robots},
                affected_urls=[final_url],
            )
        )
    if not canonical:
        findings.append(
            finding(
                "缺少 canonical",
                "Medium",
                "Indexability",
                "未发现 canonical URL。",
                "添加 canonical 标签，减少重复 URL 歧义。",
                evidence={"canonical": canonical},
                affected_urls=[final_url],
            )
        )
    return _category("Indexability", findings)


def _security(final_url: str, headers: dict[str, str]) -> AuditCategory:
    findings: list[Finding] = []
    parsed = urlparse(final_url)
    lower_headers = {key.lower(): value for key, value in headers.items()}
    if parsed.scheme != "https":
        findings.append(
            finding(
                "页面未使用 HTTPS",
                "High",
                "Security",
                "最终 URL 没有使用 HTTPS。",
                "可索引页面应通过 HTTPS 提供。",
                evidence={"final_url": final_url},
                affected_urls=[final_url],
            )
        )
    if parsed.scheme == "https" and "strict-transport-security" not in lower_headers:
        findings.append(
            finding(
                "缺少 HSTS header",
                "Low",
                "Security",
                "页面使用 HTTPS，但未检测到 HSTS header。",
                "确认 HTTPS 覆盖完整后添加 Strict-Transport-Security。",
                evidence={"headers": headers},
                affected_urls=[final_url],
            )
        )
    if "content-security-policy" not in lower_headers:
        findings.append(
            finding(
                "缺少 Content-Security-Policy",
                "Low",
                "Security",
                "未检测到 CSP header。",
                "添加适合站点的 CSP，以降低注入风险。",
                evidence={"headers": headers},
                affected_urls=[final_url],
            )
        )
    if "x-frame-options" not in lower_headers and "content-security-policy" not in lower_headers:
        findings.append(
            finding(
                "缺少 frame 防护",
                "Low",
                "Security",
                "未检测到 X-Frame-Options 或 frame-ancestors 策略。",
                "按站点需要添加 CSP frame-ancestors 或 X-Frame-Options。",
                evidence={"headers": headers},
                affected_urls=[final_url],
            )
        )
    return _category("Security", findings)


def _url_structure(final_url: str, redirects: list[dict]) -> AuditCategory:
    findings: list[Finding] = []
    parsed = urlparse(final_url)
    if len(final_url) > 115:
        findings.append(
            finding(
                "URL 过长",
                "Low",
                "URL Structure",
                "最终 URL 超过 115 个字符。",
                "canonical 页面优先使用简洁、可读的 URL。",
                evidence={"length": len(final_url)},
                affected_urls=[final_url],
            )
        )
    if parsed.query:
        findings.append(
            finding(
                "canonical 页面使用 query 参数",
                "Low",
                "URL Structure",
                "最终 URL 包含 query string。",
                "确认 query 参数确有必要，并已正确 canonical。",
                evidence={"query": parsed.query},
                affected_urls=[final_url],
            )
        )
    if len(redirects) > 1:
        findings.append(
            finding(
                "redirect chain 超过一跳",
                "Medium",
                "URL Structure",
                f"请求经历了 {len(redirects)} 次 redirect。",
                "将 redirect chain 压缩为一跳。",
                evidence={"redirect_chain": redirects},
                affected_urls=[final_url],
            )
        )
    return _category("URL Structure", findings)


def _mobile(viewport: str | None, final_url: str) -> AuditCategory:
    findings = []
    if not viewport:
        findings.append(
            finding(
                "缺少 viewport meta 标签",
                "High",
                "Mobile",
                "未发现移动端 viewport 标签。",
                "添加 `<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">`。",
                evidence={"viewport": viewport},
                affected_urls=[final_url],
            )
        )
    return _category("Mobile", findings)


def _structured_data(schemas: list[dict], final_url: str) -> AuditCategory:
    findings: list[Finding] = []
    for schema in schemas:
        findings.extend(validate_schema(schema, {"url": final_url}))
    if not schemas:
        findings.append(
            finding(
                "缺少结构化数据",
                "Low",
                "Structured Data",
                "未发现 JSON-LD。",
                "添加与页面类型匹配的 schema.org JSON-LD。",
                evidence={"schema_count": 0},
                affected_urls=[final_url],
            )
        )
    return _category("Structured Data", findings)


def _javascript(snapshot) -> AuditCategory:  # type: ignore[no-untyped-def]
    findings: list[Finding] = []
    if snapshot.is_spa and snapshot.mode_used == "raw":
        findings.append(
            finding(
                "使用了 JavaScript 渲染降级",
                "Medium",
                "JavaScript Rendering",
                "页面看起来像 SPA 外壳，但无法获得渲染后 HTML。",
                "安装 Playwright 并启用渲染支持，对比 raw 与 rendered 内容。",
                evidence={"console_errors": snapshot.console_errors},
                affected_urls=[snapshot.final_url],
            )
        )
    return _category("JavaScript Rendering", findings)


def _core_web_vitals(final_url: str) -> AuditCategory:
    return _category(
        "Core Web Vitals",
        [],
        ["未使用 FID；配置 CrUX/PSI 后应以 INP 作为现代响应性指标。"],
    )


def _indexnow(final_url: str) -> AuditCategory:
    return _category(
        "IndexNow",
        [
            finding(
                "未验证 IndexNow 支持",
                "Info",
                "IndexNow",
                "MVP 尚未验证 IndexNow key 文件或提交 endpoint。",
                "当 Bing/Yandex/Naver 的新鲜度重要时，补充 IndexNow 验证。",
                evidence={"url": final_url},
                affected_urls=[final_url],
            )
        ],
    )
