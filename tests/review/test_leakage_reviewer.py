"""Tests for the Leakage reviewer and its pattern detectors."""

from __future__ import annotations

from typing import Any

import pandas as pd
import pytest

import featuresmith as fs
from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import ProfileResult
from featuresmith.review.context import ReviewConfig, ReviewContext
from featuresmith.review.reviewers.leakage import LeakageReviewer
from featuresmith.review.schema import ReviewSection, Severity
from featuresmith.rules.leakage import (
    DuplicateTargetDetector,
    FutureInfoDetector,
    IdentifierShapeDetector,
    LeakageFinding,
    SuspiciousCorrelationDetector,
    TargetCorrelationDetector,
    TimestampLeakageDetector,
    builtin_detectors,
    confidence_label,
)


def clean_df() -> pd.DataFrame:
    """Return a dataset with no leakage signal for any detector."""
    return pd.DataFrame(
        {
            "x": [1.0, 2.0, 1.0, 2.0, 3.0, 2.0],
            "y": [3.0, 4.0, 5.0, 3.0, 4.0, 5.0],
            "cat": ["a", "b", "a", "b", "a", "b"],
        }
    )


def leakage_section(result: Any) -> ReviewSection:
    """Return the leakage section from a review result."""
    for section in result.sections:
        if section.id == "review.leakage":
            return section
    raise AssertionError("No leakage section in result.")


def run_reviewer(reviewer: LeakageReviewer, df: Any, **config: Any) -> ReviewSection:
    """Run the leakage reviewer against a dataframe with optional config."""
    dataset: Dataset = fs.load(df)
    profile = fs.profile(dataset)
    context = ReviewContext(
        profile=profile,
        dataset=dataset,
        config=ReviewConfig(
            target_column=config.pop("target_column", None),
            reviewer_config={reviewer.id: config} if config else {},
        ),
    )
    return reviewer.review(context)


def profile_of(df: pd.DataFrame) -> ProfileResult:
    """Return the ProfileResult for a dataframe."""
    return fs.profile(df)


# ---------------------------------------------------------------- confidence


def test_confidence_label_mapping() -> None:
    """Confidence labels map high, medium, and low ranges."""
    assert confidence_label(1.0) == "High"
    assert confidence_label(0.7) == "High"
    assert confidence_label(0.6) == "Medium"
    assert confidence_label(0.4) == "Medium"
    assert confidence_label(0.3) == "Low"
    assert confidence_label(0.0) == "Low"


def test_leakage_finding_is_frozen() -> None:
    """LeakageFinding evidence cannot be mutated after construction."""
    finding = LeakageFinding(
        pattern="target_correlation",
        column_name="a",
        title="t",
        rationale="r",
        evidence={"correlation": 0.99},
        confidence=0.9,
        severity="critical",
        suggested_action="drop",
    )

    with pytest.raises(TypeError):
        finding.evidence["correlation"] = 0.0


# ---------------------------------------------------------------- detectors


def test_target_correlation_detector_flags_leaky_feature() -> None:
    """A feature nearly perfectly correlated with the target is flagged."""
    df = pd.DataFrame(
        {
            "feature": [1, 2, 3, 4, 5],
            "target": [1.001, 2.002, 3.003, 4.004, 5.005],
            "normal": [5, 2, 8, 1, 9],
        }
    )
    findings = TargetCorrelationDetector().detect(
        profile_of(df), target_column="target"
    )

    assert [f.column_name for f in findings] == ["feature"]
    assert findings[0].confidence >= 0.9
    assert findings[0].severity == "critical"


def test_target_correlation_detector_no_target_no_findings() -> None:
    """Without a declared target the detector never infers one."""
    df = pd.DataFrame({"feature": [1, 2, 3, 4, 5], "normal": [5, 2, 8, 1, 9]})

    findings = TargetCorrelationDetector().detect(profile_of(df), target_column=None)

    assert findings == []


