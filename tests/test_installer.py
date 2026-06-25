from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run_installer(args: list[str], env: dict[str, str]) -> dict:
    proc = subprocess.run(
        [sys.executable, "scripts/install.py", *args, "--json"],
        cwd=ROOT,
        env={**os.environ, **env, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(proc.stdout)


def _load_installer_module():
    spec = importlib.util.spec_from_file_location("seo_agents_installer", ROOT / "scripts" / "install.py")
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_codex_dry_run_plans_skill_and_agent_reference_copy(tmp_path: Path) -> None:
    codex_home = tmp_path / "codex-home"
    data = _run_installer(
        ["--target", "codex", "--dry-run"],
        {"CODEX_HOME": str(codex_home)},
    )

    assert data["errors"] == []
    assert data["dry_run"] is True
    assert not codex_home.exists()

    destinations = {Path(op["destination"]).as_posix() for op in data["operations"]}
    assert (codex_home / "skills" / "seo").as_posix() in destinations
    assert (
        codex_home / "skills" / "seo" / "references" / "agents" / "seo-technical.md"
    ).as_posix() in destinations
    assert all(op["action"] != "run" for op in data["operations"])


def test_all_dry_run_uses_temp_homes_and_skips_cli_install(tmp_path: Path) -> None:
    home = tmp_path / "home"
    codex_home = tmp_path / "codex"
    agents_home = tmp_path / "agents"
    data = _run_installer(
        ["--target", "all", "--dry-run", "--skip-deps"],
        {
            "HOME": str(home),
            "USERPROFILE": str(home),
            "CODEX_HOME": str(codex_home),
            "AGENTS_HOME": str(agents_home),
        },
    )

    destinations = {Path(op["destination"]).as_posix() for op in data["operations"]}
    assert data["errors"] == []
    assert any(op["action"] == "skip_cli_install" for op in data["operations"])
    assert (codex_home / "skills" / "seo").as_posix() in destinations
    assert (home / ".claude" / "agents" / "seo-technical.md").as_posix() in destinations
    assert (
        agents_home / "skills" / "seo" / "references" / "agents" / "seo-technical.md"
    ).as_posix() in destinations
    assert not home.exists()
    assert not codex_home.exists()
    assert not agents_home.exists()


def test_open_agent_copy_writes_only_temp_target(tmp_path: Path) -> None:
    installer = _load_installer_module()
    agents_home = tmp_path / "agents-home"
    data = installer.install(
        source=ROOT,
        target="open-agent",
        dry_run=False,
        skip_deps=True,
        keep_temp=False,
        env={"AGENTS_HOME": str(agents_home), "HOME": str(tmp_path / "home")},
    )

    assert data["errors"] == []
    assert (agents_home / "skills" / "seo" / "SKILL.md").is_file()
    assert (agents_home / "skills" / "seo-technical" / "SKILL.md").is_file()
    assert (
        agents_home / "skills" / "seo" / "references" / "agents" / "seo-technical.md"
    ).is_file()


def test_installer_targets_are_documented() -> None:
    installer = _load_installer_module()
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    installation = (ROOT / "docs" / "INSTALLATION.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    for target in installer.TARGETS:
        needle = f"--target {target}"
        assert needle in readme
        assert needle in installation
        assert needle in agents


def test_wrappers_delegate_to_python_installer() -> None:
    sh_text = (ROOT / "install.sh").read_text(encoding="utf-8")
    ps_text = (ROOT / "install.ps1").read_text(encoding="utf-8")

    assert "scripts/install.py" in sh_text
    assert "scripts\\install.py" in ps_text
    assert "Python 3.10+" in sh_text
    assert "Python 3.10+" in ps_text
    assert "git" in sh_text
    assert "git" in ps_text
