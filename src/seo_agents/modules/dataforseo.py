from __future__ import annotations

import base64
import json
import os
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request
from urllib.parse import urlparse

from seo_agents.modules.external import (
    get_claude_settings_path,
    get_config_dir,
    offline_placeholder,
    provider_config_status,
)

API_BASE_URL = "https://api.dataforseo.com"
CONFIG_FILENAME = "dataforseo-api.json"
CLAUDE_SERVER_NAME = "dataforseo"
USER_AGENT = "seo-agents/0.1 DataForSEO client"

DATAFORSEO_COMMANDS = {
    "setup": "免费调用 /v3/appendix/user_data 验证凭据和余额。",
    "status": "免费调用 /v3/appendix/user_data 验证凭据和余额。",
    "user-data": "免费调用 /v3/appendix/user_data 验证凭据和余额。",
    "serp": "调用 Google organic live advanced SERP，会按 DataForSEO 账户计费。",
    "related-keywords": "调用 DataForSEO Labs related keywords，会按 DataForSEO 账户计费。",
    "domain-rank": "调用 DataForSEO Labs domain rank overview，会按 DataForSEO 账户计费。",
}

_REDACT_KEYS = {
    "authorization",
    "api_key",
    "apikey",
    "password",
    "secret",
    "token",
    "login",
    "email",
}


@dataclass(frozen=True)
class DataForSEOCredentials:
    username: str
    password: str
    source: str


Urlopen = Callable[..., Any]


def run_dataforseo_command(
    subcommand: str | None,
    target: str | None,
    *,
    offline: bool = False,
    location_code: int = 2840,
    language_code: str = "en",
    depth: int = 10,
    device: str = "desktop",
    limit: int = 10,
    include_raw: bool = False,
    timeout: int = 30,
    env: Mapping[str, str] | None = None,
    config_dir: Path | None = None,
    claude_settings_path: Path | None = None,
    urlopen: Urlopen | None = None,
) -> dict:
    command = (subcommand or "setup").strip().lower()
    normalized_target = (target or "").strip() or None

    if offline:
        payload = offline_placeholder("dataforseo", command, normalized_target)
        payload["available_commands"] = DATAFORSEO_COMMANDS
        payload["next_steps"] = [
            f"配置文件可放在 {payload['config_dir']}。",
            "当前只检测配置字段和来源，不会输出 secret 值。",
            "默认 DataForSEO 命令会调用真实 API；仅配置检测时添加 --offline。",
            "首次验证建议运行 seo-agents dataforseo user-data --json；该接口官方标注不收费。",
        ]
        return payload

    credentials = load_dataforseo_credentials(
        env=env,
        config_dir=config_dir,
        claude_settings_path=claude_settings_path,
    )
    config_status = provider_config_status(
        "dataforseo",
        env=env,
        config_dir=config_dir,
        claude_settings_path=claude_settings_path,
    )
    if credentials is None:
        return {
            "command": "dataforseo",
            "subcommand": command,
            "target": normalized_target,
            "status": "未配置",
            "mode": "unavailable",
            "message": "DataForSEO 真实接入需要 username/password；未检测到完整凭据，未发起网络请求。",
            "configured": False,
            "charged": False,
            "config_dir": config_status["config_dir"],
            "config": config_status,
            "available_commands": DATAFORSEO_COMMANDS,
            "next_steps": [
                "登录 https://app.dataforseo.com/api-access 获取 API login 和 API password。",
                f"写入 {config_status['config_dir']}\\{CONFIG_FILENAME}，或设置 DATAFORSEO_USERNAME / DATAFORSEO_PASSWORD。",
                "不要提交凭据文件，不要把 API password 当作账户登录密码。",
            ],
        }

    if command in {"setup", "status", "user-data"}:
        return _account_status(
            credentials,
            include_raw=include_raw,
            timeout=timeout,
            urlopen=urlopen,
            config_status=config_status,
        )
    if command == "serp":
        if not normalized_target:
            return _missing_target(command, "需要提供 keyword，例如：seo-agents dataforseo serp \"ai seo\"")
        return _serp_live(
            credentials,
            keyword=normalized_target,
            location_code=location_code,
            language_code=language_code,
            depth=depth,
            device=device,
            limit=limit,
            include_raw=include_raw,
            timeout=timeout,
            urlopen=urlopen,
            config_status=config_status,
        )
    if command == "related-keywords":
        if not normalized_target:
            return _missing_target(
                command,
                "需要提供 keyword，例如：seo-agents dataforseo related-keywords \"ai seo\"",
            )
        return _related_keywords_live(
            credentials,
            keyword=normalized_target,
            location_code=location_code,
            language_code=language_code,
            limit=limit,
            include_raw=include_raw,
            timeout=timeout,
            urlopen=urlopen,
            config_status=config_status,
        )
    if command == "domain-rank":
        if not normalized_target:
            return _missing_target(
                command,
                "需要提供 domain，例如：seo-agents dataforseo domain-rank example.com",
            )
        return _domain_rank_live(
            credentials,
            target=_normalize_domain(normalized_target),
            location_code=location_code,
            language_code=language_code,
            include_raw=include_raw,
            timeout=timeout,
            urlopen=urlopen,
            config_status=config_status,
        )

    payload = offline_placeholder("dataforseo", command, normalized_target)
    payload["status"] = "不支持的命令"
    payload["mode"] = "unsupported-command"
    payload["message"] = f"DataForSEO 暂不支持子命令：{command}。"
    payload["available_commands"] = DATAFORSEO_COMMANDS
    return payload


