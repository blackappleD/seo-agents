from __future__ import annotations

import ipaddress
import socket
from contextlib import contextmanager
from typing import Any, Iterator
from urllib.parse import unquote, urljoin, urlparse, urlunparse


class URLSafetyError(ValueError):
    """当 URL 违反公网抓取边界时抛出。"""


METADATA_HOSTS = {
    "metadata.google.internal",
    "metadata",
    "169.254.169.254",
    "100.100.100.200",
}

BLOCKED_SUFFIXES = (
    ".localhost",
    ".local",
    ".internal",
)

ALLOWED_SCHEMES = {"http", "https"}


def validate_url(url: str) -> bool:
    try:
        validate_url_strict(url)
        return True
    except URLSafetyError:
        return False


def validate_url_strict(url: str, *, resolve: bool = True) -> tuple[str, str]:
    if not isinstance(url, str) or not url.strip():
        raise URLSafetyError("URL 必须是非空字符串")

    raw_url = url.strip()
    decoded_url = unquote(raw_url)
    if "\\" in raw_url or "\\" in decoded_url:
        raise URLSafetyError("URL 不能包含反斜杠")

    parsed = urlparse(raw_url)
    scheme = parsed.scheme.lower()
    if scheme not in ALLOWED_SCHEMES:
        raise URLSafetyError("只允许 http 和 https URL")
    if not parsed.netloc:
        raise URLSafetyError("URL 必须包含 host")
    if parsed.username or parsed.password or "@" in parsed.netloc:
        raise URLSafetyError("URL authority 不能包含 userinfo")
    if "%" in parsed.netloc:
        raise URLSafetyError("URL authority 不能包含 percent-encoding")

    try:
        port = parsed.port
    except ValueError as exc:
        raise URLSafetyError("URL 包含无效端口") from exc

    hostname = _normalize_hostname(parsed.hostname)
    _reject_blocked_hostname(hostname)
    parsed_ip = _parse_any_ip(hostname)
    if parsed_ip is not None:
        _ensure_public_ip(parsed_ip)
    elif resolve:
        for resolved in _resolve_hostname(hostname):
            _ensure_public_ip(resolved)

    netloc = _format_netloc(hostname, port)
    normalized = urlunparse(
        (
            scheme,
            netloc,
            parsed.path or "/",
            parsed.params,
            parsed.query,
            "",
        )
    )
    return normalized, hostname


def resolve_redirect_url(base_url: str, location: str) -> str:
    if not location:
        raise URLSafetyError("Redirect location 为空")
    return urljoin(base_url, location)


def _normalize_hostname(hostname: str | None) -> str:
    if hostname is None or not hostname.strip():
        raise URLSafetyError("URL host 为空")
    host = hostname.strip().rstrip(".").lower()
    if not host:
        raise URLSafetyError("URL host 为空")
    try:
        host = host.encode("idna").decode("ascii")
    except UnicodeError as exc:
        raise URLSafetyError("URL host 不是有效 IDNA") from exc
    return host


def _reject_blocked_hostname(hostname: str) -> None:
    if hostname in {"localhost", *METADATA_HOSTS}:
        raise URLSafetyError("不允许 localhost 和 metadata host")
    if hostname.endswith(BLOCKED_SUFFIXES):
        raise URLSafetyError("不允许 local 或 internal hostname")


