# seo-agents

[![English](https://img.shields.io/badge/English-Current-brightgreen?style=flat-square)](README.en.md)
[![简体中文](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-%E7%82%B9%E5%87%BB%E6%9F%A5%E7%9C%8B-blue?style=flat-square)](README.md)

An agent-first SEO toolkit. It combines agent-readable `skills/` and `agents/` for Codex, Claude Code, Cursor, Cline, Aider, and similar harnesses with a testable Python CLI named `seo-agents`.

The goal is simple: agents can help with SEO analysis, while fetching, parsing, scoring, and report generation are handled by deterministic local CLI code instead of prompts alone.

---

## Why seo-agents

AI Search / GEO is becoming part of SEO workflows, but traditional SEO fundamentals still matter. `seo-agents` focuses on signals that can be inspected locally:

| Area | Coverage |
|---|---|
| Technical SEO | URL safety checks, fetching, render fallback, indexability, canonical, basic Core Web Vitals signals |
| On-Page SEO | title, meta description, headings, links, social metadata |
| Content | content quality, citation-ready paragraphs, E-E-A-T related page signals |
| Schema | JSON-LD detection, basic validation, generation suggestions |
| AI Search / GEO | entity schema, llms.txt, common AI crawler rules in robots.txt, citation-ready text |
| Vertical SEO | images, hreflang, local, ecommerce |
| Monitoring | drift baseline, compare, history |
| External Data | live DataForSEO integration; Google, Backlinks, and Firecrawl are offline placeholders |

The project does not pretend that unconnected providers have real data. Missing or not-yet-implemented providers are explicitly reported as "unconfigured" or "offline placeholder".

---

## Quick Start

### Requirements

- Python 3.10+
- Git
- Optional: Playwright, for the browser rendering path in `render`
- Optional: DataForSEO credentials, for live SERP, related keywords, and domain rank queries

### Install CLI

```bash
python scripts/install.py --target cli
```

For development, use an editable install:

```bash
python -m pip install -e ".[dev]"
```

Verify the installation:

```bash
seo-agents --help
seo-agents page https://example.com --json
```

### Install Agent Assets

Codex:

```bash
python scripts/install.py --target codex
```

Claude Code:

```bash
python scripts/install.py --target claude
```

Open Agent Skills style directory:

```bash
python scripts/install.py --target open-agent
```

Install the CLI, Codex, Claude Code, and open-agent assets together:

```bash
python scripts/install.py --target all
```

See [`docs/INSTALLATION.md`](docs/INSTALLATION.md) for more installation options. The root `install.sh` and `install.ps1` files are thin wrappers; the real installer lives in `scripts/install.py`.

---

## Commands

All deterministic capabilities run through `seo-agents`. The default output is a human-readable summary. Add `--json` for machine-readable JSON.

| Command | Status | Purpose |
|---|---|---|
| `seo-agents fetch <url> --json` | Implemented | Fetch a URL with SSRF-aware safety checks |
| `seo-agents render <url> --json` | Implemented | Render a URL in `never/auto/always` mode |
| `seo-agents parse <html-file> --json` | Implemented | Parse a local HTML file |
| `seo-agents page <url> --json` | Implemented | Run single-page on-page SEO analysis |
| `seo-agents technical <url> --json` | Implemented | Run technical SEO checks |
| `seo-agents content <url> --json` | Implemented | Analyze content quality, E-E-A-T, and AI citation-friendly signals |
| `seo-agents schema <url> --json` | Implemented | Detect, validate, and suggest Schema markup |
| `seo-agents sitemap <url> --json` | Implemented | Discover and validate sitemaps |
| `seo-agents images <url> --json` | Implemented | Check image SEO |
| `seo-agents geo <url> --json` | Implemented | Inspect locally observable AI Search / GEO signals |
| `seo-agents hreflang <url> --json` | Implemented | Check hreflang / international SEO |
| `seo-agents local <url> --json` | Implemented | Run basic local SEO checks |
| `seo-agents ecommerce <url> --json` | Implemented | Run basic ecommerce SEO checks |
| `seo-agents drift baseline <url>` | Implemented | Create an SEO drift baseline |
| `seo-agents drift compare <url>` | Implemented | Compare against the latest baseline |
| `seo-agents drift history <url>` | Implemented | View drift history |
| `seo-agents audit <url> --max-pages 20` | Implemented | Run an aggregated audit and write Markdown plus JSON artifacts |
| `seo-agents dataforseo user-data --json` | Implemented | Validate DataForSEO credentials and balance through a free endpoint |
| `seo-agents dataforseo serp "keyword" --json` | Implemented / may cost credits | Run a live DataForSEO Google SERP query |
| `seo-agents dataforseo related-keywords "keyword" --json` | Implemented / may cost credits | Run a live DataForSEO related keywords query |
| `seo-agents dataforseo domain-rank example.com --json` | Implemented / may cost credits | Run a live DataForSEO domain rank overview query |
| `seo-agents google setup --json` | Offline placeholder | Check Google config fields without calling the real API |
| `seo-agents backlinks setup --json` | Offline placeholder | Check Backlinks config fields without calling the real API |
| `seo-agents firecrawl setup --json` | Offline placeholder | Check Firecrawl config fields without calling the real API |

Common combinations:

```bash
seo-agents audit https://example.com --max-pages 20
seo-agents geo https://example.com --json
seo-agents schema https://example.com --json
seo-agents drift baseline https://example.com
seo-agents dataforseo setup --offline --json
```

See [`docs/COMMANDS.md`](docs/COMMANDS.md) for the full command reference.

---

## Architecture

```text
seo-agents/
├── AGENTS.md                    # Global instructions for agent harnesses
├── skills/                      # Agent-readable playbooks
│   ├── seo/                     # Main routing skill
│   ├── seo-audit/               # Full-site audit workflow
│   ├── seo-page/                # On-page SEO
│   ├── seo-technical/           # Technical SEO
│   ├── seo-content/             # Content quality and E-E-A-T
│   ├── seo-schema/              # Schema analysis
│   ├── seo-geo/                 # AI Search / GEO signals
│   └── ...                      # sitemap, images, hreflang, local, ecommerce, and more
├── agents/                      # Specialist agent instructions
│   ├── seo-technical.md
│   ├── seo-content.md
│   ├── seo-schema.md
│   ├── seo-geo.md
│   └── ...
├── src/seo_agents/              # Deterministic CLI and library code
│   ├── security/                # SSRF protection and URL validation
│   ├── fetch/                   # HTTP fetching, crawling, rendering
│   ├── extract/                 # HTML, schema, sitemap, and image extraction
│   ├── modules/                 # page, technical, content, geo, and other analysis modules
│   ├── audit/                   # Full-site audit orchestration and scoring
│   └── reports/                 # Markdown report rendering
├── docs/                        # Installation, commands, architecture, provider docs
├── schema/                      # Schema templates
├── scripts/                     # install, fetch, parse, render, portability check
├── tests/                       # pytest tests
└── pyproject.toml               # Python package and CLI entry point
```

Two delivery layers:

| Layer | Purpose |
|---|---|
| Agent layer | `AGENTS.md`, `skills/`, and `agents/` describe routing, language preferences, safety boundaries, and specialist workflows for agents |
| Deterministic layer | `src/seo_agents/` and the `seo-agents` CLI perform real fetching, parsing, analysis, scoring, artifact writing, and testing |

---

## Data Storage

`audit` writes report artifacts into a directory derived from the target host:

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

`drift` writes baselines to the local cache directory by default:

```text
~/.cache/seo-agents/drift/baselines.db
```

Use `--output-dir` to override the audit output directory, and `--db` to override the drift database path.

---

## How It Works

### Full Audit Flow

Run:

```bash
seo-agents audit https://example.com --max-pages 20
```

Flow:

1. Discovery: discover pages from the target URL, up to `--max-pages`.
2. Safe fetch/render: every URL goes through `validate_url_strict`; internal, private, loopback, link-local, and metadata endpoints are rejected.
3. Parse: extract metadata, headings, links, images, schema, hreflang, social tags, and visible text.
4. Module analysis: run page, technical, content, schema, images, geo, hreflang, local, ecommerce, and related modules.
5. External status: Google, Backlinks, and Firecrawl return offline placeholder status; DataForSEO is also represented as offline config status inside audit.
6. Synthesis: aggregate findings and calculate category scores plus the overall health score.
7. Report: write `audit-data.json`, `FULL-AUDIT-REPORT.md`, `ACTION-PLAN.md`, and category findings.

### Scoring Methodology

The health score is a weighted aggregation of category scores:

| Category | Weight |
|---|---:|
| Technical SEO | 22% |
| Content Quality | 23% |
| On-Page SEO | 20% |
| Schema / Structured Data | 10% |
| Performance / CWV | 10% |
| AI Search Readiness | 10% |
| Images | 5% |

Each category score subtracts penalties based on finding severity: `Critical`, `High`, `Medium`, `Low`, and `Info`. JSON audit data is the engineering contract; the current Markdown report is the rendering layer.

---

## Key Features

### SSRF-aware Fetching

Every user-provided URL is strictly validated before fetching, blocking private, loopback, link-local, metadata endpoint, and obfuscated IP targets.

### SPA-aware Rendering

`render` and most analysis commands support `--render-mode never|auto|always`. Missing browser dependencies do not break the program at import time.

### Evidence-based Findings

Every finding includes `evidence`, making it easier for agents, humans, and CI to understand the source of an issue. `--json` output can flow directly into later automation.

### GEO Readiness Checks

`geo` checks entity schema, citation-ready paragraphs, `llms.txt` / `llms-full.txt`, and common AI crawler rules in `robots.txt`. It only evaluates locally observable signals and does not claim to replace real AI platform citation data.

### Drift Monitoring

`drift baseline`, `drift compare`, and `drift history` track title, meta description, canonical, robots, headings, schema hash, HTML hash, and status code changes.

### DataForSEO Integration

`dataforseo` calls the real API by default. `user-data` validates credentials and balance through a free endpoint; `serp`, `related-keywords`, and `domain-rank` may cost credits. Use `--offline` when you only want configuration detection.

---

## Use Cases

- **SEO consultants**: quickly generate evidence-backed initial audits and action plans.
- **Marketing teams**: monitor SEO drift after page changes.
- **Content teams**: find gaps in titles, structure, citation-ready paragraphs, and E-E-A-T page signals.
- **Developers**: read JSON artifacts from CI or local scripts instead of relying only on manual SEO checklists.
- **Agent builders**: treat `skills/` and `agents/` as playbooks, and `seo-agents` CLI as the source of execution truth.
- **Local and ecommerce sites**: cover local, ecommerce, schema, images, hreflang, and other vertical basics.

---

## External Data Sources

Configuration is read from `~/.config/seo-agents/` by default. Use `SEO_AGENTS_CONFIG_DIR` to override the config directory in tests or isolated environments.

| Provider | Config | Current Behavior |
|---|---|---|
| Google | `google-api.json` or env vars such as `GOOGLE_API_KEY`, `GOOGLE_APPLICATION_CREDENTIALS` | Offline placeholder, only checks config field sources |
| Backlinks | `backlinks-api.json` or `MOZ_API_KEY`, `BING_WEBMASTER_API_KEY` | Offline placeholder, only checks config field sources |
| Firecrawl | `firecrawl-api.json` or `FIRECRAWL_API_KEY` | Offline placeholder, only checks config field sources |
| DataForSEO | `dataforseo-api.json` or `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD` | Live integration by default; `--offline` only checks configuration |

Provider commands never print secret values. See [`docs/DATAFORSEO-INTEGRATION.md`](docs/DATAFORSEO-INTEGRATION.md) for DataForSEO details.

---

## Roadmap Notes

The following capabilities have skill/agent instructions, but no CLI entry point yet: `plan`, `cluster`, `sxo`, `programmatic`, `competitor-pages`, `content-brief`, `maps`, `flow`, `image-gen`.

Before claiming that a capability is implemented, first verify that it exists in `src/seo_agents/cli.py` and has corresponding test coverage.

---

## Validation

```bash
python scripts/portability_check.py --json
pytest -q
```

The default test suite does not require real network access or paid API credentials.

---

## Uninstall

There is no automatic uninstaller yet. Remove the installed assets based on the target:

- CLI: `python -m pip uninstall seo-agents`
- Codex: delete `$CODEX_HOME/skills/seo*`
- Claude Code: delete `~/.claude/skills/seo*` and `~/.claude/agents/seo-*.md`
- Open Agent Skills: delete `$AGENTS_HOME/skills/seo*`

---

## Contributing

Contributions are welcome. Please follow Conventional Commits and keep each commit focused on a single functional area.

After changing commands, skills, or agent instructions, run at least:

```bash
python scripts/portability_check.py --json
```

---

## License

MIT License

Built for agent-first SEO workflows.