def load_dataforseo_credentials(
    *,
    env: Mapping[str, str] | None = None,
    config_dir: Path | None = None,
    claude_settings_path: Path | None = None,
) -> DataForSEOCredentials | None:
    env_map = os.environ if env is None else env
    resolved_config_dir = Path(config_dir) if config_dir else get_config_dir(env_map)
    resolved_settings_path = (
        Path(claude_settings_path) if claude_settings_path else get_claude_settings_path(env_map)
    )

    config = _read_json_object(resolved_config_dir / CONFIG_FILENAME)
    settings = _read_json_object(resolved_settings_path)
    servers = settings.get("mcpServers", {}) if isinstance(settings, dict) else {}
    server = servers.get(CLAUDE_SERVER_NAME, {}) if isinstance(servers, dict) else {}
    server_env = server.get("env", {}) if isinstance(server, dict) else {}

    username, username_source = _first_present(
        [
            (config.get("username"), "config_file"),
            (env_map.get("DATAFORSEO_USERNAME"), "environment"),
            (server_env.get("DATAFORSEO_USERNAME"), "claude_settings"),
        ]
    )
    password, password_source = _first_present(
        [
            (config.get("password"), "config_file"),
            (env_map.get("DATAFORSEO_PASSWORD"), "environment"),
            (server_env.get("DATAFORSEO_PASSWORD"), "claude_settings"),
        ]
    )
    if not username or not password:
        return None
    source = username_source if username_source == password_source else "mixed"
    return DataForSEOCredentials(username=str(username), password=str(password), source=source)


def _account_status(
    credentials: DataForSEOCredentials,
    *,
    include_raw: bool,
    timeout: int,
    urlopen: Urlopen | None,
    config_status: dict,
) -> dict:
    response = _api_request(
        "GET",
        "/v3/appendix/user_data",
        credentials,
        timeout=timeout,
        urlopen=urlopen,
    )
    data = response["data"]
    result = _first_result(data)
    money = result.get("money", {}) if isinstance(result, dict) else {}
    summary = {
        "login_present": bool(result.get("login")) if isinstance(result, dict) else False,
        "balance": money.get("balance") if isinstance(money, dict) else None,
        "total_deposited": money.get("total") if isinstance(money, dict) else None,
    }
    return _live_payload(
        "user-data",
        None,
        "/v3/appendix/user_data",
        charged=False,
        credentials=credentials,
        config_status=config_status,
        request_payload=None,
        response=response,
        summary=summary,
        include_raw=include_raw,
    )


def _serp_live(
    credentials: DataForSEOCredentials,
    *,
    keyword: str,
    location_code: int,
    language_code: str,
    depth: int,
    device: str,
    limit: int,
    include_raw: bool,
    timeout: int,
    urlopen: Urlopen | None,
    config_status: dict,
) -> dict:
    endpoint = "/v3/serp/google/organic/live/advanced"
    request_payload = [
        {
            "keyword": keyword,
            "location_code": location_code,
            "language_code": language_code,
            "depth": depth,
            "device": device,
        }
    ]
    response = _api_request(
        "POST",
        endpoint,
        credentials,
        payload=request_payload,
        timeout=timeout,
        urlopen=urlopen,
    )
    summary = {"items": _serp_items(response["data"], limit=limit)}
    return _live_payload(
        "serp",
        keyword,
        endpoint,
        charged=True,
        credentials=credentials,
        config_status=config_status,
        request_payload=request_payload[0],
        response=response,
        summary=summary,
        include_raw=include_raw,
    )


