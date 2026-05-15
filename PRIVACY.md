# 隐私说明

seo-agents 默认在本地运行。

- 传给 CLI 的 URL 会由本机抓取。
- 本地 v2 闭环不会上传 audit data 到托管服务。
- audit artifact 会写入本地输出目录。
- Google、DataForSEO、Firecrawl、Moz、Bing Webmaster 等 provider 当前为离线占位；未来接入真实 API 时，URL/查询可能发送到对应平台。
- Provider 命令会检测本机配置字段是否存在，但不会联网、不会调用真实 API、不会输出 secret 值。
- 凭据应放在 `~/.config/seo-agents/` 或受控的 `~/.claude/settings.json` 等本地配置路径中，不应提交到仓库。
