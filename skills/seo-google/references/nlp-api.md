# Google Cloud Natural Language API 参考

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

NLP 分析通过使用 Google 自己的分类法测量实体覆盖范围、内容情感和主题分类来增强 E-E-A-T 评分。

## 端点

实体使用 `POST https://language.googleapis.com/v1/documents:analyzeEntities`。
情绪、分类和调节使用
`POST https://language.googleapis.com/v2/documents:annotateText`。

在 `X-Goog-Api-Key` 标头中发送 API 密钥，而不是在 URL 中。

## 特征

|功能 |它有什么作用 |SEO使用 |
|---------|-------------|---------|
| `extractEntities` |提取具有显着性分数的人物、组织、地点、事件 |主题覆盖深度、实体优化 |
| `extractDocumentSentiment` |文档+句子级情感分数/幅度|内容语气评估|
| `classifyText` |将内容映射到 700 多个 Google 类别 |主题相关性验证 |
| `moderateText` |内容安全/审核类别 |内容质量标志 |

## 实体类型

人物、地点、组织、事件、WORK_OF_ART、CONSUMER_GOOD、其他、电话号码、地址、日期、号码、价格

每个实体包括：
- `name`：实体文本
- `type`：实体类型
- `salience`：重要性评分（0-1，越高=相关性越高）
- `sentiment`：每个实体的情绪（分数+幅度）
- `metadata`：维基百科 URL，MID（知识图 ID）
- `mentions`：文本中出现的情况

## 情绪评分

- **分数**：-1.0（负）至 +1.0（正）
- **幅度**：0到无穷大（情绪强度，越高=越情绪化）
- 中性内容：得分~0，低强度
- 混合内容：分数~0，高强度（正面和负面）

## 定价

|功能 |免费/月 |付费（每 1K 字符）|
|--------|---------|--------------------|
|实体分析| 5,000 单位 | 0.001 美元 |
|情绪分析| 5,000 单位 | 0.001 美元 |
|内容分类 | 30,000 单位 | 0.002 美元 |
|文本审核 | 50,000 单位 | 0.0005 美元 |

一个“单位”= 1,000 个字符。免费套餐每月重置。

## 启用API

1. 前往[console.cloud.google.com/apis/library](https://console.cloud.google.com/apis/library)
2.搜索“云自然语言API”
3. 单击启用
4. **必须在项目上启用计费**（免费套餐仍然适用）

使用与 PSI/CrUX 相同的 API 密钥。

## 本项目适配边界

- 当前 `seo-agents google ...` 是离线占位，只检测配置字段来源，不调用真实 Google API。
- 本文件用于未来真实接入或人工核对字段，不得声称当前 CLI 已拉取 PSI、CrUX、GSC、GA4、Keyword Planner、NLP 或 YouTube 数据。
- 不输出 secret、token、refresh token、client secret 或完整凭据。
