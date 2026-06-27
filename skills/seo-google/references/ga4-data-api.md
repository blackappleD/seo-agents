# GA4 数据 API v1beta 参考

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 概述

Google Analytics Data API v1beta 提供对 GA4 报告数据的编程访问。对于 SEO，主要用例是有机流量分析。

**基本网址：** `https://analyticsdata.googleapis.com/v1beta`

## 关键方法

|方法|描述 |
|--------|-------------|
| `properties.runReport` |运行标准报告 |
| `properties.batchRunReports` |一次通话最多可生成 5 份报告 |
| `properties.runRealtimeReport` |最近 30 分钟的数据 |
| `properties.getMetadata` |可用维度和指标 |
| `properties.checkCompatibility` |验证维度/指标组合 |

## 运行报告请求

```json
{
  "property": "properties/123456789",
  "dimensions": [
    { "name": "date" },
    { "name": "landingPage" }
  ],
  "metrics": [
    { "name": "sessions" },
    { "name": "totalUsers" }
  ],
  "dateRanges": [
    { "startDate": "28daysAgo", "endDate": "yesterday" }
  ],
  "dimensionFilter": {
    "filter": {
      "fieldName": "sessionDefaultChannelGroup",
      "stringFilter": {
        "matchType": "EXACT",
        "value": "Organic Search"
      }
    }
  },
  "orderBys": [
    { "metric": { "metricName": "sessions" }, "desc": true }
  ],
  "limit": 100,
  "returnPropertyQuota": true
}
```

## SEO 相关维度

|尺寸|描述 |
|------------|-------------|
| `date` | YYYYMMDD 格式的日期 |
| `pagePath` |页面路径（例如 `/blog/post`）|
| `landingPage` |入口页面路径 |
| `landingPagePlusQueryString` |带有查询参数的入口页面 |
| `fullPageUrl` |整页网址 |
| `pageTitle` |page title |
| `sessionSource` |流量来源（例如 `google`）|
| `sessionMedium` |流量介质（例如 `organic`）|
| `sessionDefaultChannelGroup` |渠道分组（例如，`Organic Search`）|
| `country` |用户国家|
| `deviceCategory` | `desktop`、`mobile`、`tablet` |
| `hostName` |域名|
| `pageReferrer` |引荐来源网址 |

## SEO 相关指标

|指标|描述 |
|--------|-------------|
| `sessions` |会议次数 |
| `totalUsers` |独立用户总数 |
| `newUsers` |首次使用的用户 |
| `activeUsers` |参与度高的用户 |
| `screenPageViews` |页面浏览量 |
| `bounceRate` |跳出率（0-1，乘以 100 为 %）|
| `averageSessionDuration` |平均持续时间（以秒为单位）|
| `engagementRate` |参与会话率 (0-1) |
| `keyEvents` |关键事件（替换已弃用的 `conversions`）|
| `eventCount` |事件总数 |

## 过滤表达式

## 字符串过滤器

```json
{
  "filter": {
    "fieldName": "sessionDefaultChannelGroup",
    "stringFilter": {
      "matchType": "EXACT",
      "value": "Organic Search"
    }
  }
}
```

匹配类型：`EXACT`、`BEGINS_WITH`、`ENDS_WITH`、`CONTAINS`、`FULL_REGEXP`、`PARTIAL_REGEXP`

## 组合过滤器

```json
{
  "andGroup": {
    "expressions": [
      { "filter": { "fieldName": "country", "stringFilter": { "matchType": "EXACT", "value": "US" }}},
      { "filter": { "fieldName": "deviceCategory", "stringFilter": { "matchType": "EXACT", "value": "mobile" }}}
    ]
  }
}
```

还支持 `orGroup` 和 `notExpression`。

## 日期范围快捷方式

|价值|意义|
|--------|---------|
| `today` |当前日期 |
| `yesterday` |前一天 |
| `NdaysAgo` | N 天前（例如，`28daysAgo`）|
| `YYYY-MM-DD` |具体日期 |

每个请求最多 4 个日期范围（用于期间比较）。

## 基于代币的配额

|配额 |限制|范围 |
|--------|--------|--------|
|每日代币 | 25,000 | 25,000每个项目每个属性 |
|每小时代币 | 5,000 |每个项目每个属性 |
|并发请求 | 10 | 10每个项目每个属性 |
|每小时代币（项目范围）| 1,250 | 1,250每个项目每个 GA4 property每小时 |

设置 `returnPropertyQuota: true` 来监控功耗。简单的报告花费约 1-10 个代币；复杂的最多~100。

## Python 示例

```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Filter, FilterExpression,
    Metric, OrderBy, RunReportRequest,
)
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    "service_account.json",
    scopes=["https://www.googleapis.com/auth/analytics.readonly"],
)

client = BetaAnalyticsDataClient(credentials=credentials)

request = RunReportRequest(
    property="properties/123456789",
    dimensions=[Dimension(name="landingPage")],
    metrics=[Metric(name="sessions"), Metric(name="totalUsers")],
    date_ranges=[DateRange(start_date="28daysAgo", end_date="yesterday")],
    dimension_filter=FilterExpression(
        filter=Filter(
            field_name="sessionDefaultChannelGroup",
            string_filter=Filter.StringFilter(
                match_type=Filter.StringFilter.MatchType.EXACT,
                value="Organic Search",
            ),
        )
    ),
    order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
    limit=50,
    return_property_quota=True,
)

response = client.run_report(request)
for row in response.rows:
    print(f"{row.dimension_values[0].value}: {row.metric_values[0].value} sessions")
```

## 身份验证
- **范围：** `https://www.googleapis.com/auth/analytics.readonly`
- 服务帐号必须在 GA4 媒体资源中具有 **Viewer** 角色
- 通过 GA4 管理员 > 财产访问管理添加

## 本项目适配边界

- 当前 `seo-agents google ...` 是离线占位，只检测配置字段来源，不调用真实 Google API。
- 本文件用于未来真实接入或人工核对字段，不得声称当前 CLI 已拉取 PSI、CrUX、GSC、GA4、Keyword Planner、NLP 或 YouTube 数据。
- 不输出 secret、token、refresh token、client secret 或完整凭据。
