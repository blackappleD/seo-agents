---
name: seo-audit
description: >
  全站 SEO 审计，聚合 page、technical、content、schema、sitemap、images、
  geo、hreflang、local、ecommerce 和外部数据源占位结果。
user-invocable: true
argument-hint: "[url] [--max-pages 20]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Audit

运行：

```bash
seo-agents audit <url> --max-pages 20
```

预期 artifact：

- `FULL-AUDIT-REPORT.md`
- `ACTION-PLAN.md`
- `audit-data.json`
- `findings/*.md`
