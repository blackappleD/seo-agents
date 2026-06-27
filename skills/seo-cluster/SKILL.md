---
name: seo-cluster
description: >
  语义聚类和内容架构规划 playbook。用于基于 SERP overlap、hub-spoke、
  topic cluster 和内容优先级设计内容架构；当前无 `seo-agents cluster` CLI。
user-invocable: true
argument-hint: "<seed-keyword>"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Cluster

当前保留为 Agent playbook，尚无 `seo-agents cluster` CLI。不要声称可以自动抓取 SERP 或生成 cluster JSON。

## 推荐流程

1. 明确 seed keyword、目标市场、语言和业务类型。
2. 如果用户提供 SERP/keyword 数据，基于 URL overlap、intent、page type 聚类。
3. 设计 hub-spoke 或 pillar-cluster 架构，列出每个 cluster 的主页面、支持页和内部链接。
4. 输出优先级：business value、difficulty、content gap、已有资产复用度。
5. 标注数据缺口；没有外部 SERP 数据时明确为“离线规划”。

## 聚类规则

- 7-10 个 SERP shared URLs：通常合并为同一个目标页。
- 4-6 个 shared URLs：归为同一 cluster，但可拆不同 spoke。
- 2-3 个 shared URLs：相邻主题，保留交叉内链。
- 0-1 个 shared URLs：拆成独立 cluster 或排除。
- 无 SERP 数据时，使用 intent、实体、修饰词、page type 和业务价值做弱聚类，并标注低置信度。

## 输出结构

- Cluster map：pillar、spoke、target keyword、intent、page type、priority。
- Internal link matrix：spoke -> pillar、pillar -> spoke、spoke <-> spoke、cross-cluster。
- Brief queue：每个页面的 H1、角度、必须覆盖问题、schema、E-E-A-T 证据和 CTA。
- Scorecard：coverage、cannibalization、orphan risk、link density、content gap。

## 可用辅助命令

```bash
seo-agents dataforseo related-keywords "seed keyword" --json
```

该命令会调用真实 DataForSEO API，可能计费。只做配置检测时使用 `--offline`。

## 按需引用

- `references/serp-overlap-methodology.md`
- `references/hub-spoke-architecture.md`
- `references/execution-workflow.md`
- `templates/cluster-map.html`

## 完成标准

- 不生成 `cluster-plan.json` 或 `cluster-map.html` 文件，除非用户明确要求写文件。
- 不依赖来源项目的博客生成扩展；内容执行阶段转为 content brief。
- 每个 cluster 都要有主页面、支持页、意图、内链方向和优先级理由。

## 错误处理

| 场景 | 处理 |
|---|---|
| seed keyword 缺失 | 询问或从用户提供 URL/主题中抽取候选。 |
| keyword 数量不足 | 生成二次扩展方向，但标注无外部量级。 |
| SERP 数据缺失 | 使用离线规划，不声称 SERP overlap 已验证。 |
| cannibalization 风险 | 合并页面或重新分配 primary keyword。 |
