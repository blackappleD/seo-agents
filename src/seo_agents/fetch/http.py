from __future__ import annotations

import re
import urllib.error
import urllib.request

from seo_agents.models import FetchResult
from seo_agents.security.url_safety import (
    URLSafetyError,
    resolve_redirect_url,
    validate_url_strict,
)

DEFAULT_USER_AGENT = "seo-agents/0.1 (+https://github.com/seo-agents; SEO crawler)"
REDIRECT_STATUSES = {301, 302, 303, 307, 308}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        return None


def fetch_url(
    url: str,
    *,
    method: str = "GET",
    timeout: int = 15,
    max_redirects: int = 3,
    user_agent: str = DEFAULT_USER_AGENT,
    max_bytes: int = 2_000_000,
) -> FetchResult:
    byte_result = fetch_bytes(
        url,
        method=method,
        timeout=timeout,
        max_redirects=max_redirects,
        user_agent=user_agent,
        max_bytes=max_bytes,
    )
    content = None
    if byte_result["content"] is not None:
        content = decode_response_bytes(byte_result["content"], byte_result["headers"])
    return FetchResult(
        url=url,
        final_url=byte_result["final_url"],
        status_code=byte_result["status_code"],
        headers=byte_result["headers"],
        content=content,
        redirect_chain=byte_result["redirect_chain"],
        error=byte_result["error"],
    )


def fetch_bytes(
    url: str,
    *,
    method: str = "GET",
    timeout: int = 15,
    max_redirects: int = 3,
    user_agent: str = DEFAULT_USER_AGENT,
    max_bytes: int = 5_000_000,
) -> dict:
    redirect_chain: list[dict] = []
    try:
        current_url, _ = validate_url_strict(url)
        opener = urllib.request.build_opener(_NoRedirect)

        for redirect_index in range(max_redirects + 1):
            request = urllib.request.Request(
                current_url,
                method=method.upper(),
                headers={
                    "User-Agent": user_agent,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                },
            )
            try:
                with opener.open(request, timeout=timeout) as response:
                    headers = dict(response.headers.items())
                    content = response.read(max_bytes + 1) if method.upper() != "HEAD" else b""
                    if len(content) > max_bytes:
                        return _byte_result(
                            url,
                            current_url,
                            response.status,
                            headers,
                            content[:max_bytes],
                            redirect_chain,
                            f"Response exceeded max_bytes={max_bytes}",
                        )
                    return _byte_result(
                        url,
                        current_url,
                        response.status,
                        headers,
                        content,
                        redirect_chain,
                        None,
                    )
            except urllib.error.HTTPError as exc:
                headers = dict(exc.headers.items())
                if exc.code in REDIRECT_STATUSES:
                    location = headers.get("Location")
                    if redirect_index >= max_redirects:
                        return _byte_result(
                            url,
                            current_url,
                            exc.code,
                            headers,
                            None,
                            redirect_chain,
                            f"在 {current_url} 超过 redirect 限制",
                        )
                    next_url = validate_url_strict(resolve_redirect_url(current_url, location or ""))[0]
                    redirect_chain.append(
                        {
                            "from": current_url,
                            "to": next_url,
                            "status_code": exc.code,
                        }
                    )
                    current_url = next_url
                    continue
                body = exc.read(max_bytes) if method.upper() != "HEAD" else b""
                return _byte_result(url, current_url, exc.code, headers, body, redirect_chain, None)

        return _byte_result(
            url,
            current_url,
            None,
            {},
            None,
            redirect_chain,
            f"超过 redirect 限制：{url}",
        )
    except (URLSafetyError, urllib.error.URLError, TimeoutError, OSError) as exc:
        return _byte_result(url, url, None, {}, None, redirect_chain, str(exc))


def _byte_result(
    url: str,
    final_url: str,
    status_code: int | None,
    headers: dict[str, str],
    content: bytes | None,
    redirect_chain: list[dict],
    error: str | None,
) -> dict:
    return {
        "url": url,
        "final_url": final_url,
        "status_code": status_code,
        "headers": headers,
        "content": content,
        "redirect_chain": redirect_chain,
        "error": error,
    }


def decode_response_bytes(content: bytes, headers: dict[str, str]) -> str:
    charset = _charset_from_content_type(headers.get("Content-Type") or headers.get("content-type") or "")
    if not charset:
        sample = content[:4096].decode("ascii", errors="ignore")
        charset = _charset_from_meta(sample)
    for candidate in [charset, "utf-8", "windows-1252"]:
        if not candidate:
            continue
        try:
            return content.decode(candidate, errors="replace")
        except LookupError:
            continue
    return content.decode("utf-8", errors="replace")


def _charset_from_content_type(content_type: str) -> str | None:
    match = re.search(r"charset\s*=\s*['\"]?([^;\s'\"]+)", content_type, re.I)
    return match.group(1).strip() if match else None


def _charset_from_meta(html_sample: str) -> str | None:
    match = re.search(r"<meta[^>]+charset=['\"]?([^'\"\s/>]+)", html_sample, re.I)
    if match:
        return match.group(1).strip()
    match = re.search(
        r"<meta[^>]+http-equiv=['\"]content-type['\"][^>]+content=['\"][^'\"]*charset=([^'\";]+)",
        html_sample,
        re.I,
    )
    return match.group(1).strip() if match else None
