---
name: seo-drift
description: >
  SEO 漂移监控。建立和比较页面基线，追踪 title、description、canonical、
  robots、headings、schema、Open Graph、HTML hash 和 HTTP status 变化。
user-invocable: true
argument-hint: "baseline|compare|history <url>"
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
seo-agents drift compare <url> --db .cache/baselines.db --json
```

## 数据存储

默认 SQLite DB：

```text
~/.cache/seo-agents/drift/baselines.db
```

可用 `--db` 指定项目内或 CI 专用路径。

## 比较规则

- 200 变为 4xx/5xx：Critical。
- 新增 `noindex`：Critical。
- canonical 变更：跨 host 为 High，同 host 为 Medium。
- title 变化：Medium。
- H1 消失：High。
- schema hash 变化：缺失时 High，否则 Medium。
- HTML hash 变化：Info。

按需读取 `references/comparison-rules.md` 解释变更优先级。报告中要同时给出 before/after 值，避免只说“发生变化”。

## 捕获字段

当前基线关注 title、meta description、canonical、meta robots、H1/H2/H3、JSON-LD schema、Open Graph、HTTP status、HTML hash 和 schema hash。来源中的 CWV drift 依赖 PageSpeed/CrUX；本项目未真实接入 Google API，因此不把 CWV 当作 drift 字段。

## 典型工作流

```bash
seo-agents drift baseline <url> --json
# 部署或改版后
seo-agents drift compare <url> --json
seo-agents drift history <url> --json
```

发现变更后的交接：

- schema 变更：运行 `seo-agents schema <url> --json`。
- canonical/noindex/status 变更：运行 `seo-agents technical <url> --json`。
- title/description/H1 变更：运行 `seo-agents page <url> --json`。
- 内容 hash 大变：运行 `seo-agents content <url> --json`。

## 错误处理

| 场景 | 处理 |
|---|---|
| 无 baseline | 提示先运行 `baseline`，不要把当前状态当 drift。 |
| SQLite DB 不存在 | 首次 baseline 自动创建；history/compare 需说明无记录。 |
| URL 被 SSRF 拒绝 | 报告安全拒绝，不绕过。 |
| 当前页面 4xx/5xx | 仍可作为变更记录，但标为高风险。 |
