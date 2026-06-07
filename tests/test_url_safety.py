from __future__ import annotations

import socket

import pytest

from seo_agents.security.url_safety import URLSafetyError, validate_url, validate_url_strict


def install_public_dns(monkeypatch: pytest.MonkeyPatch, address: str = "93.184.216.34") -> None:
    def fake_getaddrinfo(host, port, *args, **kwargs):  # type: ignore[no-untyped-def]
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (address, 443))]

    monkeypatch.setattr(socket, "getaddrinfo", fake_getaddrinfo)


def test_validate_public_url_normalizes_hostname(monkeypatch: pytest.MonkeyPatch) -> None:
    install_public_dns(monkeypatch)
    normalized, host = validate_url_strict("HTTPS://Example.COM/path?q=1#frag")
    assert normalized == "https://example.com/path?q=1"
    assert host == "example.com"


@pytest.mark.parametrize(
    "url",
    [
        "ftp://example.com",
        "http://",
        "http://localhost",
        "http://127.0.0.1",
        "http://2130706433",
        "http://0x7f000001",
        "http://0177.0.0.1",
        "http://127.1",
        "https://metadata.google.internal.",
        "https://user:pass@example.com",
        "https://example.com\\@127.0.0.1/",
        "https://example.com%5c@127.0.0.1/",
    ],
)
def test_validate_rejects_unsafe_urls(url: str) -> None:
    with pytest.raises(URLSafetyError):
        validate_url_strict(url)
    assert validate_url(url) is False


def test_dns_resolution_to_private_ip_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    install_public_dns(monkeypatch, "10.0.0.5")
    with pytest.raises(URLSafetyError):
        validate_url_strict("https://example.com")


def test_dns_resolution_failure_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_getaddrinfo(host, port, *args, **kwargs):  # type: ignore[no-untyped-def]
        raise socket.gaierror("nope")

    monkeypatch.setattr(socket, "getaddrinfo", fake_getaddrinfo)
    with pytest.raises(URLSafetyError):
        validate_url_strict("https://example.com")
