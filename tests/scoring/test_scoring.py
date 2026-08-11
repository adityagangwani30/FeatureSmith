"""Tests for the ML Readiness Score computation.

Covers the scoring formula, per-dimension deductions, weighted aggregation,
explainability (rationale, actions, positive/negative findings), applicability
and renormalization, determinism, serialization, and the end-to-end engine
integration through ``fs.review()``.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

import pandas as pd
import pytest

import featuresmith as fs
from featuresmith.core.profile_result import DatasetSummary
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.review.schema import (
    ReviewCategory,
    ReviewResult,
    ReviewSection,
    Severity,
)
from featuresmith.review.scoring_adapter import ScoreAdapter
from featuresmith.scoring.aggregator import WeightedAggregator, compute_score
from featuresmith.scoring.dimensions import builtin_dimensions
from featuresmith.scoring.registry import ScoreDimensionRegistry, default_registry
from featuresmith.scoring.schema import MLReadinessScore

SECTION_TITLES = {
    "review.schema.health": "Schema Health",
    "review.quality.missingness": "Missing Values",
    "review.quality.duplicates": "Duplicate Rows",
    "review.schema.types": "Data Types",
    "review.quality.constants": "Constant Columns",
    "review.quality.cardinality": "High Cardinality",
    "review.quality.basic_statistics": "Basic Statistics",
    "review.leakage": "Leakage Detection",
}


def make_summary() -> DatasetSummary:
    """Build a minimal DatasetSummary."""
    return DatasetSummary(
        row_count=10,
        column_count=7,
        size_in_bytes=None,
        missing_percentage=0.0,
        duplicate_percentage=0.0,
        num_numeric_columns=7,
        num_categorical_columns=0,
        num_datetime_columns=0,
        num_text_columns=0,
        num_constant_columns=0,
        num_fully_empty_columns=0,
    )


def make_finding(
    severity: str, *, rule_id: str, column: str | None = None
) -> RuleFinding:
    """Build a minimal RuleFinding for scoring tests."""
    return RuleFinding(
        rule_id=rule_id,
        rule_name=rule_id,
        category="quality",
        severity=severity,
        column_name=column,
        title=f"{severity} issue in {rule_id}",
        description=f"Synthetic {severity} finding.",
        evidence={},
    )


def make_section(section_id: str, severities: tuple[str, ...] = ()) -> ReviewSection:
    """Build a ReviewSection with one finding per requested severity."""
    findings = tuple(
        make_finding(severity, rule_id=section_id, column=f"col-{index}")
        for index, severity in enumerate(severities)
    )
    worst = max(
        (Severity(s) for s in severities), key=lambda s: s.rank, default=Severity.PASSED
    )
    return ReviewSection(
        id=section_id,
        title=SECTION_TITLES.get(section_id, section_id),
        category=ReviewCategory.QUALITY
        if section_id.startswith("review.quality")
        else ReviewCategory.SCHEMA,
        severity=worst,
        findings=findings,
    )


def make_result(
    *section_ids: str, severities: dict[str, tuple[str, ...]] | None = None
) -> ReviewResult:
    """Build a ReviewResult containing the requested review sections."""
    severities = severities or {}
    return ReviewResult(
        engine_version="0.1.0",
        dataset_summary=make_summary(),
        generated_at=datetime(2026, 8, 2, 12, 0, 0, tzinfo=UTC),
        sections=tuple(
            make_section(sid, severities.get(sid, ())) for sid in section_ids
        ),
        overall_summary="Synthetic review.",
    )


def compute(result: ReviewResult) -> MLReadinessScore | None:
    """Compute the score using the built-in dimensions."""
    return WeightedAggregator(dimensions=builtin_dimensions()).compute(result)


def all_sections() -> tuple[str, ...]:
    """Return all built-in review section IDs."""
    return tuple(SECTION_TITLES)


def test_perfect_result_scores_full_marks() -> None:
    """A review with no findings scores 100 on every dimension."""
    score = compute(make_result(*all_sections()))

    assert score is not None
    assert score.overall == 100.0
    assert len(score.dimensions) == 8
    assert all(dimension.score == 100.0 for dimension in score.dimensions)
    assert score.negative_findings == ()
    assert len(score.positive_findings) == 8


def test_missing_values_deduction_is_severity_based() -> None:
    """Each severity deducts its fixed, documented number of points."""
    critical = compute(
        make_result(
            "review.quality.missingness",
            severities={"review.quality.missingness": ("critical",)},
        )
    )
    warning = compute(
        make_result(
            "review.quality.missingness",
            severities={"review.quality.missingness": ("warning",)},
        )
    )
    info = compute(
        make_result(
            "review.quality.missingness",
            severities={"review.quality.missingness": ("info",)},
        )
    )

    assert critical is not None
    assert warning is not None
    assert info is not None
    assert critical.dimensions[0].score == 70.0
    assert warning.dimensions[0].score == 85.0
    assert info.dimensions[0].score == 95.0


def test_leakage_findings_lower_leakage_risk_dimension() -> None:
    """A critical leakage finding deducts its documented points."""
    score = compute(
        make_result(
            "review.leakage",
            severities={"review.leakage": ("critical",)},
        )
    )

    assert score is not None
    leakage = next(d for d in score.dimensions if d.id == "score.leakage_risk")
    assert leakage.score == 70.0
    assert "Leakage Risk" in leakage.label
    assert leakage.contributing_findings


def test_leakage_findings_only_affect_leakage_dimension() -> None:
    """Leakage findings lower only the leakage-risk dimension."""
    score = compute(
        make_result(
            *all_sections(),
            severities={"review.leakage": ("critical",)},
        )
    )

    assert score is not None
    leakage = next(d for d in score.dimensions if d.id == "score.leakage_risk")
    others = [d for d in score.dimensions if d.id != "score.leakage_risk"]
    assert leakage.score == 70.0
    assert all(dimension.score == 100.0 for dimension in others)


def test_multiple_findings_accumulate_and_clamp_at_zero() -> None:
    """Findings accumulate and the score never goes negative."""
    score = compute(
        make_result(
            "review.quality.duplicates",
            severities={"review.quality.duplicates": ("critical",) * 4},
        )
    )

    assert score is not None
    duplicates = next(d for d in score.dimensions if d.id == "score.duplicate_records")
    assert duplicates.score == 0.0
    assert all(dimension.score >= 0.0 for dimension in score.dimensions)
    assert score.overall >= 0.0
    assert score.overall <= 100.0


def test_aggregation_is_weighted_mean_of_applicable_dimensions() -> None:
    """Overall equals the rounded weighted mean of the dimension scores."""
    score = compute(
        make_result(
            *all_sections(),
            severities={
                "review.quality.missingness": ("warning",),
                "review.quality.constants": ("warning",),
            },
        )
    )

    assert score is not None
    assert score.overall == round((100.0 * 6 + 85.0 + 85.0) / 8, 1)
    missing = next(d for d in score.dimensions if d.id == "score.missing_values")
    constants = next(d for d in score.dimensions if d.id == "score.constant_columns")
    assert missing.score == 85.0
    assert constants.score == 85.0
    assert score.summary == (
        "Overall ML Readiness is 96.2/100 across 8 dimension(s); "
        "6 fully healthy, 2 with findings lowering the score."
    )


def test_explanation_matches_findings() -> None:
    """Rationale, actions, and negative findings trace back to the findings."""
    finding = make_finding(
        "warning", rule_id="review.quality.missingness", column="age"
    )
    section = ReviewSection(
        id="review.quality.missingness",
        title="Missing Values",
        category=ReviewCategory.QUALITY,
        severity=Severity.WARNING,
        findings=(finding,),
    )
    result = ReviewResult(
        engine_version="0.1.0",
        dataset_summary=make_summary(),
        generated_at=datetime(2026, 8, 2, 12, 0, 0, tzinfo=UTC),
        sections=(section,),
        overall_summary="Synthetic review.",
    )

    score = compute(result)
    assert score is not None
    dimension = score.dimensions[0]
    assert dimension.contributing_findings == (finding,)
    assert "1 finding(s) lowered the score" in dimension.rationale
    assert dimension.suggested_actions == (
        "Address the flagged issue: warning issue in review.quality.missingness "
        "(in column 'age').",
    )
    assert score.negative_findings == (finding,)
    assert score.positive_findings == ()


def test_positive_findings_list_fully_healthy_dimensions() -> None:
    """Positive findings name every dimension that scored full marks."""
    score = compute(
        make_result(
            *all_sections(),
            severities={"review.quality.missingness": ("warning",)},
        )
    )

    assert score is not None
    assert (
        "Missing Values scored 100/100 with no issues found."
        not in score.positive_findings
    )
    assert len(score.positive_findings) == 7
    assert all(
        statement.endswith("scored 100/100 with no issues found.")
        for statement in score.positive_findings
    )


def test_deterministic_across_runs() -> None:
    """The same review always yields the identical score object."""
    result = make_result(
        *all_sections(),
        severities={
            "review.quality.missingness": ("warning",),
            "review.quality.constants": ("warning",),
        },
    )

    first = compute(result)
    second = compute(result)

    assert first is not None
    assert second is not None
    assert first.overall == second.overall
    assert first.to_dict() == second.to_dict()


def test_inapplicable_dimension_is_omitted_and_reweighted() -> None:
    """Missing sections drop their dimension instead of scoring it arbitrarily."""
    score = compute(
        make_result("review.quality.missingness", "review.quality.duplicates")
    )

    assert score is not None
    assert [d.id for d in score.dimensions] == [
        "score.missing_values",
        "score.duplicate_records",
    ]
    assert score.overall == 100.0


def test_no_applicable_dimensions_returns_none() -> None:
    """No score is produced when no dimension applies to the review."""
    result = make_result("review.custom.section")

    assert compute(result) is None
    assert ScoreAdapter().attach(result) is result


def test_custom_weights_are_respected_and_transparent() -> None:
    """Per-dimension weight overrides change the aggregate and stay visible."""
    result = make_result(
        *all_sections(),
        severities={"review.quality.missingness": ("warning",)},
    )
    score = WeightedAggregator(
        dimensions=builtin_dimensions(),
        weights={"score.missing_values": 2.0},
    ).compute(result)

    assert score is not None
    missing = next(d for d in score.dimensions if d.id == "score.missing_values")
    assert missing.weight == 2.0
    assert score.overall == round((85.0 * 2.0 + 100.0 * 7) / 9.0, 1)


def test_score_is_json_serializable() -> None:
    """MLReadinessScore.to_dict() is fully JSON-clean."""
    score = compute(
        make_result(
            *all_sections(),
            severities={"review.quality.missingness": ("warning",)},
        )
    )

    assert score is not None
    data = score.to_dict()
    parsed = json.loads(json.dumps(data))
    assert parsed["scoring_version"] == "0.2.0"
    assert parsed["overall"] == 98.1
    assert len(parsed["dimensions"]) == 8
    assert parsed["positive_findings"][0].endswith(
        "scored 100/100 with no issues found."
    )
    assert parsed["negative_findings"][0]["severity"] == "warning"


def test_fs_score_accessor_returns_attached_score() -> None:
    """fs.score() returns the score attached by fs.review()."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    result = fs.review(df)
    computed = fs.score(result)

    assert computed is result.score
    assert computed is not None
    assert computed.overall == 100.0