def _related_keywords_live(
    credentials: DataForSEOCredentials,
    *,
    keyword: str,
    location_code: int,
    language_code: str,
    limit: int,
    include_raw: bool,
    timeout: int,
    urlopen: Urlopen | None,
    config_status: dict,
) -> dict:
    endpoint = "/v3/dataforseo_labs/google/related_keywords/live"
    request_payload = [
        {
            "keyword": keyword,
            "location_code": location_code,
            "language_code": language_code,
            "limit": limit,
        }
    ]
    response = _api_request(
        "POST",
        endpoint,
        credentials,
        payload=request_payload,
        timeout=timeout,
        urlopen=urlopen,
    )
    summary = {"keywords": _keyword_items(response["data"], limit=limit)}
    return _live_payload(
        "related-keywords",
        keyword,
        endpoint,
        charged=True,
        credentials=credentials,
        config_status=config_status,
        request_payload=request_payload[0],
        response=response,
        summary=summary,
        include_raw=include_raw,
    )


def _domain_rank_live(
    credentials: DataForSEOCredentials,
    *,
    target: str,
    location_code: int,
    language_code: str,
    include_raw: bool,
    timeout: int,
    urlopen: Urlopen | None,
    config_status: dict,
) -> dict:
    endpoint = "/v3/dataforseo_labs/google/domain_rank_overview/live"
    request_payload = [
        {
            "target": target,
            "location_code": location_code,
            "language_code": language_code,
        }
    ]
    response = _api_request(
        "POST",
        endpoint,
        credentials,
        payload=request_payload,
        timeout=timeout,
        urlopen=urlopen,
    )
    summary = {"domain": target, "metrics": _domain_metrics(response["data"])}
    return _live_payload(
        "domain-rank",
        target,
        endpoint,
        charged=True,
        credentials=credentials,
        config_status=config_status,
        request_payload=request_payload[0],
        response=response,
        summary=summary,
        include_raw=include_raw,
    )


