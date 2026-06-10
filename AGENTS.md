# seo-agents Agent 指南

seo-agents 是一套 Agent-first SEO 工具包。Agent harness 可以读取本文件、`skills/` 目录和 `agents/` 专家说明；人类和 CI 应使用 `src/seo_agents` 中的确定性 CLI。

## 语言偏好

- 默认使用简体中文回复、撰写报告和更新项目文档。
- 代码标识符、命令、路径、JSON key、Schema 类型、HTTP header、SEO/CLI/API/SSRF/SPA/JSON-LD 等专用名词和技术名词保留英文。
- 面向用户的错误、finding、CLI help、报告章节和 skill/agent 说明应使用中文。
- 不要把未实现能力写成已实现；外部数据源未接入时必须明确标注“未配置”或“离线占位”。

## CLI 入口

| 命令 | 状态 | 用途 |
|---|---|---|
| `seo-agents fetch <url>` | 已实现 | 带 SSRF 安全校验抓取 URL |
| `seo-agents render <url>` | 已实现 | 按 `never/auto/always` 模式渲染 URL |
| `seo-agents parse <html-file>` | 已实现 | 解析本地 HTML 文件 |
| `seo-agents audit <url>` | 已实现 | 全站审计，写入 Markdown 和 JSON artifact |
| `seo-agents page <url>` | 已实现 | 单页 On-Page SEO 分析 |
| `seo-agents technical <url>` | 已实现 | 技术 SEO 检查 |
| `seo-agents content <url>` | 已实现 | 内容质量、E-E-A-T 和 AI 引用友好信号 |
| `seo-agents schema <url>` | 已实现 | Schema 检测、验证和生成建议 |
| `seo-agents sitemap <url>` | 已实现 | sitemap 发现和校验 |
| `seo-agents images <url>` | 已实现 | 图片 SEO 检查 |
| `seo-agents geo <url>` | 已实现 | 本地可判断 AI Search / GEO 信号 |
| `seo-agents drift baseline <url>` | 已实现 | 建立 SEO 漂移基线 |
| `seo-agents drift compare <url>` | 已实现 | 与最近基线比较 |
| `seo-agents drift history <url>` | 已实现 | 查看漂移历史 |
| `seo-agents hreflang <url>` | 已实现 | hreflang / 国际化 SEO 检查 |
| `seo-agents local <url>` | 已实现 | 本地 SEO 基础检查 |
| `seo-agents ecommerce <url>` | 已实现 | Ecommerce SEO 基础检查 |
| `seo-agents google ...` | 离线占位 | Google 数据源配置检测，不联网 |
| `seo-agents backlinks ...` | 离线占位 | 外链数据源配置检测，不联网 |
| `seo-agents dataforseo ...` | 已实现 / 默认真实接入 | 默认调用 DataForSEO API；`--offline` 仅做配置检测 |
| `seo-agents firecrawl ...` | 离线占位 | Firecrawl 配置检测，不联网 |
| 无 CLI 入口 | 后续扩展 | `plan`、`cluster`、`sxo`、`programmatic`、`competitor-pages`、`content-brief` 目前只保留 skill/agent 说明 |

常用命令：

```bash
seo-agents fetch <url> --json
seo-agents render <url> --json
seo-agents parse <html-file> --json
seo-agents audit <url>
seo-agents page <url> --json
seo-agents content <url> --json
seo-agents technical <url> --json
seo-agents schema <url> --json
seo-agents sitemap <url> --json
seo-agents images <url> --json
seo-agents geo <url> --json
seo-agents drift baseline <url>
seo-agents google setup --json
seo-agents dataforseo user-data --json
```

## Harness 映射

- Codex：读取本文件和 `skills/*/SKILL.md`，用 shell 命令执行验证。
- Claude Code：读取相同 skill 文件；Claude 专用工具名需要映射到当前 harness 的 shell/文件读取能力。
- Cursor/Cline/Aider：把 `skills/` 当作任务 playbook，把 `src/seo_agents` 当作实现真相来源。

## Portability Check

编辑 skill 或命令后运行：

```bash
python scripts/portability_check.py --json
```

成功时应看到：

```json
{"errors": 0}
```

## 工程规则

- 用户输入 URL 在抓取前必须先经过 `validate_url_strict`。
- 拒绝 internal、private、loopback、link-local、metadata endpoint。
- Google、浏览器渲染、报告、付费 provider 等 optional dependency 不能在 import 阶段中断程序。
- Google、Backlinks、Firecrawl provider 命令当前只检测配置字段来源，不能调用真实 API，不能输出 secret 值。
- DataForSEO 默认调用真实 API；`user-data` 用于免费凭据验证，`serp`、`related-keywords`、`domain-rank` 可能计费。只做配置检测时使用 `--offline`。
- 每个 finding 必须有证据，且可机器读取。
- JSON audit data 是工程合同；Markdown/HTML/PDF 只是渲染层。
- `seo-agents` 是唯一 CLI 名称，不恢复旧别名。

## Git 规范

1. 遵循 Conventional Commits 规范，commit 描述均使用英文。格式如下：
<type>(<scope>): <description>

  - feat: 新功能 (feature)
  - fix: 修补 bug
  - docs: 文档变更
  - style: 不影响代码含义的格式修改（空格、分号等）
  - refactor: 重构（既不是新增功能，也不是修改 bug 的代码变动）
  - chore: 构建过程或辅助工具的变动

2. **原子性提交原则**: 每个 commit 必须只包含单一功能模块的改动，禁止将多个无关功能模块的代码混合提交。
