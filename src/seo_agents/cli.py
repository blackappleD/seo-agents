from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from seo_agents import __version__
from seo_agents.audit.orchestrator import run_audit
from seo_agents.extract.html import parse_html
from seo_agents.fetch.http import fetch_url
from seo_agents.fetch.render import render_page
from seo_agents.models import to_plain
from seo_agents.modules.content import analyze_content
from seo_agents.modules.drift import compare_to_baseline, create_baseline, history
from seo_agents.modules.ecommerce import analyze_ecommerce
from seo_agents.modules.external import offline_placeholder
from seo_agents.modules.geo import analyze_geo
from seo_agents.modules.hreflang import analyze_hreflang
from seo_agents.modules.images import analyze_images
from seo_agents.modules.local import analyze_local
from seo_agents.modules.page import analyze_page
from seo_agents.modules.schema import analyze_schema
from seo_agents.modules.sitemap import analyze_sitemap
from seo_agents.modules.technical import analyze_technical


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "handler"):
        parser.print_help()
        return 0
    try:
        return args.handler(args)
    except KeyboardInterrupt:
        return 130


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="seo-agents", description="Agent-first SEO 本地分析 CLI")
    parser.add_argument("--version", action="version", version=f"seo-agents {__version__}")
    sub = parser.add_subparsers(dest="command")

    fetch = sub.add_parser("fetch", help="带安全校验抓取 URL")
    fetch.add_argument("url")
    fetch.add_argument("--json", action="store_true")
    fetch.set_defaults(handler=_handle_fetch)

    render = sub.add_parser("render", help="按 never/auto/always 模式渲染 URL")
    render.add_argument("url")
    render.add_argument("--mode", choices=["never", "auto", "always"], default="auto")
    render.add_argument("--json", action="store_true")
    render.set_defaults(handler=_handle_render)

    parse = sub.add_parser("parse", help="解析本地 HTML 文件")
    parse.add_argument("html_file")
    parse.add_argument("--base-url")
    parse.add_argument("--json", action="store_true")
    parse.set_defaults(handler=_handle_parse)

    page = sub.add_parser("page", help="运行单页 SEO 分析")
    page.add_argument("url")
    page.add_argument("--render-mode", choices=["never", "auto", "always"], default="auto")
    page.add_argument("--json", action="store_true")
    page.set_defaults(handler=_handle_page)

    technical = sub.add_parser("technical", help="运行技术 SEO 分析")
    technical.add_argument("url")
    technical.add_argument("--render-mode", choices=["never", "auto", "always"], default="auto")
    technical.add_argument("--json", action="store_true")
    technical.set_defaults(handler=_handle_technical)

    content = sub.add_parser("content", help="分析内容质量和 E-E-A-T 信号")
    content.add_argument("url")
    content.add_argument("--render-mode", choices=["never", "auto", "always"], default="auto")
    content.add_argument("--json", action="store_true")
    content.set_defaults(handler=_handle_content)

    schema = sub.add_parser("schema", help="分析结构化数据")
    schema.add_argument("url")
    schema.add_argument("--render-mode", choices=["never", "auto", "always"], default="auto")
    schema.add_argument("--json", action="store_true")
    schema.set_defaults(handler=_handle_schema)

    sitemap = sub.add_parser("sitemap", help="发现并分析 sitemap")
    sitemap.add_argument("url")
    sitemap.add_argument("--json", action="store_true")
    sitemap.set_defaults(handler=_handle_sitemap)

    images = sub.add_parser("images", help="分析图片 SEO")
    images.add_argument("url")
    images.add_argument("--render-mode", choices=["never", "auto", "always"], default="auto")
    images.add_argument("--json", action="store_true")
    images.set_defaults(handler=_handle_images)

    geo = sub.add_parser("geo", help="分析 AI Search / GEO 本地信号")
    geo.add_argument("url")
    geo.add_argument("--render-mode", choices=["never", "auto", "always"], default="auto")
    geo.add_argument("--json", action="store_true")
    geo.set_defaults(handler=_handle_geo)

    hreflang = sub.add_parser("hreflang", help="分析 hreflang / 国际化 SEO")
    hreflang.add_argument("url")
    hreflang.add_argument("--render-mode", choices=["never", "auto", "always"], default="auto")
    hreflang.add_argument("--json", action="store_true")
    hreflang.set_defaults(handler=_handle_hreflang)

    local = sub.add_parser("local", help="分析本地 SEO 信号")
    local.add_argument("url")
    local.add_argument("--render-mode", choices=["never", "auto", "always"], default="auto")
    local.add_argument("--json", action="store_true")
    local.set_defaults(handler=_handle_local)

    ecommerce = sub.add_parser("ecommerce", help="分析 Ecommerce SEO 信号")
    ecommerce.add_argument("url")
    ecommerce.add_argument("--render-mode", choices=["never", "auto", "always"], default="auto")
    ecommerce.add_argument("--json", action="store_true")
    ecommerce.set_defaults(handler=_handle_ecommerce)

    drift = sub.add_parser("drift", help="SEO 漂移监控")
    drift_sub = drift.add_subparsers(dest="drift_command", required=True)
    drift_baseline = drift_sub.add_parser("baseline", help="建立 SEO 漂移基线")
    drift_baseline.add_argument("url")
    drift_baseline.add_argument("--db")
    drift_baseline.add_argument("--render-mode", choices=["never", "auto", "always"], default="auto")
    drift_baseline.add_argument("--json", action="store_true")
    drift_baseline.set_defaults(handler=_handle_drift_baseline)
    drift_compare = drift_sub.add_parser("compare", help="与最近基线比较")
    drift_compare.add_argument("url")
    drift_compare.add_argument("--db")
    drift_compare.add_argument("--render-mode", choices=["never", "auto", "always"], default="auto")
    drift_compare.add_argument("--json", action="store_true")
    drift_compare.set_defaults(handler=_handle_drift_compare)
    drift_history = drift_sub.add_parser("history", help="查看漂移历史")
    drift_history.add_argument("url")
    drift_history.add_argument("--db")
    drift_history.add_argument("--limit", type=int, default=10)
    drift_history.add_argument("--json", action="store_true")
    drift_history.set_defaults(handler=_handle_drift_history)

    for provider in ["google", "backlinks", "dataforseo", "firecrawl"]:
        provider_parser = sub.add_parser(provider, help=f"{provider} 离线配置检测命令")
        provider_parser.add_argument("subcommand", nargs="?")
        provider_parser.add_argument("target", nargs="?")
        provider_parser.add_argument("--json", action="store_true")
        provider_parser.set_defaults(handler=_handle_external, provider=provider)

    audit = sub.add_parser("audit", help="运行全站审计并写入 artifact")
    audit.add_argument("url")
    audit.add_argument("--max-pages", type=int, default=20)
    audit.add_argument("--output-dir")
    audit.add_argument("--json", action="store_true")
    audit.set_defaults(handler=_handle_audit)

    return parser


