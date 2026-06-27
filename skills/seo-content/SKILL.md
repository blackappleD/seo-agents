---
name: seo-content
description: >
  内容质量、E-E-A-T 和 AI Citation Readiness 检查。识别薄内容、低信息密度表达、
  作者/日期/信任信号不足，以及缺少可独立引用的定义、数字、步骤或 FAQ 式段落。
user-invocable: true
argument-hint: "<url>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Content

运行：

```bash
seo-agents content <url> --json
seo-agents content <url> --render-mode always --json
```

## 检查范围

- `word_count < 300`：薄内容风险。
- 常见泛化营销短语：例如 `cutting-edge`、`seamless experience` 等低信息密度表达。
- Author / byline / reviewed by / 组织责任主体信号。
- Published / updated / 日期格式信号。
- Contact / privacy / terms / refund / Organization / LocalBusiness 等信任信号。
- Citation-ready blocks：长度适中、可独立引用且含事实、定义或数字的段落。

## 输出解读

- `summary.filler_hits` 是命中的泛化短语数量。
- `signals.citation_blocks` 会返回最多 5 个可引用候选段落。
- finding 建议要落到具体内容补强：经验、步骤、案例、数据、政策、作者/审核说明。

## 按需引用

- `../seo/references/eeat-framework.md`：更细的 E-E-A-T 评估标准。
- `../seo/references/quality-gates.md`：按页面类型判断内容深度、重复和规模化风险。

## Who / How / Why

从来源能力迁移时，内容评估必须显式回答：

- Who：谁创建/审核内容，是否有 byline、作者页、组织责任主体或专业资质。
- How：内容如何形成，是否有一手经验、测试过程、数据来源或 AI 协助说明。
- Why：页面目的是否服务用户任务，而不是只为搜索流量堆砌关键词。

## AI 内容与引用友好

- AI 内容不是默认负面；只有缺少事实、经验、原创价值或可验证来源时才标为风险。
- Citation-ready 段落应短而完整，包含定义、步骤、数字、比较或明确结论。
- 不要把 `llms.txt` 当成引用排名因素；GEO 相关边界交给 `seo-geo`。

## 完成标准

- 输出内容质量问题、E-E-A-T 缺口、citation-ready 候选和可执行 rewrite 方向。
- 若是 YMYL、local、ecommerce 或 programmatic 页面，按更高信任门槛解释。
- 对每个建议说明需要新增的证据类型：作者、案例、截图、政策、数据、FAQ 或原创经验。

## 错误处理

| 场景 | 处理 |
|---|---|
| 可抓取正文少于 100 词 | 标注薄内容或渲染/访问限制，不补写虚构正文。 |
| 付费墙或登录墙 | 只分析公开片段，建议用户提供全文。 |
| 目标关键词缺失 | 基于页面主题做有限分析；需要关键词策略时转 `seo-content-brief` 或 DataForSEO。 |
