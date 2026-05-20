from __future__ import annotations

import json
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

CONFIG_DIR = Path.home() / ".config" / "seo-agents"
CLAUDE_SETTINGS_PATH = Path.home() / ".claude" / "settings.json"
CONFIG_DIR_ENV = "SEO_AGENTS_CONFIG_DIR"
CLAUDE_SETTINGS_ENV = "SEO_AGENTS_CLAUDE_SETTINGS"

_PROVIDER_NAMES = {
    "google": "Google SEO API",
    "backlinks": "Backlink 数据源",
    "dataforseo": "DataForSEO",
    "firecrawl": "Firecrawl",
}

_PROVIDER_CONFIG_FILES = {
    "google": "google-api.json",
    "backlinks": "backlinks-api.json",
    "dataforseo": "dataforseo-api.json",
    "firecrawl": "firecrawl-api.json",
}

_ENV_FIELDS = {
    "google": {
        "service_account_path": "GOOGLE_APPLICATION_CREDENTIALS",
        "api_key": "GOOGLE_API_KEY",
        "ga4_property_id": "GA4_PROPERTY_ID",
        "default_property": "GSC_PROPERTY",
    },
    "backlinks": {
        "moz_api_key": "MOZ_API_KEY",
        "bing_api_key": "BING_WEBMASTER_API_KEY",
    },
    "dataforseo": {
        "username": "DATAFORSEO_USERNAME",
        "password": "DATAFORSEO_PASSWORD",
    },
    "firecrawl": {
        "api_key": "FIRECRAWL_API_KEY",
    },
}

_MCP_SERVERS = {
    "dataforseo": "dataforseo",
    "firecrawl": "firecrawl-mcp",
}

_MCP_ENV_FIELDS = {
    "dataforseo": {
        "username": "DATAFORSEO_USERNAME",
        "password": "DATAFORSEO_PASSWORD",
        "field_config_path": "FIELD_CONFIG_PATH",
    },
    "firecrawl": {
        "api_key": "FIRECRAWL_API_KEY",
    },
}

_SECRET_FIELD_HINTS = ("key", "token", "secret", "password")


def get_config_dir(env: Mapping[str, str] | None = None) -> Path:
    env_map = os.environ if env is None else env
    override = env_map.get(CONFIG_DIR_ENV)
    return Path(override).expanduser() if override else CONFIG_DIR


def get_claude_settings_path(env: Mapping[str, str] | None = None) -> Path:
    env_map = os.environ if env is None else env
    override = env_map.get(CLAUDE_SETTINGS_ENV)
    return Path(override).expanduser() if override else CLAUDE_SETTINGS_PATH


def provider_config_status(
    provider: str,
    *,
    env: Mapping[str, str] | None = None,
    config_dir: Path | None = None,
    claude_settings_path: Path | None = None,
) -> dict:
    env_map = os.environ if env is None else env
    resolved_config_dir = Path(config_dir) if config_dir else get_config_dir(env_map)
    resolved_claude_settings = (
        Path(claude_settings_path) if claude_settings_path else get_claude_settings_path(env_map)
    )
    config_path = resolved_config_dir / _PROVIDER_CONFIG_FILES.get(provider, f"{provider}.json")
    config, config_error = _read_json_object(config_path)
    settings, settings_error = _read_json_object(resolved_claude_settings)

    if provider == "google":
        return _google_status(config_path, config, config_error, env_map, resolved_config_dir)
    if provider == "backlinks":
        return _backlinks_status(config_path, config, config_error, env_map, resolved_config_dir)
    if provider == "dataforseo":
        return _dataforseo_status(
            config_path,
            config,
            config_error,
            env_map,
            resolved_config_dir,
            resolved_claude_settings,
            settings,
            settings_error,
        )
    if provider == "firecrawl":
        return _firecrawl_status(
            config_path,
            config,
            config_error,
            env_map,
            resolved_config_dir,
            resolved_claude_settings,
            settings,
            settings_error,
        )

    configured_fields = _present_config_fields(config)
    return _status_payload(
        provider=provider,
        config_dir=resolved_config_dir,
        config_path=config_path,
        config_error=config_error,
        env_fields=[],
        configured_fields=configured_fields,
        required_fields=[],
        configured=bool(configured_fields),
        credential_tier=None,
    )


