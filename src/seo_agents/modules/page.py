from __future__ import annotations

from urllib.parse import urlparse

from seo_agents.extract.html import parse_html
from seo_agents.extract.images import audit_images
from seo_agents.extract.schema import validate_schema
from seo_agents.fetch.render import render_page
from seo_agents.models import Finding, finding, score_from_findings, to_plain


def analyze_page(url: str, *, render_mode: str = "auto") -> dict:
    snapshot = render_page(url, mode=render_mode)
    html = snapshot.rendered_html or snapshot.raw_html or ""
    parsed = parse_html(html, base_url=snapshot.final_url)
    findings: list[Finding] = []

    if snapshot.error:
        findings.append(
            finding(
                "页面无法抓取",
                "Critical",
                "Fetch",
                snapshot.error,
                "确认 URL 是公网可访问地址，且未被网络策略阻断。",
                evidence={"url": url},
                affected_urls=[url],
            )
        )
    if snapshot.status_code and snapshot.status_code >= 400:
        findings.append(
            finding(
                "页面返回错误状态码",
                "High",
                "Fetch",
                f"页面返回 HTTP {snapshot.status_code}。",
                "修复服务端路由，或将用户和 crawler 重定向到有效页面。",
                evidence={"status_code": snapshot.status_code},
                affected_urls=[snapshot.final_url],
            )
        )

    findings.extend(_title_findings(parsed.title, snapshot.final_url))
    findings.extend(_description_findings(parsed.meta_description, snapshot.final_url))
    findings.extend(_heading_findings(parsed.h1, snapshot.final_url))
    findings.extend(_canonical_findings(parsed.canonical, snapshot.final_url))
    findings.extend(_robots_findings(parsed.meta_robots, snapshot.final_url))
    findings.extend(_link_findings(parsed.links, snapshot.final_url))
    findings.extend(audit_images(parsed)["findings"])
    findings.extend(_schema_findings(parsed.schema, snapshot.final_url))
    findings.extend(_social_findings(parsed.open_graph, parsed.twitter_card, snapshot.final_url))
    findings.extend(_content_findings(parsed.word_count, snapshot.final_url))
    if snapshot.is_spa and snapshot.mode_used == "raw":
        findings.append(
            finding(
                "检测到 SPA 外壳但缺少渲染 HTML",
                "Medium",
                "JavaScript Rendering",
                "raw HTML 看起来是 JavaScript 应用外壳，但浏览器渲染不可用。",
                "安装 render extra 和 Playwright 浏览器，以便进行 SPA-aware audit。",
                evidence={"render_engine": snapshot.render_engine, "console_errors": snapshot.console_errors},
                affected_urls=[snapshot.final_url],
            )
        )

    score = score_from_findings(findings)
    return {
        "command": "page",
        "target": url,
        "score": score,
        "summary": {
            "status_code": snapshot.status_code,
            "final_url": snapshot.final_url,
            "finding_count": len(findings),
            "word_count": parsed.word_count,
            "is_spa": snapshot.is_spa,
            "mode_used": snapshot.mode_used,
        },
        "snapshot": to_plain(snapshot),
        "parsed": to_plain(parsed),
        "findings": to_plain(findings),
    }


def _title_findings(title: str | None, url: str) -> list[Finding]:
    if not title:
        return [
            finding(
                "缺少 title 标签",
                "High",
                "On-Page SEO",
                "页面没有暴露 title 标签。",
                "添加唯一且描述清晰的 title 标签。",
                evidence={"title": title},
                affected_urls=[url],
            )
        ]
    if len(title) > 65:
        return [
            finding(
                "title 标签过长",
                "Low",
                "On-Page SEO",
                f"title 长度为 {len(title)} 个字符。",
                "保持标题简洁，并把核心主题前置。",
                evidence={"title": title, "length": len(title)},
                affected_urls=[url],
            )
        ]
    if len(title) < 20:
        return [
            finding(
                "title 标签过短",
                "Low",
                "On-Page SEO",
                f"title 只有 {len(title)} 个字符。",
                "在保持自然的前提下，让标题更具描述性。",
                evidence={"title": title, "length": len(title)},
                affected_urls=[url],
            )
        ]
    return []


def _description_findings(description: str | None, url: str) -> list[Finding]:
    if not description:
        return [
            finding(
                "缺少 meta description",
                "Medium",
                "On-Page SEO",
                "页面没有 meta description。",
                "添加与搜索意图匹配、能提升点击意愿的简洁摘要。",
                evidence={"meta_description": description},
                affected_urls=[url],
            )
        ]
    if len(description) > 170:
        return [
            finding(
                "meta description 过长",
                "Low",
                "On-Page SEO",
                f"meta description 长度为 {len(description)} 个字符。",
                "压缩到最有吸引力的页面承诺和证据。",
                evidence={"length": len(description)},
                affected_urls=[url],
            )
        ]
    return []


