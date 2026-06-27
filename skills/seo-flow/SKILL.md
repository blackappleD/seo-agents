---
name: seo-flow
description: >
  FLOW framework 和提示词库 playbook。用于 Find、Leverage、Optimize、Win、
  Local 阶段的 SEO 工作流、提示词选择和人工执行规划；当前无 CLI 入口。
user-invocable: true
argument-hint: "<stage> [url-or-topic]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Flow

当前保留为 Agent playbook，尚无 `seo-agents flow` CLI。

## 阶段

- `find`：受众、关键词、内容机会和优先级。
- `leverage`：外链、权威、已有资产复用。
- `optimize`：页面、内容、Schema、技术和 AI 可见性优化。
- `win`：转化、BOFU 页面、dual-surface 内容。
- `local`：GBP、本地页面、服务区域和标题/描述优化。

## 使用规则

- 先用当前 CLI 收集证据，再选择 prompt 或工作流。
- 引用 `references/prompts/*` 时保留其用途，但不要声称已有自动执行命令。
- 对 Google/Backlinks/Firecrawl 相关 prompt，需要标注外部数据源未配置或离线占位。

## 阶段路由

- `find`：需要关键词、受众、内容机会时，优先结合 `content-brief`、`cluster` 和 DataForSEO。
- `leverage`：需要 authority/off-site 方案时，结合 `backlinks` 的配置状态和人工外链框架。
- `optimize`：需要页面优化时，先运行 `page/content/technical/schema/geo`，再选择 2-3 个最相关 prompt。
- `win`：需要 BOFU 或转化优化时，结合 `sxo`、comparison、pricing、FAQ 和 CTA。
- `local`：需要本地增长时，结合 `local`、`maps` 和 GBP 人工清单。

## 可结合命令

```bash
seo-agents audit <url>
seo-agents content <url> --json
seo-agents technical <url> --json
seo-agents geo <url> --json
```

## 按需引用

- `references/flow-framework.md`
- `references/bibliography.md`
- `references/flow-prompts.lock`
- `references/prompts/README.md`

## 完成标准

- 输出选中的 stage、引用的 prompt 文件、为什么选它、需要的输入和预期产物。
- 不执行远程 sync；当前 prompt 文件已在仓库中，缺失时报告文件路径。
- prompt 输出必须二次适配为中文、`seo-agents` CLI 证据和本项目能力边界。

## 错误处理

| 场景 | 处理 |
|---|---|
| stage 未指定 | 展示 Find/Leverage/Optimize/Win/Local 的选择建议。 |
| prompt 文件缺失 | 报告缺失路径，不尝试联网同步。 |
| 外部数据未配置 | 使用 CLI 证据和用户输入，标注数据缺口。 |
