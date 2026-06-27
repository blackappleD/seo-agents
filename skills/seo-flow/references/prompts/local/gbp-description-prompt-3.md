# GBP 描述提示词 3

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 来源说明

- 原始注释：Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Synced: 2026-04-26
- `title: "GBP Description 当前 Agent Prompt 3"`
- `description: "GBP Description 当前 Agent Prompt 3"`
- `updated: 2026-04-25`
- `tags:`
- `- prompts`
- `- local`

## 使用场景

当您需要结构化的本地可交付成果并希望模型分离需要验证的观察结果、假设、建议的操作和声明时，请使用此提示。

## AI 兼容性

适用于长上下文推理模型。对于较小的模型，提供较窄的输入并要求一次一个输出部分。

## 输入

- 公司或网站名称。
- 目标页面、profile、查询集或活动。
- 相关的受众和地理位置。
- 现有证据：分析、搜索结果、通话、评论、profile facts或来源注释。
- 限制、排除和所需来源。

## 提示词

```text
使用 FLOW 模型担任高级 SEO 策略师。

任务：为[业务或资产]创建本地可交付成果。

仅使用提供的输入并清楚地标记任何假设。不要发明统计数据。不要重复使用私有示例。围绕以下内容构建答案：
1. 搜索者或购买者意图。
2. 现在已有证据。
3. 阻碍信任、提取或转换的差距。
4. 建议更改优先顺序。
5. 测量事件和审查节奏。
6. 发表前需要核实来源的声明。

返回团队可以执行的简明工作文档。
```

## 输出

- 执行摘要。
- 优先级表。
- 推荐的副本、结构或审计结果。
- 需要证据。
- 测量计划。
- 验证清单。

## 示例

输入：本地服务页面，证据薄弱且profile details不一致。

预期输出：按优先顺序重写摘要、要协调的事实、要添加的内部链接以及要衡量的转化事件。

## 参见

- [Prompt Library](../README.md)
- [FLOW Framework](../../flow-framework.md)
- [Bibliography](../../bibliography.md)

## 来源注释

源自本地 SEO 知识库结构，并根据存储库证据标准重写以供公众使用。

## 本项目适配边界

- 当前项目没有 `seo-agents flow` CLI；本文件作为中文 Agent playbook 使用。
- 执行前优先运行已有 `seo-agents page/content/technical/schema/geo <url> --json` 获取可验证证据。
- Google、Backlinks、Firecrawl 数据未配置时必须标注缺口；DataForSEO 可能计费，运行前要确认用户意图。
- 输出中区分“已验证事实”“合理假设”“需要外部数据确认”。