def _handle_fetch(args: argparse.Namespace) -> int:
    result = fetch_url(args.url)
    data = to_plain(result)
    if args.json:
        _print_json(data)
    else:
        print(f"{data['status_code']} {data['final_url']}")
        if data["error"]:
            print(f"error: {data['error']}")
    return 1 if data["error"] else 0


def _handle_render(args: argparse.Namespace) -> int:
    data = to_plain(render_page(args.url, mode=args.mode))
    if args.json:
        _print_json(data)
    else:
        print(f"{data['status_code']} {data['final_url']} ({data['mode_used']})")
        if data["error"]:
            print(f"error: {data['error']}")
    return 1 if data["error"] else 0


def _handle_parse(args: argparse.Namespace) -> int:
    html = Path(args.html_file).read_text(encoding="utf-8")
    data = to_plain(parse_html(html, base_url=args.base_url))
    if args.json:
        _print_json(data)
    else:
        print(f"title: {data['title']}")
        print(f"word_count: {data['word_count']}")
        print(f"images: {len(data['images'])}")
        print(f"schema: {len(data['schema'])}")
    return 0


def _handle_page(args: argparse.Namespace) -> int:
    data = analyze_page(args.url, render_mode=args.render_mode)
    return _emit_analysis(data, args.json)


def _handle_technical(args: argparse.Namespace) -> int:
    data = analyze_technical(args.url, render_mode=args.render_mode)
    return _emit_analysis(data, args.json)


