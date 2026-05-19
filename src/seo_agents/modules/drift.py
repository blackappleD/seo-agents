from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from seo_agents.extract.html import parse_html
from seo_agents.fetch.render import render_page

DEFAULT_DB_PATH = Path.home() / ".cache" / "seo-agents" / "drift" / "baselines.db"


@dataclass
class DriftSnapshot:
    url: str
    final_url: str
    timestamp: str
    title: str | None
    meta_description: str | None
    canonical: str | None
    robots: str | None
    h1: list[str]
    h2: list[str]
    h3: list[str]
    schema: list[dict[str, Any]]
    open_graph: dict[str, str]
    html_hash: str
    schema_hash: str
    status_code: int | None


def create_baseline(url: str, *, db_path: str | Path | None = None, render_mode: str = "auto") -> dict:
    snapshot = capture_snapshot(url, render_mode=render_mode)
    db = _connect(db_path)
    _insert_snapshot(db, snapshot)
    latest_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    db.close()
    return {
        "command": "drift baseline",
        "target": url,
        "status": "已建立基线",
        "baseline_id": latest_id,
        "snapshot": asdict(snapshot),
        "db_path": str(_db_path(db_path)),
    }


def compare_to_baseline(url: str, *, db_path: str | Path | None = None, render_mode: str = "auto") -> dict:
    db = _connect(db_path)
    previous = _latest_snapshot(db, url)
    current = capture_snapshot(url, render_mode=render_mode)
    if previous is None:
        db.close()
        return {
            "command": "drift compare",
            "target": url,
            "status": "无基线",
            "changes": [],
            "current": asdict(current),
            "db_path": str(_db_path(db_path)),
        }
    changes = _compare_snapshots(previous, current)
    db.close()
    return {
        "command": "drift compare",
        "target": url,
        "status": "已比较",
        "changes": changes,
        "previous": asdict(previous),
        "current": asdict(current),
        "db_path": str(_db_path(db_path)),
    }


def history(url: str, *, db_path: str | Path | None = None, limit: int = 10) -> dict:
    db = _connect(db_path)
    rows = db.execute(
        """
        SELECT url, final_url, timestamp, title, status_code, html_hash, schema_hash
        FROM baselines
        WHERE url = ? OR final_url = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (url, url, limit),
    ).fetchall()
    db.close()
    return {
        "command": "drift history",
        "target": url,
        "status": "已读取历史",
        "items": [dict(row) for row in rows],
        "db_path": str(_db_path(db_path)),
    }


def capture_snapshot(url: str, *, render_mode: str = "auto") -> DriftSnapshot:
    from datetime import datetime, timezone

    page = render_page(url, mode=render_mode)
    html = page.rendered_html or page.raw_html or ""
    parsed = parse_html(html, base_url=page.final_url)
    schema_json = json.dumps(parsed.schema, ensure_ascii=False, sort_keys=True)
    return DriftSnapshot(
        url=url,
        final_url=page.final_url,
        timestamp=datetime.now(timezone.utc).isoformat(),
        title=parsed.title,
        meta_description=parsed.meta_description,
        canonical=parsed.canonical,
        robots=parsed.meta_robots,
        h1=parsed.h1,
        h2=parsed.h2,
        h3=parsed.h3,
        schema=parsed.schema,
        open_graph=parsed.open_graph,
        html_hash=hashlib.sha256(html.encode("utf-8")).hexdigest(),
        schema_hash=hashlib.sha256(schema_json.encode("utf-8")).hexdigest(),
        status_code=page.status_code,
    )


def _connect(db_path: str | Path | None) -> sqlite3.Connection:
    path = _db_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=TRUNCATE")
    db.execute("PRAGMA synchronous=NORMAL")
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS baselines (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          url TEXT NOT NULL,
          final_url TEXT NOT NULL,
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
          html_hash TEXT,
          schema_hash TEXT,
          status_code INTEGER
        )
        """
    )
    return db


def _insert_snapshot(db: sqlite3.Connection, snapshot: DriftSnapshot) -> None:
    db.execute(
        """
        INSERT INTO baselines (
          url, final_url, url_hash, timestamp, title, meta_description, canonical,
          robots, h1, h2_json, h3_json, schema_json, og_json, html_hash,
          schema_hash, status_code
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            snapshot.url,
            snapshot.final_url,
            _url_hash(snapshot.url),
            snapshot.timestamp,
            snapshot.title,
            snapshot.meta_description,
            snapshot.canonical,
            snapshot.robots,
            snapshot.h1[0] if snapshot.h1 else None,
            json.dumps(snapshot.h2, ensure_ascii=False),
            json.dumps(snapshot.h3, ensure_ascii=False),
            json.dumps(snapshot.schema, ensure_ascii=False),
            json.dumps(snapshot.open_graph, ensure_ascii=False),
            snapshot.html_hash,
            snapshot.schema_hash,
            snapshot.status_code,
        ),
    )
    db.commit()


def _latest_snapshot(db: sqlite3.Connection, url: str) -> DriftSnapshot | None:
    row = db.execute(
        """
        SELECT * FROM baselines
        WHERE url = ? OR final_url = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (url, url),
    ).fetchone()
    if row is None:
        return None
    return DriftSnapshot(
        url=row["url"],
        final_url=row["final_url"],
        timestamp=row["timestamp"],
        title=row["title"],
        meta_description=row["meta_description"],
        canonical=row["canonical"],
        robots=row["robots"],
        h1=[row["h1"]] if row["h1"] else [],
        h2=json.loads(row["h2_json"] or "[]"),
        h3=json.loads(row["h3_json"] or "[]"),
        schema=json.loads(row["schema_json"] or "[]"),
        open_graph=json.loads(row["og_json"] or "{}"),
        html_hash=row["html_hash"],
        schema_hash=row["schema_hash"],
        status_code=row["status_code"],
    )


def _compare_snapshots(previous: DriftSnapshot, current: DriftSnapshot) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    if previous.status_code == 200 and current.status_code and current.status_code >= 400:
        changes.append(_change("状态码从 200 变为错误", "Critical", previous.status_code, current.status_code))
    if "noindex" not in (previous.robots or "").lower() and "noindex" in (current.robots or "").lower():
        changes.append(_change("新增 noindex", "Critical", previous.robots, current.robots))
    if previous.canonical and current.canonical and previous.canonical != current.canonical:
        severity = "High" if _host(previous.canonical) != _host(current.canonical) else "Medium"
        changes.append(_change("canonical 发生变化", severity, previous.canonical, current.canonical))
    if previous.title != current.title:
        changes.append(_change("title 发生变化", "Medium", previous.title, current.title))
    if previous.h1 and not current.h1:
        changes.append(_change("H1 消失", "High", previous.h1, current.h1))
    if previous.schema_hash != current.schema_hash:
        severity = "High" if previous.schema and not current.schema else "Medium"
        changes.append(_change("Schema 发生变化", severity, previous.schema_hash, current.schema_hash))
    if previous.html_hash != current.html_hash:
        changes.append(_change("HTML 内容发生变化", "Info", previous.html_hash, current.html_hash))
    return changes


def _change(title: str, severity: str, before: Any, after: Any) -> dict[str, Any]:
    return {"title": title, "severity": severity, "before": before, "after": after}


def _db_path(db_path: str | Path | None) -> Path:
    return Path(db_path).expanduser() if db_path else DEFAULT_DB_PATH


def _url_hash(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def _host(url: str) -> str:
    from urllib.parse import urlparse

    return urlparse(url).netloc.lower()
