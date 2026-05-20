from __future__ import annotations

WEIGHTS = {
    "Technical SEO": 0.22,
    "Content Quality": 0.23,
    "On-Page SEO": 0.20,
    "Schema / Structured Data": 0.10,
    "Performance / CWV": 0.10,
    "AI Search Readiness": 0.10,
    "Images": 0.05,
}

SEVERITY_PENALTIES = {
    "Critical": 40,
    "High": 24,
    "Medium": 12,
    "Low": 5,
    "Info": 0,
}


def score_findings(findings: list[dict]) -> int:
    penalty = sum(SEVERITY_PENALTIES.get(item.get("severity"), 0) for item in findings)
    return max(0, min(100, 100 - penalty))


def weighted_health_score(categories: list[dict]) -> int:
    by_name = {category["name"]: category for category in categories}
    total = 0.0
    for name, weight in WEIGHTS.items():
        total += by_name.get(name, {"score": 100})["score"] * weight
    return round(total)
