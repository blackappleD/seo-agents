# 外链质量评分参考

> 本文件是 `seo-agents` 的中文参考卡。命令名、API 名、Schema 类型和 JSON 字段保留英文；所有解释、边界和行动建议默认使用中文。

## 使用场景

用于在用户提供外链导出、第三方 backlink 数据或人工调查结果时，判断外链质量、锚文本风险、链接增长异常和是否需要清理。当前 `seo-agents backlinks` 只做离线配置检测，不抓取真实外链；没有外部数据时只能输出数据缺口和 provider 配置状态。

## 所需输入

优先使用可机器读取的外链明细，例如 CSV、JSON、表格或第三方 provider 导出。至少需要：

- `source_url`：外链来源页面。
- `target_url`：被链接页面。
- `anchor_text`：锚文本，空值也要保留。
- `referring_domain`：来源域名。
- `follow_type`：`follow` / `nofollow` / `sponsored` / `ugc`，如果未知则标注未知。
- `first_seen` / `last_seen`：用于判断 link velocity；没有时间字段时不要推断增长异常。
- 可选字段：来源page title、语言、国家/地区、出站链接数量、流量估算、索引状态、域名年龄、主题分类、provider 名称。

## 评分原则

- 优先看 referring domain 的主题相关性、真实流量迹象、语言/地区匹配和链接上下文，而不是单一 DA/DR 分。
- 每条风险判断必须有证据字段，例如来源页面特征、锚文本分布、出站链接数量、时间变化或人工截图备注。
- `nofollow` 链接通常 SEO 风险较低，但仍可能暴露品牌、声誉或垃圾引用问题。
- 不要把低权重等同于 toxic；低权重、真实相关的小站链接通常不需要清理。
- `disavow` 属于最后手段；先做证据核查、联系移除、确认是否存在 manual action 或明确负面 SEO 证据。

## Toxic Link Indicators

## 明确垃圾链接，建议自动标为高风险

1. 来源页面单页包含 `10,000+` 个出站链接。
2. 来源域名没有可验证的 Google 索引页面；只有在用户或 provider 提供索引证据时使用该判断。
3. 来源域名注册少于 `30` 天，但已有 `100+` 个出站链接。
4. `5+` 个无关域名同时使用完全匹配商业关键词锚文本。
5. 来自 doorway pages：内容薄、关键词堆砌、只为导流或排名存在。
6. 来自被入侵页面，例如 pharma/casino 注入、异常外链块或乱码模板。
7. 来自已知 PBN、link network、link farm；需要用户提供名单或 provider 证据。
8. 来自无关站点的全站 footer/sidebar 链接。
9. 来自自动生成或明显 spun articles。
10. 来源域名有明确 manual Google penalty 证据；没有证据时不要声称存在处罚。

## 疑似垃圾链接，需要人工复核

11. 来源域名出站链接占比超过 `90%`。
12. 语言明显不匹配，例如外语站点批量链接到中文/英文商业页，且上下文无合理关系。
13. 过期域名或拍卖域名被重新用于批量 link building。
14. 来源页面包含 `50+` 个出站链接，且缺少编辑上下文。
15. 来源站点没有真实流量迹象，例如停放页、模板站或只有广告页。
16. `10+` 个域名之间存在互惠链接、交叉链接或固定模板。
17. 来自内容极薄的 Web 2.0 properties。
18. 来自低质量 article directories 或已失去编辑价值的投稿目录。
19. 来自低质量 guest post networks。
20. 来源 niche 与目标业务完全无关，例如宠物站批量链接到 SaaS 商业页。

## 需要监控的潜在问题

21. 社交书签站点在短期内大规模出现。
22. 来自 forum profiles，而不是正常讨论帖或真实推荐。
23. 来自 press release syndication networks，且重复度高。
24. 来自 coupon/deal aggregators，且目标页不是优惠或商品页。
25. 来自通用目录，而不是行业相关目录。
26. 链接使用隐藏或不可见锚文本。
27. 来源页面存在 cloaked content。
28. 来源站点以薄 affiliate content 为主。
29. 评论区链接缺少编辑上下文或真实讨论。
30. 大量来源域名只提供 `nofollow` 链接；通常 SEO 价值有限，但不直接等同 toxic。

## 锚文本比例参考

这些比例是审计时的风险参考，不是硬性阈值。样本量过小、品牌词复杂、多语言站点、强 PR 事件或平台自然引用都会影响分布。

