# 中心辐射型内容架构

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 结构概述

中心辐射型集群由一个pillar页面（中心）组成，该pillar页面连接到多个
spoke集群，每个包含 2-4 个单独的文章。该pillar提供了广阔的
覆盖范围；spoke提供了对子主题的深入探讨。

```
                    [Spoke 1a] --- [Spoke 1b]
                         \       /
                      [Cluster 1]
                           |
[Spoke 2a] -- [Cluster 2] -- [PILLAR] -- [Cluster 3] -- [Spoke 3a]
[Spoke 2b] /                                        \ [Spoke 3b]
                           |
                      [Cluster 4]
                         /       \
                    [Spoke 4a] --- [Spoke 4b]
```

## pillar页面规格

|属性 |要求|
|------------|-------------|
|字数统计 | 2,500-4,000 字 |
|关键词 |集合中最广泛、数量最多的关键字 |
|内容类型 |涵盖所有集群子主题的全面概述 |
|模板| `ultimate-guide`（默认）|
|内部链接 |链接到每个集群中的每个分支文章（强制）|
|结构|目录、每个簇的部分、每个子主题的摘要 |
|架构| Article + BreadcrumbList + ItemList（列出所有集群页面）|
|更新频率|每季度或添加新spoke时刷新 |

## spoke页规格

|属性 |要求|
|------------|-------------|
|字数统计 | 1,200-1,800 字 |
|关键词 |特定子主题关键字（每个文章唯一）|
|内容类型 |深入探讨单个子主题 |
|模板|按意图选择（请参阅下面的模板映射）|
|内部链接 |链接到pillar（强制）+ 2-3 个同级spoke |
|架构|文章 + 面包屑列表 |
|深度 |比同一子主题的pillar内容更详细 |

## 集群约束

|约束|价值|
|----------|------|
|每个柱子的集群 | 2-5 | 2-5
|每个集群的文章 | 2-4 | 2-4
|职位总数（包括pillar）| 5-21 |
|最大估计字数 | ~50,000（pillar + 最多 20 根spoke）|

## 按意图自动选择模板

|意图模式|模板|描述 |
|----------------|----------|-------------|
|信息（广泛）| `ultimate-guide` |全面的主题概述 |
|信息（如何）| `how-to` |分步说明|
|信息（列表）| `listicle` |项目/提示的编号列表|
|信息（概念）| `explainer` |一个概念的深度解释|
|商业（比较）| `comparison` |并列产品/服务比较 |
|商业（评估）| `review` |对单一产品/服务的深入回顾|
|商业（等级）| `best-of` |热门选项排名列表|
|交易 | `landing-page` |以转化为重点的页面 |

**选择逻辑：**
1.将关键词的分类意图与上表进行匹配
2. 如果有多个模板匹配，则优先选择 SERP 结果显示最多的模板
   类似的内容格式（例如，如果顶部结果都是列表文章，则使用 `listicle`）
3. 避免同一集群内出现重复模板，除非有特殊意图

## 内部链接规则

## 强制链接
- 每个spoke必须链接到pillar（在正文内容中至少一次）
- pillar必须链接到每个spoke（在其相关部分）
- 这些是不可协商的——没有这些链接的集群在结构上就被破坏了

## 推荐链接
- 同一集群内的spoke对spoke：每个文章 2-3 个链接
- 使用上下文锚文本（目标关键字或紧密变体）
- 将链接放置在正文段落中，而不仅仅是“相关文章”部分

## 可选链接
- 跨集群分支到分支：每个文章 0-1 个链接
- 仅当集群之间存在真正的主题桥梁时
- 避免强制交叉链接，这不会增加读者价值

## 最低链接要求
- 每个文章必须至少有 3 个传入内部链接
- 没有孤立页面（点击 2 次即可从pillar访问每个页面）
- 锚文本多样性：没有一个锚文本用于超过 40% 的页面链接

## 同类相食预防

1. **没有两个文章共享相同的主要关键字。** 期间。
2.如果两个关键词之间的SERP重叠超过7，则合并到一个文章中
3. 聚类后，验证唯一性：列出所有主关键字并检查
   几乎重复（例如，“最佳 CRM”和“顶级 CRM 软件”）
4. 如果发现近似重复，请合并文章或有意区分
   （例如，一个作为“最佳”列表，另一个作为“比较”）

## JSON-LD 架构模板

## pillar页面

```json
[
  { "@type": "Article", "headline": "...", "author": {...}, "datePublished": "..." },
  { "@type": "BreadcrumbList", "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "..." },
    { "@type": "ListItem", "position": 2, "name": "Pillar Title", "item": "..." }
  ]},
  { "@type": "ItemList", "name": "Topic Cluster", "itemListElement": [
    { "@type": "ListItem", "position": 1, "url": "spoke-1-url" }
  ]}
]
```

## spoke页面

```json
[
  { "@type": "Article", "headline": "...", "author": {...}, "isPartOf": { "@id": "pillar-url" } },
  { "@type": "BreadcrumbList", "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "..." },
    { "@type": "ListItem", "position": 2, "name": "Pillar Title", "item": "pillar-url" },
    { "@type": "ListItem", "position": 3, "name": "Spoke Title", "item": "..." }
  ]}
]
```

## cluster-plan.json 架构

```json
{
  "version": "1.9.0",
  "seed_keyword": "string",
  "created_at": "ISO-8601",
  "pillar": {
    "title": "string",
    "keyword": "string",
    "volume": 0,
    "template": "ultimate-guide",
    "wordCount": 4000,
    "url": "string",
    "status": "planned|written"
  },
  "clusters": [
    {
      "name": "Cluster Name",
      "posts": [
        {
          "title": "string",
          "keyword": "string",
          "volume": 0,
          "template": "string",
          "wordCount": 1500,
          "url": "string",
          "status": "planned|written"
        }
      ]
    }
  ],
  "links": [
    { "from": "pillar", "to": "cluster-0-post-0", "type": "mandatory", "anchor": "keyword" }
  ],
  "serp_matrix": {
    "keywords": ["string"],
    "scores": [[0]]
  },
  "scorecard": {
    "coverage": 0.0,
    "linkDensity": 0.0,
    "orphanPages": 0,
    "cannibalization": 0,
    "contentGaps": 0
  }
}
```

## 本项目适配边界

- 优先使用当前已实现的 `seo-agents` CLI 获取证据；没有 CLI 的能力作为 Agent playbook 或后续扩展处理。
- 不把外部数据源、付费 provider、浏览器渲染或地图 API 写成已执行，除非当前任务确实运行并取得证据。
- 每个 finding 必须有可复核 evidence；数据缺失时明确写“未配置”或“缺少输入”。
