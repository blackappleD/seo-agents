# 自建开源 SEO Agent 项目实现报告

生成日期：2026-06-24
参考项目：`D:\workspace\claude-seo`
目标：基于本项目的真实架构与功能面，设计一套可以从零搭建、逐步开源、最终达到同等能力的 SEO Agent / CLI 工具项目。

> 说明：你提到的“股价搭建”这里按上下文理解为“骨架搭建”。本报告不是教你简单 fork 原项目，而是把它拆解成可自主实现的工程路线，尽量避免只复制文档或提示词。

## 1. 总体判断

当前 `claude-seo` 不是一个传统 Web SEO 后台，而是一套面向 Agent Harness 的 SEO 工具包。它的核心价值来自四层结构：

1. `skills/`：自然语言技能层，定义命令、触发条件、分析流程、输出格式。
2. `agents/`：专项专家层，在全站审计时并行承担 technical、content、schema、visual、geo 等子任务。
3. `scripts/`：确定性执行层，负责 URL 安全、网页抓取、JS 渲染、HTML 解析、Google API、Backlink、漂移监控、报告生成等。
4. `extensions/`：外部数据源与能力扩展层，例如 DataForSEO、Firecrawl、Bing Webmaster、Banana image-gen、Ahrefs、SE Ranking 等。

当前仓库的可复刻事实如下：

| 模块 | 当前数量 | 你的项目应如何复刻 |
|---|---:|---|
| 核心 skill | 25 个 | 保留 `/seo` 总入口 + `seo-*` 专项能力拆分 |
| 扩展 skill | 8 个 | 做成插件式扩展，不要塞进核心包 |
| agent | 18 个 | 全站审计时使用，可先做 inline fallback |
| 根目录 Python 脚本 | 50 个 | 先抽成 Python package，再暴露 CLI |
| 测试文件 | 26 个 | 先覆盖安全、解析、报告契约、portability |
| 多平台兼容 | 已有 `portability_check.py` | 你的项目也应从第一天加入 skill frontmatter lint |

你如果要做一个自己的开源 SEO 项目，建议定位为：

> 一个“Agent-first SEO Toolkit”：既能被 Codex / Claude Code / Cursor / Cline 等 agent 读取，也能通过普通 CLI 独立运行。

这样比单纯做一个 Web 后台更适合复刻本项目的价值。后续如果需要 Web UI，可以在 CLI 和核心库稳定后再加。

## 2. 推荐技术架构

### 2.1 两层交付形态

建议你的项目同时提供两种入口：

1. Agent 入口：`skills/`、`agents/`、`AGENTS.md`，用于 AI 编程工具自动读取。
2. CLI / Library 入口：`src/seo_agents/` + `seo-agents` 命令，用于确定性执行、测试、CI 和普通用户使用。

当前项目大量逻辑直接散在 `scripts/*.py` 中。你自己重做时，建议把脚本改成薄包装，真实逻辑放进包里：

```text
seo-agents/
  AGENTS.md
  README.md
  LICENSE
  pyproject.toml
  requirements.txt
  skills/
    seo/SKILL.md
    seo-audit/SKILL.md
    seo-page/SKILL.md
    seo-technical/SKILL.md
    ...
  agents/
    seo-technical.md
    seo-content.md
    seo-schema.md
    ...
  src/seo_agents/
    __init__.py
    cli.py
    config.py
    models.py
    security/
      url_safety.py
    fetch/
      http.py
      render.py
      crawler.py
    extract/
      html.py
      schema.py
      sitemap.py
      images.py
    audit/
      orchestrator.py
      scoring.py
      report_contract.py
    modules/
      page.py
      technical.py
      content.py
      schema.py
      sitemap.py
      images.py
      geo.py
      local.py
      maps.py
      hreflang.py
      backlinks.py
      ecommerce.py
      drift.py
      cluster.py
      sxo.py
      programmatic.py
      competitor_pages.py
    providers/
      google/
        auth.py
        pagespeed.py
        crux.py
        gsc.py
        ga4.py
        indexing.py
        keyword_planner.py
      backlinks/
        moz.py
        bing.py
        commoncrawl.py
      dataforseo/
        client.py
      firecrawl/
        client.py
    reports/
      markdown.py
      html.py
      pdf.py
      excel.py
    storage/
      drift_store.py
      artifact_store.py
  scripts/
    fetch_page.py
    render_page.py
    parse_html.py
    pagespeed_check.py
    portability_check.py
  extensions/
    dataforseo/
    firecrawl/
    banana/
    bing-webmaster/
    ahrefs/
    seranking/
    profound/
    unlighthouse/
  schema/
    templates.json
  tests/
    test_url_safety.py
    test_render_page.py
    test_parse_html.py
    test_audit_contract.py
    test_portability.py
```

### 2.2 为什么要这样拆

本项目的强项是功能广，但它的脚本多以单文件 CLI 存在。你自己实现时，应该把“可测试、可复用、可发布”的核心逻辑放到 `src/seo_agents`。

这样可以得到三点好处：

1. CLI、skill、agent、Web API 后续都能复用同一套核心模块。
2. 测试不用通过 subprocess 调脚本，速度更快、失败更清楚。
3. 可选依赖不会在 import 阶段把测试进程退出，本项目 `google_report.py` 曾暴露过类似风险。

## 3. 第一阶段：项目骨架搭建

### 3.1 初始化仓库

建议命令：

```bash
mkdir seo-agents
cd seo-agents
git init
python -m venv .venv
.venv/Scripts/activate  # Windows
pip install -U pip
```

最低文件：

