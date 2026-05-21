from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from seo_agents.extract.html import parse_html  # noqa: E402
from seo_agents.models import to_plain  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        print("用法：python scripts/parse_html.py <html-file> [--json]", file=sys.stderr)
        return 2
    html = Path(argv[0]).read_text(encoding="utf-8")
    result = to_plain(parse_html(html))
    if "--json" in argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"title: {result['title']}")
        print(f"word_count: {result['word_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
