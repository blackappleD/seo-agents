---
name: seo-content-brief
description: >
  SEO 内容简报生成 playbook。用于从 topic、keyword、URL 或 SERP 资料生成
  content brief、outline、页面类型要求、内部链接建议和 E-E-A-T 补强；当前无 CLI 入口。
user-invocable: true
argument-hint: "<topic-or-url>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Content Brief

当前保留为 Agent playbook，尚无 `seo-agents content-brief` CLI。

## 推荐流程

1. 明确 topic、目标读者、页面类型、国家/语言和转化目标。
2. 若输入 URL，运行 `seo-agents content <url> --json` 和 `seo-agents page <url> --json` 获取当前页面证据。
3. 若需要关键词扩展，可显式运行 DataForSEO，并提醒可能计费。
4. 输出 brief：search intent、标题角度、H1/H2/H3、必须回答的问题、E-E-A-T 证据、schema 建议、内部链接、避免事项。
5. 没有外部 SERP/keyword 数据时标注“离线占位”或“基于已提供资料”。

## 简报结构

- Search intent：主要意图、次要意图、用户阶段和页面类型。
- Audience：读者画像、痛点、决策标准和信任需求。
- Outline：H1、H2/H3、FAQ、表格/清单、示例和 CTA。
- Evidence requirements：作者/审核、案例、数据来源、截图、政策、价格或产品事实。
- SEO requirements：title、meta description、slug、schema、internal links、image/alt。
- Quality guardrails：避免关键词堆砌、空泛模板、未经证实的竞品声明和 AI 生成痕迹。

## 可结合命令

```bash
seo-agents content <url> --json
seo-agents page <url> --json
seo-agents dataforseo related-keywords "topic" --json
```

## 按需引用

- `references/page-type-templates.md`
- `references/keyword-density.md`
- `references/excluded-domains.md`

## 完成标准

- 简报要能交给写作者直接执行，不能只给主题列表。
- 每个 H2 至少说明写作目的和需要回答的问题。
- 需要外部 SERP/keyword 数据但未提供时，明确列为假设或待补数据。
- 对 YMYL、local、ecommerce、comparison 页面使用更高事实核查门槛。

## 错误处理

| 场景 | 处理 |
|---|---|
| URL 不可达 | 只基于 topic 做 brief，并说明缺少页面证据。 |
| 页面类型不明确 | 从关键词/URL/用户目标推断候选并标注。 |
| 竞品数据缺失 | 不编造竞品，输出可补充的数据清单。 |
