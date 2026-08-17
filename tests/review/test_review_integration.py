"""End-to-end integration tests for fs.review() with the built-in reviewers."""

from __future__ import annotations

import json

import pandas as pd

import featuresmith as fs
from featuresmith.review.schema import ReviewResult, ReviewSection, Severity

BUILTIN_REVIEWER_IDS = {
    "review.schema.health",
    "review.schema.types",
    "review.quality.missingness",
    "review.quality.duplicates",
    "review.quality.constants",
    "review.quality.cardinality",
    "review.quality.basic_statistics",
    "review.quality.feature_quality",
    "review.leakage",
}


def clean_df() -> pd.DataFrame:
    """Return a dataset with no issues for any reviewer."""
    return pd.DataFrame(
        {
            "x": [1.0, 2.0, 1.0, 2.0, 3.0, 2.0],
            "y": [3.0, 4.0, 5.0, 3.0, 4.0, 5.0],
            "cat": ["a", "b", "a", "b", "a", "b"],
        }
    )


def missing_df() -> pd.DataFrame:
    """Return a dataset with one column at 40% missingness."""
    return pd.DataFrame({"clean": [1, 2, 3, 4, 5], "dirty": [1, None, None, 4, 5]})


def duplicate_df() -> pd.DataFrame:
    """Return a dataset with 40% duplicate rows."""
    return pd.DataFrame({"a": [1, 2, 2, 3, 3], "b": [1, 2, 2, 3, 3]})


def constant_df() -> pd.DataFrame:
    """Return a dataset with one constant and one fully empty column."""
    return pd.DataFrame(
        {
            "normal": [1, 2, 3, 4, 5],
            "const": [42, 42, 42, 42, 42],
            "empty": [None, None, None, None, None],
        }
    )


def mixed_df() -> pd.DataFrame:
    """Return a dataset mixing numeric, categorical, and text columns."""
    return pd.DataFrame(
        {
            "num": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "cat": ["a", "b", "c", "a", "b", "c"],
            "txt": [
                "the quick brown fox jumps over the lazy dog",
                "pack my box with five dozen liquor jugs",
                "the five boxing wizards jump quickly",
                "sphinx of black quartz judge my vow",
                "how vexingly quick daft zebras jump",
                "waltz bad nymph for quick jigs vex",
            ],
        }
    )


def empty_df() -> pd.DataFrame:
    """Return a zero-row dataset with two declared columns."""
    return pd.DataFrame(
        {
            "a": pd.Series([], dtype="float64"),
            "b": pd.Series([], dtype="object"),
        }
    )


def high_cardinality_df() -> pd.DataFrame:
    """Return a categorical column with 10 unique values over 30 rows."""
    return pd.DataFrame({"cat": [f"cat_{i % 10}" for i in range(30)]})


def section_by_id(result: ReviewResult, section_id: str) -> ReviewSection:
    """Return the section with the given reviewer ID."""
    for section in result.sections:
        if section.id == section_id:
            return section
    raise AssertionError(f"No section with id '{section_id}' in result.")


def test_review_clean_dataset_all_sections_pass() -> None:
    """A clean dataset reports every built-in section as passed."""
    result = fs.review(clean_df())

    assert isinstance(result, ReviewResult)
    assert {section.id for section in result.sections} == BUILTIN_REVIEWER_IDS
    assert all(section.severity is Severity.PASSED for section in result.sections)
    assert result.overall_summary == (
        "9 of 9 sections passed with 0 finding(s) identified across the review."
    )


def test_review_empty_dataset() -> None:
    """An empty dataset completes with a schema-health warning."""
    result = fs.review(empty_df())

    schema_health = section_by_id(result, "review.schema.health")
    assert schema_health.severity is Severity.WARNING
    assert {section.id for section in result.sections} == BUILTIN_REVIEWER_IDS


def test_review_missing_values() -> None:
    """High missingness surfaces in the Missing Values section."""
    result = fs.review(missing_df())

    section = section_by_id(result, "review.quality.missingness")
    assert section.severity is Severity.WARNING
    assert len(section.findings) == 1
    assert section.findings[0].column_name == "dirty"
    # Traceability: the finding resolves back to the composing rule.
    assert section.findings[0].rule_id == "quality.missing_value_threshold"


