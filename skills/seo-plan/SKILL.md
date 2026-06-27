---
name: seo-plan
description: >
  SEO 策略规划 playbook。用于 SaaS、ecommerce、local service、publisher、
  agency 或 generic 业务的 SEO roadmap、优先级、里程碑和资源计划；当前无 CLI 入口。
user-invocable: true
argument-hint: "<business-type>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Plan

当前保留为 Agent playbook，尚无 `seo-agents plan` CLI。

## 推荐流程

1. 明确 business type、目标市场、当前站点、资源约束和时间窗口。
2. 对现有站点先运行 `seo-agents audit <url>`；若无站点则基于用户提供信息做离线规划。
3. 选择 `assets/` 中的业务模板作为输出骨架。
4. 计划必须区分：已由 CLI 证据支持、需要外部数据、需要人工确认。
5. 输出 30/60/90 天路线图，附 owner、impact、effort、dependency 和验证指标。

## 规划维度

- Discovery：业务模式、目标用户、市场/语言、现有站点、内容资产、团队资源。
- Competitive analysis：仅在用户提供竞品或显式使用外部数据时进行；否则标为数据缺口。
- Architecture：站点结构、目录策略、pillar/cluster、内链和模板页面边界。
- Content strategy：页面类型、关键词主题、E-E-A-T 证据、更新节奏和内容复用。
- Technical foundation：抓取、索引、canonical、schema、sitemap、性能和监控。
- Authority：数字 PR、资源页、合作伙伴、社区和品牌实体建设。

## 可结合命令

```bash
seo-agents audit <url>
seo-agents dataforseo related-keywords "seed" --json
```

`dataforseo` 默认真实 API，可能计费；只检测配置时用 `--offline`。

## 模板

- `assets/generic.md`
- `assets/saas.md`
- `assets/ecommerce.md`
- `assets/local-service.md`
- `assets/publisher.md`
- `assets/agency.md`

## 完成标准

- 输出至少包含：现状假设、机会主题、技术基础、内容路线图、权限/资源依赖、KPI 和 30/60/90 天计划。
- KPI 不得凭空承诺具体增长；没有 baseline 时用“待建立基线”。
- 每项行动标注 evidence source：`audit`、用户输入、DataForSEO、人工假设或离线占位。

## 错误处理

| 场景 | 处理 |
|---|---|
| business type 不明确 | 使用 `generic.md`，并列出需要用户确认的问题。 |
| 没有站点 URL | 进入新站规划模式，跳过当前站点审计。 |
| 模板缺失 | 回退到 `generic.md`，在输出中说明。 |
