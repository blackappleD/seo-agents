# Google 索引 API v3 参考

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 概述

Indexing API 允许您在添加或删除页面时通知 Google。

**重要提示：** 官方仅限于具有 **JobPosting** 或 **BroadcastEvent/VideoObject** 结构化数据的页面。 Google 可能会处理其他页面类型，但不提供任何保证。始终告知用户此限制。

## 端点

## 发布通知

**`POST https://indexing.googleapis.com/v3/urlNotifications:publish`**

```json
{
  "url": "https://example.com/jobs/software-engineer",
  "type": "URL_UPDATED"
}
```

|领域|价值观 |
|--------|--------|
| `url` |完全限定的 URL |
| `type` | `URL_UPDATED`（页面已添加/更改）、`URL_DELETED`（页面已删除）|

**回复：**

```json
{
  "urlNotificationMetadata": {
    "url": "https://example.com/jobs/software-engineer",
    "latestUpdate": {
      "url": "https://example.com/jobs/software-engineer",
      "type": "URL_UPDATED",
      "notifyTime": "2026-03-27T10:00:00Z"
    }
  }
}
```

## 获取通知元数据

**`GET https://indexing.googleapis.com/v3/urlNotifications/metadata?url={ENCODED_URL}`**

返回 URL 的 `latestUpdate` 和 `latestRemove` 时间戳。

## 批量请求

**`POST https://indexing.googleapis.com/batch`**

使用 `multipart/mixed` 格式的每个批量请求最多 **100 个 URL**：

```
POST /batch HTTP/1.1
Content-Type: multipart/mixed; boundary=batch_boundary

--batch_boundary
Content-Type: application/http
Content-ID: <item1>

POST /v3/urlNotifications:publish HTTP/1.1
Content-Type: application/json

{"url": "https://example.com/jobs/1", "type": "URL_UPDATED"}
--batch_boundary
Content-Type: application/http
Content-ID: <item2>

POST /v3/urlNotifications:publish HTTP/1.1
Content-Type: application/json

{"url": "https://example.com/jobs/2", "type": "URL_UPDATED"}
--batch_boundary--
```

## 认证

- **范围：** `https://www.googleapis.com/auth/indexing`
- **身份验证类型：** 服务帐户 (OAuth 2.0)
- 服务帐户必须是目标域的 Google Search Console 中的**所有者**

## 配额

|限制|价值|范围 |
|--------|--------|--------|
|发布请求 | **200/天**（默认）|每个项目 |
|只读请求 | 180/分钟 |每个项目 |
|请求总数 | 380/分钟 |每个项目 |

请求增加配额：[Indexing API Quota Increase Form](https://developers.google.com/search/apis/indexing-api/v3/quota-increase)

## 错误代码

|代码|意义|行动|
|------|---------|--------|
| 400 | URL 或请求正文格式错误 |检查 URL 格式 |
| 403 | 403权限被拒绝或超出配额 |在 GSC 中将服务帐户添加为所有者，或检查配额 |
| 429 | 429超出速率限制 |后退并以指数延迟重试 |
| 500/503 | 500/503服务器错误|使用指数退避重试 |

## 最佳实践

1. 仅提交实际内容更改的 URL（不要发送垃圾更新）
2.仅当页面被永久删除时才使用`URL_DELETED`（返回404/410）
3. 跟踪每日配额使用情况——每天 200 个配额的限制在太平洋时间午夜重置
4. 对于大规模索引，请使用 XML 站点地图 + Search Console
5. 批量请求单独计入每日配额（100 批 = 100 配额）

## 本项目适配边界

- 当前 `seo-agents google ...` 是离线占位，只检测配置字段来源，不调用真实 Google API。
- 本文件用于未来真实接入或人工核对字段，不得声称当前 CLI 已拉取 PSI、CrUX、GSC、GA4、Keyword Planner、NLP 或 YouTube 数据。
- 不输出 secret、token、refresh token、client secret 或完整凭据。
