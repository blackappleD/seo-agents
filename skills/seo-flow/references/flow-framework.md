# 流程框架

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 来源说明

- 原始注释：Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Synced: 2026-04-26
- `title: "FLOW Framework"`
- `description: "FLOW Framework"`
- `updated: 2026-04-25`
- `tags:`
- `- framework`

![seo-agents 10-principle methodology: PERCEIVE, ANALYZE, VALIDATE, ACT](../../../assets/framework.svg)

# 流程框架

## 这是什么

FLOW 是 2026 年发现的搜索和转换循环。它处理排名、人工智能引用、
本地可见性和销售证据作为连接的表面而不是单独的渠道。

FLOW 使用四个简单的阶段：发现需求、利用分布式证据、优化自有资产以获取和信任，以及通过将发现与收入联系起来的页面和测量来获胜。本页将该循环应用于框架层。

## 为什么它在 2026 年很重要

Ahrefs 发现，当 AI 概述出现时，排名第一的内容的平均点击率降低了 58%
出现在 2025 年 12 月的数据集中。

seoClarity 发现，25% 的被引用次数最多的 ChatGPT URL 中没有 Google 有机可见度。
被引页面样本。

搜索不再是一个结果页和一键点击路径。一个有用的 SEO 系统必须能够经受住经典排名、人工智能摘要、本地包、业务简介、社区参考和销售反馈的考验。实际的目标不是平等地追逐每个表面；而是追求每一个表面。它是决定哪个表面可以改变下一个业务成果，然后在那里建立证据。

## 如何申请

- 在写作之前命名搜索界面：有机结果、人工智能答案、本地包、社区讨论、付费登陆页面或销售辅助页面。
- 将可观察的证据与假设分开。带数字的声明必须追溯到参考书目或被删除。
- 首先根据买家语言编写，然后添加实体清晰度、内部链接、证明和转换后续步骤。
- 将资产作为人工智能可读的文档进行审查：清晰的标题、直接的答案、有用的简洁表格、源标签，并且没有对私人示例的隐藏依赖。

## 操作流程

1. 在选择策略之前定义业务成果。一个旨在创建合格呼叫的页面不应仅根据印象来判断，而旨在协调业务事实的profile不应仅根据发布频率来判断。
2. 盘点现有证据：客户语言、查询数据、profile details、评论、分析、通话记录、销售异议以及任何可以支持索赔的公共来源。
3. 确定哪个 FLOW 阶段阻碍了进度。如果需求语言不清楚，请返回“查找”。如果品牌没有在场外得到证实，请利用杠杆作用。如果所拥有的资产难以提取或信任，请优化。如果存在流量但业务影响较弱，请转向 Win。
4. 仅在整理证据后重写或重建。最强大的资产通常来自清晰的源表，而不是来自空白页的头脑风暴。
5. 与三个读者一起审查完成的工作：买家、搜索引擎和人工智能代理，后者可能会在稍后总结或比较业务。

## 测量

使用平衡计分卡。跟踪可见性指标，例如排名、印象、本地包装存在、引用和人工智能提及，但将它们与业务指标（例如合格的潜在客户、来电、表单完成、销售机会、辅助转化和经常性反对）联系起来。如果无法测量页面或profile，请在判断性能之前添加测量事件。

## 常见故障模式

- 发布统计数据是因为它听起来很熟悉，而不是因为源已加载并注明日期。
- 将人工智能可见性视为格式化技巧，而忽略品牌证据、实体一致性和场外佐证。
- 围绕公司偏好撰写页面，而不是买家问题和决策风险。
- 优化流量而不定义下一个合格的操作。
- 当通用或新创建的示例更干净、更耐用时，重用旧示例。

## AI代理提示

```text
You are an SEO strategist using the FLOW model. For the asset named "FLOW Framework", analyze the target audience, search surface, evidence needed, entity facts, conversion goal, and risks. Return: priorities, page or profile changes, source requirements, internal links, measurement plan, and a list of claims that need verification before publication.
```

## 质量栏

- 公开声明使用经过验证的来源或保持定性。
- 示例是通用的或为此存储库新创建的。
- 私人社论仅用于识别候选概念，绝不作为公共散文。
- 该页面应该对人类读者和仅具有此存储库的人工智能代理有意义。

## 参见

- [Start Here](../SKILL.md)
- [Bibliography](bibliography.md)

## 来源

- 搜索引擎杂志，2026 年 SEO 状况 PDF 和公共登陆页面，检索于 2026 年 4 月 25 日。
- Ahrefs，AI 概述点击率更新，检索于 2026 年 4 月 25 日。
- seoClarity，ChatGPT 引用页面分析，检索于 2026 年 4 月 25 日。

## 本项目适配边界

- 优先使用当前已实现的 `seo-agents` CLI 获取证据；没有 CLI 的能力作为 Agent playbook 或后续扩展处理。
- 不把外部数据源、付费 provider、浏览器渲染或地图 API 写成已执行，除非当前任务确实运行并取得证据。
- 每个 finding 必须有可复核 evidence；数据缺失时明确写“未配置”或“缺少输入”。