| 行业 | Branded | URL | Generic | Exact Match | Partial Match |
|---|---:|---:|---:|---:|---:|
| SaaS | 40-55% | 15-20% | 10-15% | 3-8% | 10-15% |
| E-commerce | 35-45% | 15-25% | 10-15% | 5-10% | 10-20% |
| Local Service | 45-60% | 10-15% | 15-20% | 5-10% | 5-10% |
| Publisher / Blog | 30-40% | 20-30% | 10-15% | 3-8% | 10-20% |
| Agency | 40-50% | 15-20% | 10-15% | 5-10% | 10-15% |

锚文本分类建议：

- `Branded`：品牌名、公司名、产品名。
- `URL`：裸 URL、域名、页面 URL。
- `Generic`：例如 click here、website、read more、了解更多。
- `Exact Match`：完全匹配目标商业关键词。
- `Partial Match`：包含目标关键词的一部分或语义变体。

## Link Velocity 风险信号

只有在输入包含 `first_seen`、`last_seen` 或按时间聚合的数据时，才能判断 link velocity。

| 模式 | 风险信号 | 建议动作 |
|---|---|---|
| 1 周内新增链接达到平时 `10x` | 可能是负面 SEO 或批量投放 | 核查来源、国家/地区、锚文本和页面模板，必要时准备 disavow 证据 |
| 1 个月内丢失 `50%+` 链接 | 可能有处罚、站点迁移、合作失效或 provider 采集变化 | 检查 GSC manual actions、重要来源页面状态和重定向 |
| `3+` 个月没有新增链接 | 内容或 PR 资产缺少自然引用 | 复盘内容策略、数字资产、合作和内链曝光 |
| 新增链接都来自同一 TLD 或同一模板 | 可能是协调式 link building | 检查来源域名 ownership、CMS 模板和 anchor pattern |
| 新增链接集中来自单一国家/地区且与业务无关 | 可能是 link network 活动 | 按国家、语言、主题相关性分组复核 |

## Disavow 判断

## 可以考虑 disavow 的情况

- GSC 出现 manual action，且问题明确指向 unnatural links。
- 有清晰证据显示负面 SEO 攻击，例如短期大量无关垃圾域名、重复锚文本、异常来源国家/地区。
- toxic link ratio 超过外链总量的 `10%`，且样本量足够、证据可复核。
- 已识别具体 PBN、link farm 或被入侵站点来源，并且无法移除。

## 不建议 disavow 的情况

- 只是低质量但 Google 很可能已忽略的零散链接。
- `nofollow`、`ugc`、`sponsored` 链接，除非存在品牌安全或明显垃圾攻击问题。
- 合法但低权重的小站链接。
- 垃圾链接占比低于 `2%`，且没有 manual action、排名异常或明显攻击证据。

## Disavow 文件格式示例

```txt
# Toxic domains identified by seo-agents backlink review
# Date: YYYY-MM-DD
# Evidence source: provider export / manual review / GSC
# Total domains disavowed: X
domain:spamsite1.com
domain:linkfarm2.net
domain:pbn-network3.xyz
```

## 本项目执行边界

- `seo-agents backlinks` 当前是离线占位，只检测配置，不联网抓取外链。
- Google、Backlinks、Firecrawl provider 命令不能在未实现真实接入时声称已经抓到数据。
- DataForSEO 相关命令默认真实接入，可能计费；只有用户明确要求并理解成本时再运行可能计费的命令。
- 如果用户只给 URL、没有外链导出，应输出“缺少 backlink 数据”，并建议提供 GSC、Ahrefs、Semrush、Majestic、DataForSEO 或其他 provider 导出。
- 不要编造 referring domains、spam score、toxic ratio、link velocity、manual action 或 disavow 域名。

## 输出要求

对每条外链至少输出：

| 字段 | 说明 |
|---|---|
| `source_url` | 外链来源页面 |
| `target_url` | 被链接页面 |
| `anchor_text` | 锚文本 |
| `referring_domain` | 来源域名 |
| `risk_level` | `high` / `medium` / `low` / `monitor` |
| `evidence` | 命中的风险规则和可复核证据 |
| `recommended_action` | 保留、监控、人工复核、联系移除、准备 disavow |

汇总时输出：

- 高风险域名数量和高风险链接数量。
- 锚文本分布与行业参考差异。
- link velocity 是否可判断；不可判断时说明缺少时间字段。
- disavow 是否建议，以及“不建议 disavow”的理由。
- 需要补充的数据源和下一步验证动作。