```text
README.md
AGENTS.md
LICENSE
pyproject.toml
requirements.txt
src/seo_agents/
skills/seo/SKILL.md
scripts/portability_check.py
tests/
```

### 3.2 `pyproject.toml` 推荐

本项目使用 Python 3.10+。你可以继续保持 Python 3.10+，但建议用更规范的包结构：

```toml
[project]
name = "seo-agents"
version = "0.1.0"
description = "Agent-first SEO audit toolkit"
requires-python = ">=3.10"
license = "MIT"
readme = "README.md"
keywords = ["seo", "technical-seo", "schema", "core-web-vitals", "geo", "agent"]

[project.scripts]
seo-agents = "seo_agents.cli:main"

[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "W", "I"]
ignore = ["E501"]
```

### 3.3 依赖选择

可参考当前项目依赖：

| 用途 | 建议依赖 |
|---|---|
| HTTP | `requests`, `urllib3` |
| HTML 解析 | `beautifulsoup4`, `lxml` |
| JS 渲染 | `playwright` |
| 正文抽取 | `trafilatura` |
| 日期抽取 | `htmldate` |
| 图片处理 | `Pillow` |
| Google API | `google-api-python-client`, `google-auth`, `google-analytics-data` |
| Excel 报告 | `openpyxl` |
| 图表/PDF | `matplotlib`, `weasyprint` |
| 测试 | `pytest`, `responses` 或 `requests-mock` |

建议把依赖分为：

```text
core: requests, beautifulsoup4, lxml, validators
render: playwright, trafilatura, htmldate
google: google-* packages
report: matplotlib, weasyprint, openpyxl
dev: pytest, ruff
```

不要让 report/google/render 这些可选依赖在 import 阶段中断整个项目。

## 4. 第二阶段：Agent 指令层设计

### 4.1 `AGENTS.md`

你的 `AGENTS.md` 应该说明：

1. 项目是什么。
2. 有哪些 `/seo` 命令。
3. 哪些 harness 支持读取。
4. Claude Code 工具名如何映射到 Codex / Cursor / Cline / Aider。
5. 如何运行 portability 检查。

参考当前项目做法，核心命令表至少包含：

| 命令 | 功能 |
|---|---|
| `/seo audit <url>` | 全站审计 |
| `/seo page <url>` | 单页分析 |
| `/seo technical <url>` | 技术 SEO |
| `/seo content <url>` | E-E-A-T / 内容质量 |
| `/seo schema <url>` | Schema 检测、验证、生成 |
| `/seo sitemap <url>` | Sitemap 分析 |
| `/seo images <url>` | 图片 SEO |
| `/seo geo <url>` | AI Search / GEO |
| `/seo plan <type>` | SEO 策略规划 |
| `/seo cluster <keyword>` | SERP 语义聚类 |
| `/seo sxo <url>` | Search Experience Optimization |
| `/seo drift baseline <url>` | 建立 SEO 漂移基线 |
| `/seo drift compare <url>` | 与基线比较 |
| `/seo ecommerce <url>` | 电商 SEO |
| `/seo local <url>` | 本地 SEO |
| `/seo maps ...` | 地图排名/GBP/本地竞争 |
| `/seo hreflang <url>` | 国际化 SEO |
| `/seo google ...` | Google API 数据 |
| `/seo backlinks <url>` | 外链分析 |
| `/seo programmatic ...` | 程序化 SEO |
| `/seo competitor-pages ...` | 竞品对比页 |

### 4.2 Skill frontmatter 规范

每个 `SKILL.md` 都使用可跨平台识别的最小 frontmatter：

```yaml
---
name: seo-technical
description: >
  Technical SEO audit across crawlability, indexability, security, URL
  structure, mobile, Core Web Vitals, structured data, JavaScript rendering,
  and IndexNow.
user-invocable: true
argument-hint: "[url]"
license: MIT
metadata:
  version: "0.1.0"
  category: seo
---
```

第一版就实现 `scripts/portability_check.py`，验收标准：

```bash
python scripts/portability_check.py --json
```

必须输出：

```json
{
  "errors": 0
}
```

### 4.3 Skill 目录的最小集合

MVP 不要一开始写满 25 个 skill。建议分三批。

第一批：能完成真实单页和基础全站审计。

```text
skills/seo/
skills/seo-audit/
skills/seo-page/
skills/seo-technical/
skills/seo-content/
skills/seo-schema/
skills/seo-sitemap/
skills/seo-images/
```

第二批：增强数据和监控。

```text
skills/seo-google/
skills/seo-backlinks/
skills/seo-drift/
skills/seo-geo/
skills/seo-hreflang/
```

第三批：策略和垂直行业。

```text
skills/seo-local/
skills/seo-maps/
skills/seo-ecommerce/
skills/seo-cluster/
skills/seo-sxo/
skills/seo-plan/
skills/seo-programmatic/
skills/seo-competitor-pages/
skills/seo-content-brief/
```

扩展镜像最后做：

```text
skills/seo-dataforseo/
skills/seo-image-gen/
skills/seo-flow/
extensions/firecrawl/
extensions/bing-webmaster/
extensions/ahrefs/
extensions/seranking/
extensions/profound/
extensions/unlighthouse/
```

## 5. 第三阶段：确定性执行底座

这是整个项目最重要的基础。不要先写 25 个 skill，再补抓取和解析。顺序应反过来。

### 5.1 URL 安全模块

当前项目最值得复用思想的是 `scripts/url_safety.py`。你的项目必须先实现：

