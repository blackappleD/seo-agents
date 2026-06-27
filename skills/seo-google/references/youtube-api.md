# YouTube 数据 API v3 参考

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

YouTube 提及与 AI 可见度的相关性最强（根据 GEO 研究，为 0.737）。该API直接从Google提供权威的YouTube数据。

## 使用的端点

|方法|配额成本|描述 |
|--------|------------|-------------|
| `search.list` | 100 单位 |搜索与查询匹配的视频 |
| `videos.list` | 1 单位 |获取视频详细信息、统计数据、内容 |
| `channels.list` | 1 单位 |获取频道信息、订阅者数量 |
| `commentThreads.list` | 1 单位 |获取视频的热门评论 |

## 每日配额

默认值：**10,000 单位/天**（免费）。这允许：
- 每天约 100 次搜索，或者
- 每天约 10,000 次视频/频道查找

## 可用数据

### 视频搜索
- 标题、频道、频道 ID、发布日期
- 描述（前 300 个字符）、缩略图 URL
- 观看次数、点赞数、评论数、持续时间

### 视频详情
- 完整描述、标签、类别 ID
- 时长、清晰度（高清/标清）、有字幕
- 主题类别（维基百科 URL）
- 观看次数、点赞、评论、收藏夹
- 热门 10 条相关评论

### 频道信息
- 标题、描述、自定义 URL
- 订阅者数量、视频数量、总观看次数
- 国家/地区、发布日期、缩略图

## 认证

**仅限 API 密钥**（只读公共数据）。无需 OAuth。

## 启用API

1. 前往[console.cloud.google.com/apis/library](https://console.cloud.google.com/apis/library)
2. 搜索“YouTube 数据 API v3”
3. 单击启用

无需计费。您已有的 PSI/CrUX API 密钥可以使用。

## 本项目适配边界

- 当前 `seo-agents google ...` 是离线占位，只检测配置字段来源，不调用真实 Google API。
- 本文件用于未来真实接入或人工核对字段，不得声称当前 CLI 已拉取 PSI、CrUX、GSC、GA4、Keyword Planner、NLP 或 YouTube 数据。
- 不输出 secret、token、refresh token、client secret 或完整凭据。
