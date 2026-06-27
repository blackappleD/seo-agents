# 执行流程

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 概述

执行阶段将 `cluster-plan.json` 转换为实际内容。它处理
优先级排序、博客作者的上下文注入、外链更新、
恢复能力和执行后质量评分。

## 优先级算法

内容是按照以下严格的顺序创建的：

1. **首先是pillar页面** -- 中心必须存在，然后任何spoke才能链接到它
2. **按搜索量排列的spoke（降序）** -- 搜索量最高的spoke首先出现
   最大的早期影响
3. **在同一卷内，按集群索引** -- 在集群 1 之前处理集群 0
4. **在同一集群内，按文章索引** -- 在文章 1 之前处理文章 0

理由：pillar建立了话题权威基础。高产量
spoke产生最多的自然流量，因此应该尽早发布
以获得更快的复利回报。

## 集群上下文注入

当为每个文章调用 `blog-write` 时，传递一个结构化上下文块：

```json
{
  "cluster_context": {
    "role": "pillar|spoke",
    "pillar_title": "The Complete Guide to ...",
    "pillar_url": "/guide/...",
    "cluster_name": "Cluster Name",
    "cluster_index": 0,
    "post_index": 0,
    "primary_keyword": "target keyword",
    "secondary_keywords": ["variant 1", "variant 2"],
    "template": "how-to",
    "word_count_target": 1500,
    "outgoing_links": [
      { "url": "/pillar-url", "anchor": "main topic guide", "type": "mandatory" },
      { "url": "/sibling-post", "anchor": "related subtopic", "type": "recommended" }
    ],
    "incoming_link_placeholder": "<!-- cluster-link:cluster-0-post-1 -->",
    "differentiation_note": "This post should focus on X, while sibling post covers Y"
  }
}
```

## 上下文字段解释

|领域|目的|
|--------|---------|
| `role` |这是柱子还是spoke（影响深度和广度） |
| `pillar_title` / `pillar_url` |因此spoke可以连接回pillar|
| `cluster_name` / `cluster_index` |用于组织和标记|
| `post_index` |在集群中的位置 |
| `primary_keyword` |这篇文章的主要目标关键词|
| `secondary_keywords` |自然合并的其他关键字 |
| `template` |遵循的内容模板（操作方法、清单、比较等）|
| `word_count_target` |目标字数（不是硬性限制，而是指南）|
| `outgoing_links` |这篇文章必须包含链接，并带有建议的锚文本 |
| `incoming_link_placeholder` |用于未来内部链接注入的 HTML 注释标记 |
| `differentiation_note` |这篇文章与针对类似主题的兄弟姐妹有何不同|

## 内部链接注入

每写完一篇新文章后，更新以前写的文章以链接到它：

## 过程

1.从`cluster-plan.json`读取链接矩阵
2. 确定所有应链接到新撰写的文章的文章
3. 对于每一篇文章（已经写良好）：
   a.打开文章文件
   b.搜索占位符评论：`<!-- cluster-link:POST_ID -->`
   c.将占位符替换为实际的上下文链接
   d.如果未找到占位符，请在最相关的部分中附加上下文链接
4. 记录所有添加的外链

## 占位符格式

```html
<!-- cluster-link:cluster-0-post-1 -->
```

这是在内容创建期间插入到上下文适当的位置的。
当稍后编写目标文章时，占位符将替换为：

```html
For a deeper dive, see our guide on <a href="/target-url">anchor text</a>.
```

## 恢复能力

执行可以被中断和恢复。恢复算法：

## 检测

1.从当前目录读取`cluster-plan.json`
2. 扫描输出目录中是否存在现有的 post 文件
3. 使用以下方法将找到的文件与计划进行匹配：
   - 文件名模式（从标题或关键字派生的 slug）
   - 内容检查（检查 frontmatter 或第一个 H1 中是否有 `primary_keyword`）
4. 在计划中将匹配的文章标记为 `"status": "written"`

## 恢复逻辑

1. 加载具有更新状态的计划
2. 仅过滤 `"status": "planned"` 文章
3. 对剩余文章应用优先级算法
4. 从下一个未写的文章继续执行
5. 对新编写的和新编写的之间的任何链接运行内部链接注入
   以前写过的文章

## 边缘情况

- 如果柱子缺失但spoke存在，则先写柱子，然后写
  将内部链接注入现有spoke
- 如果分支文件存在但不完整（低于目标字数的 50%），
  将其视为未写并重新创建
- 如果 `cluster-plan.json` 自上次执行以来已被修改，则重新验证
  恢复前的计划

## 记分卡指标

执行完成后（或按需），生成`cluster-scorecard.md`：

## 指标定义

|指标|公式|目标|
|--------|---------|--------|
|覆盖范围| `written_posts / planned_posts * 100` | 100% |
|链接密度| `total_internal_links / total_posts` |每个文章 >= 3.0 |
|孤儿页面 |带有 0 个传入内部链接的文章计数 | 0 |
|pillar连接 | `spokes_linking_to_pillar / total_spokes * 100` | 100% |
|反向pillar链接| `spokes_linked_from_pillar / total_spokes * 100` | 100% |
|交叉链接| `implemented_cross_links / recommended_cross_links * 100` | >= 80% |
|蚕食|共享主要关键字的文章计数 | 0 |
|图片数量 |至少包含一张图片的文章/文章总数 | >= 90% |
|内容差距|计划中的文章尚未撰写| 0 |
|平均字数 |所有书面文章的平均字数 |距离目标 10% 以内 |

## 记分卡输出格式

```markdown
# Cluster Scorecard: [Seed Keyword]

## Summary
- Posts: X/Y written (Z%)
- Total words: N (estimated: M)
- Internal links: L (density: L/Y per post)

## Metrics
| Metric | Score | Status |
|--------|-------|--------|
| Coverage | 100% | PASS |
| Link Density | 3.2/post | PASS |
| ...

## Issues Found
- [List any FAIL or WARN metrics with remediation steps]

## Next Steps
- [Actionable items to reach 100% on all metrics]
```

## 质量门

在将执行标记为完成之前，请验证：

1. 每个spoke都与pillar相连（强制）
2. pillar连接到每个spoke（强制）
3. 没有文章的传入内部链接少于 3 个
4. 没有两个文章共享相同的主要关键字
5. 不存在孤立页面
6. 所有文章均符合最低字数要求（目标的 80%）

如果任何门失败，请在记分卡中标记它并提供具体的补救措施
说明。不要默默地通过失败的集群。

## 本项目适配边界

- 优先使用当前已实现的 `seo-agents` CLI 获取证据；没有 CLI 的能力作为 Agent playbook 或后续扩展处理。
- 不把外部数据源、付费 provider、浏览器渲染或地图 API 写成已执行，除非当前任务确实运行并取得证据。
- 每个 finding 必须有可复核 evidence；数据缺失时明确写“未配置”或“缺少输入”。
