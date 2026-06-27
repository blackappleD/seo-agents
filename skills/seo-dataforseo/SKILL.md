---
name: seo-dataforseo
description: >
  DataForSEO 外部数据源。默认调用真实 DataForSEO API；`--offline` 仅做配置检测。
  用于 user-data 免费凭据验证、Google organic SERP、related keywords 和 domain rank 查询。
user-invocable: true
argument-hint: "[subcommand] [target]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---

# SEO DataForSEO

## 重要边界

默认是真实 API。除 `setup/status/user-data` 外，`serp`、`related-keywords`、`domain-rank` 都可能按 DataForSEO 账户计费。只想检查配置时必须加 `--offline`。

## 命令

```bash
seo-agents dataforseo setup --offline --json
seo-agents dataforseo user-data --json
seo-agents dataforseo serp "keyword" --json
seo-agents dataforseo related-keywords "keyword" --json
seo-agents dataforseo domain-rank example.com --json
seo-agents dataforseo serp "ai seo" --location-code 2840 --language-code en --depth 10 --device desktop --limit 10 --json
```

## 配置来源

- 配置文件：`~/.config/seo-agents/dataforseo-api.json`，字段为 `username` 和 `password`。
- 环境变量：`DATAFORSEO_USERNAME`、`DATAFORSEO_PASSWORD`。
- agent MCP settings 中的 `dataforseo` env 也会被检测；当前代码兼容 `~/.claude/settings.json` 路径。

## 输出字段

- `mode: live` 表示真实 API 调用。
- `charged` 标明该调用是否计费。
- `credential_source` 标明凭据来源，不输出 secret。
- `cost`、`tasks_count`、`tasks_error` 来自 DataForSEO 响应。
- `--include-raw` 会输出脱敏后的原始响应，调试时才使用。

按需读取：

- `references/tool-catalog.md`：可扩展 DataForSEO 工具目录。
- `references/cost-tiers.md`：计费风险说明。

## 当前支持命令

| 命令 | 当前状态 | 费用边界 |
|---|---|---|
| `setup` / `status` / `user-data` | 已实现真实 API | 官方标注不收费 |
| `serp` | 已实现 Google organic live advanced | 可能计费 |
| `related-keywords` | 已实现 Labs related keywords | 可能计费 |
| `domain-rank` | 已实现 Labs domain rank overview | 可能计费 |

来源 skill 中的 images、YouTube、backlinks、competitors、ranked keywords、traffic、onpage、business listings、AI mentions 等 DataForSEO 工具当前未接入；只能作为 `references/tool-catalog.md` 中的扩展候选。

## 完成标准

- 真实调用前提醒费用边界，尤其是 `serp`、`related-keywords`、`domain-rank`。
- 输出时引用 `mode`、`charged`、`endpoint`、`summary`、`cost`、`tasks_error` 和 `credential_source`。
- 不输出 username/password/API raw secret；`--include-raw` 也必须依赖代码脱敏。
- 命令不支持时报告 available commands，不编造 DataForSEO 数据。

## 错误处理

| 场景 | 处理 |
|---|---|
| 未配置凭据 | 报告“未配置”，不发起网络请求。 |
| 参数缺失 | 返回命令示例，例如 keyword 或 domain。 |
| API 返回错误 | 保留 http/api status、cost 和 tasks_error，建议用户检查凭据/余额/参数。 |
| 只想检查配置 | 使用 `--offline`。 |