| 能力 | 说明 |
|---|---|
| scheme 限制 | 只允许 `http` / `https` |
| hostname 标准化 | 小写、去 trailing dot、拒绝空 host |
| 混淆 IP 处理 | 拦截 `2130706433`、`0x7f000001`、八进制、短 IPv4 |
| 私网地址拦截 | 拒绝 loopback、private、link-local、metadata endpoint |
| authority confusion 拦截 | 拒绝 userinfo、反斜杠、percent-encoding 混淆 |
| DNS 严格校验 | 解析后所有 A/AAAA 必须是公网地址 |
| DNS pinning | HTTP 请求期间固定已验证 IP，降低 rebinding 风险 |
| Playwright route 防护 | 浏览器子资源请求也要重新校验 |

推荐 API：

```python
validate_url(url: str) -> bool
validate_url_strict(url: str) -> tuple[str, str]
safe_requests_get(url: str, **kwargs) -> requests.Response
safe_requests_head(url: str, **kwargs) -> requests.Response
safe_requests_session(url: str) -> ContextManager[requests.Session]
make_safe_playwright_route_handler(blocked_resource_types: set[str])
```

验收测试：

1. `http://127.0.0.1` 必须拒绝。
2. `http://2130706433` 必须拒绝。
3. `https://metadata.google.internal.` 必须拒绝。
4. `https://user:pass@example.com` 必须拒绝。
5. DNS 解析到私网 IP 的域名必须拒绝。
6. redirect 到私网 IP 必须拒绝。

### 5.2 HTTP 抓取模块

实现 `fetch/http.py`：

```python
class FetchResult:
    url: str
    final_url: str
    status_code: int | None
    headers: dict[str, str]
    content: str | None
    redirect_chain: list[dict]
    error: str | None
```

关键点：

1. 所有 URL 先走 `validate_url_strict`。
2. 用 `safe_requests_session` 处理 DNS pinning。
3. 设置 SEO crawler UA。
4. 限制 redirect 次数，建议最多 3 次。
5. 正确处理 charset：HTTP header、HTML meta charset、fallback UTF-8。
6. 错误返回结构化 JSON，不要只 print。

### 5.3 JS 渲染模块

当前项目 `render_page.py` 是第二个核心底座。你的实现应支持：

| 模式 | 行为 |
|---|---|
| `never` | 只抓 raw HTML |
| `auto` | 先抓 raw HTML，检测 SPA shell 后再 Playwright 渲染 |
| `always` | 永远 Playwright 渲染 |

输出字段：

```json
{
  "url": "final url",
  "status_code": 200,
  "content": "rendered html",
  "raw_content": "server html",
  "is_spa": false,
  "extracted_text": "main text",
  "publication_date": "2026-06-24",
  "headers": {},
  "redirect_chain": [],
  "console_errors": [],
  "render_engine": "playwright-chromium",
  "render_ms": 1234,
  "mode_used": "raw|rendered",
  "error": null
}
```

SPA 检测可以从这些信号开始：

1. `<div id="root"></div>`
2. `<div id="__next">`
3. `<div id="app"></div>`
4. `<div id="__nuxt">`
5. `data-svelte-h=`
6. `<astro-island`
7. body 可见文本过短。

### 5.4 HTML 解析模块

实现 `extract/html.py`，解析字段至少包括：

```json
{
  "title": null,
  "meta_description": null,
  "meta_robots": null,
  "canonical": null,
  "h1": [],
  "h2": [],
  "h3": [],
  "images": [],
  "links": {
    "internal": [],
    "external": []
  },
  "schema": [],
  "open_graph": {},
  "twitter_card": {},
  "word_count": 0,
  "hreflang": []
}
```

图片解析应识别：

1. `loading="lazy"` 原生懒加载。
2. `data-src` / `data-srcset` 通用懒加载。
3. WordPress 常见插件 lazy loader，例如 Perfmatters、EWWW。
4. width / height 缺失导致的 CLS 风险。

Schema 解析：

1. JSON-LD。
2. `@graph` 自动展开。
3. Microdata / RDFa 可放到第二阶段。

### 5.5 Artifact 存储契约

全站审计不要只输出 Markdown。应同时输出机器可读 JSON：

```text
example.com-audit/
  FULL-AUDIT-REPORT.md
  ACTION-PLAN.md
  audit-data.json
  findings/
    technical.md
    content.md
    schema.md
    performance.md
    visual.md
  screenshots/
    desktop.png
    mobile.png
```

`audit-data.json` 最小结构：

```json
{
  "summary": {
    "health_score": 0,
    "business_type": "saas|local|ecommerce|publisher|agency|other",
    "top_findings": [],
    "quick_wins": []
  },
  "categories": [
    {
      "name": "Technical SEO",
      "score": 0,
      "what_works": [],
      "findings": [
        {
          "title": "Finding title",
          "severity": "Critical|High|Medium|Low|Info",
          "description": "Evidence-backed detail",
          "recommendation": "Specific fix"
        }
      ]
    }
  ],
  "action_plan": {
    "phases": [
      {"name": "Phase 1: Critical Fixes", "timeframe": "Week 1", "items": []},
      {"name": "Phase 2: High-Impact Improvements", "timeframe": "Weeks 2-3", "items": []},
      {"name": "Phase 3: Content & Authority", "timeframe": "Month 2", "items": []},
      {"name": "Phase 4: Monitoring & Iteration", "timeframe": "Ongoing", "items": []}
    ]
  },
  "artifacts": {
    "findings_dir": "findings/",
    "screenshots_dir": "screenshots/"
  }
}
```

## 6. 第四阶段：核心 SEO 功能实现

