"""Tests for the Review Engine rendering pipeline."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from featuresmith.core.profile_result import DatasetSummary
from featuresmith.review.render import (
    BaseRenderer,
    ConsoleRenderer,
    RendererRegistry,
    default_registry,
    render,
)
from featuresmith.review.schema import (
    ReviewCategory,
    ReviewResult,
    ReviewSection,
    Severity,
)


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


def make_result() -> ReviewResult:
    """Build a ReviewResult with one critical and one passed section."""
    from featuresmith.core.rule_finding import RuleFinding

    finding = RuleFinding(
        rule_id="review.test",
        rule_name="Test",
        category="quality",
        severity="critical",
        column_name="a",
        title="Critical issue",
        description="A critical description.",
        evidence={},
    )
    return ReviewResult(
        engine_version="0.1.0",
        dataset_summary=make_summary(),
        generated_at=datetime(2026, 8, 2, 12, 0, 0, tzinfo=UTC),
        sections=(
            ReviewSection(
                id="review.quality.a",
                title="Quality Section",
                category=ReviewCategory.QUALITY,
                severity=Severity.CRITICAL,
                findings=(finding,),
            ),
            ReviewSection(
                id="review.quality.b",
                title="Clean Section",
                category=ReviewCategory.QUALITY,
                severity=Severity.PASSED,
            ),
        ),
        overall_summary="1 of 2 sections passed with 1 finding(s) identified.",
    )


def test_console_renderer_name() -> None:
    """ConsoleRenderer identifies as 'console'."""
    assert ConsoleRenderer().name == "console"


def test_console_renderer_output_is_deterministic() -> None:
    """ConsoleRenderer emits stable plain text with severity ordering."""
    text = ConsoleRenderer().render(make_result())

    assert text.startswith("Featuresmith Dataset Review")
    assert "Rows: 10 | Columns: 2" in text
    assert "[CRITICAL] Quality Section (review.quality.a)" in text
    assert "  - Critical issue [a]" in text
    assert "      A critical description." in text
    assert "[PASSED] Clean Section (review.quality.b)" in text
    assert "  No issues found." in text

    assert text == ConsoleRenderer().render(make_result())


def test_render_default_target_is_console() -> None:
    """render() dispatches to the console renderer by default."""
    text = render(make_result())

    assert text.startswith("Featuresmith Dataset Review")


def test_render_unknown_target_raises() -> None:
    """render() raises for an unregistered target."""
    with pytest.raises(ValueError, match="Unknown renderer"):
        render(make_result(), target="html")


def test_renderer_registry_register_and_render() -> None:
    """RendererRegistry registers and dispatches renderers by name."""
    registry = RendererRegistry((ConsoleRenderer(),))
    text = registry.render("console", make_result())

    assert text.startswith("Featuresmith Dataset Review")
    assert registry.get("console") is not None
    assert registry.get("html") is None


def test_renderer_registry_unknown_raises() -> None:
    """RendererRegistry.render raises for an unknown renderer."""
    registry = RendererRegistry()
    with pytest.raises(ValueError, match="Unknown renderer"):
        registry.render("console", make_result())


def test_default_registry_ships_console_only() -> None:
    """The default renderer registry ships the console renderer only."""
    registry = default_registry()

    assert registry.get("console") is not None
    assert registry.get("dashboard") is None
    assert registry.get("html") is None
    assert registry.get("json") is None


def test_base_renderer_is_abstract() -> None:
    """BaseRenderer cannot be instantiated directly."""
    with pytest.raises(TypeError):
        BaseRenderer()  # type: ignore[abstract]


def make_scored_result() -> ReviewResult:
    """Build a ReviewResult with an attached ML Readiness Score."""
    from featuresmith.core.rule_finding import RuleFinding
    from featuresmith.review.scoring_adapter import ScoreAdapter

    finding = RuleFinding(
        rule_id="review.quality.missingness",
        rule_name="Missing Values",
        category="quality",
        severity="warning",
        column_name="age",
        title="High missing values in column 'age'",
        description="40% of values are missing.",
        evidence={"missing_percentage": 40.0},
    )
    result = ReviewResult(
        engine_version="0.1.0",
        dataset_summary=make_summary(),
        generated_at=datetime(2026, 8, 2, 12, 0, 0, tzinfo=UTC),
        sections=(
            ReviewSection(
                id="review.quality.missingness",
                title="Missing Values",
                category=ReviewCategory.QUALITY,
                severity=Severity.WARNING,
                findings=(finding,),
            ),
            ReviewSection(
                id="review.quality.duplicates",
                title="Duplicate Rows",
                category=ReviewCategory.QUALITY,
                severity=Severity.PASSED,
            ),
        ),
        overall_summary="1 of 2 sections passed with 1 finding(s) identified.",
    )
    return ScoreAdapter().attach(result)


def test_console_renderer_includes_score_section() -> None:
    """ConsoleRenderer pairs the overall score with its full breakdown."""
    text = ConsoleRenderer().render(make_scored_result())

    assert "ML Readiness Score (scoring v0.3.0)" in text
    assert "Overall: 92.5/100" in text
    assert "  Missing Values: 85/100 (1 finding(s))" in text
    assert "  Data Quality: 100/100" in text
    assert "Summary: Overall ML Readiness is 92.5/100 across 2 dimension(s);" in text
    assert "What would improve this score:" in text
    assert (
        "Address the flagged issue: High missing values in column 'age' (in column 'age')."
        in text
    )
    assert "Healthy dimensions:" in text
    assert "  + Data Quality scored 100/100 with no issues found." in text


def test_console_renderer_score_is_deterministic() -> None:
    """The rendered score block is stable across repeated renders."""
    result = make_scored_result()

    assert ConsoleRenderer().render(result) == ConsoleRenderer().render(result)


def test_console_renderer_omits_score_when_absent() -> None:
    """A result without a score renders without a score section."""
    text = ConsoleRenderer().render(make_result())

    assert "ML Readiness Score" not in text
