---
name: seo-maps
description: >
  Maps intelligence playbook。用于 geo-grid、GBP audit、reviews、competitor
  radius 和本地地图可见性规划；当前无 `seo-agents maps` CLI。
user-invocable: true
argument-hint: "[command] [args]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Maps

当前保留为 Agent playbook，尚无 `seo-agents maps` CLI。

## 推荐流程

1. 明确 business name、地址、服务区域、主要品类和目标城市。
2. 运行 `seo-agents local <url> --json` 获取页面级 NAP/LocalBusiness 证据。
3. 如果需要 maps rank、reviews、competitor radius，标注当前项目未接入真实 Maps/GBP/DataForSEO Local API。
4. 输出人工检查清单：GBP 品类、NAP 一致性、服务项、照片、评论响应、门店页、local schema。

## 来源能力适配

来源中的 geo-grid、GBP audit、review intelligence、competitor radius、NAP verification 和 LocalBusiness schema generation 迁移为 playbook：

- Tier 0：基于页面、用户提供 GBP 信息和公开资料做人工清单。
- Tier 1：DataForSEO Local / Maps 数据需要未来接入或用户显式提供。
- Tier 2：Google Maps Platform / GBP API 当前未实现。

## 输出结构

- GBP completeness：名称、主/副品类、服务项、营业时间、照片、描述、属性。
- Geo-grid plan：关键词、中心点、半径、网格规模、成本/配额说明。
- Reviews：数量、评分、近期性、主题、回复率、风险信号。
- Competitors：半径、品类、差异化、本地内容和 citation 机会。
- NAP/schema：网站、GBP、引用源和 LocalBusiness JSON-LD 一致性。

## 可结合命令

```bash
seo-agents local <url> --json
seo-agents dataforseo setup --offline --json
```

## 按需引用

- `../seo/references/maps-geo-grid.md`
- `../seo/references/maps-gbp-checklist.md`
- `../seo/references/maps-api-endpoints.md`
- `../seo/references/maps-free-apis.md`

## 完成标准

- 无真实 API 时输出人工 audit 和执行计划，不输出虚假的 rank/review 数字。
- 如果用户提供 reviews/rank 导出，可据此做分析，并标注数据来源。
- 对多门店，先要求地点范围或分批策略，避免把一个门店结论套到所有门店。

## 错误处理

| 场景 | 处理 |
|---|---|
| business/location 不明确 | 请求更具体名称、地址或 GBP URL。 |
| 用户要求 geo-grid | 说明当前无 API，给采样设计和成本提示。 |
| reviews 数据缺失 | 输出评论获取和响应策略，不编造数量。 |
