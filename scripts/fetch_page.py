from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from seo_agents.fetch.http import fetch_url  # noqa: E402
from seo_agents.models import to_plain  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        print("用法：python scripts/fetch_page.py <url> [--json]", file=sys.stderr)
        return 2
    url = argv[0]
    result = to_plain(fetch_url(url))
    if "--json" in argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['status_code']} {result['final_url']}")
    return 1 if result["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
