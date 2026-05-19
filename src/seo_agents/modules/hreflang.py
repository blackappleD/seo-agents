from __future__ import annotations

import re
from urllib.parse import urlparse

from seo_agents.extract.html import parse_html
from seo_agents.fetch.render import render_page
from seo_agents.models import Finding, finding, score_from_findings, to_plain

LANG_RE = re.compile(r"^[a-z]{2,3}(-[A-Z]{2})?$")


def analyze_hreflang(url: str, *, render_mode: str = "auto") -> dict:
    snapshot = render_page(url, mode=render_mode)
    html = snapshot.rendered_html or snapshot.raw_html or ""
    parsed = parse_html(html, base_url=snapshot.final_url)
    tags = parsed.hreflang
    findings: list[Finding] = []

    if not tags:
        findings.append(
            finding(
                "未发现 hreflang",
                "Info",
                "Hreflang",
                "页面没有 hreflang 标签；如果站点没有多语言/多地区版本，这是可接受的。",
                "仅在存在语言或地区版本时添加 hreflang。",
                evidence={"hreflang_count": 0},
                affected_urls=[snapshot.final_url],
            )
        )
    invalid = [tag for tag in tags if not _valid_hreflang(tag.get("hreflang", ""))]
    if invalid:
        findings.append(
            finding(
                "hreflang 代码格式异常",
                "High",
                "Hreflang",
                "部分 hreflang 不符合 ISO 语言/地区格式或 x-default。",
                "使用类似 en、en-US、zh-CN 或 x-default 的格式。",
                evidence={"invalid": invalid},
                affected_urls=[snapshot.final_url],
            )
        )

    current = _strip_fragment(snapshot.final_url)
    has_self_reference = any(_strip_fragment(tag.get("href", "")) == current for tag in tags)
    if tags and not has_self_reference:
        findings.append(
            finding(
                "缺少 hreflang 自引用",
                "Medium",
                "Hreflang",
                "有 hreflang 标签，但没有指向当前页面自身语言版本的自引用。",
                "为当前 URL 添加对应语言版本的 hreflang 自引用。",
                evidence={"current_url": current, "hreflang": tags},
                affected_urls=[snapshot.final_url],
            )
        )

    has_x_default = any(tag.get("hreflang", "").lower() == "x-default" for tag in tags)
    if tags and not has_x_default:
        findings.append(
            finding(
                "缺少 x-default",
                "Low",
                "Hreflang",
                "多语言页面通常需要 x-default 指向默认落地页或语言选择页。",
                "在适合的默认页面上添加 x-default。",
                evidence={"hreflang_count": len(tags)},
                affected_urls=[snapshot.final_url],
            )
        )

    canonical_host = urlparse(parsed.canonical or snapshot.final_url).netloc.lower()
    mismatches = [
        tag
        for tag in tags
        if parsed.canonical and urlparse(tag.get("href", "")).netloc.lower() != canonical_host
    ]
    if mismatches:
        findings.append(
            finding(
                "canonical 与 hreflang 主机不一致",
                "Medium",
                "Hreflang",
                "部分 hreflang URL 与 canonical 主机不一致，可能是跨域策略，也可能是配置错误。",
                "确认跨域 hreflang 是否符合站点国际化架构。",
                evidence={"canonical": parsed.canonical, "mismatches": mismatches},
                affected_urls=[snapshot.final_url],
            )
        )

    return {
        "command": "hreflang",
        "target": url,
        "score": score_from_findings(findings),
        "summary": {
            "final_url": snapshot.final_url,
            "hreflang_count": len(tags),
            "has_self_reference": has_self_reference,
            "has_x_default": has_x_default,
            "invalid_count": len(invalid),
        },
        "hreflang": tags,
        "findings": to_plain(findings),
        "snapshot": to_plain(snapshot),
    }


def _valid_hreflang(value: str) -> bool:
    return value.lower() == "x-default" or bool(LANG_RE.match(value))


def _strip_fragment(url: str) -> str:
    parsed = urlparse(url)
    return parsed._replace(fragment="").geturl()
