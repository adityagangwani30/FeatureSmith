"""Tests for the Plan primitive: compiler, rendering, and SDK integration."""

from __future__ import annotations

import json
from datetime import UTC, datetime

import pandas as pd
import pytest

import featuresmith as fs
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.plan import (
    PLAN_SCHEMA_VERSION,
    Plan,
    PlanItem,
    compile_plan,
    compile_plan_from_recommendations,
)
from featuresmith.recommendation.schema import Recommendation
from featuresmith.review.render import PlanRenderer, render
from featuresmith.review.schema import (
    ReviewResult,
)


def make_recommendation(
    rec_id: str,
    *,
    title: str = "Test recommendation",
    rationale: str = "Test rationale",
    confidence: float = 0.8,
    severity: str = "warning",
    affected_columns: tuple[str, ...] = ("col1",),
    suggested_action: str = "Test action",
    originating_findings: tuple[RuleFinding, ...] = (),
    originating_reviewers: tuple[str, ...] = ("review.quality.test",),
) -> Recommendation:
    """Create a test Recommendation."""
    finding = RuleFinding(
        rule_id="quality.test",
        rule_name="Test Rule",
        category="quality",
        severity=severity,
        column_name="col1",
        title="Test finding",
        description="Test finding description",
        evidence={},
        confidence=confidence,
    )
    return Recommendation(
        id=rec_id,
        title=title,
        rationale=rationale,
        confidence=confidence,
        severity=severity,
        affected_columns=affected_columns,
        suggested_action=suggested_action,
        originating_findings=originating_findings or (finding,),
        originating_reviewers=originating_reviewers,
    )


