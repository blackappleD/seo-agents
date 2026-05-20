from __future__ import annotations


def audit_report_markdown(audit_data: dict) -> str:
    summary = audit_data["summary"]
    lines = [
        "# SEO 全站审计报告",
        "",
        f"目标：`{audit_data['target']}`",
        f"健康分：**{summary['health_score']} / 100**",
        f"业务类型：`{summary['business_type']}`",
        "",
        "## 最高优先级发现",
        "",
    ]
    if summary["top_findings"]:
        for item in summary["top_findings"]:
            lines.append(f"- **[{item['severity']}] {item['title']}**: {item['description']}")
    else:
        lines.append("- 未发现高优先级问题。")
    lines.extend(["", "## 快速改进项", ""])
    if summary["quick_wins"]:
        for item in summary["quick_wins"]:
            lines.append(f"- **{item['title']}**: {item['recommendation']}")
    else:
        lines.append("- 未发现明确快速改进项。")

    lines.extend(["", "## 分类发现", ""])
    for category in audit_data["categories"]:
        lines.append(f"### {category['name']} ({category['score']}/100)")
        if category.get("what_works"):
            for item in category["what_works"]:
                lines.append(f"- 已通过：{item}")
        if category.get("findings"):
            for item in category["findings"]:
                lines.append(f"- **[{item['severity']}] {item['title']}**: {item['recommendation']}")
        else:
            lines.append("- 未发现问题。")
        lines.append("")

    lines.extend(["## 已分析页面", ""])
    for page in audit_data.get("pages_analyzed", []):
        lines.append(f"- {page}")
    lines.append("")
    return "\n".join(lines)


def action_plan_markdown(audit_data: dict) -> str:
    lines = ["# SEO 行动计划", ""]
    for phase in audit_data["action_plan"]["phases"]:
        lines.append(f"## {phase['name']}")
        lines.append("")
        lines.append(f"时间范围：{phase['timeframe']}")
        lines.append("")
        if phase["items"]:
            for item in phase["items"]:
                lines.append(f"- **[{item['severity']}] {item['title']}**: {item['recommendation']}")
        else:
            lines.append("- 暂无事项。")
        lines.append("")
    return "\n".join(lines)


def findings_markdown(title: str, findings: list[dict]) -> str:
    lines = [f"# {title}", ""]
    if not findings:
        lines.append("未发现问题。")
        return "\n".join(lines)
    for item in findings:
        lines.extend(
            [
                f"## [{item['severity']}] {item['title']}",
                "",
                item["description"],
                "",
                f"建议：{item['recommendation']}",
                "",
                f"证据：`{item.get('evidence', {})}`",
                "",
            ]
        )
    return "\n".join(lines)