def test_target_correlation_detector_missing_target_column() -> None:
    """A declared target that is not numeric yields no findings."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    findings = TargetCorrelationDetector().detect(profile_of(df), target_column="b")

    assert findings == []


def test_identifier_detector_flags_id_column() -> None:
    """An identifier-like column that tracks the target is flagged."""
    ids = list(range(100, 200))
    target = [1 if value >= 150 else 0 for value in ids]
    df = pd.DataFrame({"row_id": ids, "target": target})

    findings = IdentifierShapeDetector().detect(profile_of(df), target_column="target")

    assert [f.column_name for f in findings] == ["row_id"]
    assert findings[0].severity == "critical"


def test_identifier_detector_ignores_unique_but_predictive_column() -> None:
    """A unique sequential column with no target correlation is not flagged."""
    df = pd.DataFrame(
        {
            "sample_index": list(range(50)),
            "target": [value % 2 for value in range(50)],
        }
    )

    findings = IdentifierShapeDetector().detect(profile_of(df), target_column="target")

    assert findings == []


def test_identifier_detector_no_target_returns_empty() -> None:
    """Identifier detection is correlation-gated and needs a target."""
    df = pd.DataFrame({"row_id": list(range(100, 200)), "v": [1, 2, 1, 2, 3] * 20})

    findings = IdentifierShapeDetector().detect(profile_of(df), target_column=None)

    assert findings == []


def test_timestamp_detector_requires_cutoff() -> None:
    """Without a configured prediction cutoff no timestamps are flagged."""
    df = pd.DataFrame({"ts": pd.to_datetime(["2025-01-01", "2026-01-01"])})

    findings = TimestampLeakageDetector().detect(profile_of(df), config={})

    assert findings == []


def test_timestamp_detector_flags_post_cutoff_values() -> None:
    """Datetime columns extending past the cutoff are flagged."""
    df = pd.DataFrame(
        {"ts": pd.to_datetime(["2025-01-01", "2025-06-01", "2026-01-01"])}
    )

    findings = TimestampLeakageDetector().detect(
        profile_of(df), config={"prediction_cutoff": "2025-12-31"}
    )

    assert [f.column_name for f in findings] == ["ts"]
    assert findings[0].severity == "warning"


def test_timestamp_detector_ignores_malformed_cutoff() -> None:
    """A malformed cutoff yields no findings instead of a crash."""
    df = pd.DataFrame({"ts": pd.to_datetime(["2025-01-01"])})

    findings = TimestampLeakageDetector().detect(
        profile_of(df), config={"prediction_cutoff": "not-a-date"}
    )

    assert findings == []


def test_duplicate_target_detector_flags_copy_of_target() -> None:
    """A column that is an exact copy of the target is flagged."""
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "target": [1, 2, 3, 4, 5]})

    findings = DuplicateTargetDetector().detect(profile_of(df), target_column="target")

    assert [f.column_name for f in findings] == ["a"]
    assert findings[0].severity == "critical"


def test_duplicate_target_detector_requires_target() -> None:
    """Without a target column the duplicate-target detector stays silent."""
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": [1, 2, 3, 4, 5]})

    findings = DuplicateTargetDetector().detect(profile_of(df), target_column=None)

    assert findings == []


def test_future_info_detector_flags_outcome_column_without_target() -> None:
    """An unmistakable outcome-named column is surfaced even without a target."""
    df = pd.DataFrame({"feature": [1, 2, 3, 4, 5], "target": [0, 1, 0, 1, 0]})

    findings = FutureInfoDetector().detect(profile_of(df), target_column=None)

    assert [f.column_name for f in findings] == ["target"]
    assert findings[0].severity == "info"


def test_future_info_detector_flags_outcome_column_with_target() -> None:
    """An outcome-like column correlated with a different target is critical."""
    df = pd.DataFrame(
        {"prediction": [1, 2, 3, 4, 5], "target": [1, 2, 3, 4, 5], "v": [5, 4, 3, 2, 1]}
    )

    findings = FutureInfoDetector().detect(profile_of(df), target_column="target")

    assert any(
        f.column_name == "prediction" and f.severity == "critical" for f in findings
    )


def test_future_info_detector_event_timestamp() -> None:
    """Datetime columns extending beyond a declared event timestamp are flagged."""
    df = pd.DataFrame(
        {
            "event_ts": pd.to_datetime(["2025-01-01", "2025-01-02"]),
            "resolved_ts": pd.to_datetime(["2025-02-01", "2025-02-02"]),
        }
    )

    findings = FutureInfoDetector().detect(
        profile_of(df), config={"event_timestamp_column": "event_ts"}
    )

    assert [f.column_name for f in findings] == ["resolved_ts"]
    assert findings[0].severity == "warning"


def test_suspicious_detector_flags_near_identical_pair() -> None:
    """A near-identical column pair without a target is suspicious."""
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [1, 2, 3, 4, 5]})

    findings = SuspiciousCorrelationDetector().detect(profile_of(df))

    assert len(findings) == 1
    assert findings[0].severity == "warning"


def test_suspicious_detector_ignores_affine_but_distinct_pair() -> None:
    """Perfectly correlated but clearly distinct columns are not flagged."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    findings = SuspiciousCorrelationDetector().detect(profile_of(df))

    assert findings == []


def test_suspicious_detector_target_band_is_low_confidence() -> None:
    """Correlation just below the leakage threshold is reported as info."""
    df = pd.DataFrame(
        {
            "feature": [1.0, 2.0, 3.0, 4.0, 5.0],
            "target": [1.0, 2.0, 3.6, 4.0, 5.2],
        }
    )

    findings = SuspiciousCorrelationDetector().detect(
        profile_of(df), target_column="target"
    )

    assert findings and all(f.severity == "info" for f in findings)


# ---------------------------------------------------------------- reviewer


def test_leakage_reviewer_clean_dataset_passes() -> None:
    """A clean dataset yields a passed leakage section with no findings."""
    section = run_reviewer(LeakageReviewer(), clean_df())

    assert section.id == "review.leakage"
    assert section.severity is Severity.PASSED
    assert section.findings == ()


