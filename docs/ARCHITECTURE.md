# 架构说明

seo-agents 采用两层交付形态：

- Agent 层：`AGENTS.md`、`skills/`、`agents/`，用于 Codex、Claude Code、Cursor、Cline、Aider 等 harness 读取。
- 确定性执行层：`src/seo_agents/` 和 `seo-agents` CLI，用于测试、CI、本地脚本和未来 Web UI。

## 数据流

```text
URL
  -> validate_url_strict
  -> fetch/render
  -> parse_html
  -> module analysis
  -> Finding[]
  -> audit-data.json
  -> Markdown report
```

## 核心模块

- `security/url_safety.py`：SSRF 防护、混淆 IP 拦截、DNS 公网地址校验。
- `fetch/http.py` 和 `fetch/render.py`：安全抓取、redirect 校验、SPA-aware render。
- `extract/html.py`：HTML metadata、heading、link、image、schema、hreflang 解析。
- `modules/`：page、technical、content、geo、drift、hreflang、local、ecommerce 等业务分析。
- `audit/orchestrator.py`：URL 发现、模块聚合、评分、artifact 写入。
- `reports/markdown.py`：Markdown 渲染层；JSON 是工程合同。

## 外部数据源策略

Google、Backlink、DataForSEO、Firecrawl 当前是离线占位。它们只检测本机配置字段来源，不调用真实 API。真实接入前必须补齐凭据校验、错误处理、mock 测试和“未配置”降级路径。
