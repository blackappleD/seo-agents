from __future__ import annotations

import re

from seo_agents.extract.html import parse_html
from seo_agents.fetch.render import render_page
from seo_agents.models import Finding, finding, score_from_findings, to_plain

PRICE_RE = re.compile(r"([$€£¥]\s?\d+|\d+(?:\.\d{2})?\s?(USD|EUR|GBP|CNY|RMB))", re.I)


def analyze_ecommerce(url: str, *, render_mode: str = "auto") -> dict:
    snapshot = render_page(url, mode=render_mode)
    html = snapshot.rendered_html or snapshot.raw_html or ""
    parsed = parse_html(html, base_url=snapshot.final_url)
    lower_text = parsed.text.lower()
    schema_types = _schema_types(parsed.schema)
    has_product = "Product" in schema_types
    has_offer = _schema_has_key(parsed.schema, "offers") or "Offer" in schema_types
    has_rating = _schema_has_key(parsed.schema, "aggregateRating") or "AggregateRating" in schema_types
    has_review = _schema_has_key(parsed.schema, "review") or "Review" in schema_types
    has_price = bool(PRICE_RE.search(parsed.text))
    has_stock = any(word in lower_text for word in ["in stock", "out of stock", "库存", "现货", "缺货"])
    has_policy = any(word in lower_text for word in ["shipping", "return", "refund", "配送", "退货", "退款"])
    findings: list[Finding] = []

    if not has_product:
        findings.append(
            finding(
                "缺少 Product schema",
                "High",
                "Ecommerce SEO",
                "商品页未发现 Product 结构化数据。",
                "为商品页添加 Product schema，并确保名称、图片、描述与可见内容一致。",
                evidence={"schema_types": schema_types},
                affected_urls=[snapshot.final_url],
            )
        )
    if has_product and not has_offer:
        findings.append(
            finding(
                "Product schema 缺少 Offer",
                "High",
                "Ecommerce SEO",
                "商品结构化数据缺少价格/可售状态信息。",
                "补充 offers，包括 price、priceCurrency、availability。",
                evidence={"has_offer": has_offer},
                affected_urls=[snapshot.final_url],
            )
        )
    if not has_price:
        findings.append(
            finding(
                "页面缺少明显价格信号",
                "Medium",
                "Ecommerce SEO",
                "未在可见文本中发现价格或货币信号。",
                "在商品页清晰展示价格和币种，并同步到 Offer schema。",
                evidence={"price_detected": False},
                affected_urls=[snapshot.final_url],
            )
        )
    if not has_stock:
        findings.append(
            finding(
                "缺少库存/可售状态",
                "Medium",
                "Ecommerce SEO",
                "页面没有明显库存、现货或缺货状态。",
                "展示可售状态，并在 Offer schema 中使用 availability。",
                evidence={"stock_signal": False},
                affected_urls=[snapshot.final_url],
            )
        )
    if not has_policy:
        findings.append(
            finding(
                "缺少配送或退换政策信号",
                "Low",
                "Ecommerce SEO",
                "页面没有明显配送、退货或退款说明。",
                "补充 shipping/return policy，并在适用时扩展商品结构化数据。",
                evidence={"policy_signal": False},
                affected_urls=[snapshot.final_url],
            )
        )

    return {
        "command": "ecommerce",
        "target": url,
        "score": score_from_findings(findings),
        "summary": {
            "final_url": snapshot.final_url,
            "has_product_schema": has_product,
            "has_offer": has_offer,
            "has_rating": has_rating,
            "has_review": has_review,
            "has_price": has_price,
            "has_stock": has_stock,
            "has_policy": has_policy,
        },
        "findings": to_plain(findings),
        "snapshot": to_plain(snapshot),
    }


def _schema_types(schemas: list[dict]) -> list[str]:
    types: list[str] = []
    for schema in schemas:
        schema_type = schema.get("@type")
        if isinstance(schema_type, list):
            types.extend(str(item) for item in schema_type)
        elif schema_type:
            types.append(str(schema_type))
    return types


def _schema_has_key(schemas: list[dict], key: str) -> bool:
    return any(key in schema for schema in schemas if isinstance(schema, dict))
