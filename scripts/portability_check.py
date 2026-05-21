from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_KEYS = ["name", "description", "user-invocable", "argument-hint", "license", "metadata"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="检查 agent skill 可移植性")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = check_portability(ROOT)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"错误数：{result['errors']}")
        print(f"警告数：{result['warnings']}")
        for error in result["error_details"]:
            print(f"ERROR {error['file']}: {error['message']}")
        for warning in result["warning_details"]:
            print(f"WARN {warning['file']}: {warning['message']}")
    return 1 if result["errors"] else 0


def check_portability(root: Path) -> dict:
    skills_root = root / "skills"
    errors: list[dict] = []
    warnings: list[dict] = []
    skill_files = sorted(skills_root.glob("*/SKILL.md")) if skills_root.exists() else []
    if not skill_files:
        errors.append({"file": "skills", "message": "未找到 skill 文件"})

    skills: list[dict] = []
    for path in skill_files:
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        frontmatter = _frontmatter(text)
        if frontmatter is None:
            errors.append({"file": relative, "message": "缺少 YAML 风格 frontmatter"})
            continue
        parsed = _parse_simple_frontmatter(frontmatter)
        for key in REQUIRED_KEYS:
            if key not in parsed:
                errors.append({"file": relative, "message": f"缺少 frontmatter key：{key}"})
        if parsed.get("license") != "MIT":
            warnings.append({"file": relative, "message": "Skill license 应为 MIT"})
        if parsed.get("user-invocable") not in {"true", "false", True, False}:
            errors.append({"file": relative, "message": "user-invocable 必须是 true 或 false"})
        if "version" not in frontmatter:
            errors.append({"file": relative, "message": "metadata.version 是必填项"})
        if "category" not in frontmatter:
            errors.append({"file": relative, "message": "metadata.category 是必填项"})
        skills.append({"file": relative, "name": str(parsed.get("name", ""))})

    return {
        "errors": len(errors),
        "warnings": len(warnings),
        "skills_checked": len(skill_files),
        "skills": skills,
        "error_details": errors,
        "warning_details": warnings,
    }


def _frontmatter(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return match.group(1) if match else None


def _parse_simple_frontmatter(frontmatter: str) -> dict:
    parsed: dict[str, object] = {}
    for line in frontmatter.splitlines():
        if not line.strip() or line.startswith(" ") or line.strip() in {">"}:
            continue
        key, sep, value = line.partition(":")
        if sep:
            parsed[key.strip()] = value.strip().strip('"')
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())
