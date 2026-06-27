# seo-agents

![seo-agents pixel art banner](docs/assets/readme-banner.png)

[![简体中文](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-%E5%BD%93%E5%89%8D-brightgreen?style=flat-square)](README.md)
[![English](https://img.shields.io/badge/English-Click-blue?style=flat-square)](README.en.md)

Agent-first SEO 工具包。它把可被 Codex、Claude Code、Cursor、Cline、Aider 等 harness 读取的 `skills/`、`agents/`，和可测试、可复用的 Python CLI `seo-agents` 放在同一个项目里。

目标很简单：让 Agent 可以做 SEO 分析，但真正执行抓取、解析、评分和报告生成时，依赖确定性的本地 CLI，而不是只靠提示词。

这也是项目的本地 v2 闭环：Agent 负责理解任务和组织报告，`seo-agents` CLI 负责本地抓取、解析、验证、评分和 artifact 输出。

---

## 为什么选择 seo-agents

AI Search / GEO 正在成为 SEO 工作流的一部分，但传统 SEO 基础仍然不能丢。`seo-agents` 目前聚焦本地可判断的信号：

| 方向 | 覆盖内容 |
|---|---|
| Technical SEO | URL 安全校验、抓取、render 降级、indexability、canonical、Core Web Vitals 基础信号 |
| On-Page SEO | title、meta description、heading、link、social metadata |
| Content | 内容质量、可引用段落、E-E-A-T 相关页面信号 |
| Schema | JSON-LD 检测、基础校验、生成建议 |
| AI Search / GEO | entity schema、llms.txt、robots.txt 中常见 AI crawler 规则、citation-ready text |
| 垂直 SEO | images、hreflang、local、ecommerce |
| 监控 | drift baseline、compare、history |
| 外部数据 | DataForSEO 真实接入；Google、Backlinks、Firecrawl 当前为离线占位 |

不会把未接入的数据源伪装成真实数据。没有配置或尚未实现的 provider 会明确返回“未配置”或“离线占位”。

---

## 快速开始

### 环境要求

- Python 3.10+
- Git
- 可选：Playwright，用于 `render` 的浏览器渲染路径
- 可选：DataForSEO credentials，用于真实 SERP、related keywords、domain rank 查询

### 安装 CLI

```bash
python scripts/install.py --target cli
```

开发环境可以使用 editable install：

```bash
python -m pip install -e ".[dev]"
```

验证安装：

```bash
seo-agents --help
seo-agents page https://example.com --json
```

### 安装 Agent 资源

Codex：

```bash
python scripts/install.py --target codex
```

Claude Code：

```bash
python scripts/install.py --target claude
```

Open Agent Skills 风格目录：

```bash
python scripts/install.py --target open-agent
```

一次安装 CLI、Codex、Claude Code 和 open-agent assets：

```bash
python scripts/install.py --target all
```

更多安装选项见 [`docs/INSTALLATION.md`](docs/INSTALLATION.md)。根目录 `install.sh` 和 `install.ps1` 只是薄 wrapper，真实安装逻辑在 `scripts/install.py`。

---

## 命令

所有确定性能力都通过 `seo-agents` 运行。默认输出为人类可读摘要，添加 `--json` 输出机器可读 JSON。

| 命令 | 状态 | 用途 |
|---|---|---|
| `seo-agents fetch <url> --json` | 已实现 | 带 SSRF 安全校验抓取 URL |
| `seo-agents render <url> --json` | 已实现 | 按 `never/auto/always` 模式渲染 URL |
| `seo-agents parse <html-file> --json` | 已实现 | 解析本地 HTML 文件 |
| `seo-agents page <url> --json` | 已实现 | 单页 On-Page SEO 分析 |
| `seo-agents technical <url> --json` | 已实现 | 技术 SEO 检查 |
| `seo-agents content <url> --json` | 已实现 | 内容质量、E-E-A-T 和 AI 引用友好信号 |
| `seo-agents schema <url> --json` | 已实现 | Schema 检测、验证和生成建议 |
| `seo-agents sitemap <url> --json` | 已实现 | sitemap 发现和校验 |
| `seo-agents images <url> --json` | 已实现 | 图片 SEO 检查 |
| `seo-agents geo <url> --json` | 已实现 | AI Search / GEO 本地可判断信号 |
| `seo-agents hreflang <url> --json` | 已实现 | hreflang / 国际化 SEO 检查 |
| `seo-agents local <url> --json` | 已实现 | 本地 SEO 基础检查 |
| `seo-agents ecommerce <url> --json` | 已实现 | Ecommerce SEO 基础检查 |
| `seo-agents drift baseline <url>` | 已实现 | 建立 SEO 漂移基线 |
| `seo-agents drift compare <url>` | 已实现 | 与最近基线比较 |
| `seo-agents drift history <url>` | 已实现 | 查看漂移历史 |
| `seo-agents audit <url> --max-pages 20` | 已实现 | 聚合审计并写入 Markdown 和 JSON artifact |
| `seo-agents dataforseo user-data --json` | 已实现 | DataForSEO 免费凭据和余额验证 |
| `seo-agents dataforseo serp "keyword" --json` | 已实现 / 可能计费 | DataForSEO Google SERP live 查询 |
| `seo-agents dataforseo related-keywords "keyword" --json` | 已实现 / 可能计费 | DataForSEO related keywords live 查询 |
| `seo-agents dataforseo domain-rank example.com --json` | 已实现 / 可能计费 | DataForSEO domain rank overview live 查询 |
| `seo-agents google setup --json` | 离线占位 | 检测 Google 配置字段来源，不调用真实 API |
| `seo-agents backlinks setup --json` | 离线占位 | 检测 Backlinks 配置字段来源，不调用真实 API |
| `seo-agents firecrawl setup --json` | 离线占位 | 检测 Firecrawl 配置字段来源，不调用真实 API |

常用组合：

```bash
seo-agents audit https://example.com --max-pages 20
seo-agents geo https://example.com --json
seo-agents schema https://example.com --json
seo-agents drift baseline https://example.com
seo-agents dataforseo setup --offline --json
```

完整命令参考见 [`docs/COMMANDS.md`](docs/COMMANDS.md)。

---

## 架构

```text
seo-agents/
├── AGENTS.md                    # Agent harness 全局说明
├── skills/                      # Agent 可读 playbook
│   ├── seo/                     # 主路由 skill
│   ├── seo-audit/               # 全站审计流程
│   ├── seo-page/                # On-Page SEO
│   ├── seo-technical/           # 技术 SEO
│   ├── seo-content/             # 内容质量和 E-E-A-T
│   ├── seo-schema/              # Schema 分析
│   ├── seo-geo/                 # AI Search / GEO 信号
│   └── ...                      # sitemap、images、hreflang、local、ecommerce 等
├── agents/                      # 专家 agent 说明
│   ├── seo-technical.md
│   ├── seo-content.md
│   ├── seo-schema.md
│   ├── seo-geo.md
│   └── ...
├── src/seo_agents/              # 确定性 CLI 和库代码
│   ├── security/                # SSRF 防护和 URL 校验
│   ├── fetch/                   # HTTP 抓取、crawl、render
│   ├── extract/                 # HTML、schema、sitemap、images 解析
│   ├── modules/                 # page、technical、content、geo 等分析模块
│   ├── audit/                   # 全站审计编排和评分
│   └── reports/                 # Markdown 报告渲染
├── docs/                        # 安装、命令、架构、provider 文档
├── schema/                      # Schema 模板
├── scripts/                     # install、fetch、parse、render、portability check
├── tests/                       # pytest 测试
└── pyproject.toml               # Python package 和 CLI entry point
```

两层交付形态：

| 层级 | 用途 |
|---|---|
| Agent 层 | `AGENTS.md`、`skills/`、`agents/` 负责给 Agent 说明任务路由、语言偏好、安全边界和专家流程 |
| 确定性执行层 | `src/seo_agents/` 和 `seo-agents` CLI 负责真实抓取、解析、分析、评分、artifact 写入和测试 |

---

## 数据存储

`audit` 会在目标域名对应目录写入报告 artifact：

```text
<host>-audit/
├── audit-data.json
├── FULL-AUDIT-REPORT.md
├── ACTION-PLAN.md
├── findings/
│   ├── technical-seo.md
│   ├── content-quality.md
│   └── ...
└── screenshots/
```

`drift` 默认把 baseline 写入本机缓存目录：

```text
~/.cache/seo-agents/drift/baselines.db
```

可以用 `--output-dir` 覆盖 audit 输出目录，用 `--db` 覆盖 drift 数据库路径。

---

## 工作原理

### 全站审计流程

运行：

```bash
seo-agents audit https://example.com --max-pages 20
```

流程：

1. Discovery：从目标 URL 发现页面，最多分析 `--max-pages` 指定数量。
2. Safe fetch/render：所有 URL 先经过 `validate_url_strict`，拒绝 internal、private、loopback、link-local、metadata endpoint。
3. Parse：提取 metadata、heading、link、image、schema、hreflang、social tag 和正文文本。
4. Module analysis：运行 page、technical、content、schema、images、geo、hreflang、local、ecommerce 等模块。
5. External status：Google、Backlinks、Firecrawl 返回离线占位；DataForSEO 在 audit 中也按离线配置状态呈现。
6. Synthesis：聚合 findings，计算分类分和健康分。
7. Report：写入 `audit-data.json`、`FULL-AUDIT-REPORT.md`、`ACTION-PLAN.md` 和分类 findings。

### 评分方法

健康分来自分类得分的加权聚合：

| 分类 | 权重 |
|---|---:|
| Technical SEO | 22% |
| Content Quality | 23% |
| On-Page SEO | 20% |
| Schema / Structured Data | 10% |
| Performance / CWV | 10% |
| AI Search Readiness | 10% |
| Images | 5% |

单个分类分基于 finding severity 扣分：`Critical`、`High`、`Medium`、`Low`、`Info` 分别有不同 penalty。JSON audit data 是工程合同，当前 Markdown 报告是渲染层。

---

## 核心功能

### SSRF 安全抓取

所有用户输入 URL 在抓取前都会进行严格校验，阻止 private、loopback、link-local、metadata endpoint 和混淆 IP 等高风险目标。

### SPA 渲染降级

`render` 和多数分析命令支持 `--render-mode never|auto|always`。没有浏览器依赖时，optional dependency 不会在 import 阶段中断程序。

### 基于证据的发现项

每个 finding 都带 `evidence`，便于 Agent、人类和 CI 判断问题来源。`--json` 输出可直接进入后续自动化流程。

### GEO 就绪度检查

`geo` 会检查实体 schema、可引用段落、`llms.txt` / `llms-full.txt`、以及 `robots.txt` 中常见 AI crawler 规则。它只判断本地可观察信号，不声称能替代真实 AI 平台引用数据。

### 漂移监控

`drift baseline`、`drift compare`、`drift history` 可追踪 title、meta description、canonical、robots、heading、schema hash、HTML hash 和 status code 变化。

### DataForSEO 接入

`dataforseo` 默认调用真实 API。`user-data` 用于免费凭据和余额验证；`serp`、`related-keywords`、`domain-rank` 可能计费。只做配置检测时必须显式使用 `--offline`。

---

## 使用场景

- **SEO 顾问**：快速生成带证据的初步审计和行动计划。
- **市场团队**：持续检查页面改版后的 SEO drift。
- **内容团队**：发现标题、结构、可引用段落和 E-E-A-T 页面信号缺口。
- **开发者**：在 CI 或本地脚本里读取 JSON artifact，避免 SEO 检查只停留在人工 checklist。
- **Agent 构建者**：把 `skills/` 和 `agents/` 当作 playbook，把 `seo-agents` CLI 当作执行真相来源。
- **本地和电商站点**：补齐 local、ecommerce、schema、images、hreflang 等垂直基础检查。

---

## 外部数据源

配置默认读取 `~/.config/seo-agents/`，测试或隔离环境可用 `SEO_AGENTS_CONFIG_DIR` 覆盖配置目录。

| Provider | 配置 | 当前行为 |
|---|---|---|
| Google | `google-api.json` 或 `GOOGLE_API_KEY`、`GOOGLE_APPLICATION_CREDENTIALS` 等 env | 离线占位，只检测配置字段来源 |
| Backlinks | `backlinks-api.json` 或 `MOZ_API_KEY`、`BING_WEBMASTER_API_KEY` | 离线占位，只检测配置字段来源 |
| Firecrawl | `firecrawl-api.json` 或 `FIRECRAWL_API_KEY` | 离线占位，只检测配置字段来源 |
| DataForSEO | `dataforseo-api.json` 或 `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD` | 默认真实接入；`--offline` 仅做配置检测 |

所有 provider 命令都不会输出 secret 值。DataForSEO 细节见 [`docs/DATAFORSEO-INTEGRATION.md`](docs/DATAFORSEO-INTEGRATION.md)。

---

## 路线图说明

以下能力已有 skill/agent 说明，但当前没有 CLI 入口：`plan`、`cluster`、`sxo`、`programmatic`、`competitor-pages`、`content-brief`、`maps`、`flow`、`image-gen`。

如果要对外宣称某个能力已实现，请优先确认它是否存在于 `src/seo_agents/cli.py`，并有对应测试覆盖。

---

## 验证

```bash
python scripts/portability_check.py --json
pytest -q
```

默认测试不依赖真实网络或付费 API 凭据。

---

## 卸载

当前没有自动 uninstaller。按安装目标删除对应内容：

- CLI：`python -m pip uninstall seo-agents`
- Codex：删除 `$CODEX_HOME/skills/seo*`
- Claude Code：删除 `~/.claude/skills/seo*` 和 `~/.claude/agents/seo-*.md`
- Open Agent Skills：删除 `$AGENTS_HOME/skills/seo*`

---

## 参与贡献

欢迎提交改进。请遵循 Conventional Commits，并保持一个 commit 只包含一个功能模块的改动。

修改命令、skill 或 agent 说明后，至少运行：

```bash
python scripts/portability_check.py --json
```

---

## 许可证

MIT License

为 Agent-first SEO 工作流而构建。
