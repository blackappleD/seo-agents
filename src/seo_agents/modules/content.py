from __future__ import annotations

import re

from seo_agents.extract.html import parse_html
from seo_agents.fetch.render import render_page
from seo_agents.models import Finding, finding, score_from_findings, to_plain

FILLER_PATTERNS = [
    "in today's digital landscape",
    "unlock your potential",
    "game changer",
    "cutting-edge",
    "seamless experience",
    "leverage the power",
]


def analyze_content(url: str, *, render_mode: str = "auto") -> dict:
    snapshot = render_page(url, mode=render_mode)
    html = snapshot.rendered_html or snapshot.raw_html or ""
    parsed = parse_html(html, base_url=snapshot.final_url)
    text = parsed.text
    lower_text = text.lower()
    findings: list[Finding] = []

    if parsed.word_count < 300:
        findings.append(
            finding(
                "内容偏薄",
                "Medium",
                "Content Quality",
                f"页面可见正文约 {parsed.word_count} 个词，可能不足以支撑搜索意图。",
                "补充真实经验、步骤、案例、数据或 FAQ 段落，让页面能独立回答核心问题。",
                evidence={"word_count": parsed.word_count},
                affected_urls=[snapshot.final_url],
            )
        )

    filler_hits = sorted(pattern for pattern in FILLER_PATTERNS if pattern in lower_text)
    if filler_hits:
        findings.append(
            finding(
                "存在低信息密度表达",
                "Low",
                "Content Quality",
                "页面命中了常见泛化营销短语，可能削弱内容可信度。",
                "用具体事实、功能、限制、数字和用户场景替换泛化表达。",
                evidence={"phrases": filler_hits},
                affected_urls=[snapshot.final_url],
            )
        )

    if not _has_author_signal(html, text):
        findings.append(
            finding(
                "作者或责任主体不清晰",
                "Medium",
                "E-E-A-T",
                "页面没有明显作者、编辑者、公司或责任主体信号。",
                "添加作者/组织信息、简介页链接或编辑责任说明。",
                evidence={"signals_checked": ["author", "byline", "Organization"]},
                affected_urls=[snapshot.final_url],
            )
        )

    if not _has_date_signal(html, text):
        findings.append(
            finding(
                "缺少发布时间或更新时间",
                "Low",
                "Content Freshness",
                "页面没有明显日期信号，用户和搜索系统难以判断内容新鲜度。",
                "为需要时效性的内容添加发布日期或最近更新时间。",
                evidence={"date_detected": False},
                affected_urls=[snapshot.final_url],
            )
        )

    if not _has_trust_signal(lower_text, parsed.schema):
        findings.append(
            finding(
                "信任信号不足",
                "Medium",
                "Trustworthiness",
                "页面没有明显联系方式、隐私政策、退款/服务条款或组织结构化数据。",
                "补充可验证的联系、政策和组织实体信息。",
                evidence={"schema_types": _schema_types(parsed.schema)},
                affected_urls=[snapshot.final_url],
            )
        )

    citation_blocks = _citation_ready_blocks(text)
    if not citation_blocks:
        findings.append(
            finding(
                "缺少可引用段落",
                "Low",
                "AI Citation Readiness",
                "未发现长度适中、可独立引用且包含事实/定义/数字的段落。",
                "增加自包含定义、步骤、数据点、表格或 FAQ 式答案块。",
                evidence={"citation_ready_blocks": 0},
                affected_urls=[snapshot.final_url],
            )
        )

    return {
        "command": "content",
        "target": url,
        "score": score_from_findings(findings),
        "summary": {
            "word_count": parsed.word_count,
            "filler_hits": len(filler_hits),
            "citation_ready_blocks": len(citation_blocks),
            "final_url": snapshot.final_url,
        },
        "signals": {
            "has_author": _has_author_signal(html, text),
            "has_date": _has_date_signal(html, text),
            "has_trust": _has_trust_signal(lower_text, parsed.schema),
            "citation_blocks": citation_blocks[:5],
        },
        "findings": to_plain(findings),
        "snapshot": to_plain(snapshot),
    }


def _has_author_signal(html: str, text: str) -> bool:
    lower = f"{html} {text}".lower()
    return any(signal in lower for signal in ["author", "byline", "作者", "编辑", "reviewed by"])


def _has_date_signal(html: str, text: str) -> bool:
    if re.search(r"\b20\d{2}[-/年.]\d{1,2}[-/月.]\d{1,2}", html + text):
        return True
    return any(signal in (html + text).lower() for signal in ["published", "updated", "更新", "发布"])


def _has_trust_signal(lower_text: str, schemas: list[dict]) -> bool:
    trust_words = ["contact", "privacy", "terms", "refund", "about", "联系", "隐私", "条款", "退款", "关于"]
    if any(word in lower_text for word in trust_words):
        return True
    return bool({"Organization", "LocalBusiness"} & set(_schema_types(schemas)))


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
    blocks = [block.strip() for block in re.split(r"\n+|(?<=[。.!?])\s+", text) if block.strip()]
    ready: list[str] = []
    for block in blocks:
        words = re.findall(r"\w+", block, flags=re.UNICODE)
        has_fact_signal = bool(re.search(r"\d|%|：|:| because | means | refers to |是指|定义|包括", block, re.I))
        if 40 <= len(words) <= 180 and has_fact_signal:
            ready.append(block)
    return ready