def make_review_result_with_recommendations(
    *recs: Recommendation,
) -> ReviewResult:
    """Create a ReviewResult with the given recommendations."""
    summary = fs.core.profile_result.DatasetSummary(
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
    return ReviewResult(
        engine_version="0.4.0",
        dataset_summary=summary,
        generated_at=datetime(2026, 8, 17, 12, 0, 0, tzinfo=UTC),
        sections=(),
        overall_summary="Test review.",
        recommendations=recs,
    )


def test_compile_plan_deterministic() -> None:
    """Same accepted IDs always produce the same Plan (excluding timestamps)."""
    rec1 = make_recommendation("rec.quality.missingness.col1")
    rec2 = make_recommendation("rec.quality.duplicates.col2")
    result = make_review_result_with_recommendations(rec1, rec2)

    plan1 = compile_plan(
        result, ["rec.quality.missingness.col1", "rec.quality.duplicates.col2"]
    )
    plan2 = compile_plan(
        result, ["rec.quality.missingness.col1", "rec.quality.duplicates.col2"]
    )

    # Compare all fields except generated_at (which is not in Plan)
    assert plan1.plan_schema_version == plan2.plan_schema_version
    assert plan1.accepted_recommendation_ids == plan2.accepted_recommendation_ids
    assert len(plan1.items) == len(plan2.items)
    for item1, item2 in zip(plan1.items, plan2.items, strict=True):
        assert item1.id == item2.id
        assert item1.recommendation_id == item2.recommendation_id
        assert item1.title == item2.title
        assert item1.rationale == item2.rationale
        assert item1.confidence == item2.confidence
        assert item1.severity == item2.severity
        assert item1.affected_columns == item2.affected_columns
        assert item1.suggested_action == item2.suggested_action
        assert item1.originating_findings == item2.originating_findings
        assert item1.originating_reviewers == item2.originating_reviewers


def test_compile_plan_item_ids_are_deterministic() -> None:
    """Plan item IDs follow the deterministic pattern plan.{rec_id}.{idx}."""
    rec1 = make_recommendation("rec.quality.missingness.col1")
    rec2 = make_recommendation("rec.quality.duplicates.col2")
    result = make_review_result_with_recommendations(rec1, rec2)

    plan = compile_plan(
        result, ["rec.quality.missingness.col1", "rec.quality.duplicates.col2"]
    )

    assert plan.items[0].id == "plan.rec.quality.missingness.col1.0"
    assert plan.items[1].id == "plan.rec.quality.duplicates.col2.1"


def test_compile_plan_validates_accepted_ids() -> None:
    """Unknown accepted IDs raise ValueError listing available IDs."""
    rec1 = make_recommendation("rec.quality.missingness.col1")
    result = make_review_result_with_recommendations(rec1)

    with pytest.raises(ValueError, match="Unknown recommendation ID"):
        compile_plan(result, ["rec.bogus.id"])

    with pytest.raises(ValueError, match="Available:"):
        compile_plan(result, ["rec.bogus.id"])


def test_compile_plan_empty_accept() -> None:
    """Empty accept list produces an empty plan."""
    rec1 = make_recommendation("rec.quality.missingness.col1")
    result = make_review_result_with_recommendations(rec1)

    plan = compile_plan(result, [])

    assert plan.items == ()
    assert plan.accepted_recommendation_ids == ()


def test_compile_plan_preserves_order() -> None:
    """Plan items follow the order of accepted_recommendation_ids."""
    rec1 = make_recommendation("rec.a")
    rec2 = make_recommendation("rec.b")
    rec3 = make_recommendation("rec.c")
    result = make_review_result_with_recommendations(rec1, rec2, rec3)

    plan = compile_plan(result, ["rec.c", "rec.a", "rec.b"])

    assert [item.recommendation_id for item in plan.items] == [
        "rec.c",
        "rec.a",
        "rec.b",
    ]


def test_plan_to_dict_serialization() -> None:
    """Plan.to_dict() produces JSON-serializable output."""
    rec1 = make_recommendation("rec.quality.missingness.col1")
    result = make_review_result_with_recommendations(rec1)

    plan = compile_plan(result, ["rec.quality.missingness.col1"])
    data = plan.to_dict()

    # Should be JSON-serializable
    serialized = json.dumps(data)
    parsed = json.loads(serialized)

    assert parsed["plan_schema_version"] == PLAN_SCHEMA_VERSION
    assert len(parsed["items"]) == 1
    assert parsed["items"][0]["recommendation_id"] == "rec.quality.missingness.col1"
    assert parsed["accepted_recommendation_ids"] == ["rec.quality.missingness.col1"]


def test_plan_item_to_dict_includes_traceability() -> None:
    """PlanItem.to_dict() includes originating findings and reviewers."""
    finding = RuleFinding(
        rule_id="quality.missing_value_threshold",
        rule_name="Missing Value Threshold",
        category="quality",
        severity="warning",
        column_name="col1",
        title="High missing values in column 'col1'",
        description="40% of values are missing.",
        evidence={"missing_percentage": 40.0},
        confidence=0.9,
    )
    rec = make_recommendation(
        "rec.quality.missingness.col1",
        originating_findings=(finding,),
        originating_reviewers=("review.quality.missingness",),
    )
    result = make_review_result_with_recommendations(rec)

    plan = compile_plan(result, ["rec.quality.missingness.col1"])
    item_dict = plan.items[0].to_dict()

    # to_dict() serializes findings as list of dicts (with volatile IDs)
    assert isinstance(item_dict["originating_findings"], list)
    assert len(item_dict["originating_findings"]) == 1
    serialized_finding = item_dict["originating_findings"][0]
    assert serialized_finding["rule_id"] == "quality.missing_value_threshold"
    assert serialized_finding["column_name"] == "col1"
    assert serialized_finding["title"] == "High missing values in column 'col1'"
    # originating_reviewers is serialized as a list
    assert item_dict["originating_reviewers"] == ["review.quality.missingness"]


def test_plan_renderer_name() -> None:
    """PlanRenderer identifies as 'plan_console'."""
    assert PlanRenderer().name == "plan_console"


def test_plan_renderer_output_is_deterministic() -> None:
    """PlanRenderer emits stable plain text."""
    rec1 = make_recommendation(
        "rec.quality.missingness.col1",
        title="Fix Missing Value Threshold in column col1",
    )
    result = make_review_result_with_recommendations(rec1)
    plan = compile_plan(result, ["rec.quality.missingness.col1"])

    text1 = PlanRenderer().render(plan)
    text2 = PlanRenderer().render(plan)

    assert text1 == text2
    assert text1.startswith("Featuresmith Plan")
    assert "Plan Schema Version: 0.1.0" in text1
    assert "Accepted Recommendations: 1" in text1
    assert "Plan Items: 1" in text1
    assert "[WARNING] Fix Missing Value Threshold in column col1" in text1
    assert "ID: plan.rec.quality.missingness.col1.0" in text1
    assert "From Recommendation: rec.quality.missingness.col1" in text1
    assert "Confidence: 0.80" in text1
    assert "Severity: warning" in text1
    assert "Affected Columns: col1" in text1
    assert "Action: Test action" in text1
    assert "Rationale: Test rationale" in text1
    assert "Originating Findings: 1" in text1
    assert "Originating Reviewers: review.quality.test" in text1


def test_plan_renderer_empty_plan() -> None:
    """PlanRenderer handles empty plans gracefully."""
    result = make_review_result_with_recommendations()
    plan = compile_plan(result, [])

    text = PlanRenderer().render(plan)

    assert "Featuresmith Plan" in text
    assert "Plan Items: 0" in text
    assert "No plan items (no recommendations accepted)." in text


def test_render_dispatches_to_plan_renderer() -> None:
    """render() dispatches to PlanRenderer for Plan objects."""
    rec1 = make_recommendation("rec.quality.missingness.col1")
    result = make_review_result_with_recommendations(rec1)
    plan = compile_plan(result, ["rec.quality.missingness.col1"])

    text = render(plan, "console")

    assert text.startswith("Featuresmith Plan")
    assert "Plan Schema Version: 0.1.0" in text


def test_render_ignores_target_for_plan() -> None:
    """render() ignores target parameter for Plan and uses plan_console."""
    rec1 = make_recommendation("rec.quality.missingness.col1")
    result = make_review_result_with_recommendations(rec1)
    plan = compile_plan(result, ["rec.quality.missingness.col1"])

    # Should work with any target since Plan only has plan_console renderer
    text1 = render(plan, "console")
    text2 = render(plan, "html")  # ignored for Plan
    text3 = render(plan, "unknown")

    assert text1 == text2 == text3
    assert text1.startswith("Featuresmith Plan")


def test_fs_plan_sdk_accessor() -> None:
    """fs.plan() compiles a Plan from a ReviewResult."""
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": [None, None, 3.0, 4.0, 5.0]})
    result = fs.review(df)

    # Get a recommendation ID from the result
    assert result.recommendations
    rec_id = result.recommendations[0].id

    plan = fs.plan(result, accept=[rec_id])

    assert isinstance(plan, Plan)
    assert len(plan.items) == 1
    assert plan.items[0].recommendation_id == rec_id
    assert plan.plan_schema_version == PLAN_SCHEMA_VERSION


def test_fs_plan_empty_accept() -> None:
    """fs.plan() with empty accept returns empty plan."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    result = fs.review(df)

    plan = fs.plan(result, accept=[])

    assert plan.items == ()
    assert plan.accepted_recommendation_ids == ()


def test_fs_plan_invalid_id_raises() -> None:
    """fs.plan() raises ValueError for unknown recommendation ID."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    result = fs.review(df)

    with pytest.raises(ValueError, match="Unknown recommendation ID"):
        fs.plan(result, accept=["rec.bogus.id"])


def test_plan_schema_version_constant() -> None:
    """PLAN_SCHEMA_VERSION is a stable constant."""
    assert PLAN_SCHEMA_VERSION == "0.1.0"
    # Verify it's the same in both modules
    from featuresmith.plan.compiler import PLAN_SCHEMA_VERSION as COMPILER_VERSION

    assert PLAN_SCHEMA_VERSION == COMPILER_VERSION


def test_plan_item_validation() -> None:
    """PlanItem validates confidence and severity."""
    # Valid confidence
    item = PlanItem(
        id="plan.test.0",
        recommendation_id="rec.test",
        title="Test",
        rationale="Test",
        confidence=0.5,
        severity="warning",
    )
    assert item.confidence == 0.5

    # Invalid confidence
    with pytest.raises(ValueError, match="confidence must be between 0.0 and 1.0"):
        PlanItem(
            id="plan.test.0",
            recommendation_id="rec.test",
            title="Test",
            rationale="Test",
            confidence=1.5,
            severity="warning",
        )

    # Invalid severity
    with pytest.raises(
        ValueError, match="severity must be 'critical', 'warning', or 'info'"
    ):
        PlanItem(
            id="plan.test.0",
            recommendation_id="rec.test",
            title="Test",
            rationale="Test",
            confidence=0.5,
            severity="invalid",
        )


def test_compile_plan_from_recommendations() -> None:
    """compile_plan_from_recommendations works without a full ReviewResult."""
    rec1 = make_recommendation("rec.quality.missingness.col1")
    rec2 = make_recommendation("rec.quality.duplicates.col2")

    plan = compile_plan_from_recommendations(
        [rec1, rec2], ["rec.quality.missingness.col1"]
    )

    assert len(plan.items) == 1
    assert plan.items[0].recommendation_id == "rec.quality.missingness.col1"
    assert plan.plan_schema_version == PLAN_SCHEMA_VERSION
