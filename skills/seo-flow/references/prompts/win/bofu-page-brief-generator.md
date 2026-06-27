# BOFU 页面简介生成器

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 来源说明

- 原始注释：Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Synced: 2026-04-26
- `title: "BOFU Page Brief Generator"`
- `description: "BOFU Page Brief Generator"`
- `updated: 2026-04-25`
- `tags:`
- `- prompts`
- `- win`

## 使用场景

当您需要服务、产品、位置、比较、定价、演示或潜在客户捕获页面的底部漏斗页面简介时，请使用此选项。

## AI 兼容性

当前 Agent、GPT、Gemini 等长上下文模型。最适合当前客户语言和转化证据。

## 输入

- 优惠、服务或产品。
- 目标受众和细分市场。
- 购买阶段意图。
- 已知的反对意见或犹豫点。
- 来自电话、聊天、评论或调查的客户语言。
- 转换目标。
- 所需的证明点。
- 现有的页面文本（如果有）。

## 提示词

```text
创建针对 [优惠] 定位 [受众] 的漏斗底部页面简介。

仅使用提供的输入。围绕受众需要做出的决定制定简报。

分析：
1. 访问者试图解决的直接问题。
2. 他们在转换之前可能需要的决策因素。
3. 反对意见、犹豫点和不清楚的地方。
4. 应自然出现的客户语言短语。
5. 支持信任所需的证据。
6. CTA角度和页面部分需要减少摩擦。

返回：页面目标、搜索/转化意图、主要受众、买家问题、反对意见、推荐的 H1、部分大纲、证明点、CTA 策略、常见问题解答主题以及表单、通话、聊天和合格潜在客户衡量的跟踪说明。标记缺失的输入。
```

## 输出

- 结构化的 Win 阶段工作文档。
- 优先推荐。
- 证据和测量差距。
- 需要验证的主张或假设。

## 示例

输入：设施经理的商业维修页面，对响应时间、周末可用性和定价清晰度有异议。输出：强调紧迫性、服务范围、决策标准、证据、常见问题解答和电话/表格跟踪的简介。

## 参见

- [Prompt Library](../README.md)
- BOFU和转换内容
- 双面记分卡

## 来源注释

源自 SEJ State of SEO 2026、SEJ B2B Lead Generation 和 CallRail/SEJ Better Leads More Sales 2025。

## 本项目适配边界

- 当前项目没有 `seo-agents flow` CLI；本文件作为中文 Agent playbook 使用。
- 执行前优先运行已有 `seo-agents page/content/technical/schema/geo <url> --json` 获取可验证证据。
- Google、Backlinks、Firecrawl 数据未配置时必须标注缺口；DataForSEO 可能计费，运行前要确认用户意图。
- 输出中区分“已验证事实”“合理假设”“需要外部数据确认”。