### 6.1 `/seo page <url>` 单页分析

这是最适合作为第一个业务功能的模块。

输入：

```bash
seo-agents page https://example.com --json
```

执行流程：

1. `render_page(url, mode="auto")`
2. `parse_html(rendered.content)`
3. 生成单页 findings。
4. 输出 Markdown + JSON。

检查项：

| 类别 | 规则 |
|---|---|
| Title | 是否存在，长度是否合理，是否重复/过长 |
| Meta Description | 是否存在，长度和可点击性 |
| H1 | 是否唯一，是否为空或纯数字 |
| Headings | H2/H3 层级是否清晰 |
| Canonical | 是否存在，是否自引用，是否和当前 URL 冲突 |
| Robots | noindex/nofollow 是否意外出现 |
| Links | 内链/外链数量、空锚文本、nofollow |
| Images | alt、lazy、尺寸、CLS 风险 |
| Schema | 类型、合法性、机会点 |
| OG/Twitter | 社交分享元数据 |
| Word Count | thin content 风险 |
| SPA | raw HTML 与 rendered HTML 差异 |

验收标准：

1. 静态页面和 SPA 页面都能输出有效结果。
2. JSON 字段稳定，方便后续报告生成。
3. 对无法访问 URL 明确返回错误，不猜内容。

### 6.2 `/seo technical <url>` 技术 SEO

参考当前项目，技术 SEO 分 9 类：

1. Crawlability：robots.txt、sitemap、重要页面是否可抓。
2. Indexability：canonical、noindex、重复内容、参数 URL。
3. Security：HTTPS、HSTS、CSP、X-Frame-Options、mixed content。
4. URL Structure：路径层级、长度、query、redirect chain。
5. Mobile：viewport、字体、触控目标、横向滚动。
6. Core Web Vitals：LCP、INP、CLS，优先真实 CrUX，缺失时用 PSI/Lighthouse。
7. Structured Data：JSON-LD、Google 支持类型、错误。
8. JavaScript Rendering：raw vs rendered 差异、meta 是否靠 JS 注入。
9. IndexNow：是否支持 Bing/Yandex/Naver 的 IndexNow。

实现顺序：

1. 本地 HTML 可判断项：title、canonical、robots、schema、JS 渲染差异。
2. HTTP header 可判断项：HTTPS、安全头、redirect chain。
3. 外部 API：PageSpeed Insights、CrUX、GSC Inspection。
4. 浏览器可判断项：mobile viewport、可访问性树、截图。

验收标准：

1. 输出 `technical_score`。
2. 每个类别有 `pass/warn/fail` 和分数。
3. Critical / High / Medium / Low 分级清晰。
4. 不再提 FID，只使用 INP。

### 6.3 `/seo content <url>` 内容质量与 E-E-A-T

实现模块：

```text
modules/content.py
extract/main_text.py
modules/content_quality.py
modules/content_verify.py
```

检查项：

| 类别 | 实现方式 |
|---|---|
| Thin Content | word count + 页面类型阈值 |
| Filler Content | 固定短语/低信息密度/重复度 |
| AI Pattern | 保守短语命中，不做“AI 生成”最终判断 |
| Experience | 是否有第一手经验、案例、照片、过程细节 |
| Expertise | 作者、资质、引用来源 |
| Authoritativeness | 外部背书、品牌实体、sameAs |
| Trustworthiness | 联系方式、隐私、退款、HTTPS、作者透明度 |
| Freshness | 发布/更新日期、过期声明 |
| AI Citation Readiness | 可引用段落、定义、数字、表格、FAQ 结构 |

注意：不要做“AI 检测器”式绝对判断。应输出“质量风险信号”。

### 6.4 `/seo schema <url>`

实现三部分：

1. 检测：解析 JSON-LD、Microdata、RDFa。
2. 验证：类型、必填字段、Google rich result 支持情况。
3. 生成：输出可直接复制的 JSON-LD。

第一版支持类型：

| 类型 | 用途 |
|---|---|
| Organization | 公司实体 |
| WebSite | 站点级别 |
| WebPage | 页面级别 |
| Article / BlogPosting | 内容页 |
| BreadcrumbList | 面包屑 |
| Product | 电商 |
| LocalBusiness | 本地商家 |
| FAQPage | 仅说明 AI/LLM 价值，不再承诺 Google FAQ rich result |
| QAPage | 真正用户问答页 |
| ProfilePage | 作者/专家实体 |
| DiscussionForumPosting | 社区/论坛内容 |
| Reservation / OrderAction | 本地服务、餐饮、电商动作 |

生成器 API：

```python
generate_schema(kind: str, data: dict) -> dict
validate_schema(schema: dict, page_context: dict) -> list[Finding]
```

验收标准：

1. 能发现 invalid JSON-LD。
2. 能展开 `@graph`。
3. 能标记 deprecated rich result。
4. 能生成带 `@context: https://schema.org` 的 JSON-LD。

### 6.5 `/seo sitemap <url>` Sitemap

当前项目 sitemap skill 更偏规则说明，你自己实现时应补真正 parser/generator。

实现能力：

1. 发现 sitemap：`/robots.txt` 中的 `Sitemap:`，以及常见路径 `/sitemap.xml`。
2. 解析 sitemap index 和 URL set。
3. 校验每个 sitemap 不超过 50,000 URL。
4. 校验 URL 状态码。
5. 检查 `lastmod` 是否存在、是否未来日期。
6. 标记 deprecated 的 `priority` / `changefreq` 不再作为重要信号。
7. 生成 sitemap XML。

