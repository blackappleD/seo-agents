---
name: seo-local
description: >
  本地 SEO 基础检查。检测 NAP、LocalBusiness schema、营业时间/服务时间、
  Google Maps/GBP 链接，以及本地页面应具备的信任与服务区域信号。
user-invocable: true
argument-hint: "<url>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Local

运行：

```bash
seo-agents local <url> --json
```

## 当前检查

- 电话号码、地址模式、营业/服务时间。
- `LocalBusiness` schema。
- Google Maps 或 Google Business Profile 链接/嵌入。
- 页面级 NAP 信号是否足以支撑本地搜索理解。

## 建议规则

- NAP 建议要强调和 GBP、引用源、网站页脚/门店页保持一致。
- 多门店页面需关注唯一内容、服务区域和对应门店 schema。
- 当前 CLI 不调用 GBP API、不抓取 citation、不读取评论；这些只能作为手动检查或后续扩展。
- 行业垂直判断可参考页面信号：restaurant、healthcare、legal、home services、real estate、automotive 等，但不确定时必须让用户确认。

## 按需引用

- `../seo/references/local-seo-signals.md`
- `../seo/references/local-schema-types.md`
- `../seo/references/maps-gbp-checklist.md`

## 来源能力适配

来源中的 GBP audit、review intelligence、citation audit、map pack 和 geo-grid 能力在本项目没有真实 API。迁移后按三层处理：

- 页面级证据：运行 `seo-agents local <url> --json`。
- 人工清单：GBP 品类、服务项、照片、评论响应、NAP 一致性、门店页和本地 schema。
- 外部数据：标注未配置或后续扩展；需要真实 maps/reviews 时转 `seo-maps` playbook 或 DataForSEO 计费说明。

## 完成标准

- 输出 NAP、LocalBusiness schema、营业/服务时间、Google Maps/GBP 链接和本地信任信号。
- 对本地页面建议包含：服务区域、门店唯一内容、路线/停车/服务半径、评价入口和联系 CTA。
- 多门店或 location page 规模化时，结合 `quality-gates` 判断重复内容和 noindex 策略。

## 错误处理

| 场景 | 处理 |
|---|---|
| 页面无本地信号 | 询问或说明这可能不是 local business 页面。 |
| NAP 不完整 | 指出缺 phone/address/hours 中哪一项，并建议可见内容与 schema 同步。 |
| 行业不明确 | 给出候选行业和证据，不套用行业特定建议。 |