def test_leakage_reviewer_target_leakage_is_critical() -> None:
    """A feature that duplicates the target produces a critical finding."""
    df = pd.DataFrame(
        {
            "feature": [1, 2, 3, 4, 5],
            "target": [1.001, 2.002, 3.003, 4.004, 5.005],
            "normal": [5, 2, 8, 1, 9],
        }
    )
    section = run_reviewer(LeakageReviewer(), df, target_column="target")

    assert section.severity is Severity.CRITICAL
    assert [f.column_name for f in section.findings] == ["feature"]


def test_leakage_reviewer_dedupes_per_column() -> None:
    """Multiple detectors firing on one column merge into a single finding."""
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "target": [1, 2, 3, 4, 5]})
    section = run_reviewer(LeakageReviewer(), df, target_column="target")

    assert len(section.findings) == 1
    finding = section.findings[0]
    assert finding.rule_id == "leakage.multiple_patterns"
    patterns = set(finding.evidence["patterns"])
    assert patterns == {"target_correlation", "identifier", "duplicate_target"}
    assert finding.severity == "critical"


def test_leakage_reviewer_identifier_leakage() -> None:
    """Identifier leakage surfaces as an identifier finding."""
    ids = list(range(100, 200))
    target = [1 if value >= 150 else 0 for value in ids]
    df = pd.DataFrame({"row_id": ids, "target": target})

    section = run_reviewer(LeakageReviewer(), df, target_column="target")

    assert len(section.findings) == 1
    assert section.findings[0].rule_id == "leakage.identifier"
    assert section.findings[0].severity == "critical"


def test_leakage_reviewer_timestamp_config() -> None:
    """A configured prediction cutoff drives timestamp findings."""
    df = pd.DataFrame(
        {
            "ts": pd.to_datetime(["2025-01-01", "2025-06-01", "2026-01-01"]),
            "v": [1, 2, 3],
        }
    )
    section = run_reviewer(LeakageReviewer(), df, prediction_cutoff="2025-12-31")

    assert section.severity is Severity.WARNING
    assert [f.rule_id for f in section.findings] == ["leakage.timestamp"]
    assert section.findings[0].metadata["confidence_level"] == "Medium"


def test_leakage_reviewer_outcome_column_no_target() -> None:
    """An outcome-named column is surfaced at info without a target."""
    df = pd.DataFrame({"feature": [1, 2, 3, 4, 5], "target": [0, 1, 0, 1, 0]})
    section = run_reviewer(LeakageReviewer(), df)

    assert section.severity is Severity.INFO
    assert [f.rule_id for f in section.findings] == ["leakage.future_info"]
    assert section.findings[0].column_name == "target"


def test_leakage_reviewer_empty_dataset_passes() -> None:
    """An empty or fully empty dataset does not crash and stays clean."""
    empty = pd.DataFrame({"a": pd.Series([], dtype="float64")})
    section = run_reviewer(LeakageReviewer(), empty)

    assert section.severity is Severity.PASSED
    assert section.findings == ()


def test_leakage_reviewer_no_numeric_columns_passes() -> None:
    """A dataset with no numeric columns produces no leakage findings."""
    df = pd.DataFrame({"cat": ["a", "b", "c"], "txt": ["foo", "bar", "baz"]})
    section = run_reviewer(LeakageReviewer(), df)

    assert section.severity is Severity.PASSED
    assert section.findings == ()


def test_leakage_reviewer_deterministic_across_runs() -> None:
    """The same dataset yields identical leakage findings across runs."""
    df = pd.DataFrame(
        {"feature": [1, 2, 3, 4, 5], "target": [1.001, 2.002, 3.003, 4.004, 5.005]}
    )

    first = run_reviewer(LeakageReviewer(), df, target_column="target")
    second = run_reviewer(LeakageReviewer(), df, target_column="target")

    first_payload = [
        (f.rule_id, f.severity, f.column_name, f.confidence) for f in first.findings
    ]
    second_payload = [
        (f.rule_id, f.severity, f.column_name, f.confidence) for f in second.findings
    ]
    assert first_payload == second_payload


def test_builtin_detectors_are_stable_and_unique() -> None:
    """The built-in detector set is stable and has unique pattern IDs."""
    detectors = builtin_detectors()

    assert [detector.id for detector in detectors] == [
        "target_correlation",
        "identifier",
        "timestamp",
        "future_info",
        "duplicate_target",
        "suspicious_correlation",
    ]
    assert len({detector.id for detector in detectors}) == len(detectors)


def test_leakage_section_integrated_via_sdk() -> None:
    """fs.review() includes the leakage section in the canonical result."""
    result = fs.review(clean_df())

    section = leakage_section(result)
    assert section.category.value == "leakage"
    assert section.severity is Severity.PASSED
    assert result.overall_summary == (
        "8 of 8 sections passed with 0 finding(s) identified across the review."
    )
