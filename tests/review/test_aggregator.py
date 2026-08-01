"""Tests for the ResultAggregator."""

from __future__ import annotations

from datetime import UTC, datetime

from featuresmith.core.profile_result import DatasetSummary
from featuresmith.review.aggregator import ResultAggregator
from featuresmith.review.schema import ReviewCategory, ReviewSection, Severity


def make_summary() -> DatasetSummary:
    """Build a minimal DatasetSummary."""
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


def make_section(
    section_id: str, severity: Severity, findings: int = 0
) -> ReviewSection:
    """Build a ReviewSection with an optional finding count."""
    from featuresmith.core.rule_finding import RuleFinding

    findings_tuple = tuple(
        RuleFinding(
            rule_id="review.test",
            rule_name="Test",
            category="quality",
            severity=severity.value,
            column_name=None,
            title=f"Finding {index}",
            description="A synthetic finding.",
            evidence={},
        )
        for index in range(findings)
    )
    return ReviewSection(
        id=section_id,
        title=section_id,
        category=ReviewCategory.QUALITY,
        severity=severity,
        findings=findings_tuple,
    )


def test_aggregate_empty_sections() -> None:
    """Aggregating no sections yields a complete, empty review."""
    result = ResultAggregator().aggregate(
        engine_version="0.1.0",
        dataset_summary=make_summary(),
        sections=[],
    )

    assert result.sections == ()
    assert result.overall_summary == "Review complete: no reviewers ran."
    assert result.engine_version == "0.1.0"
    assert isinstance(result.generated_at, datetime)


def test_aggregate_sorts_sections_by_severity() -> None:
    """Sections are sorted most-severe-first."""
    aggregator = ResultAggregator()
    result = aggregator.aggregate(
        engine_version="0.1.0",
        dataset_summary=make_summary(),
        sections=(
            make_section("a", Severity.INFO),
            make_section("b", Severity.CRITICAL),
            make_section("c", Severity.PASSED),
            make_section("d", Severity.WARNING),
        ),
    )

    assert [section.severity for section in result.sections] == [
        Severity.CRITICAL,
        Severity.WARNING,
        Severity.INFO,
        Severity.PASSED,
    ]


def test_aggregate_overall_summary_is_templated() -> None:
    """The overall summary counts passed sections and findings."""
    result = ResultAggregator().aggregate(
        engine_version="0.1.0",
        dataset_summary=make_summary(),
        sections=(
            make_section("passed-a", Severity.PASSED),
            make_section("info-b", Severity.INFO, findings=2),
        ),
    )

    assert result.overall_summary == (
        "1 of 2 sections passed with 2 finding(s) identified across the review."
    )


def test_aggregate_includes_failed_reviewer_warning() -> None:
    """Failed reviewers surface as a warning in the overall summary."""
    result = ResultAggregator().aggregate(
        engine_version="0.1.0",
        dataset_summary=make_summary(),
        sections=(make_section("a", Severity.PASSED),),
        failed_reviewers={"review.quality.broken": "boom"},
    )

    assert result.overall_summary.endswith("1 reviewer(s) failed and were skipped.")


def test_aggregate_freezes_sections_and_accepts_generated_at() -> None:
    """Sections are frozen and a caller-supplied timestamp is honored."""
    generated_at = datetime(2026, 8, 2, 12, 0, 0, tzinfo=UTC)
    result = ResultAggregator().aggregate(
        engine_version="0.1.0",
        dataset_summary=make_summary(),
        sections=[make_section("a", Severity.INFO)],
        generated_at=generated_at,
    )

    assert isinstance(result.sections, tuple)
    assert result.generated_at == generated_at
