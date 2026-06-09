from __future__ import annotations

from seo_agents.extract.schema import generate_schema, validate_schema


def test_generate_faq_schema() -> None:
    schema = generate_schema(
        "faq",
        {"questions": [{"question": "What is SEO?", "answer": "Search engine optimization."}]},
    )
    assert schema["@context"] == "https://schema.org"
    assert schema["@type"] == "FAQPage"
    assert schema["mainEntity"][0]["@type"] == "Question"


def test_validate_schema_missing_type_is_high() -> None:
    findings = validate_schema({"@context": "https://schema.org"})
    assert findings[0].severity == "High"
    assert "缺少 @type" in findings[0].title


def test_validate_schema_required_fields() -> None:
    findings = validate_schema({"@context": "https://schema.org", "@type": "Organization"})
    assert any(item.severity == "Medium" for item in findings)
    assert any("缺少" in item.title for item in findings)


def test_validate_faq_schema_warns_about_deprecated_google_value() -> None:
    schema = generate_schema("FAQPage", {"questions": []})
    findings = validate_schema(schema)
    assert any("FAQPage" in item.title for item in findings)
