from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Iterable, Mapping
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ("cli", "codex", "claude", "open-agent", "all")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="安装 seo-agents CLI 和 agent assets")
    parser.add_argument(
        "--target",
        choices=TARGETS,
        default="cli",
        help="安装目标：cli、codex、claude、open-agent 或 all，默认 cli",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=ROOT,
        help="源码 checkout 路径，默认使用当前脚本所在仓库",
    )
    parser.add_argument("--dry-run", action="store_true", help="只输出将执行的操作，不写文件")
    parser.add_argument("--skip-deps", action="store_true", help="跳过 Python package 安装")
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="保留临时目录；本地 checkout 安装不会创建临时目录",
    )
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    args = parser.parse_args(argv)

    result = install(
        source=args.source,
        target=args.target,
        dry_run=args.dry_run,
        skip_deps=args.skip_deps,
        keep_temp=args.keep_temp,
        env=os.environ,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_human(result)
    return 0 if not result["errors"] else 1


def install(
    *,
    source: Path,
    target: str,
    dry_run: bool,
    skip_deps: bool,
    keep_temp: bool,
    env: Mapping[str, str],
) -> dict:
    source = source.expanduser().resolve()
    operations: list[dict[str, str]] = []
    warnings: list[str] = []
    errors: list[str] = []

    _validate_source(source, errors)
    if errors:
        return _result(source, target, dry_run, operations, warnings, errors)

    if keep_temp:
        warnings.append("本地 checkout 安装不会创建临时目录，--keep-temp 当前无需处理。")

    expanded_targets = _expand_targets(target)
    for item in expanded_targets:
        if item == "cli":
            _install_cli(source, dry_run, skip_deps, operations)
        elif item == "codex":
            _install_codex(source, env, dry_run, operations)
        elif item == "claude":
            _install_claude(source, env, dry_run, operations)
        elif item == "open-agent":
            _install_open_agent(source, env, dry_run, operations)
        else:
            errors.append(f"未知安装目标：{item}")

    return _result(source, target, dry_run, operations, warnings, errors)


def _validate_source(source: Path, errors: list[str]) -> None:
    required = ["pyproject.toml", "skills", "agents"]
    for name in required:
        if not (source / name).exists():
            errors.append(f"源码路径缺少 {name}: {source}")


def _expand_targets(target: str) -> list[str]:
    if target == "all":
        return ["cli", "codex", "claude", "open-agent"]
    return [target]


def _install_cli(
    source: Path,
    dry_run: bool,
    skip_deps: bool,
    operations: list[dict[str, str]],
) -> None:
    command = [sys.executable, "-m", "pip", "install", str(source)]
    if skip_deps:
        operations.append(
            {
                "action": "skip_cli_install",
                "source": str(source),
                "destination": "",
                "detail": "已按 --skip-deps 跳过 Python package 安装",
            }
        )
        return
    operations.append(
        {
            "action": "run",
            "source": str(source),
            "destination": "",
            "detail": " ".join(command),
        }
    )
    if not dry_run:
        subprocess.run(command, check=True)


def _install_codex(
    source: Path,
    env: Mapping[str, str],
    dry_run: bool,
    operations: list[dict[str, str]],
) -> None:
    codex_home = Path(env.get("CODEX_HOME", str(_home(env) / ".codex"))).expanduser()
    skills_root = codex_home / "skills"
    _copy_skills(source, skills_root, dry_run, operations)
    _copy_agent_references(source, skills_root / "seo" / "references" / "agents", dry_run, operations)


def _install_claude(
    source: Path,
    env: Mapping[str, str],
    dry_run: bool,
    operations: list[dict[str, str]],
) -> None:
    claude_home = _home(env) / ".claude"
    skills_root = claude_home / "skills"
    agents_root = claude_home / "agents"
    _copy_skills(source, skills_root, dry_run, operations)
    _copy_agent_files(source / "agents", agents_root, dry_run, operations)


def _install_open_agent(
    source: Path,
    env: Mapping[str, str],
    dry_run: bool,
    operations: list[dict[str, str]],
) -> None:
    agents_home = Path(env.get("AGENTS_HOME", str(_home(env) / ".agents"))).expanduser()
    skills_root = agents_home / "skills"
    _copy_skills(source, skills_root, dry_run, operations)
    _copy_agent_references(source, skills_root / "seo" / "references" / "agents", dry_run, operations)


def _copy_skills(
    source: Path,
    skills_root: Path,
    dry_run: bool,
    operations: list[dict[str, str]],
) -> None:
    for skill_dir in _skill_dirs(source / "skills"):
        _copy_tree(skill_dir, skills_root / skill_dir.name, dry_run, operations)


def _skill_dirs(skills_dir: Path) -> Iterable[Path]:
    return sorted(
        path for path in skills_dir.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
    )


def _copy_agent_references(
    source: Path,
    destination: Path,
    dry_run: bool,
    operations: list[dict[str, str]],
) -> None:
    _copy_agent_files(source / "agents", destination, dry_run, operations)


def _copy_agent_files(
    agents_source: Path,
    destination: Path,
    dry_run: bool,
    operations: list[dict[str, str]],
) -> None:
    for agent_file in sorted(agents_source.glob("*.md")):
        _copy_file(agent_file, destination / agent_file.name, dry_run, operations)


def _copy_tree(
    source: Path,
    destination: Path,
    dry_run: bool,
    operations: list[dict[str, str]],
) -> None:
    operations.append(
        {
            "action": "copy_tree",
            "source": str(source),
            "destination": str(destination),
            "detail": "",
        }
    )
    if dry_run:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, dirs_exist_ok=True)


def _copy_file(
    source: Path,
    destination: Path,
    dry_run: bool,
    operations: list[dict[str, str]],
) -> None:
    operations.append(
        {
            "action": "copy_file",
            "source": str(source),
            "destination": str(destination),
            "detail": "",
        }
    )
    if dry_run:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def _home(env: Mapping[str, str]) -> Path:
    home = env.get("HOME") or env.get("USERPROFILE")
    return Path(home).expanduser() if home else Path.home()


def _result(
    source: Path,
    target: str,
    dry_run: bool,
    operations: list[dict[str, str]],
    warnings: list[str],
    errors: list[str],
) -> dict:
    return {
        "source": str(source),
        "target": target,
        "dry_run": dry_run,
        "operations": operations,
        "warnings": warnings,
        "errors": errors,
    }


def _print_human(result: dict) -> None:
    label = "DRY RUN" if result["dry_run"] else "INSTALL"
    print(f"seo-agents {label}: target={result['target']}")
    for warning in result["warnings"]:
        print(f"WARN: {warning}")
    for error in result["errors"]:
        print(f"ERROR: {error}")
    for operation in result["operations"]:
        destination = operation["destination"]
        suffix = f" -> {destination}" if destination else ""
        detail = f" ({operation['detail']})" if operation["detail"] else ""
        print(f"{operation['action']}: {operation['source']}{suffix}{detail}")


if __name__ == "__main__":
    raise SystemExit(main())
