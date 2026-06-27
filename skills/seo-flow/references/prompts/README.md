# FLOW 提示词索引

> 当前项目没有 `seo-agents flow` CLI；这些文件是中文离线 playbook。使用时先运行已有 `seo-agents` CLI 获取证据，再选择合适提示词。

## 使用顺序

1. 明确业务、页面、目标市场和当前约束。
2. 运行可用 CLI 获取证据，例如 `seo-agents page/content/technical/schema/geo <url> --json`。
3. 选择对应阶段的 prompt，并把“已验证事实”“合理假设”“需要外部数据确认”分开输出。
4. 如果涉及 Google、Backlinks、Firecrawl 或 DataForSEO，按本项目 provider 边界说明数据状态和成本风险。

| 阶段 | 提示词 | 用途 |
|---|---|---|
| Find | [主题相关性提示的内容规划](find/content-planning-for-topical-relevance-prompt.md) | 当您需要结构化的查找可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Find | [内容优先级提示](find/content-prioritization-prompt.md) | 当您需要结构化的查找可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Find | [关键词研究提示](find/keyword-research-prompt.md) | 当您需要结构化的查找可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Find | [主题相关性提示的关键词变体](find/keyword-variations-for-topical-relevance-prompt.md) | 当您需要结构化的查找可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Find | [提示：观众头像](find/prompt-audience-avatar.md) | 当您需要结构化的查找可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Leverage | [外链竞争提示](leverage/backlink-competition-prompt.md) | 当您需要结构化杠杆可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Local | [AI主页重写提示](local/ai-homepage-rewrite-prompt.md) | 当您需要结构化的本地可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Local | [本地深度研究提示词](local/deep-research-prompt.md) | 当您需要结构化的本地可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Local | [GBP类别提示](local/gbp-categories-prompt.md) | 当您需要结构化的本地可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Local | [GBP 描述提示词 1](local/gbp-description-prompt-1.md) | 当您需要结构化的本地可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Local | [GBP 描述提示词 2](local/gbp-description-prompt-2.md) | 当您需要结构化的本地可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Local | [GBP 描述提示词 3](local/gbp-description-prompt-3.md) | 当您需要结构化的本地可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Local | [GBP服务提示](local/gbp-services-prompt.md) | 当您需要结构化的本地可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Local | [提示：生成meta description](local/prompt-generating-a-meta-description.md) | 当您需要结构化的本地可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Local | [提示：生成title tag](local/prompt-generating-a-title-tag.md) | 当您需要结构化的本地可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Local | [提示：重写现有主页](local/prompt-rewriting-existing-homepage.md) | 当您需要结构化的本地可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Local | [提示：重写现有服务页面](local/prompt-rewriting-existing-service-page.md) | 当您需要结构化的本地可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [AI探测器测试后续提示](optimize/ai-detector-test-follow-up-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [AI支持页面重写提示](optimize/ai-supporting-pages-rewrite-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [基础优化提示词](optimize/basic-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [博客文章大纲提示](optimize/blog-post-outline-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [博客文章写作提示](optimize/blog-post-writing-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [点击率审核提示](optimize/ctr-audit-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [后续提示1](optimize/follow-up-prompt-1.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [后续提示2](optimize/follow-up-prompt-2.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [后续提示](optimize/follow-up-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [通用优化提示词 1](optimize/general-optimization-prompt-1.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [通用优化提示词 2](optimize/general-optimization-prompt-2.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [PAA 问题改写提示](optimize/paa-question-rewording-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [提示：核心 30 内容审核](optimize/prompt-core-30-content-audit.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [带有权限审核提示的属性内容](optimize/property-content-with-authority-audit-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [Reddit 洞察提示词](optimize/reddit-insights-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [架构提示 1](optimize/schema-prompt-1.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [第 1 步：ChatGPT 发现提示](optimize/step-1-the-chatgpt-discovery-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [第 2 步：后续资格提示](optimize/step-2-the-follow-up-qualifying-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [技术审核提示](optimize/technical-audit-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [可见性跟进提示](optimize/visibility-follow-up-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Optimize | [可见性提示](optimize/visiblity-prompt.md) | 当您需要结构化的优化可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。 |
| Win | [BOFU 页面简介生成器](win/bofu-page-brief-generator.md) | 当您需要服务、产品、位置、比较、定价、演示或潜在客户捕获页面的底部漏斗页面简介时，请使用此选项。 |
| Win | [转换审核提示](win/conversion-audit-prompt.md) | 当页面、营销活动或渠道获得流量但产生的销售线索较弱、转化率较低、归因不明确或销售跟进质量较差时，请使用此功能。 |
| Win | [双表面内容记分卡](win/dual-surface-content-scorecard.md) | 当您需要判断页面是否可以在传统搜索和人工智能辅助发现中执行，同时仍然支持转换时，请使用此选项。 |

## 本项目适配边界

- 所有 prompt 默认中文输出；命令、字段名、Schema/API/SEO 术语保留英文。
- 不编造搜索量、排名、CTR、流量、评论、外链、价格或竞品功能。
- 没有真实外部数据时，输出离线规划和数据缺口。
