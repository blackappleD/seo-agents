---
name: seo-programmatic
description: >
  Programmatic SEO 规划 playbook。用于模板化页面、数据源、索引控制、质量门槛、
  内链和规模化内容风险评估；当前无 `seo-agents programmatic` CLI。
user-invocable: true
argument-hint: "[url|plan]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Programmatic

当前保留为 Agent playbook，尚无 `seo-agents programmatic` CLI。

## 推荐流程

1. 明确页面规模、数据源、模板变量、目标搜索意图和差异化内容。
2. 对样板页运行 `seo-agents page/content/schema <url> --json`。
3. 使用 `quality-gates` 判断薄内容、重复内容和 location/keyword 页面规模风险。
4. 输出页面模板字段、唯一内容要求、index/noindex 规则、canonical、sitemap、internal links 和监控指标。
5. 规模化页面未达质量门槛时，建议先 noindex、分批发布或缩小范围。

## 评估维度

- Data source：来源、更新频率、唯一字段、缺失率、版权/许可。
- Template uniqueness：每页独有描述、示例、图片、FAQ、评价、统计或地点信息。
- URL pattern：短、稳定、可解释，避免参数页泛滥。
- Internal linking：hub、facets、breadcrumbs、相邻页、热门页和孤岛页治理。
- Index management：noindex 规则、canonical、sitemap inclusion、分批发布和 drift 监控。
- Scaled content abuse：页面是否为用户任务服务，而不是只替换关键词/城市名。

## 可结合命令

```bash
seo-agents page <url> --json
seo-agents content <url> --json
seo-agents sitemap <url> --json
```

按需读取 `../seo/references/quality-gates.md`。

## 完成标准

- 输出 programmatic SEO score 或风险等级、模板字段、质量门槛、发布策略和监控计划。
- 对 100+ 未审查页面、500+ 无明确价值页面、唯一内容低于阈值的情况给出强警告。
- 不建议大规模 index 低价值页面；优先 noindex、合并、补唯一内容或缩小范围。

## 错误处理

| 场景 | 处理 |
|---|---|
| 未发现 programmatic 页面 | 说明没有模板/规模化迹象，并建议用户提供样板 URL 或数据模型。 |
| 数据源不可信 | 建议暂停 index 计划，先补数据质量和人工审核。 |
| 页面过多且无质量证据 | 输出 hard stop 建议，需要用户确认后再继续规划。 |