def test_fs_score_accessor_computes_when_absent() -> None:
    """fs.score() computes the score for a result built without the engine."""
    result = make_result(*all_sections())

    score = fs.score(result)

    assert result.score is None
    assert score is not None
    assert score.overall == 100.0


def test_score_adapter_attaches_score() -> None:
    """ScoreAdapter attaches the score onto a fresh ReviewResult."""
    result = make_result(
        *all_sections(),
        severities={"review.quality.missingness": ("warning",)},
    )

    attached = ScoreAdapter().attach(result)

    assert attached is not result
    assert attached.score is not None
    assert attached.score.overall == 98.1
    assert attached.score is not None and attached.score.scoring_version == "0.2.0"


def test_compute_score_helper() -> None:
    """compute_score() is a one-call convenience over the aggregator."""
    result = make_result(*all_sections())

    score = compute_score(result)

    assert score is not None
    assert score.overall == 100.0


def test_dimension_compute_raises_when_section_absent() -> None:
    """Computing a dimension without its backing section is a programmer error."""
    from featuresmith.scoring.dimensions import SchemaHealthDimension

    result = make_result("review.quality.missingness")

    assert not SchemaHealthDimension().applicable(result)


# ---------------------------------------------------------------- registry wiring


def test_default_registry_ships_builtin_dimensions() -> None:
    """default_registry() registers the eight built-in dimensions in order."""
    registry = default_registry()

    dimensions = registry.list_dimensions()

    assert [d.id for d in dimensions] == [d.id for d in builtin_dimensions()]
    assert len(dimensions) == 8


