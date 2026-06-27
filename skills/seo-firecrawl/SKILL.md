---
name: seo-firecrawl
description: >
  Firecrawl 离线占位。保留 crawl/map/scrape 命令面，检测 FIRECRAWL_API_KEY
  和 MCP 配置来源；当前不调用真实 Firecrawl API、不抓取站点地图、不输出 secret 值。
user-invocable: true
argument-hint: "[subcommand] [url]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Firecrawl

运行：

```bash
seo-agents firecrawl setup --json
seo-agents firecrawl crawl <url> --json
seo-agents firecrawl map <url> --json
seo-agents firecrawl scrape <url> --json
```

所有子命令当前只返回离线配置检测结果。

## 配置检测

- 配置文件：`~/.config/seo-agents/firecrawl-api.json`，字段 `api_key`。
- 环境变量：`FIRECRAWL_API_KEY`。
- agent MCP settings 中的 `firecrawl-mcp` server env；当前代码兼容 `~/.claude/settings.json` 路径。

## 边界

- 当前 `audit` 使用本项目内置 crawler，不依赖 Firecrawl。
- 不调用 Firecrawl API，不执行 crawl/map/scrape。
- 如果后续接入真实 API，需要增加凭据校验、网络错误处理、配额/费用提示和 mock 测试。

## 来源能力适配

Firecrawl 在来源生态里可用于 crawl、map、scrape 和渲染抓取。本项目迁移后只保留命令面和配置检测，用来：

- 告诉用户是否已准备好未来接入。
- 避免 `audit` 默认产生外部 API 成本。
- 为后续实现记录需要的凭据、错误处理和测试范围。

## 完成标准

- 输出配置路径、环境变量字段、MCP server 是否存在和 secret 字段脱敏状态。
- 当用户要求抓取站点时，优先使用 `seo-agents audit` 内置 crawler。
- 当用户明确要求 Firecrawl 真实抓取时，说明当前未实现，不伪造 crawl/map/scrape 结果。

## 错误处理

| 场景 | 处理 |
|---|---|
| 未配置 API key | 返回“未配置”，但说明内置 audit 不依赖它。 |
| 用户要求 scrape 内容 | 建议使用 `fetch/render/page` 或后续接入 Firecrawl。 |
| MCP 配置存在但无 key | 报告 server configured 但 required fields 缺失。 |
