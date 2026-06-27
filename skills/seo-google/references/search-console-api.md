# Google Search Console API 参考

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 目录
1.[Search Analytics API](#search-analytics-api)
2.[URL Inspection API](#url-inspection-api)
3.[Sitemaps API](#sitemaps-api)
4.[Sites API](#sites-api)

---

## 搜索分析 API

**端点：** `POST https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/searchAnalytics/query`

### 请求正文

|领域|类型 |描述 |
|--------|------|-------------|
| `startDate` |字符串|必需的。 YYYY-MM-DD 格式。 |
| `endDate` |字符串|必需的。 YYYY-MM-DD 格式。 |
| `dimensions` |字符串[] | `query`、`page`、`country`、`device`、`date`、`searchAppearance` |
| `type` |字符串| `web`（默认）、`image`、`video`、`news`、`discover`、`googleNews` |
| `dimensionFilterGroups` |对象[] |过滤器组数组（见下文）|
| `aggregationType` |字符串| `auto`（默认）、`byPage`、`byProperty`、`byNewsShowcasePanel` |
| `rowLimit` |整数 | 1-25000（默认：1000）|
| `startRow` |整数 |分页偏移量（默认：0）|
| `dataState` |字符串| `final`（默认）、`all`、`hourly_all` |

### 维度过滤器

```json
{
  "dimensionFilterGroups": [{
    "filters": [{
      "dimension": "query",
      "operator": "contains",
      "expression": "seo"
    }]
  }]
}
```

**操作员：** `contains`、`equals`、`notContains`、`notEquals`、`includingRegex`、`excludingRegex`
- 正则表达式使用 RE2 语法，最多 4096 个字符

### 响应

```json
{
  "rows": [
    {
      "keys": ["seo tools", "https://example.com/tools"],
      "clicks": 150,
      "impressions": 5000,
      "ctr": 0.03,
      "position": 4.2
    }
  ],
  "responseAggregationType": "byPage"
}
```

### 重要提示
- 数据有 **2-3 天的滞后**。有效期约为 16 个月。
- `discover` 和 `googleNews` 类型不支持 `query` 尺寸或 `position` 指标。
- 国家/地区代码为 **ISO 3166-1 alpha-3**（例如 `USA`、`GBR`、`DEU`）。
- 分页：将 `startRow` 增加 `rowLimit`，直到返回的行数减少。

### 速率限制
- 每个用户 1,200 QPM
- 每个站点 1,200 QPM
- 每个项目 40,000 QPM / 30,000,000 QPD

---

## URL 检查 API

**端点：** `POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect`

### 请求

```json
{
  "inspectionUrl": "https://example.com/page",
  "siteUrl": "sc-domain:example.com",
  "languageCode": "en"
}
```

### 响应字段

**`indexStatusResult`：**

|领域|价值观 |
|--------|--------|
| `verdict` | `PASS`、`FAIL`、`NEUTRAL`、`PARTIAL`、`VERDICT_UNSPECIFIED` |
| `coverageState` |人类可读的覆盖范围描述 |
| `robotsTxtState` | `ALLOWED`、`DISALLOWED` |
| `indexingState` | `INDEXING_ALLOWED`、`BLOCKED_BY_META_TAG`、`BLOCKED_BY_HTTP_HEADER` |
| `pageFetchState` | `SUCCESSFUL`、`SOFT_404`、`BLOCKED_ROBOTS_TXT`、`NOT_FOUND`、`ACCESS_DENIED`、`SERVER_ERROR`、`REDIRECT_ERROR`、`ACCESS_FORBIDDEN`、`BLOCKED_4XX`、`INTERNAL_CRAWL_ERROR`、`INVALID_URL` |
| `lastCrawlTime` | ISO 8601 时间戳 |
| `googleCanonical` | URL Google 选为规范 |
| `userCanonical` |页面声明为规范的 URL |
| `crawledAs` | `DESKTOP`、`MOBILE` |

**`richResultsResult`：** 结论 + 检测到的丰富结果类型（FAQPage、HowTo 等）

### 速率限制
- 每个站点 2,000 QPD / 600 QPM
- 每个项目 10,000,000 QPD / 15,000 QPM

---

## 站点地图 API

**底座：** `https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps`

|方法|端点|描述 |
|--------|----------|-------------|
| `GET` | `/sitemaps` |列出所有站点地图 |
| `GET` | `/sitemaps/{feedpath}` |获取具体站点地图 |
| `PUT` | `/sitemaps/{feedpath}` |提交站点地图 |
| `DELETE` | `/sitemaps/{feedpath}` |删除站点地图 |

### 站点地图资源

|领域|描述 |
|--------|-------------|
| `path` |站点地图的 URL |
| `lastSubmitted` |上次提交时间戳 |
| `isPending` |是否加工不完整 |
| `isSitemapsIndex` |这是否是站点地图索引 |
| `type` | `sitemap`、`atomFeed`、`rssFeed`、`urlList`、`notSitemap` |
| `warnings` |警告计数 |
| `errors` |错误计数 |
| `contents[]` | `type`（网络、图像、视频、新闻）和 `submitted` 计数数组 |

---

## 站点 API

**底座：** `https://www.googleapis.com/webmasters/v3/sites`

|方法|端点|描述 |
|--------|----------|-------------|
| `GET` | `/sites` |列出所有已验证的属性 |
| `GET` | `/sites/{siteUrl}` |获取房产信息 |
| `PUT` | `/sites/{siteUrl}` |添加属性 |
| `DELETE` | `/sites/{siteUrl}` |删除属性 |

### 财产资源

|领域|价值观 |
|--------|--------|
| `siteUrl` |属性 URL（例如 `sc-domain:example.com`）|
| `permissionLevel` | `siteOwner`、`siteFullUser`、`siteRestrictedUser`、`siteUnverifiedUser` |

## 本项目适配边界

- 当前 `seo-agents google ...` 是离线占位，只检测配置字段来源，不调用真实 Google API。
- 本文件用于未来真实接入或人工核对字段，不得声称当前 CLI 已拉取 PSI、CrUX、GSC、GA4、Keyword Planner、NLP 或 YouTube 数据。
- 不输出 secret、token、refresh token、client secret 或完整凭据。