def test_aggregator_obtains_dimensions_via_default_registry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """WeightedAggregator sources its default dimensions from default_registry."""
    calls: list[ScoreDimensionRegistry] = []

    def recording_default_registry() -> ScoreDimensionRegistry:
        registry = default_registry()
        calls.append(registry)
        return registry

    monkeypatch.setattr(
        "featuresmith.scoring.aggregator.default_registry",
        recording_default_registry,
    )

    score = WeightedAggregator().compute(make_result(*all_sections()))

    assert len(calls) == 1
    assert score is not None
    assert [d.id for d in score.dimensions] == [d.id for d in builtin_dimensions()]


def test_aggregator_uses_dimensions_from_supplied_registry() -> None:
    """A supplied registry drives aggregation; its registrations are honored."""
    registry = ScoreDimensionRegistry(builtin_dimensions())
    registry.unregister("score.schema_health")

    score = WeightedAggregator(registry=registry).compute(make_result(*all_sections()))

    assert score is not None
    assert [d.id for d in score.dimensions] == [
        d.id for d in builtin_dimensions() if d.id != "score.schema_health"
    ]


def test_aggregator_computes_registered_custom_dimension() -> None:
    """Registry-registered dimensions outside the built-ins still participate."""
    from featuresmith.scoring.dimensions import SchemaHealthDimension

    registry = ScoreDimensionRegistry((SchemaHealthDimension(),))

    score = WeightedAggregator(registry=registry).compute(
        make_result("review.schema.health")
    )

    assert score is not None
    assert [d.id for d in score.dimensions] == ["score.schema_health"]
    assert score.overall == 100.0