验收标准：

1. 支持 sitemap index 嵌套。
2. 支持 gzip sitemap。
3. 大站可设置抽样或并发限制。
4. 输出 coverage gap：站内发现 URL 与 sitemap URL 差异。

### 6.6 `/seo images <url>` 图片 SEO

实现能力：

1. HTML 图片审计：alt、width/height、lazy、srcset/sizes。
2. 文件审计：大小、格式、尺寸。
3. 性能建议：WebP/AVIF、压缩、预加载 LCP 图片。
4. CLS 防护：缺尺寸或 CSS aspect-ratio 风险。
5. 图片元数据：IPTC/XMP，AI 图片标注。
6. 可选优化：Pillow 转换、压缩、批量输出。

第一版不要承诺完整视觉理解。先做到确定性字段检查。

### 6.7 `/seo audit <url>` 全站审计

全站审计是前面模块的聚合，不应从零写一套新逻辑。

流程：

1. 渲染首页。
2. 检测行业：SaaS / Local / Ecommerce / Publisher / Agency / Other。
3. URL 发现：sitemap、内链爬取、可选 Firecrawl。
4. 限制：默认最多 500 页，尊重 robots.txt。
5. 并发：默认 5 个请求，站点级 delay 1 秒。
6. 对代表性 URL 跑 page/technical/content/schema/images。
7. 条件性增加 google/backlinks/local/maps/ecommerce/drift/cluster/sxo。
8. 汇总分数和 action plan。
9. 写入 artifacts。

评分权重可参考当前项目：

| 类别 | 权重 |
|---|---:|
| Technical SEO | 22% |
| Content Quality | 23% |
| On-Page SEO | 20% |
| Schema / Structured Data | 10% |
| Performance / CWV | 10% |
| AI Search Readiness | 10% |
| Images | 5% |

注意：分数要可解释。每个扣分都应能追溯到 finding。

## 7. 第五阶段：外部数据源功能

### 7.1 `/seo google ...`

当前项目的 Google 集成是最落地的模块之一。你应按凭据能力分层：

| Tier | 凭据 | 可用功能 |
|---|---|---|
| 0 | API Key | PageSpeed, CrUX, YouTube, NLP, Knowledge Graph, Web Risk |
| 1 | OAuth / Service Account | Tier 0 + GSC Search Analytics, URL Inspection, Sitemap, Indexing |
| 2 | GA4 Property | Tier 1 + GA4 Organic Traffic |
| 3 | Google Ads | Tier 2 + Keyword Planner |

配置路径：

```text
~/.config/seo-agents/google-api.json
```

配置结构：

```json
{
  "service_account_path": "/path/to/service-account.json",
  "api_key": "<GOOGLE_API_KEY>",
  "default_property": "sc-domain:example.com",
  "ga4_property_id": "properties/123456789",
  "ads_developer_token": "",
  "ads_customer_id": ""
}
```

命令：

```text
seo-agents google setup
seo-agents google pagespeed <url>
seo-agents google crux <url>
seo-agents google crux-history <url>
seo-agents google gsc <property>
seo-agents google inspect <url>
seo-agents google sitemaps <property>
seo-agents google ga4 [property-id]
seo-agents google keywords <seed>
```

注意：Google Ads 在当前项目里主要是 Keyword Planner，不是完整 Ads Manager。你自己的项目也要明确边界。

### 7.2 `/seo backlinks <url>`

实现数据源：

| 数据源 | 免费/付费 | 用途 |
|---|---|---|
| Moz API | 部分免费/需账号 | DA/PA、链接指标 |
| Bing Webmaster | 免费/需验证 | 已知外链 |
| Common Crawl | 免费 | 域名级提及和链接图 |
| DataForSEO | 付费 | 更完整 backlink profile |
| Ahrefs / SE Ranking | 付费扩展 | 可做插件，不放核心 |

输出：

1. referring domains。
2. anchor text distribution。
3. toxic / suspicious links。
4. competitor gap。
5. disavow 建议，但默认不要自动生成提交文件。

### 7.3 `/seo drift ...`

漂移监控是非常适合开源项目差异化的功能。

存储：

```text
~/.cache/seo-agents/drift/baselines.db
```

SQLite 表：

```sql
CREATE TABLE baselines (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  url TEXT NOT NULL,
  url_hash TEXT NOT NULL,
  timestamp TEXT NOT NULL,
  title TEXT,
  meta_description TEXT,
  canonical TEXT,
  robots TEXT,
  h1 TEXT,
  h2_json TEXT,
  h3_json TEXT,
  schema_json TEXT,
  og_json TEXT,
  cwv_json TEXT,
  html_hash TEXT,
  schema_hash TEXT,
  status_code INTEGER
);
```

命令：

```text
seo-agents drift baseline <url>
seo-agents drift compare <url>
seo-agents drift history <url>
```

比较规则：

| 变化 | 严重度 |
|---|---|
| status 从 200 变 4xx/5xx | Critical |
| 新增 noindex | Critical |
| canonical 指向其他域 | Critical/High |
| title 大幅变化 | Medium/High |
| H1 消失 | High |
| schema 移除 | Medium/High |
| CWV 明显变差 | High |

### 7.4 `/seo geo <url>`

GEO / AI Search Readiness 实现重点：

1. robots.txt 是否允许 AI crawler。
2. `llms.txt` / `llms-full.txt` 是否存在。
3. 页面是否有可引用的事实、定义、数字、表格。
4. 作者/组织实体是否清晰。
5. Schema 是否支撑实体图。
6. 内容是否有 passage-level citability。
7. 品牌在外部来源中的 mention 信号，可选 YouTube、Common Crawl、Search APIs。

