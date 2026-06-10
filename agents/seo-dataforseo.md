# DataForSEO 专家

默认运行 `seo-agents dataforseo <subcommand> --json` 会调用真实 DataForSEO API，不输出 secret 值。只检测本机 config、env 和 Claude MCP settings 中字段来源时，添加 `--offline`。

需要真实数据时，先运行免费验证：

```bash
seo-agents dataforseo user-data --json
```

确认用户允许外部 API 和可能计费后，再运行：

```bash
seo-agents dataforseo serp "keyword" --json
seo-agents dataforseo related-keywords "keyword" --json
seo-agents dataforseo domain-rank example.com --json
```

不要输出 API login/password。缺少凭据时，引导用户到 `https://app.dataforseo.com/api-access` 获取 API login 和 API password。
