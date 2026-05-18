from __future__ import annotations

from seo_agents.models import Finding, ParsedPage, finding


def audit_images(parsed: ParsedPage) -> dict:
    images = parsed.images
    missing_alt = [image for image in images if not (image.get("alt") or "").strip()]
    missing_dimensions = [image for image in images if image.get("cls_risk")]
    lazy_count = [image for image in images if image.get("is_lazy")]
    responsive_count = [image for image in images if image.get("srcset") or image.get("sizes")]
    findings: list[Finding] = []

    if missing_alt:
        findings.append(
            finding(
                "图片缺少 alt text",
                "Medium",
                "Images",
                f"{len(missing_alt)} 张图片没有提供 alt text。",
                "为内容图片添加简洁描述性 alt；装饰图片可使用空 alt。",
                evidence={"count": len(missing_alt), "examples": missing_alt[:5]},
            )
        )
    if missing_dimensions:
        findings.append(
            finding(
                "图片可能导致 CLS",
                "Medium",
                "Images",
                f"{len(missing_dimensions)} 张图片缺少 width 或 height 属性。",
                "提供原始 width/height，或用 CSS aspect-ratio 预留空间。",
                evidence={"count": len(missing_dimensions), "examples": missing_dimensions[:5]},
            )
        )

    lcp_candidate = images[0] if images else None
    if lcp_candidate and lcp_candidate.get("is_lazy"):
        findings.append(
            finding(
                "疑似 LCP 图片被 lazy-load",
                "High",
                "Images",
                "文档中的第一张图片启用了 lazy-load，可能延迟 LCP。",
                "不要 lazy-load 首屏 hero/LCP 图片；可考虑 preload/fetchpriority。",
                evidence={"image": lcp_candidate},
            )
        )

    return {
        "summary": {
            "total": len(images),
            "missing_alt": len(missing_alt),
            "missing_dimensions": len(missing_dimensions),
            "lazy_loaded": len(lazy_count),
            "responsive": len(responsive_count),
        },
        "findings": findings,
        "images": images,
    }
