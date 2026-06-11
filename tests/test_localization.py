from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_chinese_language_rule_present_and_old_alias_absent() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "默认使用简体中文" in agents
    assert "语言偏好" in agents
    assert "本地 v2 闭环" in readme

    scanned_roots = [
        ROOT / "src",
        ROOT / "scripts",
        ROOT / "skills",
        ROOT / "agents",
        ROOT / "docs",
        ROOT / "schema",
        ROOT / "tests",
    ]
    root_files = [
        ROOT / "AGENTS.md",
        ROOT / "README.md",
        ROOT / "SECURITY.md",
        ROOT / "PRIVACY.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "CODE_OF_CONDUCT.md",
        ROOT / "pyproject.toml",
    ]
    source_files = [
        path
        for base in scanned_roots
        for path in base.rglob("*")
        if path.is_file() and path.suffix in {".md", ".py", ".toml", ".json"}
    ]
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in [*root_files, *source_files]
    )
    old_hyphen_alias = "your" + "-seo"
    old_snake_alias = "your" + "_seo"
    assert old_hyphen_alias not in combined
    assert old_snake_alias not in combined
