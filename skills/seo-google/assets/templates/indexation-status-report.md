# 中文提示词卡：indexation status report

> 本文件是 `seo-agents` 的中文参考卡，用于补充检查方法、执行边界和输出要求。

## 使用场景

用于未来 Google 数据报告模板设计。当前项目未真实调用 Google API，报告中必须标注数据未配置或离线占位。

## 检查清单

- 先运行当前项目已有 CLI 获取证据，优先使用 --json。
- 判断结果时区分：已实现检查、人工判断、外部数据缺口、后续扩展能力。
- Google、Backlinks、Firecrawl 当前是离线占位；DataForSEO 默认真实 API，可能计费。
- 不编造搜索量、排名、流量、评论、外链、价格或竞品事实。

## 输出格式

- 用中文写 finding、说明和行动项。
- 保留必要英文术语，例如 canonical、hreflang、Schema、INP、GSC、GBP。
- 每条建议给出 evidence、impact、effort、dependency 和验证指标。