def offline_placeholder(provider: str, command: str | None = None, target: str | None = None) -> dict:
    name = _PROVIDER_NAMES.get(provider, provider)
    config_status = provider_config_status(provider)
    status = "已检测到配置" if config_status["configured"] else "未配置"
    if config_status["configured"]:
        message = f"{name} 已检测到本地配置，但当前仍为离线占位：本轮不联网、不调用真实 API、不输出凭据。"
    else:
        message = f"{name} 当前为离线占位：未检测到本地配置，本轮不联网、不调用真实 API。"

    return {
        "command": provider,
        "subcommand": command,
        "target": target,
        "status": status,
        "mode": "offline-placeholder",
        "message": message,
        "configured": config_status["configured"],
        "config_dir": config_status["config_dir"],
        "config": config_status,
        "next_steps": [
            f"配置文件可放在 {config_status['config_dir']}。",
            "当前只检测配置字段和来源，不会输出 secret 值。",
            "接入真实 API 前，需要为该 provider 增加凭据校验、错误处理和 mock 测试。",
        ],
    }


def _google_status(
    config_path: Path,
    config: dict,
    config_error: str | None,
    env: Mapping[str, str],
    config_dir: Path,
) -> dict:
    env_fields = _present_env_fields("google", env)
    configured_fields = _effective_fields(
        config,
        env,
        "google",
        [
            "service_account_path",
            "api_key",
            "default_property",
            "ga4_property_id",
            "oauth_client_path",
            "ads_developer_token",
            "ads_customer_id",
            "ads_login_customer_id",
        ],
    )
    token_path = config_dir / "oauth-token.json"
    has_oauth_token = token_path.exists()
    has_api_key = "api_key" in configured_fields
    has_authenticated = (
        "service_account_path" in configured_fields
        or "oauth_client_path" in configured_fields
        or has_oauth_token
    )
    has_ga4 = has_authenticated and "ga4_property_id" in configured_fields
    has_ads = has_ga4 and {
        "ads_developer_token",
        "ads_customer_id",
    }.issubset(configured_fields)

    if has_ads:
        tier = {
            "tier": 3,
            "label": "Ads",
            "capabilities": ["PageSpeed/CrUX", "GSC/Indexing", "GA4", "Keyword Planner"],
            "missing": [],
        }
    elif has_ga4:
        tier = {
            "tier": 2,
            "label": "Full",
            "capabilities": ["PageSpeed/CrUX", "GSC/Indexing", "GA4"],
            "missing": ["ads_developer_token", "ads_customer_id"],
        }
    elif has_authenticated:
        tier = {
            "tier": 1,
            "label": "Authenticated",
            "capabilities": ["GSC/Indexing"],
            "missing": ["ga4_property_id"],
        }
    elif has_api_key:
        tier = {
            "tier": 0,
            "label": "API Key",
            "capabilities": ["PageSpeed/CrUX"],
            "missing": ["service_account_path 或 oauth-token.json"],
        }
    else:
        tier = {
            "tier": -1,
            "label": "No credentials",
            "capabilities": [],
            "missing": ["api_key"],
        }

    payload = _status_payload(
        provider="google",
        config_dir=config_dir,
        config_path=config_path,
        config_error=config_error,
        config_fields=_present_config_fields(
            config,
            [
                "service_account_path",
                "api_key",
                "default_property",
                "ga4_property_id",
                "oauth_client_path",
                "ads_developer_token",
                "ads_customer_id",
                "ads_login_customer_id",
            ],
        ),
        env_fields=env_fields,
        configured_fields=sorted(configured_fields),
        required_fields=["api_key"],
        configured=bool(configured_fields or has_oauth_token),
        credential_tier=tier,
    )
    payload["oauth_token"] = {
        "path": str(token_path),
        "exists": has_oauth_token,
    }
    return payload


