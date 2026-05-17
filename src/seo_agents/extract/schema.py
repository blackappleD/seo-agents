from __future__ import annotations

from typing import Any

from seo_agents.models import Finding, finding

GOOGLE_SUPPORTED_TYPES = {
    "Article",
    "BlogPosting",
    "BreadcrumbList",
    "DiscussionForumPosting",
    "FAQPage",
    "LocalBusiness",
    "Organization",
    "Product",
    "ProfilePage",
    "QAPage",
    "WebPage",
    "WebSite",
}

REQUIRED_FIELDS: dict[str, set[str]] = {
    "Organization": {"name", "url"},
    "WebSite": {"name", "url"},
    "WebPage": {"name", "url"},
    "Article": {"headline"},
    "BlogPosting": {"headline"},
    "BreadcrumbList": {"itemListElement"},
    "Product": {"name"},
    "LocalBusiness": {"name", "address"},
    "FAQPage": {"mainEntity"},
    "QAPage": {"mainEntity"},
    "ProfilePage": {"mainEntity"},
}


def generate_schema(kind: str, data: dict[str, Any]) -> dict[str, Any]:
    schema_type = _normalize_schema_type(kind)
    schema: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": schema_type,
    }

    if schema_type == "FAQPage":
        schema["mainEntity"] = [
            {
                "@type": "Question",
                "name": item.get("question", ""),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item.get("answer", ""),
                },
            }
            for item in data.get("questions", [])
        ]
    elif schema_type == "BreadcrumbList":
        schema["itemListElement"] = [
            {
                "@type": "ListItem",
                "position": index + 1,
                "name": item.get("name", ""),
                "item": item.get("url", ""),
            }
            for index, item in enumerate(data.get("items", []))
        ]
    else:
        for key, value in data.items():
            if value is not None:
                schema[key] = value
    return schema


def validate_schema(schema: dict[str, Any], page_context: dict[str, Any] | None = None) -> list[Finding]:
    page_context = page_context or {}
    findings: list[Finding] = []
    if "error" in schema:
        findings.append(
            finding(
                "JSON-LD 无效",
                "High",
                "Schema",
                str(schema.get("error")),
                "修复 JSON-LD 语法，确保 parser 可以消费。",
                evidence={"raw": schema.get("raw", "")[:200]},
            )
        )
        return findings

    schema_type = schema.get("@type")
    if isinstance(schema_type, list):
        schema_type = schema_type[0] if schema_type else None
    if not schema.get("@context"):
        findings.append(
            finding(
                "Schema 缺少 @context",
                "Low",
                "Schema",
                "JSON-LD 应声明 @context，让消费者知道它使用 schema.org。",
                "添加 '@context': 'https://schema.org'。",
                evidence={"schema": schema},
            )
        )
    if not schema_type:
        findings.append(
            finding(
                "Schema 缺少 @type",
                "High",
                "Schema",
                "没有 @type 的 JSON-LD 对象无法被可靠解释。",
                "为页面添加最具体的 schema.org @type。",
                evidence={"schema": schema},
            )
        )
        return findings

    if schema_type not in GOOGLE_SUPPORTED_TYPES:
        findings.append(
            finding(
                "Schema 类型可能不会产生 Google rich result",
                "Info",
                "Schema",
                f"{schema_type} 是有效 schema.org 词汇，但不在 MVP 支持列表中。",
                "如果它能代表实体可以保留，但不要依赖它获得 rich-result 资格。",
                evidence={"type": schema_type},
            )
        )

    required = REQUIRED_FIELDS.get(str(schema_type), set())
    missing = sorted(field for field in required if not schema.get(field))
    if missing:
        findings.append(
            finding(
                "Schema 缺少推荐字段",
                "Medium",
                "Schema",
                f"{schema_type} 缺少字段：{', '.join(missing)}。",
                "从页面可见内容中补齐必需和推荐字段。",
                evidence={"type": schema_type, "missing": missing, "url": page_context.get("url")},
            )
        )

    if schema_type == "FAQPage":
        findings.append(
            finding(
                "FAQPage 的 Google rich-result 价值有限",
                "Info",
                "Schema",
                "FAQPage 仍可帮助 LLM 和结构化理解，但广泛 FAQ rich result 展示已弱化。",
                "仅对真实可见 FAQ 使用 FAQPage，不要承诺 Google FAQ rich result。",
                evidence={"type": schema_type},
            )
        )
    return findings


def _normalize_schema_type(kind: str) -> str:
    aliases = {
        "article": "Article",
        "blog": "BlogPosting",
        "blogposting": "BlogPosting",
        "breadcrumbs": "BreadcrumbList",
        "breadcrumb": "BreadcrumbList",
        "faq": "FAQPage",
        "local": "LocalBusiness",
        "organization": "Organization",
        "product": "Product",
        "profile": "ProfilePage",
        "qa": "QAPage",
        "webpage": "WebPage",
        "website": "WebSite",
    }
    return aliases.get(kind.lower().replace("_", "").replace("-", ""), kind)
