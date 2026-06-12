# 命令参考

所有命令通过 `seo-agents` 运行。默认输出为人类可读摘要；加 `--json` 输出机器可读 JSON。

## 已实现命令

| 命令 | 用途 |
|---|---|
| `seo-agents fetch <url> --json` | 带 URL 安全校验的抓取 |
| `seo-agents render <url> --json` | SPA-aware render，支持 `never/auto/always` |
| `seo-agents parse <html-file> --json` | 解析本地 HTML 文件 |
| `seo-agents page <url> --json` | 单页 On-Page SEO 分析 |
| `seo-agents technical <url> --json` | 技术 SEO 分析 |
| `seo-agents content <url> --json` | 内容质量、E-E-A-T、AI 引用友好信号 |
| `seo-agents schema <url> --json` | JSON-LD 检测、验证和生成建议 |
| `seo-agents sitemap <url> --json` | sitemap 发现和校验 |
| `seo-agents images <url> --json` | 图片 SEO 检查 |
| `seo-agents geo <url> --json` | AI Search / GEO 本地可判断信号 |
| `seo-agents hreflang <url> --json` | hreflang / 国际化 SEO 检查 |
| `seo-agents local <url> --json` | 本地 SEO 基础检查 |
| `seo-agents ecommerce <url> --json` | Ecommerce SEO 基础检查 |
| `seo-agents drift baseline <url>` | 建立漂移基线 |
| `seo-agents drift compare <url>` | 与最近基线比较 |
| `seo-agents drift history <url>` | 查看漂移历史 |
| `seo-agents audit <url> --max-pages 20` | 聚合审计并写入 artifact |

## 离线占位命令

这些命令保持“离线占位”：会检测配置字段和来源，但不联网、不调用真实 API、不输出 secret 值、不伪造数据：

```bash
seo-agents google setup --json
seo-agents backlinks https://example.com --json
seo-agents dataforseo serp "keyword" --json
seo-agents firecrawl crawl https://example.com --json
```

配置路径默认在 `~/.config/seo-agents/`：

- `google-api.json`：`api_key`、`service_account_path`、`default_property`、`ga4_property_id`、`oauth_client_path`、`ads_developer_token`、`ads_customer_id`。
- `backlinks-api.json`：`moz_api_key`、`bing_api_key`、`bing_verified_sites`、`commoncrawl_cache_dir`。
- `dataforseo-api.json`：`username`、`password`；也检测 `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD` 和 `~/.claude/settings.json` 的 `mcpServers.dataforseo.env`。
- `firecrawl-api.json`：`api_key`；也检测 `FIRECRAWL_API_KEY` 和 `~/.claude/settings.json` 的 `mcpServers.firecrawl-mcp.env`。

测试隔离时可设置 `SEO_AGENTS_CONFIG_DIR` 和 `SEO_AGENTS_CLAUDE_SETTINGS`。

## 后续扩展命令

以下能力已有 skill/agent 说明，但本轮不提供 CLI 实现：`plan`、`cluster`、`sxo`、`programmatic`、`competitor-pages`、`content-brief`、`maps`、`flow`、`image-gen`。
