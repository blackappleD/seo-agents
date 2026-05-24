---
name: seo-sitemap
description: >
  sitemap 发现、XML/gzip 解析、sitemap index 展开、lastmod 检查和 URL 数量限制。
user-invocable: true
argument-hint: "[url]"
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

MVP 会从 `robots.txt` 和 `/sitemap.xml` 发现 sitemap。