def _backlinks_status(
    config_path: Path,
    config: dict,
    config_error: str | None,
    env: Mapping[str, str],
    config_dir: Path,
) -> dict:
    env_fields = _present_env_fields("backlinks", env)
    configured_fields = _effective_fields(
        config,
        env,
        "backlinks",
        ["moz_api_key", "bing_api_key", "bing_verified_sites", "commoncrawl_cache_dir"],
    )
    has_moz = "moz_api_key" in configured_fields
    has_bing = "bing_api_key" in configured_fields
    has_sites = "bing_verified_sites" in configured_fields
    if has_moz and has_bing:
        tier = {
            "tier": 2,
            "label": "Moz + Bing",
            "capabilities": ["Moz Link Explorer", "Bing Webmaster"],
            "missing": [] if has_sites else ["bing_verified_sites"],
        }
    elif has_moz:
        tier = {
            "tier": 1,
            "label": "Moz",
            "capabilities": ["Moz Link Explorer"],
            "missing": ["bing_api_key"],
        }
    elif has_bing:
        tier = {
            "tier": 1,
            "label": "Bing",
            "capabilities": ["Bing Webmaster"],
            "missing": ["moz_api_key"],
        }
    else:
        tier = {
            "tier": 0,
            "label": "Local/Common Crawl only",
            "capabilities": ["Common Crawl cache path"],
            "missing": ["moz_api_key", "bing_api_key"],
        }

    return _status_payload(
        provider="backlinks",
        config_dir=config_dir,
        config_path=config_path,
        config_error=config_error,
        config_fields=_present_config_fields(
            config,
            ["moz_api_key", "bing_api_key", "bing_verified_sites", "commoncrawl_cache_dir"],
        ),
        env_fields=env_fields,
        configured_fields=sorted(configured_fields),
        required_fields=["moz_api_key 或 bing_api_key"],
        configured=has_moz or has_bing,
        credential_tier=tier,
    )


def _dataforseo_status(
    config_path: Path,
    config: dict,
    config_error: str | None,
    env: Mapping[str, str],
    config_dir: Path,
    settings_path: Path,
    settings: dict,
    settings_error: str | None,
) -> dict:
    env_fields = _present_env_fields("dataforseo", env)
    mcp = _mcp_source("dataforseo", settings_path, settings, settings_error)
    configured_fields = _effective_fields(config, env, "dataforseo", ["username", "password"])
    configured_fields.update(mcp["logical_fields"])
    configured = {"username", "password"}.issubset(configured_fields)
    return _status_payload(
        provider="dataforseo",
        config_dir=config_dir,
        config_path=config_path,
        config_error=config_error,
        config_fields=_present_config_fields(config, ["username", "password"]),
        env_fields=env_fields,
        configured_fields=sorted(configured_fields),
        required_fields=["username", "password"],
        configured=configured,
        credential_tier={
            "tier": 1 if configured else -1,
            "label": "Configured" if configured else "No credentials",
            "capabilities": ["DataForSEO MCP/Python env"] if configured else [],
            "missing": [] if configured else ["DATAFORSEO_USERNAME", "DATAFORSEO_PASSWORD"],
        },
        mcp_source=mcp,
    )


def _firecrawl_status(
    config_path: Path,
    config: dict,
    config_error: str | None,
    env: Mapping[str, str],
    config_dir: Path,
    settings_path: Path,
    settings: dict,
    settings_error: str | None,
) -> dict:
    env_fields = _present_env_fields("firecrawl", env)
    mcp = _mcp_source("firecrawl", settings_path, settings, settings_error)
    configured_fields = _effective_fields(config, env, "firecrawl", ["api_key"])
    configured_fields.update(mcp["logical_fields"])
    configured = "api_key" in configured_fields
    return _status_payload(
        provider="firecrawl",
        config_dir=config_dir,
        config_path=config_path,
        config_error=config_error,
        config_fields=_present_config_fields(config, ["api_key"]),
        env_fields=env_fields,
        configured_fields=sorted(configured_fields),
        required_fields=["api_key"],
        configured=configured,
        credential_tier={
            "tier": 1 if configured else -1,
            "label": "Configured" if configured else "No credentials",
            "capabilities": ["Firecrawl MCP/env"] if configured else [],
            "missing": [] if configured else ["FIRECRAWL_API_KEY"],
        },
        mcp_source=mcp,
    )


