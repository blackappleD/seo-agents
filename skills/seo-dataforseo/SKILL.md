---
name: seo-dataforseo
description: >
  DataForSEO 外部数据源：默认调用真实 DataForSEO API，--offline 仅做配置检测，不输出 secret 值。
user-invocable: true
argument-hint: "[subcommand] [target]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO DataForSEO

默认真实数据源：

```bash
seo-agents dataforseo serp "keyword" --json
```

免费凭据验证：

```bash
seo-agents dataforseo user-data --json
```

付费查询：

```bash
seo-agents dataforseo serp "keyword" --json
seo-agents dataforseo related-keywords "keyword" --json
seo-agents dataforseo domain-rank example.com --json
```

只做配置检测时运行：

```bash
seo-agents dataforseo setup --offline --json
```

SERP、related keywords、domain rank 会按 DataForSEO 账户计费。