不要把 GEO 写成玄学。要把它拆成可检查信号。

## 8. 第六阶段：垂直 SEO 能力

### 8.1 Local SEO

`seo-local` 第一版实现：

1. NAP：Name / Address / Phone 一致性。
2. LocalBusiness schema。
3. 页面是否包含城市、服务区域、营业时间。
4. GBP 链接和地图嵌入。
5. Reviews：数量、评分、近期性、回复情况。
6. 多门店页面质量：30+ location pages 警告，50+ hard stop，需要唯一内容。

### 8.2 Maps Intelligence

`seo-maps` 建议做成扩展能力：

1. 免费层：Overpass / OpenStreetMap、Geoapify。
2. 付费层：DataForSEO Maps / Business Listings。
3. Google 层：GBP API，需更复杂授权。

输出：

1. geo-grid rank tracking。
2. Share of Local Voice。
3. competitor radius。
4. review velocity。
5. NAP cross-platform consistency。

### 8.3 Ecommerce SEO

实现：

1. Product schema 验证。
2. Offer / AggregateRating / Review。
3. 库存、价格、货币、shipping/return policy。
4. Google Shopping feed 检查。
5. 商品页标题、描述、图片、变体 URL canonical。
6. DataForSEO Merchant API 可做扩展。

### 8.4 Hreflang / International SEO

实现：

1. `hreflang` 语言和地区码校验。
2. self-reference。
3. return tag。
4. x-default。
5. sitemap hreflang。
6. locale formatting。
7. content parity：不同语言页面是否明显缺失核心内容。

### 8.5 Programmatic SEO

实现：

1. URL pattern 评估。
2. 模板重复度。
3. thin content guard。
4. index bloat 风险。
5. 内链自动化。
6. pagination / faceted navigation。
7. noindex / canonical 策略。

### 8.6 Competitor Pages

实现：

1. `X vs Y` 页面结构。
2. Alternatives 页面结构。
3. feature matrix。
4. Review / Product / FAQ / Breadcrumb schema。
5. 合规提醒：不要虚构竞品数据。

### 8.7 Cluster / SXO / Content Brief

这三块可以共用 SERP 数据：

1. `seo-cluster`：SERP overlap 聚类，不要只做字符串相似度。
2. `seo-sxo`：根据 SERP 反推 Google 奖励的页面类型。
3. `seo-content-brief`：生成关键词、意图、heading outline、内部链接、竞争角度。

如果没有 DataForSEO 或搜索 API，第一版可以要求用户提供 SERP 截图/导出，或做手工辅助模式。

## 9. 第七阶段：报告系统

当前项目有 `google_report.py`，能把 audit data 变成 PDF/HTML/XLSX。你自己的报告系统建议独立成 `reports/` 包。

报告类型：

| 类型 | 输出 |
|---|---|
| Markdown | 默认，开源友好 |
| JSON | 机器可读，供 CI 和 Web UI 使用 |
| HTML | 本地可打开 |
| PDF | 客户交付 |
| XLSX | 数据表、URL 清单、finding 清单 |

报告结构：

1. Executive Summary。
2. SEO Health Score。
3. Business Type。
4. Top Critical Issues。
5. Quick Wins。
6. Category Findings。
7. Evidence。
8. Action Plan。
9. Implementation Roadmap。
10. Appendix：raw metrics、URL list、schema dump、screenshots。

重要原则：

1. 报告中的每个建议都要有证据字段。
2. PDF 只是渲染层，不能是唯一输出。
3. 缺少 Google API 数据时，报告要明确写“未配置”而不是空白。
4. 不要在 import 阶段强依赖 `matplotlib` / `weasyprint`。

## 10. 第八阶段：扩展系统

参考当前 `extensions/`，你的扩展系统应采用“核心稳定、外部能力可选安装”的原则。

### 10.1 扩展目录规范

```text
extensions/dataforseo/
  README.md
  install.sh
  install.ps1
  uninstall.sh
  uninstall.ps1
  skills/seo-dataforseo/SKILL.md
  docs/DATAFORSEO-SETUP.md

extensions/firecrawl/
  README.md
  install.sh
  install.ps1
  skills/seo-firecrawl/SKILL.md
  docs/FIRECRAWL-SETUP.md
```

### 10.2 第一批扩展

| 扩展 | 价值 |
|---|---|
| DataForSEO | SERP、关键词、外链、电商、AI visibility |
| Firecrawl | 大站 URL 发现和抓取 |
| Bing Webmaster | 免费外链和 IndexNow 生态 |
| Banana / Image Gen | SEO 图片资产生成 |
| Unlighthouse | Lighthouse 批量站点审计 |

### 10.3 设计规则

1. 核心项目不要求用户安装付费 API。
2. 扩展 skill 可以 mirror 到核心命令，但路径要清楚。
3. 扩展安装脚本不能修改用户文件前不备份。
4. 扩展缺失时，主命令应降级而不是失败。

## 11. 测试策略

### 11.1 必测模块

| 测试 | 原因 |
|---|---|
| URL safety | SEO 工具会访问用户输入 URL，SSRF 是最高风险 |
| HTML parser | 所有 SEO 判断都依赖解析稳定性 |
| render_page | SPA 是现代站点常态 |
| schema parser/generator | 输出要可复制，不能生成坏 JSON-LD |
| sitemap parser | XML 和 gzip sitemap 容易出边界问题 |
| audit-data contract | 报告系统依赖稳定 JSON |
| portability check | Agent harness 兼容性 |
| optional dependencies | 缺可选依赖时不能影响核心功能 |

