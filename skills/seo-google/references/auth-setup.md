# Google API 身份验证设置

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 概述

三种凭证类型服务于不同的 API：

|类型 |使用者 |成本|
|------|---------|------|
| **API 密钥** | PageSpeed 见解、CrUX、CrUX 历史、知识图 |免费|
| **服务帐户** |Search Console、索引 API、GA4 |免费|
| **两者** |完整的 SEO-Google 技能 |免费|

## 第 1 步：创建 Google Cloud 项目

1. 前往[console.cloud.google.com](https://console.cloud.google.com)
2. 单击 **选择项目** > **新建项目**
3. 为其命名（例如“seo-agents”）并记下项目 ID
4.创建后选择项目

## 步骤 2：启用 API

导航到 **API 和服务 > 库** 并启用：

|应用程序接口 |需要 |
|-----|-------------|
|GoogleSearch ConsoleAPI | GSC 搜索分析、URL 检查、站点地图 |
| PageSpeed Insights API | PSI Lighthouse Lab 数据 |
| Chrome 用户体验报告 API | CrUX 真实用户数据 + 历史 |
|网页搜索索引 API |索引 API v3 |
|Google分析数据API | GA4 自然流量 |
|知识图谱搜索API |实体验证（可选）|

## 步骤 3：创建 API 密钥

1. **API 和服务 > 凭证 > 创建凭证 > API 密钥**
2. 单击**限制键**：
   - 在 **API 限制** 下，选择：PageSpeed Insights API、Chrome UX Report API、Knowledge Graph Search API
3. 复制生成的API密钥并安全存储

## 步骤 4：创建服务帐户

1. **IAM 和管理 > 服务帐户 > 创建服务帐户**
2.名称：`seo-agents`（或类似名称）
3. 跳过可选权限步骤
4. 单击创建的服务帐户 > **密钥 > 添加密钥 > 创建新密钥 > JSON**
5. 下载 JSON 文件并安全存储（例如 `~/.config/seo-agents/service_account.json`）

JSON 文件如下所示：

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "seo-agents@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
```

`client_email` 字段是您添加到 GSC 和 GA4 的字段。

## 步骤 5：授予 Search Console 访问权限

1. 前往[Google Search Console](https://search.google.com/search-console)
2. 选择您的房产
3. **设置 > 用户和权限 > 添加用户**
4.粘贴服务帐户`client_email`
5. 设置权限级别：
   - **完整**只读（搜索分析、URL 检查、站点地图）
   - **所有者** 如果您还需要索引 API

## 第 6 步：授予 GA4 访问权限

1. 前往[Google Analytics](https://analytics.google.com)
2. **管理 > 财产访问管理 > 添加用户**（+ 图标）
3.粘贴服务帐户`client_email`
4. 设置角色：**查看者**（只读报告的最低限度）
5. 记下 **管理 > 属性详细信息** 中的数字属性 ID（例如 `123456789`）

## 步骤 7：创建配置文件

```bash
mkdir -p ~/.config/seo-agents
```

保存到 `~/.config/seo-agents/google-api.json`：

```json
{
  "service_account_path": "~/.config/seo-agents/service_account.json",
  "api_key": "<GOOGLE_API_KEY>",
  "default_property": "sc-domain:example.com",
  "ga4_property_id": "properties/123456789"
}
```

## 属性 URL 格式

|格式|示例|何时使用 |
|--------|---------|-------------|
|域名属性 | `sc-domain:example.com` |涵盖域上的所有 URL（推荐）|
| URL 前缀属性 | `https://example.com/` |仅涵盖该特定前缀 |

## 步骤 8：验证设置

```bash
python3 scripts/google_auth.py --check
```

第 2 层的预期产出（完整）：

```
Credential Tier: 2 -- Full (API key + Service Account + GA4)

  [OK] PageSpeed Insights v5
  [OK] Chrome UX Report (CrUX) API
  [OK] CrUX History API
  [OK] Google Search Console API
       Service account: seo-agents@your-project.iam.gserviceaccount.com
  [OK] Google Indexing API v3
  [OK] GA4 Data API v1beta
```

## 环境变量替代方案

代替（或补充）配置文件：

|变量|目的|
|----------|---------|
| `GOOGLE_API_KEY` | PSI/CrUX 的 API 密钥 |
| `GOOGLE_APPLICATION_CREDENTIALS` |服务帐户 JSON 的路径 |
| `GA4_PROPERTY_ID` | GA4 媒体资源（例如 `properties/123456789`）|
| `GSC_PROPERTY` |默认 GSC 属性（例如 `sc-domain:example.com`）|

## 使用的 OAuth 范围

|范围 | API |
|--------|------|
| `https://www.googleapis.com/auth/webmasters.readonly` | GSC（读）|
| `https://www.googleapis.com/auth/webmasters` | GSC（读/写，提交站点地图所需）|
| `https://www.googleapis.com/auth/indexing` |索引 API |
| `https://www.googleapis.com/auth/analytics.readonly` | GA4（阅读）|

## 故障排除

|错误|修复 |
|--------|-----|
| GSC 上的 `403 Forbidden` |服务帐户电子邮件未添加到 GSC 属性，或权限级别错误 |
| GA4 上的 `403 Forbidden` |服务帐号电子邮件未作为查看者添加到 GA4 媒体资源 |
| GSC 上的 `404 Not Found` |属性 URL 格式错误。使用 `sc-domain:` 或在 URL 前缀中包含尾部斜杠 |
| CrUX 上的 `404 Not Found` |网站 Chrome 流量不足。不是凭证问题。 |
| `429 Rate Limit` |等待并重试。请参阅rate-limits-quotas.md 了解每个 API 的限制 |
| `API not enabled` |在 GCP Console > API 和服务 > 库 | 中启用特定 API

## 本项目适配边界

- 当前 `seo-agents google ...` 是离线占位，只检测配置字段来源，不调用真实 Google API。
- 本文件用于未来真实接入或人工核对字段，不得声称当前 CLI 已拉取 PSI、CrUX、GSC、GA4、Keyword Planner、NLP 或 YouTube 数据。
- 不输出 secret、token、refresh token、client secret 或完整凭据。
