# 安装指南

seo-agents 有两层交付形态：

- 确定性 CLI：`seo-agents`，用于 CI、本地脚本和所有 harness 的真实执行。
- Agent assets：`AGENTS.md`、`skills/`、`agents/`，用于 Codex、Claude Code、Cursor、Cline、Aider 等 agent 读取。

## 前置要求

- Python 3.10+
- Git

根目录 `install.sh` 和 `install.ps1` 会检查 Python/Git，然后调用 `scripts/install.py`。远程安装请先 `git clone` 再运行脚本，避免 pipe-to-shell。

## CLI-only

安装 Python package，不复制 skill/agent 文件：

```bash
python scripts/install.py --target cli
```

开发环境可使用：

```bash
python -m pip install -e ".[dev]"
```

验证：

```bash
seo-agents --help
seo-agents page https://example.com --json
```

## Codex

安装到 Codex 用户级 skill 目录：

```bash
python scripts/install.py --target codex
```

默认路径：

- `$CODEX_HOME/skills/seo*`
- `$CODEX_HOME/skills/seo/references/agents/seo-*.md`

如果没有设置 `CODEX_HOME`，默认使用 `~/.codex`。Codex 没有采用 Claude Code 的全局 `agents` 目录，因此专家说明以 main skill reference 的形式分发。

## Claude Code

安装到 Claude Code 的 skill/agent 目录：

```bash
python scripts/install.py --target claude
```

默认路径：

- `~/.claude/skills/seo*`
- `~/.claude/agents/seo-*.md`

本项目不把 Claude Code plugin marketplace 作为唯一安装路径；Claude Code 用户也可以直接读取仓库并运行 CLI。

## Open Agent Skills

安装到 Open Agent Skills 风格目录：

```bash
python scripts/install.py --target open-agent
```

默认路径：

- `$AGENTS_HOME/skills/seo*`
- `$AGENTS_HOME/skills/seo/references/agents/seo-*.md`

如果没有设置 `AGENTS_HOME`，默认使用 `~/.agents`。

## Other harnesses

Cursor、Cline、Aider 等框架当前没有在本项目中假设统一的全局 skill 目录。推荐使用仓库模式：

1. 让 harness 读取本仓库的 `AGENTS.md`、`skills/`、`agents/`。
2. 通过 `seo-agents` CLI 执行确定性检查。
3. 把 JSON artifact 作为工程合同，Markdown 报告只作为渲染层。

## 常用选项

```bash
python scripts/install.py --target all
python scripts/install.py --target codex --dry-run --json
python scripts/install.py --target claude --skip-deps
python scripts/install.py --source /path/to/seo-agents --target open-agent
```

参数说明：

- `--target cli|codex|claude|open-agent|all`：安装目标，默认 `cli`。
- `--dry-run`：只输出将执行的操作，不写文件。
- `--skip-deps`：跳过 Python package 安装。
- `--source`：指定源码 checkout 路径。
- `--keep-temp`：保留临时目录；本地 checkout 安装不会创建临时目录。
- `--json`：输出机器可读 JSON。

## 安全边界

- 安装器不写入 secret。
- 安装器不修改 Google、Backlinks、Firecrawl、DataForSEO provider 配置。
- Google、Backlinks、Firecrawl 仍是离线占位，只检测配置来源。
- DataForSEO 保持现有行为：默认真实接入；只做配置检测时使用 `--offline`。
- `seo-agents` 是唯一 CLI 名称，不恢复旧别名。

## 验证

```bash
python scripts/portability_check.py --json
pytest -q
python -m pip install -e ".[dev]"
```

成功安装后：

```bash
seo-agents --help
seo-agents audit https://example.com --max-pages 20
```

## 卸载

当前没有自动 uninstaller。按安装目标删除对应目录即可：

- CLI：使用当前 Python 环境的 package 管理命令卸载，例如 `python -m pip uninstall seo-agents`。
- Codex：删除 `$CODEX_HOME/skills/seo*`。
- Claude Code：删除 `~/.claude/skills/seo*` 和 `~/.claude/agents/seo-*.md`。
- Open Agent Skills：删除 `$AGENTS_HOME/skills/seo*`。
