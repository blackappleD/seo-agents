---
name: seo
description: >
  SEO 主路由，覆盖 audit、page、technical、content、schema、sitemap、images、
  geo、drift、hreflang、local、ecommerce，以及离线占位 provider。
user-invocable: true
argument-hint: "<command> [url]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO

当用户需要 SEO 分析、站点审计或命令发现时使用本 skill。

优先使用确定性 CLI：

```bash
seo-agents page <url> --json
seo-agents content <url> --json
seo-agents technical <url> --json
seo-agents audit <url> --max-pages 20
```

所有网络目标都会在抓取前执行 URL 安全校验。默认使用中文输出；命令名、JSON key 和技术名词保留英文。