def _handle_content(args: argparse.Namespace) -> int:
    data = analyze_content(args.url, render_mode=args.render_mode)
    return _emit_analysis(data, args.json)


def _handle_schema(args: argparse.Namespace) -> int:
    data = analyze_schema(args.url, render_mode=args.render_mode)
    return _emit_analysis(data, args.json)


def _handle_sitemap(args: argparse.Namespace) -> int:
    data = analyze_sitemap(args.url)
    return _emit_analysis(data, args.json)


def _handle_images(args: argparse.Namespace) -> int:
    data = analyze_images(args.url, render_mode=args.render_mode)
    return _emit_analysis(data, args.json)


def _handle_geo(args: argparse.Namespace) -> int:
    data = analyze_geo(args.url, render_mode=args.render_mode)
    return _emit_analysis(data, args.json)


def _handle_hreflang(args: argparse.Namespace) -> int:
    data = analyze_hreflang(args.url, render_mode=args.render_mode)
    return _emit_analysis(data, args.json)


def _handle_local(args: argparse.Namespace) -> int:
    data = analyze_local(args.url, render_mode=args.render_mode)
    return _emit_analysis(data, args.json)


def _handle_ecommerce(args: argparse.Namespace) -> int:
    data = analyze_ecommerce(args.url, render_mode=args.render_mode)
    return _emit_analysis(data, args.json)


def _handle_drift_baseline(args: argparse.Namespace) -> int:
    data = create_baseline(args.url, db_path=args.db, render_mode=args.render_mode)
    return _emit_analysis(data, args.json)


def _handle_drift_compare(args: argparse.Namespace) -> int:
    data = compare_to_baseline(args.url, db_path=args.db, render_mode=args.render_mode)
    return _emit_analysis(data, args.json)


def _handle_drift_history(args: argparse.Namespace) -> int:
    data = history(args.url, db_path=args.db, limit=args.limit)
    return _emit_analysis(data, args.json)


def _handle_external(args: argparse.Namespace) -> int:
    data = offline_placeholder(args.provider, args.subcommand, args.target)
    return _emit_analysis(data, args.json)


def _handle_audit(args: argparse.Namespace) -> int:
    data = run_audit(args.url, max_pages=args.max_pages, output_dir=args.output_dir)
    if args.json:
        _print_json(data)
    else:
        artifacts = data["artifacts"]
        print(f"健康分：{data['summary']['health_score']}/100")
        print(f"业务类型：{data['summary']['business_type']}")
        print(f"输出目录：{artifacts['output_dir']}")
        print("Artifacts：FULL-AUDIT-REPORT.md、ACTION-PLAN.md、audit-data.json")
    return 0


def _emit_analysis(data: dict, as_json: bool) -> int:
    if as_json:
        _print_json(data)
    else:
        score = data.get("score") or data.get("technical_score")
        if score is not None:
            print(f"分数：{score}/100")
        if "status" in data:
            print(f"状态：{data['status']}")
        print(f"发现项：{len(data.get('findings', []))}")
        for item in data.get("findings", data.get("changes", []))[:10]:
            print(f"- [{item['severity']}] {item['title']}")
        if data.get("mode") == "offline-placeholder":
            print(data["message"])
    return 0


def _print_json(data: dict) -> None:
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
