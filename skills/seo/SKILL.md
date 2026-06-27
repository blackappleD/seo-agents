---
name: seo
description: >
  SEO 主路由。用于站点审计、单页分析、technical/content/schema/sitemap/images、
  GEO、drift、hreflang、local、ecommerce、DataForSEO 真实数据和离线占位 provider
  的命令发现与任务分流。
user-invocable: true
argument-hint: "<command> [url]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO

当用户需要 SEO 分析、站点审计、SEO CLI 命令发现或多模块报告编排时使用本 skill。优先执行 `seo-agents` CLI；不要把未在本项目实现的命令写成可执行入口。

## 快速路由

| 需求 | 首选命令 | 状态 |
|---|---|---|
| 全站审计 | `seo-agents audit <url> --max-pages 20` | 已实现 |
| 单页 On-Page SEO | `seo-agents page <url> --json` | 已实现 |
| 技术 SEO | `seo-agents technical <url> --json` | 已实现 |
| 内容质量 / E-E-A-T | `seo-agents content <url> --json` | 已实现 |
| Schema 检测与建议 | `seo-agents schema <url> --json` | 已实现 |
| Sitemap 发现与校验 | `seo-agents sitemap <url> --json` | 已实现 |
| 图片 SEO | `seo-agents images <url> --json` | 已实现 |
| AI Search / GEO | `seo-agents geo <url> --json` | 已实现 |
| Hreflang / 国际化 | `seo-agents hreflang <url> --json` | 已实现 |
| Local SEO 基础检查 | `seo-agents local <url> --json` | 已实现 |
| Ecommerce SEO 基础检查 | `seo-agents ecommerce <url> --json` | 已实现 |
| 漂移监控 | `seo-agents drift baseline/compare/history <url>` | 已实现 |
| DataForSEO | `seo-agents dataforseo ...` | 默认真实 API |
| Google / Backlinks / Firecrawl | `seo-agents google/backlinks/firecrawl ... --json` | 离线占位 |

常用组合：

```bash
seo-agents page <url> --json
seo-agents content <url> --json
seo-agents technical <url> --json
seo-agents audit <url> --max-pages 20
```

## 工作规则

- 所有用户输入 URL 必须经过 `validate_url_strict`；拒绝 internal、private、loopback、link-local 和 metadata endpoint。
- 默认使用中文报告 finding、建议和文档；命令名、JSON key、HTTP header、Schema 类型、SEO/API 术语保留英文。
- 每个 finding 必须带 `evidence`，并尽量使用 `--json` 输出作为机器可读合同。
- `audit` 会写入 Markdown 和 JSON artifact；JSON audit data 是工程合同，Markdown 是渲染层。
- Google、Backlinks、Firecrawl 当前只检测配置来源，必须标注“离线占位”；DataForSEO 默认会调用真实 API，涉及计费的命令先提醒用户。

## 编排方式

1. 先判断任务类型：单页、全站、技术、内容、结构化数据、图片、GEO、国际化、本地、Ecommerce、外部数据源或策略 playbook。
2. 有确定性 CLI 时优先运行 CLI；若 CLI 抓取失败，不猜测页面内容，直接报告错误和可复现命令。
3. 需要综合报告时，先收集 `page/technical/content/schema/images` 等 JSON，再按 Critical / High / Medium / Low 合并。
4. 业务类型可从 schema、URL、页面文案和用户说明推断；不确定时说明候选类型和证据。
5. playbook 型 skill 只能基于已提供资料、CLI 证据和明确标注的外部数据工作，不能暗示已有自动化命令。

## 迁移适配

原始参考项目里的 `/seo ...` 命令，在本项目映射为 `seo-agents ...` CLI 或 Agent playbook。处理时按以下优先级降级：

- 已实现 CLI：直接运行并引用 JSON 字段。
- DataForSEO：用户显式需要真实数据时运行；计费命令先提醒。
- Google / Backlinks / Firecrawl：只做离线配置检测。
- plan / cluster / sxo / maps / content-brief / competitor-pages / programmatic / image-gen / flow：保留为中文 playbook，输出可执行方案，不声称存在 CLI。

## 错误处理

| 场景 | 处理 |
|---|---|
| URL 不可达或被 SSRF 拒绝 | 报告 CLI 错误；不要绕过安全校验。 |
| 页面需要登录或 403 | 只分析可见部分，建议用户提供公开 URL 或 HTML。 |
| JavaScript 渲染不足 | 使用 `--render-mode always` 复核；仍失败时标注限制。 |
| 子模块失败 | 保留已成功模块结果，指出失败命令和原因。 |
| 用户请求未实现命令 | 指向对应 playbook，并明确“当前无 CLI 入口”。 |

## 按需引用

长参考资料只在需要时读取，不要启动时全量加载：

- `references/thinking-framework.md`：审计综合和优先级推理框架。
- `references/quality-gates.md`：页面类型、薄内容和规模化页面质量阈值。
- `references/cwv-thresholds.md`：Core Web Vitals 和 INP 阈值。
- `references/schema-types.md`：Schema 类型、支持状态和弃用提醒。
- `references/eeat-framework.md`：E-E-A-T 内容评估维度。
- `references/backlink-quality.md`、`references/free-backlink-sources.md`：外链质量与免费来源背景。
- `references/local-*.md`、`references/maps-*.md`：Local SEO 和 Maps 资料。

## 输出收口

完成分析后给出：

- 关键问题：按 Critical / High / Medium / Low 排序。
- 证据：引用 CLI JSON 字段或 artifact 路径。
- 下一步：把建议限定在当前 CLI 或已明确标注的离线/后续能力内。
- 局限：列出未配置外部数据源、未渲染成功页面或人工判断部分。

## Harness notes

- Codex：读取本 skill 和目标子 skill；用 shell 执行 `seo-agents` 验证。
- Cursor/Cline/Aider：把 `AGENTS.md`、`skills/`、`agents/` 当作 playbook；执行动作仍以 `seo-agents` CLI 为准。