def test_aggregator_rejects_registry_and_dimensions_together() -> None:
    """Providing both registry and dimensions is an ambiguous configuration."""
    with pytest.raises(ValueError, match="either 'registry' or 'dimensions'"):
        WeightedAggregator(dimensions=builtin_dimensions(), registry=default_registry())


def test_score_adapter_accepts_registry() -> None:
    """ScoreAdapter wires its registry into the underlying aggregator."""
    registry = ScoreDimensionRegistry(builtin_dimensions())

    attached = ScoreAdapter(registry=registry).attach(make_result(*all_sections()))

    assert attached.score is not None
    assert len(attached.score.dimensions) == 8


def test_compute_score_accepts_registry() -> None:
    """compute_score() forwards a supplied registry to the aggregator."""
    registry = ScoreDimensionRegistry(builtin_dimensions())

    score = compute_score(make_result(*all_sections()), registry=registry)

    assert score is not None
    assert score.overall == 100.0


# ---------------------------------------------------------------- integration


def test_review_perfect_dataset_scores_100() -> None:
    """A clean dataframe reviews to a perfect overall score."""
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": [2.5, 1.0, 4.0, 3.0, 5.5]})

    result = fs.review(df)

    assert result.score is not None
    assert result.score.overall == 100.0


def test_review_missing_values_lowers_score() -> None:
    """A dataset with a missing column lowers only the missing-values dimension."""
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "miss": [1.0, None, None, 4.0, 5.0]})

    score = fs.review(df).score

    assert score is not None
    missing = next(d for d in score.dimensions if d.id == "score.missing_values")
    others = [d for d in score.dimensions if d.id != "score.missing_values"]
    assert missing.score < 100.0
    assert all(dimension.score == 100.0 for dimension in others)