### 11.2 测试原则

1. 默认测试不依赖真实网络。
2. live API 测试用环境变量显式开启，例如 `RUN_LIVE_GOOGLE_TESTS=1`。
3. DNS 测试用 mock，不依赖 `example.com` 本机解析。
4. Windows / Linux 权限语义分开处理。
5. import 阶段禁止 `sys.exit(1)`。
6. 脚本退出码测试与库函数测试分开。

### 11.3 推荐 CI

```yaml
name: test

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: python scripts/portability_check.py --json
      - run: ruff check .
      - run: pytest -q
```

后续再加 Windows matrix：

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
```

## 12. 开源发布与合规

### 12.1 License

当前项目是 MIT。你如果基于其思想重新实现，也建议 MIT；如果直接复制大量代码/文本，需要保留原 license 和 attribution。

如果你想做“自己的开源项目”，推荐：

1. 代码重新组织和实现。
2. 文档用自己的表述。
3. 保留参考项目 credit。
4. 不复制原项目社区 footer、品牌名、作者信息。
5. 引入第三方资料时记录许可证，例如 CC BY-SA、CC BY 4.0。

### 12.2 Privacy / Security 文档

至少提供：

```text
SECURITY.md
PRIVACY.md
CONTRIBUTING.md
CODE_OF_CONDUCT.md
```

`PRIVACY.md` 要说明：

1. URL 会被本地抓取。
2. 配置 Google/DataForSEO 等 API 时，凭据存在本机 config 路径。
3. 默认不上传用户数据。
4. 使用第三方 API 时会把 URL/查询发送给对应平台。

`SECURITY.md` 要说明：

1. SSRF 防护策略。
2. DNS rebinding 风险和防护。
3. Playwright 浏览器访问的边界。
4. 不支持内网 URL。
5. 如何报告漏洞。

## 13. 推荐开发路线图

### Phase 0：项目骨架，1-2 天

交付：

1. `pyproject.toml`
2. `README.md`
3. `AGENTS.md`
4. `skills/seo/SKILL.md`
5. `src/seo_agents/cli.py`
6. `scripts/portability_check.py`
7. 基础 CI

验收：

```bash
seo-agents --help
python scripts/portability_check.py --json
pytest -q
```

### Phase 1：安全抓取与解析，3-5 天

交付：

1. `security/url_safety.py`
2. `fetch/http.py`
3. `fetch/render.py`
4. `extract/html.py`
5. `scripts/fetch_page.py`
6. `scripts/render_page.py`
7. `scripts/parse_html.py`

验收：

```bash
seo-agents fetch https://example.com --json
seo-agents render https://example.com --json
seo-agents parse page.html --json
pytest tests/test_url_safety.py tests/test_parse_html.py
```

### Phase 2：单页 SEO 与技术 SEO，5-7 天

交付：

1. `modules/page.py`
2. `modules/technical.py`
3. `modules/images.py`
4. `modules/schema.py`
5. `skills/seo-page`
6. `skills/seo-technical`
7. `skills/seo-images`
8. `skills/seo-schema`

验收：

```bash
seo-agents page https://example.com --json
seo-agents technical https://example.com --json
seo-agents schema https://example.com --json
seo-agents images https://example.com --json
```

### Phase 3：全站审计，7-10 天

交付：

1. `fetch/crawler.py`
2. `extract/sitemap.py`
3. `audit/orchestrator.py`
4. `audit/scoring.py`
5. `reports/markdown.py`
6. `skills/seo-audit`
7. `agents/seo-technical.md`
8. `agents/seo-content.md`
9. `agents/seo-schema.md`

验收：

```bash
seo-agents audit https://example.com --max-pages 20
```

必须生成：

```text
example.com-audit/FULL-AUDIT-REPORT.md
example.com-audit/ACTION-PLAN.md
example.com-audit/audit-data.json
```

### Phase 4：Google API，5-8 天

交付：

1. `providers/google/auth.py`
2. `providers/google/pagespeed.py`
3. `providers/google/crux.py`
4. `providers/google/gsc.py`
5. `providers/google/ga4.py`
6. `providers/google/indexing.py`
7. `skills/seo-google`

验收：

```bash
seo-agents google setup
seo-agents google pagespeed https://example.com --json
seo-agents google crux https://example.com --json
```

GSC / GA4 测试需要凭据，默认不进 CI。

### Phase 5：漂移监控与报告，4-6 天

交付：

1. `storage/drift_store.py`
2. `modules/drift.py`
3. `reports/html.py`
4. `reports/pdf.py`
5. `reports/excel.py`
6. `skills/seo-drift`

验收：

```bash
seo-agents drift baseline https://example.com
seo-agents drift compare https://example.com
seo-agents report example.com-audit/audit-data.json --pdf
```

### Phase 6：GEO / Backlinks / Local / Ecommerce，2-4 周

按价值排序：

1. `seo-geo`
2. `seo-backlinks`
3. `seo-local`
4. `seo-ecommerce`
5. `seo-hreflang`

验收：

1. 每个模块至少有 JSON 输出。
2. 每个模块至少有 10 条单元测试。
3. 没有凭据时能降级。

### Phase 7：策略型能力，2-4 周

实现：

1. `seo-cluster`
2. `seo-sxo`
3. `seo-plan`
4. `seo-content-brief`
5. `seo-programmatic`
6. `seo-competitor-pages`

这些模块可以先是半自动：结合 SERP 数据、用户输入和模板生成。

### Phase 8：扩展生态，长期

实现：

1. `extensions/dataforseo`
2. `extensions/firecrawl`
3. `extensions/bing-webmaster`
4. `extensions/banana`
5. `extensions/unlighthouse`
6. `extensions/ahrefs`
7. `extensions/seranking`
8. `extensions/profound`

每个扩展都提供：

1. README。
2. install/uninstall。
3. setup doc。
4. skill。
5. tests 或 smoke check。

## 14. 你自己的项目可以差异化的地方

当前项目已经功能很全，但也有一些你可以做得更好的地方：

1. 把 `scripts/*.py` 升级成真正的 Python package，脚本只做入口。
2. 自动生成命令清单，避免 README / AGENTS / docs / skills 多处漂移。
3. 用 Pydantic 或 dataclass 固定 Finding / AuditReport / PageSnapshot 数据模型。
4. 做一个稳定的 JSON Schema，第三方可以消费审计结果。
5. 把 live API 测试全部隔离到显式环境变量。
6. 把 optional dependency 变成 extras，例如 `pip install seo-agents[google,report,render]`。
7. 给每个模块做 `--explain`，输出扣分原因。
8. 提供 Web UI，但只消费 CLI 生成的 `audit-data.json`，不要让 UI 成为核心逻辑。
9. 提供 GitHub Action：对网站部署前后做 drift compare。
10. 提供 Docker 镜像，方便在 CI 和服务器中运行。

## 15. 关键不要踩的坑

基于当前项目观察，建议你避开这些问题：

1. 不要在 import 阶段 `sys.exit(1)`，缺依赖应在命令执行时返回错误。
2. 不要让测试依赖真实 DNS 结果，尤其是 `example.com`。
3. 不要把 POSIX 文件权限测试原样搬到 Windows。
4. 不要让 skill 文档承诺脚本层不存在的能力。
5. 不要在核心包里强制 DataForSEO、Ahrefs、GA4 等付费凭据。
6. 不要把“Google Ads Keyword Planner”说成完整 Google Ads Manager 集成。
7. 不要只看 raw HTML，SPA 会造成大量 SEO 误判。
8. 不要让 PDF 报告成为唯一结果，JSON 才是工程契约。
9. 不要复制原项目品牌 footer 或作者信息到你的项目。
10. 不要一次性实现 25 个 skill，先跑通 page / technical / audit。

## 16. MVP 功能边界

如果你想最快做出可开源、可演示的第一版，建议 MVP 只包含：

```text
seo-agents page <url>
seo-agents technical <url>
seo-agents schema <url>
seo-agents sitemap <url>
seo-agents images <url>
seo-agents audit <url> --max-pages 20
```

MVP 必须具备：

1. SSRF-safe URL fetch。
2. SPA-aware render。
3. HTML SEO parser。
4. Markdown + JSON report。
5. 结构化 finding。
6. 至少 50 条测试。
7. Agent `skills/` 可被 Codex / Cursor / Claude Code 读取。

MVP 暂缓：

1. GA4/GSC/GAds。
2. Backlink paid providers。
3. PDF 报告。
4. GEO 外部 mention 数据。
5. Maps geo-grid。
6. AI image generation。

## 17. 建议的核心数据模型

```python
from dataclasses import dataclass, field
from typing import Any, Literal

Severity = Literal["Critical", "High", "Medium", "Low", "Info"]

@dataclass
class Finding:
    title: str
    severity: Severity
    category: str
    description: str
    recommendation: str
    evidence: dict[str, Any] = field(default_factory=dict)
    affected_urls: list[str] = field(default_factory=list)
    effort: str | None = None
    impact: str | None = None

@dataclass
class PageSnapshot:
    url: str
    final_url: str
    status_code: int | None
    raw_html: str | None
    rendered_html: str | None
    is_spa: bool
    extracted_text: str | None
    headers: dict[str, str]
    console_errors: list[str]

@dataclass
class AuditCategory:
    name: str
    score: int
    findings: list[Finding]
    what_works: list[str] = field(default_factory=list)

@dataclass
class AuditReport:
    target: str
    health_score: int
    business_type: str
    categories: list[AuditCategory]
    top_findings: list[Finding]
    quick_wins: list[Finding]
```

有了这些模型，所有模块都能统一输出，报告层也不会被每个脚本的自定义 JSON 拖散。

## 18. 最终落地顺序

最推荐你按这个顺序开工：

1. 建 repo、包结构、CLI、CI。
2. 实现 `url_safety`，先把安全边界写牢。
3. 实现 `fetch_page` 和 `render_page`。
4. 实现 `parse_html`。
5. 实现 `page`。
6. 实现 `technical`。
7. 实现 `schema/images/sitemap`。
8. 实现 `audit orchestrator` 和 `audit-data.json`。
9. 实现 Markdown 报告。
10. 再上 Google、drift、backlinks。
11. 最后做 local、ecommerce、maps、cluster、sxo、extensions。

如果只能先做一个月，做到第 8 步就已经是一个能开源、能演示、能继续扩展的项目。

## 19. 一句话总结

你要复刻的不是“25 个 Markdown skill”，而是一套三件事：

1. 安全可靠的网页获取和解析底座。
2. 模块化、可证据追溯的 SEO finding 系统。
3. Agent 可读、CLI 可跑、报告可交付的开放式工程架构。

先把这三件事做好，再逐步增加 Google、GEO、Backlink、本地 SEO、电商 SEO 和外部扩展，最终就能形成一个功能上接近当前项目、但工程结构更适合长期维护的开源 SEO 项目。
