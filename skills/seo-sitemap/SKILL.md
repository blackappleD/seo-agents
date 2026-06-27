---
name: seo-sitemap
description: >
  Sitemap 发现和校验。从 robots.txt 和 /sitemap.xml 发现 sitemap，解析
  urlset/sitemapindex、gzip、lastmod、嵌套 sitemap，以及 priority/changefreq
  等弱化字段提醒。
user-invocable: true
argument-hint: "<url>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Sitemap

运行：

```bash
seo-agents sitemap <url> --json
```

## 检查范围

- 从 `<origin>/robots.txt` 读取 `Sitemap:` 声明。
- 自动追加 `<origin>/sitemap.xml` 作为候选。
- 支持 XML sitemap、sitemap index 和 gzip 内容。
- 递归分析 sitemap index，当前最多 10 个嵌套 sitemap。
- 标记超过 50,000 URL、未来 `lastmod`、`priority/changefreq` 等问题。

## 输出解读

- `discovered` 是候选 sitemap URL 列表。
- `sitemaps[*].type` 为 `urlset`、`sitemapindex` 或 `unknown`。
- `summary.urls_found` 是已解析 sitemap 中 URL 总数。
- `summary.errors` 与 `summary.warnings` 用于报告优先级。

## 生成模式适配

来源 skill 支持 sitemap generation；当前项目没有 `seo-agents sitemap generate` CLI。若用户要求生成 sitemap：

- 可以基于用户提供的 URL 列表或 `audit` crawl 结果输出 XML 草稿。
- 超过 50,000 URL 或 50MB 未压缩时，建议拆分为 sitemap index。
- `lastmod` 只在有真实更新时间时填写；不要批量伪造同一天更新时间。
- `priority` / `changefreq` 可省略；如果保留，要说明 Google 基本忽略。
- 不自动提交到 Search Console；当前 Google provider 是离线占位。

## 完成标准

- 分析模式下给出发现来源、解析成功/失败的 sitemap、URL 数量和严重问题。
- 生成模式下给出 XML 草稿、拆分策略、robots.txt `Sitemap:` 声明建议和验证步骤。
- 对 noindex、redirect、404 URL 是否出现在 sitemap 中，只在已抓取或用户提供证据时判断。

## 错误处理

| 场景 | 处理 |
|---|---|
| robots.txt 不可达 | 继续尝试 `/sitemap.xml`，并标注发现来源限制。 |
| sitemap index 嵌套过多 | 说明当前最多检查 10 个嵌套 sitemap。 |
| XML 无效或 gzip 解压失败 | 报告具体 sitemap URL，不推断其中 URL 状态。 |
| 用户要求提交 sitemap | 给出手动提交步骤；不声称本项目已调用 GSC。 |