def _status_payload(
    *,
    provider: str,
    config_dir: Path,
    config_path: Path,
    config_error: str | None,
    env_fields: list[str],
    configured_fields: list[str],
    required_fields: list[str],
    configured: bool,
    credential_tier: dict | None,
    mcp_source: dict | None = None,
    config_fields: list[str] | None = None,
) -> dict:
    sources: dict[str, Any] = {
        "config_file": {
            "path": str(config_path),
            "exists": config_path.exists(),
            "fields": config_fields if config_fields is not None else configured_fields,
            "error": config_error,
        },
        "environment": {
            "fields": env_fields,
        },
    }
    if mcp_source is not None:
        sources["claude_settings"] = {
            key: value
            for key, value in mcp_source.items()
            if key not in {"logical_fields"}
        }

    return {
        "provider": provider,
        "provider_name": _PROVIDER_NAMES.get(provider, provider),
        "configured": configured,
        "config_dir": str(config_dir),
        "required_fields": required_fields,
        "configured_fields": configured_fields,
        "credential_tier": credential_tier,
        "sources": sources,
    }


def _read_json_object(path: Path) -> tuple[dict, str | None]:
    if not path.exists():
        return {}, None
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        return {}, str(exc)
    if not isinstance(data, dict):
        return {}, "JSON root must be an object"
    return data, None


def _truthy(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


def _present_config_fields(config: dict, fields: list[str] | None = None) -> list[str]:
    field_names = fields or list(config)
    return [field for field in field_names if _truthy(config.get(field))]


def _present_env_fields(provider: str, env: Mapping[str, str]) -> list[str]:
    return [
        env_name
        for env_name in _ENV_FIELDS.get(provider, {}).values()
        if _truthy(env.get(env_name))
    ]


def _effective_fields(
    config: dict,
    env: Mapping[str, str],
    provider: str,
    fields: list[str],
) -> set[str]:
    effective = set(_present_config_fields(config, fields))
    for logical_name, env_name in _ENV_FIELDS.get(provider, {}).items():
        if logical_name not in effective and _truthy(env.get(env_name)):
            effective.add(logical_name)
    return effective


def _mcp_source(
    provider: str,
    settings_path: Path,
    settings: dict,
    settings_error: str | None,
) -> dict:
    server_name = _MCP_SERVERS.get(provider)
    if not server_name:
        return {
            "path": str(settings_path),
            "exists": settings_path.exists(),
            "server": None,
            "server_configured": False,
            "env_fields": [],
            "error": settings_error,
            "logical_fields": set(),
        }

    server = settings.get("mcpServers", {}).get(server_name, {})
    server_env = server.get("env", {}) if isinstance(server, dict) else {}
    env_map = _MCP_ENV_FIELDS.get(provider, {})
    logical_fields = {
        logical_name
        for logical_name, env_name in env_map.items()
        if _truthy(server_env.get(env_name))
    }
    return {
        "path": str(settings_path),
        "exists": settings_path.exists(),
        "server": server_name,
        "server_configured": bool(server),
        "env_fields": [
            env_name
            for env_name in env_map.values()
            if _truthy(server_env.get(env_name)) and not _looks_secret(env_name)
        ],
        "secret_env_fields": [
            env_name
            for env_name in env_map.values()
            if _truthy(server_env.get(env_name)) and _looks_secret(env_name)
        ],
        "error": settings_error,
        "logical_fields": logical_fields,
    }


def _looks_secret(name: str) -> bool:
    lower = name.lower()
    return any(hint in lower for hint in _SECRET_FIELD_HINTS)
