"""Tests for the Review Engine serializable schemas."""

from __future__ import annotations

import json
from datetime import UTC, datetime

from featuresmith.core.profile_result import DatasetSummary
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.review.schema import (
    ReviewCategory,
    ReviewResult,
    ReviewSection,
    Severity,
)


def make_finding(severity: str = "info") -> RuleFinding:
    """Build a minimal RuleFinding for schema tests."""
    return RuleFinding(
        rule_id="review.test",
        rule_name="Test Rule",
        category="quality",
        severity=severity,
        column_name=None,
        title="Test finding",
        description="A synthetic finding.",
        evidence={},
    )


def make_summary() -> DatasetSummary:
    """Build a minimal DatasetSummary for schema tests."""
    return DatasetSummary(
        row_count=10,
        column_count=2,
        size_in_bytes=None,
        missing_percentage=0.0,
        duplicate_percentage=0.0,
        num_numeric_columns=2,
        num_categorical_columns=0,
        num_datetime_columns=0,
        num_text_columns=0,
        num_constant_columns=0,
        num_fully_empty_columns=0,
    )


def test_severity_values_and_rank() -> None:
    """Severity values follow the shared lowercase vocabulary and order."""
    assert Severity.CRITICAL.value == "critical"
    assert Severity.WARNING.value == "warning"
    assert Severity.INFO.value == "info"
    assert Severity.PASSED.value == "passed"

    assert Severity.PASSED.rank < Severity.INFO.rank
    assert Severity.INFO.rank < Severity.WARNING.rank
    assert Severity.WARNING.rank < Severity.CRITICAL.rank


def test_review_category_values() -> None:
    """ReviewCategory matches the architecture's reviewer categories."""
    values = {category.value for category in ReviewCategory}
    assert values == {
        "schema",
        "quality",
        "leakage",
        "diff",
        "feature_quality",
        "custom",
    }


def test_review_section_freezes_sequences() -> None:
    """ReviewSection is frozen and sequence fields become tuples."""
    section = ReviewSection(
        id="review.quality.test",
        title="Test Section",
        category=ReviewCategory.QUALITY,
        severity=Severity.INFO,
        findings=[make_finding()],
        recommendations=[],
    )

    assert isinstance(section.findings, tuple)
    assert isinstance(section.recommendations, tuple)
    assert section.findings[0].title == "Test finding"


def test_review_section_to_dict_serializes_enum() -> None:
    """ReviewSection.to_dict() converts enums to their string values."""
    section = ReviewSection(
        id="review.quality.test",
        title="Test Section",
        category=ReviewCategory.QUALITY,
        severity=Severity.WARNING,
        findings=(make_finding("warning"),),
    )

    data = section.to_dict()
    assert data["category"] == "quality"
    assert data["severity"] == "warning"
    assert data["findings"][0]["title"] == "Test finding"

    json.dumps(data)


def test_review_result_to_dict_serializes_datetime_and_enums() -> None:
    """ReviewResult.to_dict() is fully JSON-serializable."""
    generated_at = datetime(2026, 8, 2, 12, 0, 0, tzinfo=UTC)
    result = ReviewResult(
        engine_version="0.1.0",
        dataset_summary=make_summary(),
        generated_at=generated_at,
        sections=(
            ReviewSection(
                id="review.quality.test",
                title="Test Section",
                category=ReviewCategory.QUALITY,
                severity=Severity.INFO,
                findings=(make_finding(),),
            ),
        ),
        overall_summary="1 of 1 sections passed with 1 finding(s) identified.",
    )

    data = result.to_dict()
    assert data["engine_version"] == "0.1.0"
    assert data["generated_at"] == "2026-08-02T12:00:00+00:00"
    assert data["sections"][0]["severity"] == "info"
    assert data["dataset_summary"]["row_count"] == 10
    assert data["score"] is None
    assert data["diff"] is None

    json.dumps(data)


def test_review_result_freezes_sections() -> None:
    """ReviewResult converts sections to an immutable tuple."""
    result = ReviewResult(
        engine_version="0.1.0",
        dataset_summary=make_summary(),
        generated_at=datetime.now(UTC),
        sections=[
            ReviewSection(
                id="x",
                title="X",
                category=ReviewCategory.CUSTOM,
                severity=Severity.PASSED,
            )
        ],
    )

    assert isinstance(result.sections, tuple)
