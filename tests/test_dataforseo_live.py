from __future__ import annotations

import base64
import json
from pathlib import Path
from urllib.request import Request

from seo_agents.modules.dataforseo import run_dataforseo_command


class FakeResponse:
    def __init__(self, payload: dict, status: int = 200) -> None:
        self.payload = payload
        self.status = status

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")

    def getcode(self) -> int:
        return self.status


def test_dataforseo_live_serp_builds_basic_auth_without_leaking_secret(tmp_path: Path) -> None:
    captured: dict[str, object] = {}

    def fake_urlopen(req: Request, timeout: int) -> FakeResponse:
        captured["url"] = req.full_url
        captured["method"] = req.get_method()
        captured["body"] = json.loads(req.data.decode("utf-8")) if req.data else None
        captured["authorization"] = req.get_header("Authorization")
        captured["timeout"] = timeout
        return FakeResponse(
            {
                "status_code": 20000,
                "status_message": "Ok.",
                "cost": 0.002,
                "tasks_count": 1,
                "tasks_error": 0,
                "tasks": [
                    {
                        "status_code": 20000,
                        "result": [
                            {
                                "items": [
                                    {
                                        "type": "organic",
                                        "rank_group": 1,
                                        "rank_absolute": 1,
                                        "domain": "example.com",
                                        "url": "https://example.com/",
                                        "title": "Example",
                                        "description": "Example snippet",
                                    }
                                ]
                            }
                        ],
                    }
                ],
            }
        )

    result = run_dataforseo_command(
        "serp",
        "ai seo",
        env={
            "DATAFORSEO_USERNAME": "user@example.com",
            "DATAFORSEO_PASSWORD": "provider-secret",
        },
        config_dir=tmp_path / "config",
        claude_settings_path=tmp_path / "settings.json",
        urlopen=fake_urlopen,
    )

    expected_auth = "Basic " + base64.b64encode(b"user@example.com:provider-secret").decode("ascii")
    assert captured["url"] == "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
    assert captured["method"] == "POST"
    assert captured["authorization"] == expected_auth
    assert captured["body"] == [
        {
            "keyword": "ai seo",
            "location_code": 2840,
            "language_code": "en",
            "depth": 10,
            "device": "desktop",
        }
    ]
    assert result["status"] == "ok"
    assert result["charged"] is True
    assert result["summary"]["items"][0]["domain"] == "example.com"
    dumped = json.dumps(result, ensure_ascii=False)
    assert "provider-secret" not in dumped
    assert "user@example.com" not in dumped


def test_dataforseo_user_data_redacts_login_in_raw_response(tmp_path: Path) -> None:
    def fake_urlopen(req: Request, timeout: int) -> FakeResponse:
        return FakeResponse(
            {
                "status_code": 20000,
                "status_message": "Ok.",
                "cost": 0,
                "tasks_count": 1,
                "tasks_error": 0,
                "tasks": [
                    {
                        "result": [
                            {
                                "login": "api-login@example.com",
                                "money": {"balance": 12.34, "total": 20.0},
                            }
                        ]
                    }
                ],
            }
        )

    result = run_dataforseo_command(
        "user-data",
        None,
        include_raw=True,
        env={
            "DATAFORSEO_USERNAME": "api-login@example.com",
            "DATAFORSEO_PASSWORD": "provider-secret",
        },
        config_dir=tmp_path / "config",
        claude_settings_path=tmp_path / "settings.json",
        urlopen=fake_urlopen,
    )

    assert result["status"] == "ok"
    assert result["charged"] is False
    assert result["summary"] == {
        "login_present": True,
        "balance": 12.34,
        "total_deposited": 20.0,
    }
    dumped = json.dumps(result, ensure_ascii=False)
    assert "api-login@example.com" not in dumped
    assert "provider-secret" not in dumped
    assert result["raw_response"]["tasks"][0]["result"][0]["login"] == "[redacted]"


def test_dataforseo_live_without_credentials_does_not_call_network(tmp_path: Path) -> None:
    def fail_urlopen(req: Request, timeout: int) -> FakeResponse:
        raise AssertionError("network should not be called without credentials")

    result = run_dataforseo_command(
        "user-data",
        None,
        env={},
        config_dir=tmp_path / "config",
        claude_settings_path=tmp_path / "settings.json",
        urlopen=fail_urlopen,
    )

    assert result["status"] == "未配置"
    assert result["mode"] == "unavailable"
    assert result["charged"] is False
