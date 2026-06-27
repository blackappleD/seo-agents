---
name: seo-audit
description: >
  全站 SEO 审计。用于 crawl 站点、聚合 page、technical、content、schema、
  images、GEO、hreflang、local、ecommerce 和外部数据源配置状态，生成
  Markdown/JSON artifact 与优先级行动计划。
user-invocable: true
argument-hint: "[url] [--max-pages 20]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Audit

运行：

```bash
seo-agents audit <url> --max-pages 20
seo-agents audit <url> --max-pages 20 --output-dir reports/example
seo-agents audit <url> --max-pages 20 --json
```

## 执行逻辑

- `discover_urls` 会从 seed URL 出发抓取同 host 内链，最多分析 `--max-pages` 个页面。
- 每个页面执行 `page`，前 5 个页面执行 `technical/content/schema/images/hreflang`。
- 首个页面执行 `geo/local/ecommerce`，用于识别 AI Search、Local 和 Ecommerce 基础信号。
- `google`、`backlinks`、`firecrawl` 以离线占位形式检测配置；`dataforseo` 在 audit 内也按占位处理，避免审计默认产生计费。
- artifact 默认写入 `<host>-audit/`。

## 预期 artifact

| 文件 | 用途 |
|---|---|
| `audit-data.json` | 机器可读合同，包含 summary、categories、raw_results、action_plan |
| `FULL-AUDIT-REPORT.md` | 面向用户的综合报告 |
| `ACTION-PLAN.md` | 分阶段行动计划 |
| `findings/*.md` | 按类别拆分的 findings |
| `screenshots/` | 预留目录；当前 CLI 不自动截图 |

## 综合判断

读取 `../seo/references/quality-gates.md` 和 `../seo/references/thinking-framework.md` 只在需要更深解释时进行。输出建议时：

- 优先列出会阻塞索引、抓取、canonical 或 noindex 的 Critical/High 问题。
- 对 thin content、Schema、AI Search Readiness、Images、Local/Ecommerce 机会给出证据字段。
- 不要声称 Google API、Backlinks 或 Firecrawl 已返回真实数据；这些 provider 在当前项目中是配置检测。
- DataForSEO 的真实查询必须由用户显式运行 `seo-agents dataforseo ...`。

## 完成标准

- 报告必须包含 health score、业务类型、已抓取页面数、类别分数和优先级 action plan。
- 每个 finding 必须能追溯到 `audit-data.json` 中的 `raw_results`、`categories` 或 `action_plan`。
- 若 crawl 只覆盖部分页面，写明 `max_pages`、失败 URL 和限制，不扩大结论。
- 对原始参考项目中的 PageSpeed/CrUX、GSC、Backlinks、Firecrawl 能力，只能在本项目里作为未配置/离线占位说明。

## 错误处理

| 场景 | 处理 |
|---|---|
| seed URL 不可达 | 报告 fetch 错误并停止，不生成虚构审计。 |
| 部分页面抓取失败 | 保留成功页面结果，在报告限制中列出失败样本。 |
| `robots.txt` 或站点策略阻止抓取 | 说明可访问范围，不建议绕过。 |
| 大站点超出 `--max-pages` | 说明这是抽样审计，并建议分目录或提高上限复跑。 |