def _parse_any_ip(hostname: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address | None:
    try:
        return ipaddress.ip_address(hostname)
    except ValueError:
        pass
    return _parse_ambiguous_ipv4(hostname)


def _parse_ambiguous_ipv4(hostname: str) -> ipaddress.IPv4Address | None:
    if ":" in hostname:
        return None
    parts = hostname.split(".")
    if not 1 <= len(parts) <= 4:
        return None
    values: list[int] = []
    for part in parts:
        if not part:
            return None
        base = 10
        digits = part
        if part.lower().startswith("0x"):
            base = 16
            digits = part[2:]
        elif len(part) > 1 and part.startswith("0") and part.isdigit():
            base = 8
            digits = part[1:] or "0"
        elif not part.isdigit():
            return None
        try:
            values.append(int(digits, base))
        except ValueError:
            return None

    try:
        if len(values) == 1:
            if values[0] > 0xFFFFFFFF:
                return None
            packed = values[0]
        elif len(values) == 2:
            if values[0] > 0xFF or values[1] > 0xFFFFFF:
                return None
            packed = (values[0] << 24) | values[1]
        elif len(values) == 3:
            if values[0] > 0xFF or values[1] > 0xFF or values[2] > 0xFFFF:
                return None
            packed = (values[0] << 24) | (values[1] << 16) | values[2]
        else:
            if any(value > 0xFF for value in values):
                return None
            packed = (
                (values[0] << 24)
                | (values[1] << 16)
                | (values[2] << 8)
                | values[3]
            )
        return ipaddress.IPv4Address(packed)
    except ipaddress.AddressValueError:
        return None


def _ensure_public_ip(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> None:
    if not ip.is_global:
        raise URLSafetyError(f"解析地址不是公网地址：{ip}")
    if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
        raise URLSafetyError(f"解析地址不允许访问：{ip}")


def _resolve_hostname(hostname: str) -> list[ipaddress.IPv4Address | ipaddress.IPv6Address]:
    try:
        infos = socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise URLSafetyError(f"DNS 解析失败：{hostname}") from exc

    addresses: list[ipaddress.IPv4Address | ipaddress.IPv6Address] = []
    seen: set[str] = set()
    for info in infos:
        sockaddr = info[4]
        if not sockaddr:
            continue
        address = sockaddr[0]
        if address in seen:
            continue
        seen.add(address)
        try:
            addresses.append(ipaddress.ip_address(address))
        except ValueError as exc:
            raise URLSafetyError(f"DNS 返回无效地址：{address}") from exc
    if not addresses:
        raise URLSafetyError(f"DNS 解析未返回地址：{hostname}")
    return addresses


def _format_netloc(hostname: str, port: int | None) -> str:
    host = f"[{hostname}]" if ":" in hostname and not hostname.startswith("[") else hostname
    if port is None:
        return host
    return f"{host}:{port}"


@contextmanager
def safe_requests_session(url: str) -> Iterator[Any]:
    validate_url_strict(url)
    try:
        import requests
    except ImportError as exc:  # pragma: no cover - depends on optional package state
        raise RuntimeError("safe_requests_session 需要安装 requests") from exc

    class SafeSession(requests.Session):  # type: ignore[misc]
        def request(self, method: str, request_url: str, **kwargs: Any) -> Any:
            validate_url_strict(request_url)
            kwargs.setdefault("allow_redirects", False)
            return super().request(method, request_url, **kwargs)

    session = SafeSession()
    try:
        yield session
    finally:
        session.close()


def safe_requests_get(url: str, **kwargs: Any) -> Any:
    return _safe_requests_request("GET", url, **kwargs)


def safe_requests_head(url: str, **kwargs: Any) -> Any:
    return _safe_requests_request("HEAD", url, **kwargs)


def _safe_requests_request(method: str, url: str, **kwargs: Any) -> Any:
    try:
        import requests
    except ImportError as exc:  # pragma: no cover - depends on optional package state
        raise RuntimeError("safe_requests_get/head 需要安装 requests") from exc

    timeout = kwargs.pop("timeout", 15)
    max_redirects = int(kwargs.pop("max_redirects", 3))
    headers = kwargs.pop("headers", {})
    current_url, _ = validate_url_strict(url)
    response = None
    for _ in range(max_redirects + 1):
        response = requests.request(
            method,
            current_url,
            timeout=timeout,
            headers=headers,
            allow_redirects=False,
            **kwargs,
        )
        if response.status_code not in {301, 302, 303, 307, 308}:
            return response
        location = response.headers.get("Location")
        current_url, _ = validate_url_strict(resolve_redirect_url(current_url, location or ""))
    raise URLSafetyError(f"超过 redirect 限制：{url}")


def make_safe_playwright_route_handler(blocked_resource_types: set[str] | None = None) -> Any:
    blocked = blocked_resource_types or set()

    async def handler(route: Any, request: Any) -> None:
        if request.resource_type in blocked:
            await route.abort()
            return
        try:
            validate_url_strict(request.url)
        except URLSafetyError:
            await route.abort()
            return
        await route.continue_()

    return handler
