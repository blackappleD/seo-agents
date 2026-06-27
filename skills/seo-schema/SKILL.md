---
name: seo-schema
description: >
  Schema 检测、验证和生成建议。解析 JSON-LD，检查 @context、@type、Google
  常见 rich result 类型和推荐字段，并生成 WebPage/BreadcrumbList 草稿机会。
user-invocable: true
argument-hint: "<url>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Schema

运行：

```bash
seo-agents schema <url> --json
```

## 当前能力

- 从 raw/rendered HTML 中提取 JSON-LD。
- 对无效 JSON-LD、缺少 `@context`、缺少 `@type`、缺少推荐字段生成 finding。
- 支持常见类型：`Organization`、`WebSite`、`WebPage`、`Article`、`BlogPosting`、`BreadcrumbList`、`Product`、`LocalBusiness`、`FAQPage`、`QAPage`、`ProfilePage` 等。
- 当页面缺少 `WebPage` 或 `BreadcrumbList` 时，在 `opportunities` 中生成草稿。

## 使用规则

- 只建议添加与页面可见内容一致的 schema。
- 不要把 schema 当作排名保证；优先用于实体理解、rich result 资格和 AI 可读性。
- `FAQPage` 可保留其结构化理解价值，但不要承诺 Google FAQ rich result。
- 生成的 schema 草稿需要人工审阅字段、URL、实体关系和内容一致性。
- 来源中的 Microdata/RDFa 检测能力在当前 CLI 中未实现；本项目主要解析 JSON-LD。

## 按需引用

- `../seo/references/schema-types.md`：Schema 类型与适用页面。
- `references/deprecated-types-2024-2026.md`：弃用或价值下降类型的提醒。

## 生成建议

- 通用页面优先建议 `WebPage`、`BreadcrumbList`、`Organization` 或 `WebSite`。
- 文章页使用 `Article` / `BlogPosting`，必须有 headline、author/publisher、datePublished/dateModified 和 image 候选。
- 本地业务页使用 `LocalBusiness` 子类型时，字段要和可见 NAP、营业时间和服务区域一致。
- 商品页使用 `Product` / `Offer`，不得臆造价格、库存、评分或评论。

## 完成标准

- 输出现有 schema 列表、验证问题、推荐新增类型和 JSON-LD 草稿机会。
- 每个草稿都要说明来自页面的证据字段，以及哪些字段需要人工补齐。
- 发现弃用或 rich result 价值下降类型时，说明“可保留实体理解价值”或“建议移除/替换”的理由。

## 错误处理

| 场景 | 处理 |
|---|---|
| 无 JSON-LD | 根据页面类型给新增建议，不说“schema 全无价值”。 |
| JSON-LD 语法错误 | 报告解析错误，必要时给最小修复草稿。 |
| schema 与可见内容冲突 | 优先建议修改 schema 或页面内容保持一致。 |
| 用户要求保证 rich result | 明确不能保证，只能提升资格和可读性。 |
