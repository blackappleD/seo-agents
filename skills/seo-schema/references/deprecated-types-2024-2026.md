# 已弃用的 Schema.org 富结果类型 (2024–2026)

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

Google在此期间退休的每一个丰富结果的权威参考
2024-2025 年清理。每当用户请求其中之一时，
`seo-schema` 技能必须解释该类型已弃用，并且
重定向到有效的替代方案或注意不存在替代方案。

## 2025 年 6 月 19 日退休

宣布于
[Simplifying our Search rich results](https://developers.google.com/search/blog/2025/06/simplifying-search-results)
（developers.google.com/search/blog）。

|类型 |退休 |笔记|
|---|---|---|
| **车辆列表** (`@type: VehicleListing` / `Vehicle`) | 2025 年 6 月 |没有替代品。 Google 不再提供经销商库存丰富的卡片。如果在线销售商品，请使用常规 `Product` 架构。 |
| **索赔审核** (`@type: ClaimReview`) | 2025 年 6 月 |没有替代品。事实核查丰富结果是 ClaimReview 的主要消费者；没有它，标记就没有 SERP 效果。 ClaimReview *词汇表*仍在 schema.org 中，但 Google 忽略了它。 |
| **预计薪资** (`@type: EstimatedSalary` / `OccupationalAggregateRating`) | 2025 年 6 月 |没有替代品。 `JobPosting` 对于各个作业仍然有效。 |
| **学习视频** | 2025 年 6 月 |没有替代品。通用 `VideoObject` 丰富结果仍然呈现。 |
| **课程信息轮播** | 2025 年 6 月 |轮播变体退役了。单果`Course`富卡依然上线。当询问“课程信息”时，验证用户是否想要轮播（死）或实时单一结果变体。 |

## 2025 年 7 月 31 日退休

|类型 |退休 |笔记|
|---|---|---|
| **特别公告** (`@type: SpecialAnnouncement`) | 2025 年 7 月 |新冠疫情时期的紧急信息卡已被弃用。没有替代品。 |

## 提前（v2 之前的基线）退休

列出这些是为了完整性，因此法学硕士不建议使用它们。

|类型 |退休 |笔记|
|---|---|---|
| **操作方法** (`@type: HowTo`) | 2023 年 9 月 |从桌面和移动设备中删除了丰富的结果。词汇表仍然存在，但不产生 SERP 功能。一些网站仍然使用 HowTo 来提高 AI 引文的易读性——这是保留它的一个合理的理由，但将其标记为“无 SERP 效果”。 |
| **常见问题解答** (`@type: FAQPage`) | 2023 年 8 月（受限）； **2026 年 5 月 7 日（完全退休）** | **所有**网站的丰富搜索结果将于 2026 年 5 月 7 日全面停用 - 这取代了 2023 年政府/卫生部门的限制。丰富结果测试/报告支持将于 2026 年 6 月下降； Search Console API 2026 年 8 月。将现有 FAQ 页面标记为信息（非关键），因为它仍然有助于将 AI/LLM 引用作为实体信号； **不**建议删除或新的 FAQ 页面以获得 SERP 优势。对于真正的单问题页面，请使用 `QAPage`。 |

## 替换决策表

生成架构时，首选以下替代方案：

|要求 |更换|
|---|---|
| `ClaimReview` |无——说明富结果已死；如果是新闻上下文，建议使用 `Article` 和 `dateline`。 |
| `EstimatedSalary` | `JobPosting` 和 `baseSalary` 适用于特定角色。 |
| `LearningVideo` | `VideoObject`（仍在运行）。 |
| `Course Info` 旋转木马 |单`Course`富贵卡（尚在）。 |
| `SpecialAnnouncement` | `Event` 如果有时间限制；否则为 `Article` 或 `WebPage`。 |
| `VehicleListing` | `Product` 具有车辆特定的属性。 |
| `HowTo`（用于 SERP）|无 - 说明丰富的结果已死。如果目标是理解，则建议具有清晰 `<h2>` 步骤标题的文章结构；排名优势不再是模式驱动的。 |
| `FAQPage`（用于 SERP）|无 — 丰富的结果将于 2026 年 5 月停用。保留 AI 引用的标记；使用 `QAPage` 来获取真实的用户提交的问答页面。 |

## 主要来源

- Google 退役公告（2025 年 6 月）：https://developers.google.com/search/blog/2025/06/simplifying-search-results
- 特别公告弃用（2025 年 7 月）：https://developers.google.com/search/blog
- 如何退休（2023 年 9 月）：https://developers.google.com/search/blog/2023/09/structured-data-changes
- 常见问题解答限制（2023 年 8 月）：https://developers.google.com/search/blog/2023/08/howto-faq-changes
- 富贵退休常见问题解答（2026 年 5 月 7 日）：https://developers.google.com/search/docs/appearance/structured-data/faqpage

上次针对 Developers.google.com 进行验证：2026 年 5 月 25 日。

## 本项目适配边界

- 优先使用当前已实现的 `seo-agents` CLI 获取证据；没有 CLI 的能力作为 Agent playbook 或后续扩展处理。
- 不把外部数据源、付费 provider、浏览器渲染或地图 API 写成已执行，除非当前任务确实运行并取得证据。
- 每个 finding 必须有可复核 evidence；数据缺失时明确写“未配置”或“缺少输入”。
