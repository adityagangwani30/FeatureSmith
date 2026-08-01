"""Unit tests for each built-in review reviewer."""

from __future__ import annotations

from typing import Any

import pandas as pd

import featuresmith as fs
from featuresmith.core.dataset import Dataset
from featuresmith.review.base import BaseReviewer
from featuresmith.review.context import ReviewConfig, ReviewContext
from featuresmith.review.reviewers import (
    BasicStatisticsReviewer,
    CardinalityReviewer,
    ConstantColumnReviewer,
    DuplicateReviewer,
    MissingValueReviewer,
    SchemaHealthReviewer,
    TypeReviewer,
)
from featuresmith.review.schema import ReviewSection, Severity


def run_reviewer(reviewer: BaseReviewer, df: Any, **config: Any) -> ReviewSection:
    """Run a single reviewer against a dataframe with optional configuration."""
    dataset: Dataset = fs.load(df)
    profile = fs.profile(dataset)
    context = ReviewContext(
        profile=profile,
        dataset=dataset,
        config=ReviewConfig(reviewer_config={reviewer.id: config} if config else {}),
    )
    return reviewer.review(context)


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


def high_cardinality_df() -> pd.DataFrame:
    """Return a categorical column with 10 unique values over 30 rows."""
    return pd.DataFrame({"cat": [f"cat_{i % 10}" for i in range(30)]})


def identifier_df() -> pd.DataFrame:
    """Return a dataset with one identifier-like numeric column."""
    return pd.DataFrame({"id": list(range(100, 200)), "v": [1, 2, 1, 2, 3] * 20})


def text_df() -> pd.DataFrame:
    """Return a dataset with a free-text column."""
    return pd.DataFrame(
        {
            "txt": [
                "the quick brown fox jumps over the lazy dog",
                "pack my box with five dozen liquor jugs",
                "the five boxing wizards jump quickly",
                "sphinx of black quartz judge my vow",
            ]
        }
    )


def skewed_df() -> pd.DataFrame:
    """Return a dataset with a heavily right-skewed numeric column."""
    return pd.DataFrame({"s": [1.0] * 100 + [100.0, 500.0, 2000.0]})


def empty_df() -> pd.DataFrame:
    """Return a zero-row dataset with two declared columns."""
    return pd.DataFrame(
        {
            "a": pd.Series([], dtype="float64"),
            "b": pd.Series([], dtype="object"),
        }
    )


def test_missing_value_reviewer_flags_high_missingness() -> None:
    """MissingValueReviewer flags columns above the missingness threshold."""
    section = run_reviewer(MissingValueReviewer(), missing_df())

    assert section.id == "review.quality.missingness"
    assert section.severity is Severity.WARNING
    assert len(section.findings) == 1
    assert section.findings[0].column_name == "dirty"
    assert section.findings[0].severity == "warning"


def test_missing_value_reviewer_threshold_config() -> None:
    """MissingValueReviewer honors a configured threshold."""
    section = run_reviewer(MissingValueReviewer(), missing_df(), threshold=50.0)

    assert section.severity is Severity.PASSED
    assert section.findings == ()


def test_missing_value_reviewer_excludes_fully_empty_columns() -> None:
    """Fully empty columns are owned by schema health, not missing values."""
    df = pd.DataFrame({"normal": [1, 2, 3, 4, 5], "empty": [None] * 5})
    section = run_reviewer(MissingValueReviewer(), df)

    assert section.severity is Severity.PASSED
    assert section.findings == ()


def test_duplicate_reviewer_flags_duplicate_rows() -> None:
    """DuplicateReviewer flags datasets above the duplicate threshold."""
    section = run_reviewer(DuplicateReviewer(), duplicate_df())

    assert section.severity is Severity.WARNING
    assert len(section.findings) == 1
    assert section.findings[0].evidence["duplicate_percentage"] == 40.0


def test_duplicate_reviewer_threshold_config() -> None:
    """DuplicateReviewer honors a configured threshold."""
    section = run_reviewer(DuplicateReviewer(), duplicate_df(), threshold=50.0)

    assert section.severity is Severity.PASSED
    assert section.findings == ()


