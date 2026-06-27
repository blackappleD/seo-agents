---
name: seo-geo
description: >
  AI Search / GEO 信号检查。覆盖实体 schema、可引用段落、llms.txt/
  llms-full.txt、robots.txt 中 AI crawler 阻断，以及页面是否适合被答案引擎引用。
user-invocable: true
argument-hint: "<url>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO GEO

运行：

```bash
seo-agents geo <url> --json
```

## 检查范围

- 页面是否有 `Organization`、`WebSite`、`WebPage`、`Article`、`BlogPosting` 等实体 schema。
- 是否存在至少 2 个可引用段落。
- 根目录是否有 `llms.txt` 或 `llms-full.txt`。
- `robots.txt` 是否出现 `GPTBot`、`Google-Extended`、`CCBot`、`ClaudeBot`、`PerplexityBot` 等 AI crawler 阻断信号。

## 输出规则

- `llms.txt` 是 Info 级机会，不是排名必要条件。
- 如果 robots 阻断 AI crawler，先确认这是业务策略，再建议调整。
- 建议必须围绕可见内容、实体一致性和引用友好结构，避免玄学化 GEO 承诺。
- 品牌提及、社区讨论、Wikipedia/Reddit/YouTube 等外部信号当前不由 CLI 自动采集；只能作为人工调研或外部数据缺口。

## 按需引用

- `references/google-ai-optimization-guide.md`：Google AI 搜索优化背景。
- `references/llmstxt-evidence.md`：llms.txt 的证据和边界。

## 评估维度

- Citability：段落是否能被单独引用，是否有定义、数字、步骤、来源或明确结论。
- Structural readability：标题层级、列表、FAQ、表格和 schema 是否帮助机器理解。
- Multi-modal：图片、视频、图表是否有文字上下文和替代文本。
- Authority：作者、组织、引用、品牌实体和外部认可是否清晰。
- Technical accessibility：robots、状态码、渲染、canonical 和实体 schema 是否允许抓取和理解。

## 完成标准

- 输出 `schema_types`、citation block 数量、`llms.txt` 状态、AI crawler robots 状态和优先建议。
- 明确区分“当前页面可检测信号”和“需要外部品牌/社区/日志数据”的信号。
- 若生成 `llms.txt` 建议，只给最小可维护草稿，不宣称它会提升 AI citation ranking。

## 错误处理

| 场景 | 处理 |
|---|---|
| robots 阻断 AI crawler | 列出被阻断 token，先确认策略，再给开放建议。 |
| 无可引用段落 | 建议增加定义、FAQ、步骤、数据摘要或对比块。 |
| 无 schema | 转 `seo-schema` 给实体 schema 草稿。 |
| 用户要求 AI 平台排名保证 | 明确无法保证，只能提升可访问性和引用友好度。 |
