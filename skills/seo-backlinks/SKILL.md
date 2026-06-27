---
name: seo-backlinks
description: >
  Backlinks 外链数据源离线占位。检测 Moz、Bing Webmaster、Common Crawl
  配置字段来源和 credential tier；当前不联网、不调用真实外链 API、不输出 secret 值。
user-invocable: true
argument-hint: "[subcommand] [domain]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Backlinks

运行：

```bash
seo-agents backlinks setup --json
seo-agents backlinks profile example.com --json
```

所有子命令当前只做配置检测。

## 配置检测

- 配置文件：`~/.config/seo-agents/backlinks-api.json`。
- 环境变量：`MOZ_API_KEY`、`BING_WEBMASTER_API_KEY`。
- 可选字段：`bing_verified_sites`、`commoncrawl_cache_dir`。

credential tier：

- `Local/Common Crawl only`：没有 Moz/Bing key。
- `Moz` 或 `Bing`：检测到单一 provider 字段。
- `Moz + Bing`：同时检测到两个 provider 字段。

## 边界

- 当前不抓取外链、不调用 Moz/Bing/DataForSEO backlinks。
- 不输出 secret 值；只输出字段名和来源。
- 如果用户需要真实外链数据，优先说明需要新增 provider 客户端、mock 测试和计费/配额处理。
- 来源中的 profile、gap、toxic、new/lost、verify known backlinks 等能力当前未实现为 CLI；可以作为人工分析框架或后续扩展需求。

可按需读取 `../seo/references/backlink-quality.md` 和 `../seo/references/free-backlink-sources.md` 用于人工解读外链质量。

## 人工分析框架

当用户提供外链导出表或第三方数据时，可以按以下维度分析：

- Profile overview：referring domains、follow/nofollow、domain diversity、增长/流失趋势。
- Anchor text：branded、naked URL、generic、exact match、partial match 和过度优化风险。
- Referring domain quality：主题相关性、国家/语言、spam/toxic 指标、站群/目录风险。
- Top pages：哪些 URL 获得链接，是否与商业目标和内链结构匹配。
- Gap / opportunities：竞品共同链接源、资源页、行业媒体、合作伙伴和可复用内容资产。

## 完成标准

- 无外部数据时只输出配置状态和数据缺口。
- 有用户提供数据时，逐条引用数据来源，不把推断写成事实。
- toxic/disavow 建议必须保守：优先调查和移除，不轻易建议提交 disavow。

## 错误处理

| 场景 | 处理 |
|---|---|
| 无 provider 配置 | 标注“离线占位”，建议用户提供外链导出或接入 provider。 |
| 数据列缺失 | 列出缺少的列，例如 source URL、target URL、anchor、follow、domain metric。 |
| 用户要求实时外链 | 说明当前 CLI 未实现真实抓取/API。 |
