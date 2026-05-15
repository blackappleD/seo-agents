# seo-agents

Agent-first SEO 工具包，核心是一套可测试、可复用的 Python CLI。

当前实现覆盖 `SEO_PROJECT_IMPLEMENTATION_REPORT.zh-CN.md` 中的本地 v2 闭环：

- SSRF-aware URL 校验。
- 安全抓取和 SPA-aware render 降级。
- HTML SEO parser：metadata、heading、link、image、schema、hreflang、social tag。
- CLI 命令：page、technical、content、schema、sitemap、images、geo、drift、hreflang、local、ecommerce、audit。
- Google / Backlink / DataForSEO / Firecrawl 离线占位命令，默认不联网、不调用真实 API；会检测本机配置字段但不会输出 secret 值。
- Markdown + JSON audit artifact。
- Agent 可读的 `AGENTS.md`、`skills/` 和 `agents/`。

## 安装

```bash
python -m pip install -e ".[dev]"
```

CLI 名称为 `seo-agents`。

## 常用命令

```bash
seo-agents --help
seo-agents fetch https://example.com --json
seo-agents render https://example.com --json
seo-agents page https://example.com --json
seo-agents content https://example.com --json
seo-agents technical https://example.com --json
seo-agents schema https://example.com --json
seo-agents sitemap https://example.com --json
seo-agents images https://example.com --json
seo-agents geo https://example.com --json
seo-agents drift baseline https://example.com
seo-agents audit https://example.com --max-pages 20
```

## 验证

```bash
python scripts/portability_check.py --json
pytest -q
```

默认测试不依赖真实网络或付费 API 凭据。

## 外部数据源

`google`、`backlinks`、`dataforseo`、`firecrawl` 目前仍是离线占位。命令会检测本机配置状态，返回 `configured`、`credential_tier` 和字段来源，但不会联网、不会调用真实 API、不会输出 secret 值，也不会伪造数据。

配置位置借鉴 `claude-seo` 的分层方式：

- Google：`~/.config/seo-agents/google-api.json`，支持 `api_key`、`service_account_path`、`default_property`、`ga4_property_id`、`oauth_client_path`、`ads_developer_token`、`ads_customer_id`、`ads_login_customer_id`；env fallback 为 `GOOGLE_API_KEY`、`GOOGLE_APPLICATION_CREDENTIALS`、`GSC_PROPERTY`、`GA4_PROPERTY_ID`。
- Backlinks：`~/.config/seo-agents/backlinks-api.json`，支持 `moz_api_key`、`bing_api_key`、`bing_verified_sites`、`commoncrawl_cache_dir`；env fallback 为 `MOZ_API_KEY`、`BING_WEBMASTER_API_KEY`。
- DataForSEO：`~/.config/seo-agents/dataforseo-api.json` 或 env `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD`；同时可检测 Claude MCP 的 `~/.claude/settings.json` 中 `mcpServers.dataforseo.env`。
- Firecrawl：`~/.config/seo-agents/firecrawl-api.json` 或 env `FIRECRAWL_API_KEY`；同时可检测 Claude MCP 的 `~/.claude/settings.json` 中 `mcpServers.firecrawl-mcp.env`。

测试或隔离环境可用 `SEO_AGENTS_CONFIG_DIR` 覆盖配置目录，用 `SEO_AGENTS_CLAUDE_SETTINGS` 覆盖 Claude settings 路径。
