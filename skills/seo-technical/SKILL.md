---
name: seo-technical
description: >
  技术 SEO 检查。覆盖 crawlability、indexability、HTTPS/security headers、
  URL structure、mobile viewport、structured data、JavaScript rendering、
  Core Web Vitals 占位说明和 IndexNow 验证提醒。
user-invocable: true
argument-hint: "<url>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Technical

运行：

```bash
seo-agents technical <url> --json
seo-agents technical <url> --render-mode auto --json
```

## 类别

当前 CLI 会生成 9 个类别：

- `Crawlability`
- `Indexability`
- `Security`
- `URL Structure`
- `Mobile`
- `Structured Data`
- `JavaScript Rendering`
- `Core Web Vitals`
- `IndexNow`

## 解释规则

- `technical_score` 是各类别分数的平均值。
- 抓取失败、错误状态码、`noindex`、非 HTTPS、缺少 viewport 等优先级较高。
- `Core Web Vitals` 当前不调用 PSI/CrUX，只提醒使用 INP 而不是 FID；如果用户需要真实 field data，明确说明本项目 Google provider 仍是离线占位。
- `IndexNow` 当前是验证提醒，不代表已经检查 key 文件或提交 endpoint。
- JavaScript SEO 结论以 raw/rendered HTML 差异为准；canonical、robots、schema 不应只依赖客户端后注入。
- AI crawler robots 规则属于技术可访问性补充项；报告时区分搜索抓取、AI search 访问和训练数据授权。

## 按需引用

- `references/agent-friendly-pages.md`：面向 crawler/agent 的页面可读性建议。
- `../seo/references/cwv-thresholds.md`：CWV 阈值背景；用于解释，不代表当前 CLI 已接入 CrUX。

## 完成标准

- 报告 9 个类别的 status、score、findings 和关键证据。
- Critical/High 优先给出会阻塞抓取、索引、安全或移动可用性的事项。
- 若用户要求 PageSpeed、CrUX 或真实 CWV，改用 `seo-google` 离线配置检测说明，不能声称已测。
- 对可修复建议给出验证命令，例如修复后复跑 `seo-agents technical <url> --json`。

## 错误处理

| 场景 | 处理 |
|---|---|
| URL 不可达 | 报告状态码/错误，不继续推断技术状态。 |
| `robots.txt` 缺失 | 作为提示处理；不自动视为严重错误。 |
| 非 HTTPS | 标为高优先级，并建议 HTTP 到 HTTPS 301。 |
| 渲染依赖缺失 | 说明需安装 render extra/Playwright，或用 `--render-mode never` 做有限分析。 |
