# DataForSEO 外部数据源接入方案

## 方案选择

本轮选择 DataForSEO 作为第一个完整外部数据源接入对象。

原因：

- 覆盖 SERP、related keywords、domain rank overview 等 SEO 工作流，能补足本地 HTML 分析无法判断的外部搜索数据。
- 认证模型是 API login + API password 的 Basic Auth，不需要复杂 OAuth 回调，适合 CLI-first 工具。
- 官方提供免费账户信息接口 `/v3/appendix/user_data`，可先做不计费的连通性验证。
- DataForSEO 命令默认接入真实 API；只做本地配置检测时使用 `--offline`。

官方入口：

- API 认证说明：https://docs.dataforseo.com/v3/auth/
- API Access 页面：https://app.dataforseo.com/api-access
- 免费账户信息接口：https://docs.dataforseo.com/v3/appendix-user-data/
- SERP live advanced：https://docs.dataforseo.com/v3/serp-se-type-live-advanced/
- Related keywords：https://docs.dataforseo.com/v3/dataforseo_labs-google-related_keywords-live/
- Domain rank overview：https://docs.dataforseo.com/v3/dataforseo_labs-google-domain_rank_overview-live/

## 凭据获取

如果本机没有凭据，需要使用内置浏览器打开：

```text
https://app.dataforseo.com/api-access
```

由人类用户完成注册、登录、邮箱/手机验证和付款/试用设置后，在 API Access 页面获取：

- API login
- API password

注意：API password 是 DataForSEO 自动生成的 API 凭据，不是账户登录密码。

## 本机配置

推荐配置文件：

```json
{
  "username": "DATAFORSEO_API_LOGIN",
  "password": "DATAFORSEO_API_PASSWORD"
}
```

默认路径：

```text
~/.config/seo-agents/dataforseo-api.json
```

也支持环境变量：

```bash
DATAFORSEO_USERNAME=...
DATAFORSEO_PASSWORD=...
```

测试隔离时可设置：

```bash
SEO_AGENTS_CONFIG_DIR=/tmp/seo-agents-config
SEO_AGENTS_CLAUDE_SETTINGS=/tmp/claude-settings.json
```

## CLI 命令

默认接入真实数据源：

```bash
seo-agents dataforseo user-data --json
seo-agents dataforseo serp "ai seo" --json
```

离线配置检测：

```bash
seo-agents dataforseo setup --offline --json
```

付费查询：

```bash
seo-agents dataforseo serp "ai seo" --json
seo-agents dataforseo related-keywords "ai seo" --json --limit 20
seo-agents dataforseo domain-rank example.com --json
```

可调参数：

- `--location-code`：默认 `2840`，United States。
- `--language-code`：默认 `en`。
- `--depth`：SERP 深度，默认 `10`。
- `--device`：`desktop` 或 `mobile`。
- `--limit`：summary 输出条数，默认 `10`。
- `--include-raw`：输出脱敏后的原始 API response。

## 数据合同

真实 API 输出必须包含：

- `mode: "live"`
- `configured: true`
- `charged: true/false`
- `endpoint`
- `request`
- `http_status`
- `api_status_code`
- `api_status_message`
- `cost`
- `summary`

默认不输出凭据值；`--include-raw` 也会脱敏 `login`、`password`、`token`、`secret`、`authorization` 等字段。

## 错误和降级

- 没有完整凭据时，默认真实接入返回 `mode: "unavailable"`，且不发起网络请求。
- 添加 `--offline` 时返回 `mode: "offline-placeholder"`，只检测配置字段和来源。
- DataForSEO 返回 `401/402` 或内部 `status_code` 非成功时，CLI 返回非零退出码，并保留可机器读取的错误状态。
- SERP、related keywords、domain rank 默认调用真实 API，可能按 DataForSEO 账户计费；`audit` 当前仍只聚合配置状态，不会自动触发这些付费查询。

## 验收清单

- `python scripts/portability_check.py --json` 返回 `{"errors": 0}`。
- `pytest -q` 通过，且测试不依赖真实网络或真实 DataForSEO 凭据。
- 无凭据时运行 `seo-agents dataforseo user-data --json` 不联网，返回 `unavailable`。
- 配置凭据后运行 `seo-agents dataforseo user-data --json` 能完成免费验证。
- `seo-agents dataforseo --help` 不再出现旧的 live 参数，并提供 `--offline`。
