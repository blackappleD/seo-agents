# seo-agents

Agent-first SEO 工具包，核心是一套可测试、可复用的 Python CLI，用于本地 v2 闭环。

- SSRF-aware URL 校验。
- 安全抓取和 SPA-aware render 降级。
- HTML SEO parser：metadata、heading、link、image、schema、hreflang、social tag。
- CLI 命令：page、technical、content、schema、sitemap、images、geo、drift、hreflang、local、ecommerce、audit。
- Google / Backlink / Firecrawl 离线占位命令；DataForSEO 默认调用真实 API，`--offline` 仅做配置检测且不输出 secret 值。
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
seo-agents dataforseo user-data --json
```

## 验证

```bash
python scripts/portability_check.py --json
pytest -q
```

默认测试不依赖真实网络或付费 API 凭据。

## 外部数据源

`google`、`backlinks`、`firecrawl` 目前仍是离线占位。`dataforseo` 默认调用真实 DataForSEO API；如只需检测配置，添加 `--offline`。所有 provider 命令都不会输出 secret 值，也不会伪造数据。

配置位置：

- Google：`~/.config/seo-agents/google-api.json`，支持 `api_key`、`service_account_path`、`default_property`、`ga4_property_id`、`oauth_client_path`、`ads_developer_token`、`ads_customer_id`、`ads_login_customer_id`；env fallback 为 `GOOGLE_API_KEY`、`GOOGLE_APPLICATION_CREDENTIALS`、`GSC_PROPERTY`、`GA4_PROPERTY_ID`。
- Backlinks：`~/.config/seo-agents/backlinks-api.json`，支持 `moz_api_key`、`bing_api_key`、`bing_verified_sites`、`commoncrawl_cache_dir`；env fallback 为 `MOZ_API_KEY`、`BING_WEBMASTER_API_KEY`。
- DataForSEO：`~/.config/seo-agents/dataforseo-api.json` 或 env `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD`；同时可检测 Claude MCP 的 `~/.claude/settings.json` 中 `mcpServers.dataforseo.env`。
- Firecrawl：`~/.config/seo-agents/firecrawl-api.json` 或 env `FIRECRAWL_API_KEY`；同时可检测 Claude MCP 的 `~/.claude/settings.json` 中 `mcpServers.firecrawl-mcp.env`。

测试或隔离环境可用 `SEO_AGENTS_CONFIG_DIR` 覆盖配置目录，用 `SEO_AGENTS_CLAUDE_SETTINGS` 覆盖 Claude settings 路径。

DataForSEO 真实数据源命令：

```bash
seo-agents dataforseo user-data --json
seo-agents dataforseo serp "ai seo" --json
seo-agents dataforseo related-keywords "ai seo" --json --limit 20
seo-agents dataforseo domain-rank example.com --json
seo-agents dataforseo setup --offline --json
```

`user-data` 是凭据和余额验证；SERP、related keywords、domain rank 查询会按 DataForSEO 账户计费。完整接入流程见 `docs/DATAFORSEO-INTEGRATION.md`。
