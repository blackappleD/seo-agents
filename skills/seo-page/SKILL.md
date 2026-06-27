---
name: seo-page
description: >
  单页 On-Page SEO 分析。检查 title、meta description、heading、canonical、
  robots、链接、图片、schema、Open Graph/Twitter metadata、薄内容和 SPA 渲染风险。
user-invocable: true
argument-hint: "<url>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Page

运行：

```bash
seo-agents page <url> --json
seo-agents page <url> --render-mode never --json
seo-agents page <url> --render-mode always --json
```

## 检查范围

- Fetch：抓取错误、4xx/5xx 状态。
- On-Page SEO：title 长度、meta description、H1 缺失或多个 H1。
- Indexability：canonical 缺失、跨 host canonical、meta robots noindex。
- Links：空 anchor text。
- Images：alt text、width/height、疑似 LCP 图片 lazy-load。
- Schema：JSON-LD 解析和基础字段。
- Social Metadata：Open Graph 和 Twitter/X card。
- Content Quality：可见文本低于 300 词。
- JavaScript Rendering：SPA 外壳在 raw 模式下无法获得渲染 HTML。

## 输出字段

- `summary.status_code`、`summary.final_url`、`summary.word_count` 用于快速判断页面状态。
- `parsed` 是结构化 HTML 提取结果，可作为后续内容或 schema 建议的依据。
- `snapshot` 保留 raw/rendered HTML 状态和渲染模式。
- `findings[*].evidence` 是报告引用的事实来源。

必要时读取 `../seo/references/quality-gates.md` 判断页面类型的内容深度阈值。

## 完成标准

- 先运行 `seo-agents page <url> --json`，必要时用 `--render-mode always` 复核 SPA 页面。
- 输出时覆盖 title、description、H1、canonical、robots、links、images、schema、social metadata 和内容深度。
- 建议必须落到具体 HTML 元素或 JSON 字段；例如说明缺的是 `meta description`、`og:image` 还是 `BreadcrumbList`。
- Core Web Vitals 只能作为参考提醒；当前 `page` 命令不测真实 field data。

## 错误处理

| 场景 | 处理 |
|---|---|
| URL 抓取失败 | 报告 `snapshot.error` 或 CLI 退出信息，不猜测页面。 |
| 401/403/登录墙 | 只分析可见 HTML，并建议提供公开 URL 或本地 HTML。 |
| raw HTML 为空但疑似 SPA | 用 `--render-mode always`，仍为空则标注结果不完整。 |
| schema JSON-LD 无效 | 交给 `seo-schema` 深入验证并给修复建议。 |
