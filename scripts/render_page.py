from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from seo_agents.fetch.render import render_page  # noqa: E402
from seo_agents.models import to_plain  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        print("用法：python scripts/render_page.py <url> [--mode auto] [--json]", file=sys.stderr)
        return 2
    url = argv[0]
    mode = "auto"
    if "--mode" in argv:
        mode = argv[argv.index("--mode") + 1]
    result = to_plain(render_page(url, mode=mode))
    if "--json" in argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['status_code']} {result['final_url']} ({result['mode_used']})")
    return 1 if result["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
