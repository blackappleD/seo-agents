from __future__ import annotations

import json

from seo_agents.modules.external import provider_config_status


def test_google_config_detects_tier_without_leaking_values(tmp_path) -> None:  # type: ignore[no-untyped-def]
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "google-api.json").write_text(
        json.dumps(
            {
                "service_account_path": "/secrets/service-account.json",
                "api_key": "google-api-secret",
                "default_property": "sc-domain:example.com",
                "ga4_property_id": "properties/123456789",
                "ads_developer_token": "ads-secret",
                "ads_customer_id": "123-456-7890",
            }
        ),
        encoding="utf-8",
    )

    status = provider_config_status(
        "google",
        env={},
        config_dir=config_dir,
        claude_settings_path=tmp_path / "settings.json",
    )

    assert status["configured"] is True
    assert status["credential_tier"]["tier"] == 3
    assert "api_key" in status["configured_fields"]
    dumped = json.dumps(status, ensure_ascii=False)
    assert "google-api-secret" not in dumped
    assert "ads-secret" not in dumped


def test_dataforseo_mcp_settings_are_detected_without_leaking_values(tmp_path) -> None:  # type: ignore[no-untyped-def]
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        json.dumps(
            {
                "mcpServers": {
                    "dataforseo": {
                        "command": "npx",
                        "env": {
                            "DATAFORSEO_USERNAME": "user@example.com",
                            "DATAFORSEO_PASSWORD": "provider-secret",
                            "FIELD_CONFIG_PATH": "/tmp/fields.json",
                        },
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    status = provider_config_status(
        "dataforseo",
        env={},
        config_dir=tmp_path / "config",
        claude_settings_path=settings_path,
    )

    assert status["configured"] is True
    assert status["configured_fields"] == ["field_config_path", "password", "username"]
    assert status["sources"]["claude_settings"]["server"] == "dataforseo"
    assert "DATAFORSEO_PASSWORD" in status["sources"]["claude_settings"]["secret_env_fields"]
    dumped = json.dumps(status, ensure_ascii=False)
    assert "provider-secret" not in dumped
    assert "user@example.com" not in dumped


def test_firecrawl_env_fallback_is_detected_without_leaking_value(tmp_path) -> None:  # type: ignore[no-untyped-def]
    status = provider_config_status(
        "firecrawl",
        env={"FIRECRAWL_API_KEY": "fc-secret"},
        config_dir=tmp_path / "config",
        claude_settings_path=tmp_path / "settings.json",
    )

    assert status["configured"] is True
    assert status["configured_fields"] == ["api_key"]
    assert status["sources"]["environment"]["fields"] == ["FIRECRAWL_API_KEY"]
    assert "fc-secret" not in json.dumps(status, ensure_ascii=False)