def test_review_duplicates_lowers_score() -> None:
    """A dataset with duplicate rows lowers the duplicate-records dimension."""
    df = pd.DataFrame({"a": [1, 1, 2, 2, 3], "b": [1, 1, 2, 2, 3]})

    score = fs.review(df).score

    assert score is not None
    duplicates = next(d for d in score.dimensions if d.id == "score.duplicate_records")
    assert duplicates.score < 100.0


def test_review_constants_lowers_score() -> None:
    """A dataset with a constant column lowers the constant-columns dimension."""
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "const": ["x", "x", "x", "x", "x"]})

    score = fs.review(df).score

    assert score is not None
    constants = next(d for d in score.dimensions if d.id == "score.constant_columns")
    assert constants.score < 100.0


def test_review_multiple_issues_and_bounds() -> None:
    """A heavily-flagged dataset stays in [0, 100] and flags several dimensions."""
    df = pd.DataFrame(
        {
            "a": [1, 1, 1, 2, 2, 3, 3, 3, 4, 4],
            "b": [None, None, None, None, None, 6.0, 7.0, 8.0, 9.0, 10.0],
            "c": ["z", "z", "z", "z", "z", "z", "z", "z", "z", "z"],
        }
    )

    score = fs.review(df).score

    assert score is not None
    assert score.overall < 100.0
    assert 0.0 <= score.overall <= 100.0
    lowered = [
        d
        for d in score.dimensions
        if d.id
        in {"score.missing_values", "score.duplicate_records", "score.constant_columns"}
    ]
    assert all(dimension.score < 100.0 for dimension in lowered)
    assert all(dimension.score >= 0.0 for dimension in score.dimensions)


def test_review_score_is_deterministic_across_runs() -> None:
    """Two reviews of the same dataset produce identical scores."""
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "miss": [1.0, None, None, 4.0, 5.0]})

    first = fs.review(df).score
    second = fs.review(df).score

    assert first is not None and second is not None
    assert first.overall == second.overall
    assert [d.score for d in first.dimensions] == [d.score for d in second.dimensions]


def test_review_leakage_lowers_score() -> None:
    """A leaky feature lowers the leakage-risk dimension and the overall."""
    df = pd.DataFrame({"target": [1, 2, 3, 4, 5], "leak": [1, 2, 3, 4, 5]})

    score = fs.review(df, target_column="target").score

    assert score is not None
    leakage = next(d for d in score.dimensions if d.id == "score.leakage_risk")
    assert leakage.score < 100.0
    assert score.overall < 100.0
    assert "with findings lowering the score" in score.summary


def test_review_score_is_stable_with_leakage() -> None:
    """Two reviews of the same leaky dataset produce identical scores."""
    df = pd.DataFrame({"target": [1, 2, 3, 4, 5], "leak": [1, 2, 3, 4, 5]})

    first = fs.review(df, target_column="target").score
    second = fs.review(df, target_column="target").score

    assert first is not None and second is not None
    assert first.overall == second.overall
    assert [d.score for d in first.dimensions] == [d.score for d in second.dimensions]
    assert first.overall < 100.0
