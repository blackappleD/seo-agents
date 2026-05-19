from __future__ import annotations

from urllib.parse import urlparse, urlunparse

from seo_agents.extract.html import parse_html
from seo_agents.fetch.http import fetch_url
from seo_agents.fetch.render import render_page
from seo_agents.models import Finding, finding, score_from_findings, to_plain


def analyze_geo(url: str, *, render_mode: str = "auto") -> dict:
    snapshot = render_page(url, mode=render_mode)
    html = snapshot.rendered_html or snapshot.raw_html or ""
    parsed = parse_html(html, base_url=snapshot.final_url)
    origin = _origin(snapshot.final_url)
    robots_result = fetch_url(f"{origin}/robots.txt", timeout=10, max_bytes=500_000)
    llms_result = fetch_url(f"{origin}/llms.txt", timeout=10, max_bytes=500_000)
    llms_full_result = fetch_url(f"{origin}/llms-full.txt", timeout=10, max_bytes=500_000)
    findings: list[Finding] = []

    schema_types = _schema_types(parsed.schema)
    if not {"Organization", "WebSite", "WebPage", "Article", "BlogPosting"} & set(schema_types):
        findings.append(
            finding(
                "实体 Schema 支撑不足",
                "Medium",
                "AI Search Readiness",
                "页面缺少 Organization/WebSite/WebPage/Article 等实体结构化数据。",
                "补充与页面可见内容一致的实体 Schema，帮助 AI 搜索理解主体和页面类型。",
                evidence={"schema_types": schema_types},
                affected_urls=[snapshot.final_url],
            )
        )

    citation_blocks = _citation_ready_blocks(parsed.text)
    if len(citation_blocks) < 2:
        findings.append(
            finding(
                "可引用段落偏少",
                "Low",
                "AI Search Readiness",
                "页面缺少可独立引用的定义、数字、步骤或 FAQ 段落。",
                "增加短而完整的事实段落，让答案引擎能引用而不脱离上下文。",
                evidence={"citation_ready_blocks": len(citation_blocks)},
                affected_urls=[snapshot.final_url],
            )
        )

    if llms_result.status_code != 200 and llms_full_result.status_code != 200:
        findings.append(
            finding(
                "未发现 llms.txt",
                "Info",
                "AI Search Readiness",
                "站点根目录未发现 llms.txt 或 llms-full.txt。它不是排名必要条件，但可作为给 AI 工具的人类可读索引。",
                "如果站点有大量文档或产品说明，可添加 llms.txt；不要把它当作搜索排名保证。",
                evidence={
                    "llms_txt_status": llms_result.status_code,
                    "llms_full_txt_status": llms_full_result.status_code,
                },
                affected_urls=[origin],
            )
        )

    ai_crawler_blocked = _robots_blocks_ai(robots_result.content or "")
    if ai_crawler_blocked:
        findings.append(
            finding(
                "robots.txt 可能阻止 AI crawler",
                "Medium",
                "AI Search Readiness",
                "robots.txt 中存在针对常见 AI crawler 的 Disallow 规则。",
                "确认这是业务策略；如果希望进入 AI 搜索生态，需要允许对应 crawler 抓取可公开内容。",
                evidence={"robots_url": f"{origin}/robots.txt"},
                affected_urls=[origin],
            )
        )

    return {
        "command": "geo",
        "target": url,
        "score": score_from_findings(findings),
        "summary": {
            "final_url": snapshot.final_url,
            "schema_types": schema_types,
            "citation_ready_blocks": len(citation_blocks),
            "llms_txt_status": llms_result.status_code,
            "llms_full_txt_status": llms_full_result.status_code,
            "robots_status": robots_result.status_code,
        },
        "signals": {
            "ai_crawler_blocked": ai_crawler_blocked,
            "citation_blocks": citation_blocks[:5],
            "robots_error": robots_result.error,
            "llms_txt_error": llms_result.error,
        },
        "findings": to_plain(findings),
        "snapshot": to_plain(snapshot),
    }


def _origin(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))


def _schema_types(schemas: list[dict]) -> list[str]:
    types: list[str] = []
    for schema in schemas:
        schema_type = schema.get("@type")
        if isinstance(schema_type, list):
            types.extend(str(item) for item in schema_type)
        elif schema_type:
            types.append(str(schema_type))
    return types


def _citation_ready_blocks(text: str) -> list[str]:
    import re

    blocks = [block.strip() for block in re.split(r"\n+|(?<=[。.!?])\s+", text) if block.strip()]
    return [
        block
        for block in blocks
        if 35 <= len(re.findall(r"\w+", block, flags=re.UNICODE)) <= 180
        and re.search(r"\d|%|：|:|是指|定义|包括|means|refers", block, re.I)
    ]


def _robots_blocks_ai(robots: str) -> bool:
    lower = robots.lower()
    ai_agents = ["gptbot", "google-extended", "ccbot", "claudebot", "perplexitybot"]
    return any(agent in lower and "disallow: /" in lower for agent in ai_agents)