def _api_request(
    method: str,
    path: str,
    credentials: DataForSEOCredentials,
    *,
    payload: list[dict] | None = None,
    timeout: int = 30,
    urlopen: Urlopen | None = None,
) -> dict:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    auth = base64.b64encode(f"{credentials.username}:{credentials.password}".encode("utf-8")).decode(
        "ascii"
    )
    req = request.Request(
        f"{API_BASE_URL}{path}",
        data=body,
        method=method,
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    opener = urlopen or request.urlopen
    try:
        with opener(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            http_status = getattr(response, "status", None)
            if http_status is None:
                http_status = response.getcode()
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        return {
            "ok": False,
            "http_status": exc.code,
            "error": f"HTTP {exc.code}",
            "data": _decode_json(raw),
        }
    except error.URLError as exc:
        return {
            "ok": False,
            "http_status": None,
            "error": str(exc.reason),
            "data": {},
        }

    data = _decode_json(raw)
    status_code = data.get("status_code") if isinstance(data, dict) else None
    return {
        "ok": http_status == 200 and status_code in {None, 20000},
        "http_status": http_status,
        "error": None if http_status == 200 else f"HTTP {http_status}",
        "data": data,
    }


def _live_payload(
    subcommand: str,
    target: str | None,
    endpoint: str,
    *,
    charged: bool,
    credentials: DataForSEOCredentials,
    config_status: dict,
    request_payload: dict | None,
    response: dict,
    summary: dict,
    include_raw: bool,
) -> dict:
    data = response["data"]
    status_code = data.get("status_code") if isinstance(data, dict) else None
    status_message = data.get("status_message") if isinstance(data, dict) else None
    payload = {
        "command": "dataforseo",
        "subcommand": subcommand,
        "target": target,
        "status": "ok" if response["ok"] else "error",
        "mode": "live",
        "message": _live_message(subcommand, response["ok"], charged),
        "configured": True,
        "credential_source": credentials.source,
        "charged": charged,
        "endpoint": endpoint,
        "request": request_payload,
        "http_status": response["http_status"],
        "api_status_code": status_code,
        "api_status_message": status_message,
        "cost": data.get("cost") if isinstance(data, dict) else None,
        "tasks_count": data.get("tasks_count") if isinstance(data, dict) else None,
        "tasks_error": data.get("tasks_error") if isinstance(data, dict) else None,
        "summary": summary,
        "config": config_status,
    }
    if response["error"]:
        payload["error"] = response["error"]
    if include_raw:
        payload["raw_response"] = _sanitize(response["data"])
    return payload


def _live_message(subcommand: str, ok: bool, charged: bool) -> str:
    charge_note = "该查询会按 DataForSEO 账户计费。" if charged else "该验证接口官方标注不收费。"
    if ok:
        return f"DataForSEO {subcommand} 真实 API 调用完成；{charge_note}"
    return f"DataForSEO {subcommand} 真实 API 调用失败；{charge_note}"


def _missing_target(subcommand: str, message: str) -> dict:
    return {
        "command": "dataforseo",
        "subcommand": subcommand,
        "target": None,
        "status": "参数错误",
        "mode": "invalid-arguments",
        "message": message,
        "configured": False,
        "charged": False,
    }


def _serp_items(data: dict, *, limit: int) -> list[dict]:
    items: list[dict] = []
    for result in _task_results(data):
        for item in result.get("items", []) if isinstance(result, dict) else []:
            if not isinstance(item, dict):
                continue
            items.append(
                {
                    "type": item.get("type"),
                    "rank_group": item.get("rank_group"),
                    "rank_absolute": item.get("rank_absolute"),
                    "domain": item.get("domain"),
                    "url": item.get("url"),
                    "title": item.get("title"),
                    "description": item.get("description"),
                }
            )
            if len(items) >= limit:
                return items
    return items


def _keyword_items(data: dict, *, limit: int) -> list[dict]:
    items: list[dict] = []
    for result in _task_results(data):
        for item in result.get("items", []) if isinstance(result, dict) else []:
            if not isinstance(item, dict):
                continue
            keyword_data = item.get("keyword_data", {})
            keyword_info = keyword_data.get("keyword_info", {}) if isinstance(keyword_data, dict) else {}
            items.append(
                {
                    "keyword": keyword_data.get("keyword") if isinstance(keyword_data, dict) else item.get("keyword"),
                    "location_code": keyword_data.get("location_code") if isinstance(keyword_data, dict) else None,
                    "language_code": keyword_data.get("language_code") if isinstance(keyword_data, dict) else None,
                    "search_volume": keyword_info.get("search_volume") if isinstance(keyword_info, dict) else None,
                    "competition": keyword_info.get("competition") if isinstance(keyword_info, dict) else None,
                    "cpc": keyword_info.get("cpc") if isinstance(keyword_info, dict) else None,
                    "related_keywords": item.get("related_keywords", [])[:5]
                    if isinstance(item.get("related_keywords"), list)
                    else [],
                }
            )
            if len(items) >= limit:
                return items
    return items


def _domain_metrics(data: dict) -> dict:
    for result in _task_results(data):
        for item in result.get("items", []) if isinstance(result, dict) else []:
            if not isinstance(item, dict):
                continue
            metrics = item.get("metrics", {})
            if isinstance(metrics, dict):
                return {
                    "organic": metrics.get("organic", {}),
                    "paid": metrics.get("paid", {}),
                }
    return {}


def _task_results(data: dict) -> list[dict]:
    tasks = data.get("tasks", []) if isinstance(data, dict) else []
    results: list[dict] = []
    for task in tasks if isinstance(tasks, list) else []:
        if not isinstance(task, dict):
            continue
        task_results = task.get("result", [])
        if isinstance(task_results, list):
            results.extend(item for item in task_results if isinstance(item, dict))
    return results


def _first_result(data: dict) -> dict:
    results = _task_results(data)
    if not results:
        return {}
    first = results[0]
    if isinstance(first, dict):
        return first
    return {}


def _normalize_domain(value: str) -> str:
    parsed = urlparse(value if "://" in value else f"https://{value}")
    return parsed.netloc or parsed.path


def _sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            if _should_redact_key(str(key)):
                redacted[str(key)] = "[redacted]"
            else:
                redacted[str(key)] = _sanitize(item)
        return redacted
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    return value


def _should_redact_key(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    return normalized in _REDACT_KEYS or normalized.endswith("_password")


def _decode_json(raw: str) -> dict:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}
    return data if isinstance(data, dict) else {"raw": data}


def _read_json_object(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _first_present(candidates: list[tuple[Any, str]]) -> tuple[Any | None, str | None]:
    for value, source in candidates:
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        return value, source
    return None, None
