from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any, Literal

Severity = Literal["Critical", "High", "Medium", "Low", "Info"]
FindingStatus = Literal["pass", "warn", "fail"]


@dataclass
class Finding:
    title: str
    severity: Severity
    category: str
    description: str
    recommendation: str
    evidence: dict[str, Any] = field(default_factory=dict)
    affected_urls: list[str] = field(default_factory=list)
    effort: str | None = None
    impact: str | None = None


@dataclass
class FetchResult:
    url: str
    final_url: str
    status_code: int | None
    headers: dict[str, str]
    content: str | None
    redirect_chain: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None


@dataclass
class PageSnapshot:
    url: str
    final_url: str
    status_code: int | None
    raw_html: str | None
    rendered_html: str | None
    is_spa: bool
    extracted_text: str | None
    headers: dict[str, str]
    console_errors: list[str] = field(default_factory=list)
    redirect_chain: list[dict[str, Any]] = field(default_factory=list)
    render_engine: str = "raw"
    render_ms: int | None = None
    mode_used: str = "raw"
    error: str | None = None


@dataclass
class ParsedPage:
    title: str | None = None
    meta_description: str | None = None
    meta_robots: str | None = None
    canonical: str | None = None
    h1: list[str] = field(default_factory=list)
    h2: list[str] = field(default_factory=list)
    h3: list[str] = field(default_factory=list)
    images: list[dict[str, Any]] = field(default_factory=list)
    links: dict[str, list[dict[str, Any]]] = field(
        default_factory=lambda: {"internal": [], "external": []}
    )
    schema: list[dict[str, Any]] = field(default_factory=list)
    open_graph: dict[str, str] = field(default_factory=dict)
    twitter_card: dict[str, str] = field(default_factory=dict)
    word_count: int = 0
    hreflang: list[dict[str, str]] = field(default_factory=list)
    viewport: str | None = None
    text: str = ""


@dataclass
class AuditCategory:
    name: str
    score: int
    findings: list[Finding]
    what_works: list[str] = field(default_factory=list)
    status: FindingStatus | None = None


@dataclass
class AuditReport:
    target: str
    health_score: int
    business_type: str
    categories: list[AuditCategory]
    top_findings: list[Finding]
    quick_wins: list[Finding]
    pages_analyzed: list[str] = field(default_factory=list)
    artifacts: dict[str, str] = field(default_factory=dict)


def to_plain(value: Any) -> Any:
    if is_dataclass(value):
        return {key: to_plain(item) for key, item in asdict(value).items()}
    if isinstance(value, list):
        return [to_plain(item) for item in value]
    if isinstance(value, dict):
        return {str(key): to_plain(item) for key, item in value.items()}
    return value


def finding(
    title: str,
    severity: Severity,
    category: str,
    description: str,
    recommendation: str,
    *,
    evidence: dict[str, Any] | None = None,
    affected_urls: list[str] | None = None,
    effort: str | None = None,
    impact: str | None = None,
) -> Finding:
    return Finding(
        title=title,
        severity=severity,
        category=category,
        description=description,
        recommendation=recommendation,
        evidence=evidence or {},
        affected_urls=affected_urls or [],
        effort=effort,
        impact=impact,
    )


def severity_weight(severity: str) -> int:
    return {
        "Critical": 40,
        "High": 24,
        "Medium": 12,
        "Low": 5,
        "Info": 0,
    }.get(severity, 0)


def score_from_findings(findings: list[Finding], base: int = 100) -> int:
    penalty = sum(severity_weight(item.severity) for item in findings)
    return max(0, min(100, base - penalty))
