---
name: seo-google
description: >
  Google SEO API 离线占位。检测 Search Console、PageSpeed/CrUX、Indexing、
  GA4、Keyword Planner 等配置字段来源和 credential tier；当前不联网、不调用真实 API、
  不输出 secret 值。
user-invocable: true
argument-hint: "[subcommand] [target]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO Google

运行：

```bash
seo-agents google setup --json
seo-agents google pagespeed <url> --json
seo-agents google gsc <property> --json
```

所有子命令当前都会进入同一个离线占位处理器，返回配置状态和下一步建议，不发起 Google API 请求。

## 配置检测

会检查：

- 配置目录：`~/.config/seo-agents/google-api.json`，可通过 `SEO_AGENTS_CONFIG_DIR` 覆盖。
- 环境变量：`GOOGLE_APPLICATION_CREDENTIALS`、`GOOGLE_API_KEY`、`GA4_PROPERTY_ID`、`GSC_PROPERTY`。
- OAuth token：`oauth-token.json` 是否存在。

credential tier 只代表本地字段完整度：

- Tier 0：API key，可支撑未来 PageSpeed/CrUX。
- Tier 1：service account 或 OAuth，可支撑未来 GSC/Indexing。
- Tier 2：另有 GA4 property。
- Tier 3：另有 Ads developer token 和 customer ID。

## 边界

- 不调用 PageSpeed、CrUX、GSC、URL Inspection、Indexing、GA4 或 Ads。
- 不输出 API key、token、password、service account 内容。
- `references/` 中的 Google API 文档用于后续真实接入设计；引用时必须说明当前项目尚未实现。
- 来源 skill 中的 pagespeed、crux、gsc、inspect、index、ga4、youtube、nlp、keywords、volume 和 report 命令，在本项目里都映射为同一个离线占位处理器。

## 可读资料

- `references/auth-setup.md`
- `references/pagespeed-crux-api.md`
- `references/search-console-api.md`
- `references/ga4-data-api.md`
- `references/indexing-api.md`
- `references/rate-limits-quotas.md`
- `assets/templates/*.md`

## 完成标准

- 输出 `configured`、`configured_fields`、`credential_tier`、`sources` 和下一步建议。
- 如果用户要求真实 PSI/CrUX/GSC/GA4 数据，说明当前未实现，并建议后续增加 provider 客户端、mock 测试、配额处理和 secret redaction。
- 对 `audit` 或 `technical` 中的 CWV 建议，只引用阈值背景，不伪造 field data。

## 错误处理

| 场景 | 处理 |
|---|---|
| 无配置 | 返回“未配置”和配置路径，不报错退出真实调用。 |
| 配置 JSON 无效 | 报告 `config_error`，不输出文件内容。 |
| 用户提供 service account 内容 | 提醒不要贴 secret，建议保存到本地路径。 |
| 用户要求提交 Indexing API | 说明当前不会联网提交。 |
