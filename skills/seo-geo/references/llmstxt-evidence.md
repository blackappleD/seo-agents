# `/llms.txt` — 基于证据的重构（2026 年 5 月）

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 长篇大论；博士

`/llms.txt` **目前没有被任何主要的人工智能搜索系统使用**。
无论如何生成一个作为低成本选项，但不要将其呈现为
任何 seo-agents 报告中的排名或引用杠杆。

## 主要来源证据

|来源 |日期 |他们说什么 |
|---|---|---|
| **约翰·穆勒** (Google) — Reddit + Bluesky | 2025 | 2025 “目前没有人工智能系统使用 llms.txt。”将该文件与已弃用的元关键字进行比较。 |
| **加里·伊利斯** (Google) — 搜索中心直播 | 2025 年 7 月 | Google 没有计划支持 llms.txt。 |
| **SE 排名** — 30 万域研究 | 2025 年 11 月 |在 50 个人工智能引用最多的域名中，**只有一个**具有 `/llms.txt`。 |
| **OtterlyAI** — 服务器日志审计 | 2025 | 2025 **0.1%** 的 AI 机器人流量目标为 `/llms.txt`（62,100 个请求中的 84 个）。 |
| **Anthropic、Stripe、Cloudflare、NVIDIA** — 已发布文件 | 2024–2025 |全部发布 `llms.txt`。 **没有**表示他们的爬虫会消耗第三方 `llms.txt` 文件。 |

## 重要的地方

`llms.txt` 越来越多地被 **AI 编码代理** 使用（光标、
继续，Cline，当前 Agent Code）加载每个库的文档时。
Mintlify 为数千人自动生成 `/llms.txt` 和 `/llms-full.txt`
开发人员文档网站。对于开发人员工具网站，发布
`llms.txt` 是一个净胜——它可以帮助代理准确地引用文档。

对于非开发者商业网站，该值纯粹是防御性的：零
成本，如果主要的人工智能提供商最终成为未来可能的选择
采用它。

## seo-agents 如何对待 `llms.txt`

- `seo-geo` 审核 **报告 `/llms.txt` 和 `/llms-full.txt` 的存在**。
- 审核记录文件是否格式良好（Mintlify 风格的降价）。
- 审计明确**不**为其分配引文排名权重。
- 如果用户要求生成一个，seo-agents 会生成一个最小的有效
  示例和横幅指出“没有主要的 LLM 提供商已确认
  截至 2026 年 5 月的消费量；发布是为了选择，而不是为了引用”。

## 当本指南发生变化时

在以下情况下更新此文件（以及 seo-geo 审核副本）：

- 任何主要的人工智能搜索系统（Google AI Overviews、ChatGPT Search、
  Perplexity，Bing Copilot）发布文档确认
  `llms.txt` 消耗。
- OtterlyAI 或 SE Ranking 发布了一项后续研究，显示了可衡量的
  `/llms.txt` 请求率的变化。
- John Mueller / Gary Illyes / 同等人士撤回了他们的 2025 年声明。

最后验证时间：2026 年 5 月 17 日。

## 本项目适配边界

- 优先使用当前已实现的 `seo-agents` CLI 获取证据；没有 CLI 的能力作为 Agent playbook 或后续扩展处理。
- 不把外部数据源、付费 provider、浏览器渲染或地图 API 写成已执行，除非当前任务确实运行并取得证据。
- 每个 finding 必须有可复核 evidence；数据缺失时明确写“未配置”或“缺少输入”。
