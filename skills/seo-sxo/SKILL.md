---
name: seo-sxo
description: >
  Search Experience Optimization playbook。用于判断页面类型、search intent、
  user stories、persona fit、转化路径和搜索体验问题；当前无 `seo-agents sxo` CLI。
user-invocable: true
argument-hint: "<url>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO SXO

当前保留为 Agent playbook，尚无 `seo-agents sxo` CLI。

## 推荐流程

1. 运行 `page/content/technical` 获取页面证据。
2. 判断页面类型是否匹配 query intent：informational、commercial、transactional、local、support 等。
3. 写出用户故事、阻力点、信任缺口、CTA 和信息架构建议。
4. 对每条建议标注 SEO 影响、转化影响、验证方式和依赖项。
5. 当前 CLI 不采集真实行为分析、热图或 A/B test 数据；不要把 SXO 结论说成用户实测。

## 执行框架

- Target acquisition：确认 URL、目标关键词、业务目标和主要转化。
- SERP backwards analysis：只有在用户提供 SERP 或显式使用外部数据时进行；否则用 intent 假设。
- Page-type alignment：目标页类型与搜索意图不匹配时优先修正页面形态。
- User stories：把搜索者问题写成“作为...我想...以便...”。
- Gap analysis：page type、content depth、UX、schema、media、authority、freshness。
- Persona scoring：不同 persona 对信任、速度、价格、证明和支持的敏感度。

## 可结合命令

```bash
seo-agents page <url> --json
seo-agents content <url> --json
seo-agents technical <url> --json
```

## 按需引用

- `references/page-type-taxonomy.md`
- `references/persona-scoring.md`
- `references/user-story-framework.md`
- `references/wireframe-templates.md`

## 完成标准

- 输出 target intent、页面类型匹配度、用户故事、SXO gaps、persona scores、priority actions 和 limitations。
- 建议必须同时说明 SEO impact 与 conversion impact。
- wireframe 只能作为文本结构/模块顺序建议；除非用户要求，不生成设计文件。

## 错误处理

| 场景 | 处理 |
|---|---|
| 没有目标关键词 | 从页面推断候选，但标注低置信度并建议用户确认。 |
| SERP 数据缺失 | 用 intent playbook 做离线分析，不声称已比较 SERP。 |
| 页面 JS 渲染不足 | 使用 `page --render-mode always` 或标注 HTML 限制。 |