def _heading_findings(h1: list[str], url: str) -> list[Finding]:
    if not h1:
        return [
            finding(
                "缺少 H1",
                "High",
                "On-Page SEO",
                "页面没有 H1 heading。",
                "添加一个清晰描述页面核心主题的 H1。",
                evidence={"h1": h1},
                affected_urls=[url],
            )
        ]
    if len(h1) > 1:
        return [
            finding(
                "存在多个 H1",
                "Medium",
                "On-Page SEO",
                f"页面有 {len(h1)} 个 H1 heading。",
                "保留一个主 H1，并将次级标题降级为 H2/H3。",
                evidence={"h1": h1},
                affected_urls=[url],
            )
        ]
    if h1[0].strip().isdigit():
        return [
            finding(
                "H1 描述性不足",
                "Medium",
                "On-Page SEO",
                "H1 看起来只有数字。",
                "替换为能描述页面主题的 heading。",
                evidence={"h1": h1[0]},
                affected_urls=[url],
            )
        ]
    return []


def _canonical_findings(canonical: str | None, final_url: str) -> list[Finding]:
    if not canonical:
        return [
            finding(
                "缺少 canonical URL",
                "Medium",
                "Indexability",
                "页面没有声明 canonical URL。",
                "除非页面故意 canonical 到其他地址，否则添加自引用 canonical。",
                evidence={"canonical": canonical},
                affected_urls=[final_url],
            )
        ]
    final_host = urlparse(final_url).netloc.lower()
    canonical_host = urlparse(canonical).netloc.lower()
    if canonical_host and canonical_host != final_host:
        return [
            finding(
                "canonical 指向其他 host",
                "High",
                "Indexability",
                "canonical URL 指向不同 host。",
                "确认跨域 canonical 是有意配置。",
                evidence={"canonical": canonical, "final_url": final_url},
                affected_urls=[final_url],
            )
        ]
    return []


def _robots_findings(meta_robots: str | None, url: str) -> list[Finding]:
    if meta_robots and "noindex" in meta_robots.lower():
        return [
            finding(
                "页面被标记为 noindex",
                "Critical",
                "Indexability",
                "robots meta 标签包含 noindex。",
                "如果页面应出现在搜索结果中，移除 noindex。",
                evidence={"meta_robots": meta_robots},
                affected_urls=[url],
            )
        ]
    return []


def _link_findings(links: dict, url: str) -> list[Finding]:
    all_links = [*links.get("internal", []), *links.get("external", [])]
    empty_anchor_count = sum(1 for item in all_links if not item.get("text"))
    findings: list[Finding] = []
    if empty_anchor_count:
        findings.append(
            finding(
                "链接缺少 anchor text",
                "Low",
                "Links",
                f"{empty_anchor_count} 个链接没有 anchor text。",
                "为重要链接添加描述性文本或可访问标签。",
                evidence={"count": empty_anchor_count},
                affected_urls=[url],
            )
        )
    return findings


def _schema_findings(schemas: list[dict], url: str) -> list[Finding]:
    if not schemas:
        return [
            finding(
                "未发现结构化数据",
                "Low",
                "Schema",
                "页面没有暴露 JSON-LD 结构化数据。",
                "添加能反映可见实体和页面类型的 schema。",
                evidence={"schema_count": 0},
                affected_urls=[url],
            )
        ]
    findings: list[Finding] = []
    for schema in schemas:
        findings.extend(validate_schema(schema, {"url": url}))
    return findings


def _social_findings(open_graph: dict, twitter_card: dict, url: str) -> list[Finding]:
    findings: list[Finding] = []
    if not open_graph.get("og:title") and not open_graph.get("og:description"):
        findings.append(
            finding(
                "Open Graph metadata 不完整",
                "Low",
                "Social Metadata",
                "页面没有暴露核心 Open Graph title/description metadata。",
                "添加 og:title 和 og:description，保证分享预览稳定。",
                evidence={"open_graph": open_graph},
                affected_urls=[url],
            )
        )
    if not twitter_card:
        findings.append(
            finding(
                "缺少 Twitter/X card metadata",
                "Info",
                "Social Metadata",
                "页面没有暴露 Twitter/X card metadata。",
                "如果社交分享预览重要，添加 twitter:card metadata。",
                evidence={"twitter_card": twitter_card},
                affected_urls=[url],
            )
        )
    return findings


def _content_findings(word_count: int, url: str) -> list[Finding]:
    if word_count < 300:
        return [
            finding(
                "薄内容风险",
                "Medium",
                "Content Quality",
                f"可见文本约 {word_count} 个词。",
                "添加有用、具体、能满足页面意图的内容。",
                evidence={"word_count": word_count},
                affected_urls=[url],
            )
        ]
    return []
