# 双表面内容记分卡

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 来源说明

- 原始注释：Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Synced: 2026-04-26
- `title: "Dual-Surface Content Scorecard"`
- `description: "Dual-Surface Content Scorecard"`
- `updated: 2026-04-25`
- `tags:`
- `- prompts`
- `- win`

## 使用场景

当您需要判断页面是否可以在传统搜索和人工智能辅助发现中执行，同时仍然支持转换时，请使用此选项。

## AI 兼容性

当前 Agent、GPT、Gemini 等长上下文模型。最适合当前客户语言和转化证据。

## 输入

- 页面副本。
- 目标查询或主题。
- 预期转化目标。
- 观众部分。
- 已知的第一方见解。
- 性能数据（如果有）。
- 竞争页面示例，可选。

## 提示词

```text
针对两个发现界面对此内容进行评分：传统搜索和人工智能辅助答案环境。

评价：
1.原始的有用性和特异性。
2. 与受众需求和决策阶段保持一致。
3. 证据、例子、数据或第一手见解。
4. 明确解答买家问题。
5. 转换支持：CTA、证明、异议处理和下一步。
6.刷新或更新需要。
7. 衡量准备情况：流量、参与度、合格潜在客户、销售转化和投资回报率指标。

返回传统搜索分数、人工智能辅助发现分数、转换就绪分数、证据强度、差距、风险、建议更新以及影响最大的接下来三个操作。使用具有业务影响力的语言，而不是仅用于流量的语言。
```

## 输出

- 结构化的 Win 阶段工作文档。
- 优先推荐。
- 证据和测量差距。
- 需要验证的主张或假设。

## 示例

输入：现有的服务页面，有流量但表单提交量低。输出：显示页面是否缺乏买家证明、直接答案、客户语言、CTA 清晰度或可衡量的转化路径的分数。

## 参见

- [Prompt Library](../README.md)
- BOFU和转换内容
- 双面记分卡

## 来源注释

源自 SEJ State of SEO 2026、经过验证的人工智能搜索证据和 SEJ B2B Lead Generation。

## 本项目适配边界

- 当前项目没有 `seo-agents flow` CLI；本文件作为中文 Agent playbook 使用。
- 执行前优先运行已有 `seo-agents page/content/technical/schema/geo <url> --json` 获取可验证证据。
- Google、Backlinks、Firecrawl 数据未配置时必须标注缺口；DataForSEO 可能计费，运行前要确认用户意图。
- 输出中区分“已验证事实”“合理假设”“需要外部数据确认”。
