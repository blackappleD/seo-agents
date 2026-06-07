# 与 claude-seo 的差距对比

对比对象：`D:\workspace\claude-seo` 当前实现。

## 数量差距

| 面向 | seo-agents 当前 | claude-seo 当前 | 差距 |
|---|---:|---:|---|
| skill | 26 个含离线占位 | 25 个核心/镜像 skill | 数量已接近，但深度仍不足 |
| agent | 23 个最小说明 | 18 个专家 agent | 数量已覆盖，深度仍不足 |
| Python 脚本 | 4 个入口脚本 | 约 50 个执行脚本 | 缺 Google、外链、报告、drift 深度和扩展脚本 |
| extensions | 0 个真实扩展 | 8 个扩展 | 当前仅离线占位 |
| docs | 3 个核心 docs | 安装、命令、架构、迁移、MCP、排障等完整 docs | 需要持续补文档 |
| schema/templates | 1 个本地模板文件 | 完整 schema 模板和引用 | 需要扩展模板深度 |

## 已补齐的本地短板

- 中文语言规则、中文 AGENTS/README/skill/agent/CLI/report 文案。
- content、geo、drift、hreflang、local、ecommerce 本地分析命令。
- Google、Backlink、Firecrawl 离线占位，只检测本机配置字段来源，不联网、不伪造数据。
- DataForSEO 已支持默认真实接入的 user-data、SERP、related keywords、domain rank overview；`--offline` 仅做配置检测。
- audit-data.json 聚合新增模块和外部数据源未配置提示。

## 仍未对齐的能力

- 真实 Google API：PageSpeed Insights、CrUX、GSC、URL Inspection、Indexing API、GA4、Keyword Planner。
- 真实外链数据：Moz、Bing Webmaster、Common Crawl、Ahrefs 等；DataForSEO 已具备第一批 live 查询但尚未接入 audit 聚合。
- 真实扩展安装器：DataForSEO、Firecrawl、Banana、Bing Webmaster、Ahrefs、SE Ranking、Profound、Unlighthouse。
- PDF/XLSX 报告、图表、截图和视觉审计。
- SERP-based cluster、SXO、content brief、programmatic SEO、competitor pages 的真实数据流。

## 推荐下一步

1. 先把本地模块的测试覆盖扩大到真实 HTML fixture。
2. 再接 Google Tier 0：PageSpeed Insights 和 CrUX，保持无凭据降级。
3. 将 DataForSEO live 结果接入 audit 聚合，再做扩展安装器和其他付费 provider。
