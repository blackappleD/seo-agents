---
name: seo-drift
description: >
  SEO 漂移监控，使用 SQLite 保存页面关键元素基线并比较 title、canonical、robots、heading、schema 和 HTML hash。
user-invocable: true
argument-hint: "baseline|compare|history [url]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Drift

运行：

```bash
seo-agents drift baseline <url>
seo-agents drift compare <url>
seo-agents drift history <url>
```

默认数据库位于 `~/.cache/seo-agents/drift/baselines.db`，测试可使用 `--db` 指定临时路径。
