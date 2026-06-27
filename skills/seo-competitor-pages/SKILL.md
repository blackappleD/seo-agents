---
name: seo-competitor-pages
description: >
  竞品对比页规划 playbook。用于生成 alternative/comparison 页面策略、对比矩阵、
  差异化定位、Schema 和内部链接建议；当前无 `seo-agents competitor-pages` CLI。
user-invocable: true
argument-hint: "<url-or-topic>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Competitor Pages

当前保留为 Agent playbook，尚无 `seo-agents competitor-pages` CLI。

## 推荐流程

1. 明确自家产品、竞品、目标用户、使用场景和合规边界。
2. 对用户提供的页面运行 `seo-agents page/content/schema <url> --json`，提取事实证据。
3. 生成页面结构：定位、适合/不适合人群、功能对比、迁移成本、价格/限制、FAQ、CTA。
4. 标注哪些内容需要人工事实核查，避免编造竞品功能、价格或评价。
5. Schema 建议以 `WebPage`、`BreadcrumbList`、真实 FAQ 或 `Product` 为主，必须和可见内容一致。

## 页面类型

- `X vs Y`：适合高意图品牌对比，必须事实严谨、来源清楚。
- `Alternatives to X`：适合竞品替代方案，强调适合/不适合场景。
- `Best [category] tools`：适合 category intent，需披露评估标准。
- Migration page：适合从竞品迁移，强调成本、步骤、限制和风险。

## 输出结构

- Positioning：一句话定位、目标人群、主要差异点。
- Comparison matrix：功能、价格、集成、支持、安全/合规、适用场景。
- Proof：客户案例、截图、文档链接、公开价格和用户评价来源。
- SEO：title、meta、H1、FAQ、schema、内部链接和 CTA。
- Legal/fairness：避免虚假贬低、过期价格、未经证实性能对比。

## 可结合命令

```bash
seo-agents page <url> --json
seo-agents content <url> --json
seo-agents schema <url> --json
```

## 完成标准

- 只使用用户提供资料、公开页面证据或明确标注的假设。
- 每个竞品事实都要有“已验证/需核查”状态。
- 输出可落地的页面 brief，而不是泛泛营销文案。

## 错误处理

| 场景 | 处理 |
|---|---|
| 竞品资料不足 | 输出信息缺口清单，不补造功能或价格。 |
| 用户要求攻击性文案 | 改为事实型对比和适用场景差异。 |
| 竞品页面不可达 | 保留自家页面分析，标注竞品证据缺失。 |
