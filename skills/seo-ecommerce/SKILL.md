---
name: seo-ecommerce
description: >
  Ecommerce SEO 基础检查。检测 Product/Offer/Rating/Review schema、价格、
  库存/可售状态、配送/退换政策信号，以及商品页 rich result 与转化信任基础。
user-invocable: true
argument-hint: "<url>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Ecommerce

运行：

```bash
seo-agents ecommerce <url> --json
```

## 当前检查

- `Product` schema 是否存在。
- `offers` / `Offer`、`aggregateRating`、`review` 字段或类型。
- 可见价格和币种信号。
- 库存/现货/缺货信号。
- shipping、return、refund 等政策信号。

## 建议规则

- Product schema 字段必须和可见商品内容一致。
- Offer 需要价格、币种、availability；不要从不可见或未知数据臆造。
- 商品页优先补价格、库存、图片、评价、配送/退换政策和面包屑。
- 当前 CLI 不调用 Merchant Center、marketplace 或 UCP API；引用资料只作为扩展背景。
- 来源中的 Google Shopping、Amazon、marketplace gap 分析需真实外部数据；本项目只能在用户显式使用 DataForSEO 或提供数据时辅助解读。

## 按需引用

- `references/marketplace-endpoints.md`
- `references/ucp-universal-commerce-protocol.md`

## 商品页评分维度

- Schema completeness：`Product`、`Offer`、priceCurrency、availability、rating/review、sku/gtin/mpn。
- Title / meta：商品核心词、品牌、型号、用途和差异点是否清晰。
- Images：商品图 alt、尺寸、首图 LCP、图片 schema / OG image。
- Content quality：唯一描述、规格、FAQ、对比、使用场景和退换/配送政策。
- Internal linking：breadcrumb、分类页、相关商品和购买指南。
- Technical：mobile、canonical、库存变体、分页/筛选和速度风险。

## 完成标准

- 输出商品页基础信号、schema 缺口、价格/库存/政策证据和优先级建议。
- 对不可见价格、评价或库存只标“缺失/不可验证”，不生成虚假字段。
- 若用户要求 marketplace intelligence，先说明当前无 Merchant Center/Amazon/Shopping API，需用户提供数据或显式 DataForSEO 查询。

## 错误处理

| 场景 | 处理 |
|---|---|
| 非商品页 | 说明检测结果，并建议用 `page/content/schema` 或提供商品页。 |
| 无 Product schema | 基于可见内容给最小 schema 草稿建议。 |
| 变体/多价格 | 建议清晰建模 Offer/AggregateOffer，并保持和可见选择器一致。 |