def test_review_duplicates() -> None:
    """Excess duplicate rows surface in the Duplicate Rows section."""
    result = fs.review(duplicate_df())

    section = section_by_id(result, "review.quality.duplicates")
    assert section.severity is Severity.WARNING
    assert section.findings[0].evidence["duplicate_percentage"] == 40.0


def test_review_constant_columns() -> None:
    """Constant and fully empty columns surface in their sections."""
    result = fs.review(constant_df())

    constants = section_by_id(result, "review.quality.constants")
    assert constants.severity is Severity.WARNING
    assert [f.column_name for f in constants.findings] == ["const"]

    schema_health = section_by_id(result, "review.schema.health")
    assert schema_health.severity is Severity.CRITICAL
    assert [f.column_name for f in schema_health.findings] == ["empty"]


def test_review_mixed_data_types() -> None:
    """Mixed data types surface in the Data Types section."""
    result = fs.review(mixed_df())

    section = section_by_id(result, "review.schema.types")
    assert section.severity is Severity.INFO
    assert [f.column_name for f in section.findings] == ["txt"]


def test_review_high_cardinality() -> None:
    """High-cardinality categorical columns surface via reviewer configuration."""
    result = fs.review(
        high_cardinality_df(),
        reviewer_config={
            "review.quality.cardinality": {"threshold": 0.30, "min_cardinality": 5}
        },
    )

    section = section_by_id(result, "review.quality.cardinality")
    assert section.severity is Severity.WARNING
    assert [f.column_name for f in section.findings] == ["cat"]


def test_review_missing_threshold_config() -> None:
    """Reviewer configuration overrides default thresholds."""
    result = fs.review(
        missing_df(),
        reviewer_config={"review.quality.missingness": {"threshold": 50.0}},
    )

    section = section_by_id(result, "review.quality.missingness")
    assert section.severity is Severity.PASSED
    assert section.findings == ()


def test_review_result_json_serializable_with_findings() -> None:
    """ReviewResult with findings serializes to clean JSON."""
    data = fs.review(missing_df()).to_dict()

    serialized = json.dumps(data)
    parsed = json.loads(serialized)
    assert len(parsed["sections"]) == 9
    missingness = next(
        s for s in parsed["sections"] if s["id"] == "review.quality.missingness"
    )
    assert missingness["severity"] == "warning"
    assert len(missingness["findings"]) == 1


def test_review_sections_never_absent() -> None:
    """Every built-in section renders even when it finds nothing."""
    result = fs.review(clean_df())

    assert len(result.sections) == 9
    assert all(section.severity is Severity.PASSED for section in result.sections)


def test_review_with_previous_adds_diff_section() -> None:
    """Diff-aware review adds a diff section to the built-in sections."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new = pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]})

    result = fs.review(new, previous=old)

    assert {section.id for section in result.sections} == BUILTIN_REVIEWER_IDS | {
        "review.diff"
    }
    diff_section = section_by_id(result, "review.diff")
    assert diff_section.category.value == "diff"
    assert diff_section.severity is Severity.WARNING
    assert result.diff is not None
    assert result.diff.schema.added_columns == ("c",)


def test_review_with_previous_identical_snapshots() -> None:
    """Identical snapshots produce a passed diff section and unchanged health."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    result = fs.review(df, previous=df.copy())

    diff_section = section_by_id(result, "review.diff")
    assert diff_section.severity is Severity.PASSED
    assert result.diff is not None
    assert result.diff.summary.overall_health == "unchanged"


def test_review_with_previous_json_serializable() -> None:
    """A diff-aware review serializes to clean JSON including the diff."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new = pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]})

    data = fs.review(new, previous=old).to_dict()

    serialized = json.dumps(data)
    parsed = json.loads(serialized)
    assert len(parsed["sections"]) == 10
    assert parsed["diff"] is not None
    assert parsed["diff"]["schema"]["added_columns"] == ["c"]
    assert parsed["diff"]["summary"]["overall_health"] == "regressed"


def test_review_with_previous_keeps_score_dimensions() -> None:
    """The diff section does not alter the ML Readiness Score dimensions."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new = pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]})

    result = fs.review(new, previous=old)

    assert result.score is not None
    assert len(result.score.dimensions) == 7
