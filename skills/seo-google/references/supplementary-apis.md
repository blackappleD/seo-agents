# 用于 SEO 的补充 Google API

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 知识图谱搜索API

验证 Google 知识图谱中的品牌/实体存在情况。

**端点：** `GET https://kgsearch.googleapis.com/v1/entities:search`

|参数|描述 |
|--------|-------------|
| `query` |搜索查询 |
| `ids` |特定实体 ID（例如 `/m/0d6lp`）|
| `languages` |语言代码（例如 `en`）|
| `types` |要过滤的 Schema.org 类型（例如 `Organization`、`Person`）|
| `limit` |最大结果 (1-500) |
| `key` | API 密钥（必需）|

**回复：**

```json
{
  "itemListElement": [{
    "result": {
      "@id": "kg:/m/0d6lp",
      "name": "Google",
      "@type": ["Organization", "Corporation"],
      "description": "Technology company",
      "detailedDescription": {
        "articleBody": "Google LLC is an American...",
        "url": "https://en.wikipedia.org/wiki/Google"
      },
      "image": { "url": "..." },
      "url": "https://www.google.com"
    },
    "resultScore": 4892.5
  }]
}
```

**用于 SEO：** 验证品牌是否有知识面板、检查实体消歧、查找相关实体。

**配额：** 100,000 次阅读/天。自由的。仅 API 密钥。

---

## 自定义搜索 JSON API

程序化 Google 搜索结果（有限）。

**端点：** `GET https://customsearch.googleapis.com/customsearch/v1`

|参数|描述 |
|--------|-------------|
| `key` | API 密钥（必需）|
| `cx` |可编程搜索引擎 ID（必需）|
| `q` |搜索查询 |
| `num` |每页结果 (1-10) |
| `start` |开始索引（最大 91）|
| `dateRestrict` |日期限制（例如，`d30` 为 30 天）|
| `gl` |国家/地区（例如 `us`）|
| `lr` |语言限制 |
| `searchType` | `image` 用于图像搜索 |
| `siteSearch` |限制到某个域 |

**限制：**
- 每个查询最多 100 个总结果（10 页 x 10 个结果）
- **自 2025 年起不再向新客户开放。** 现有客户必须在 2027 年 1 月之前迁移。
- 每天 100 次免费查询，每天每 1,000 次至 10,000 次查询 5 美元

**对于 SERP 数据，首选 DataForSEO** (`/seo dataforseo serp`)，它没有此类限制。

---

## 网络风险 API

检查 URL 是否被 Google 安全浏览标记为不安全。

**端点：** `GET https://webrisk.googleapis.com/v1/uris:search`

|参数|描述 |
|--------|-------------|
| `threatTypes` | `MALWARE`、`SOCIAL_ENGINEERING`、`UNWANTED_SOFTWARE`、`SOCIAL_ENGINEERING_EXTENDED_COVERAGE` |
| `uri` |要检查的网址 |
| `key` | API 密钥（必需）|

**响应（干净的 URL）：** 空威胁对象。

**响应（标记的 URL）：**

```json
{
  "threat": {
    "threatTypes": ["MALWARE"],
    "expireTime": "2026-04-01T00:00:00Z"
  }
}
```

**用于SEO：** 检查页面是否被标记（可以解释取消索引），验证竞争对手的安全，审核出站链接。

**配额：** 6,000 QPM。 100,000/月免费套餐。需要在 GCP 项目上启用结算功能。

## 本项目适配边界

- 当前 `seo-agents google ...` 是离线占位，只检测配置字段来源，不调用真实 Google API。
- 本文件用于未来真实接入或人工核对字段，不得声称当前 CLI 已拉取 PSI、CrUX、GSC、GA4、Keyword Planner、NLP 或 YouTube 数据。
- 不输出 secret、token、refresh token、client secret 或完整凭据。