def test_constant_reviewer_flags_constant_columns() -> None:
    """ConstantColumnReviewer flags constant but not fully empty columns."""
    section = run_reviewer(ConstantColumnReviewer(), constant_df())

    assert section.severity is Severity.WARNING
    assert [f.column_name for f in section.findings] == ["const"]


def test_constant_reviewer_clean() -> None:
    """ConstantColumnReviewer passes a dataset with no constant columns."""
    section = run_reviewer(ConstantColumnReviewer(), clean_df())

    assert section.severity is Severity.PASSED
    assert section.findings == ()


def test_cardinality_reviewer_flags_high_cardinality() -> None:
    """CardinalityReviewer flags high-ratio categorical columns."""
    section = run_reviewer(
        CardinalityReviewer(), high_cardinality_df(), threshold=0.30, min_cardinality=5
    )

    assert section.severity is Severity.WARNING
    assert [f.column_name for f in section.findings] == ["cat"]


def test_cardinality_reviewer_clean() -> None:
    """CardinalityReviewer passes when unique ratio stays under the threshold."""
    section = run_reviewer(
        CardinalityReviewer(), high_cardinality_df(), threshold=0.90, min_cardinality=5
    )

    assert section.severity is Severity.PASSED
    assert section.findings == ()


def test_schema_health_flags_fully_empty_columns() -> None:
    """SchemaHealthReviewer surfaces fully empty columns as critical."""
    section = run_reviewer(SchemaHealthReviewer(), constant_df())

    assert section.severity is Severity.CRITICAL
    assert [f.column_name for f in section.findings] == ["empty"]


def test_schema_health_warns_on_empty_dataset() -> None:
    """SchemaHealthReviewer warns when the dataset has no rows."""
    section = run_reviewer(SchemaHealthReviewer(), empty_df())

    assert section.severity is Severity.WARNING
    assert section.findings[0].title == "Dataset has no rows"


def test_schema_health_warns_on_no_columns() -> None:
    """SchemaHealthReviewer warns when the dataset declares no columns."""
    section = run_reviewer(SchemaHealthReviewer(), pd.DataFrame())

    assert section.severity is Severity.WARNING
    titles = {f.title for f in section.findings}
    assert "Dataset has no rows" in titles
    assert "Dataset has no columns" in titles


def test_schema_health_clean() -> None:
    """SchemaHealthReviewer passes a healthy dataset."""
    section = run_reviewer(SchemaHealthReviewer(), clean_df())

    assert section.severity is Severity.PASSED
    assert section.findings == ()


def test_type_reviewer_flags_identifier_columns() -> None:
    """TypeReviewer flags all-distinct numeric columns as identifier-like."""
    section = run_reviewer(TypeReviewer(), identifier_df())

    assert section.severity is Severity.INFO
    assert [f.column_name for f in section.findings] == ["id"]


def test_type_reviewer_flags_text_columns() -> None:
    """TypeReviewer flags free-text columns."""
    section = run_reviewer(TypeReviewer(), text_df())

    assert section.severity is Severity.INFO
    assert section.findings[0].column_name == "txt"
    assert section.findings[0].title == "Text column 'txt'"


def test_type_reviewer_clean() -> None:
    """TypeReviewer passes when no type misuse is detected."""
    section = run_reviewer(TypeReviewer(), clean_df())

    assert section.severity is Severity.PASSED
    assert section.findings == ()


def test_basic_statistics_reviewer_flags_skew() -> None:
    """BasicStatisticsReviewer flags highly skewed numeric columns."""
    section = run_reviewer(BasicStatisticsReviewer(), skewed_df())

    assert section.severity is Severity.WARNING
    assert section.findings[0].column_name == "s"
    assert "skewness" in section.findings[0].evidence


def test_basic_statistics_reviewer_clean() -> None:
    """BasicStatisticsReviewer passes well-behaved numeric columns."""
    section = run_reviewer(BasicStatisticsReviewer(), clean_df())

    assert section.severity is Severity.PASSED
    assert section.findings == ()


def test_basic_statistics_reviewer_threshold_config() -> None:
    """BasicStatisticsReviewer honors configured thresholds."""
    section = run_reviewer(
        BasicStatisticsReviewer(),
        skewed_df(),
        skew_threshold=100.0,
        kurtosis_threshold=100.0,
    )

    assert section.findings == ()
