# 隐私说明

seo-agents 默认在本地运行。

- 传给 CLI 的 URL 会由本机抓取。
- 本地 v2 闭环不会上传 audit data 到托管服务。
- audit artifact 会写入本地输出目录。
- Google、Firecrawl、Moz、Bing Webmaster 等 provider 当前为离线占位；未来接入真实 API 时，URL/查询可能发送到对应平台。
- DataForSEO 默认调用真实 DataForSEO API，keyword/domain/query 会发送到 DataForSEO；只做本机配置检测时使用 `--offline`。
- Provider 命令不会输出 secret 值；DataForSEO `--include-raw` 也会对 credential-like 字段做脱敏。
- 凭据应放在 `~/.config/seo-agents/` 或受控的 `~/.claude/settings.json` 等本地配置路径中，不应提交到仓库。
