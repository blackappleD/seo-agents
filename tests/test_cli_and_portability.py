from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
PROVIDER_ENV_KEYS = [
    "GOOGLE_APPLICATION_CREDENTIALS",
    "GOOGLE_API_KEY",
    "GA4_PROPERTY_ID",
    "GSC_PROPERTY",
    "MOZ_API_KEY",
    "BING_WEBMASTER_API_KEY",
    "DATAFORSEO_USERNAME",
    "DATAFORSEO_PASSWORD",
    "FIRECRAWL_API_KEY",
]


def test_portability_script_json_success() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/portability_check.py", "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["errors"] == 0
    assert data["skills_checked"] >= 8


def test_cli_parse_local_file() -> None:
    artifact_dir = ROOT / ".test-artifacts"
    artifact_dir.mkdir(exist_ok=True)
    html_file = artifact_dir / f"page-{uuid4().hex}.html"
    html_file.write_text("<html><head><title>T</title></head><body><h1>H</h1></body></html>", encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "-m", "seo_agents", "parse", str(html_file), "--json"],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
        capture_output=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["title"] == "T"
    assert data["h1"] == ["H"]


def test_cli_help_is_chinese() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "seo_agents", "--help"],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
        capture_output=True,
        check=True,
    )
    assert "本地分析 CLI" in proc.stdout
    assert "运行单页 SEO 分析" in proc.stdout


def test_cli_external_placeholder_is_offline(tmp_path) -> None:  # type: ignore[no-untyped-def]
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONDONTWRITEBYTECODE": "1"}
    for key in PROVIDER_ENV_KEYS:
        env.pop(key, None)
    env["SEO_AGENTS_CONFIG_DIR"] = str(tmp_path / "config")
    env["SEO_AGENTS_CLAUDE_SETTINGS"] = str(tmp_path / "settings.json")
    proc = subprocess.run(
        [sys.executable, "-m", "seo_agents", "google", "setup", "--json"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    assert data["status"] == "未配置"
    assert data["mode"] == "offline-placeholder"
    assert data["configured"] is False
    assert data["config"]["sources"]["config_file"]["path"].endswith("google-api.json")
