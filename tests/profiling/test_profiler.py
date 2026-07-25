"""Comprehensive tests for the data profiling engine."""

from __future__ import annotations

import math
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import polars as pl
import pytest

import featuresmith as fs
from featuresmith.core.profile_result import ProfileResult
from featuresmith.profiling import profile_dataset
from featuresmith.profiling.summary import classify_logical_type


@pytest.fixture
def sample_pandas_df() -> pd.DataFrame:
    """Create a pandas DataFrame with mixed logical types."""
    return pd.DataFrame(
        {
            "num_col": [1.0, 2.0, -1.0, 0.0, None],
            "cat_col": ["apple", "banana", "apple", "cherry", None],
            "date_col": pd.to_datetime(
                ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", None]
            ),
            "text_col": [
                "This is a longer text paragraph that serves as a text column.",
                "Another sentence in the dataset to make it qualify as text.",
                "Short text here.",
                "   ",  # whitespace-only
                "",  # empty string
            ],
        }
    )


@pytest.fixture
def sample_polars_df() -> pl.DataFrame:
    """Create a Polars DataFrame with mixed logical types."""
    return pl.DataFrame(
        {
            "num_col": [1.0, 2.0, -1.0, 0.0, None],
            "cat_col": ["apple", "banana", "apple", "cherry", None],
            "date_col": [
                datetime(2026, 1, 1),
                datetime(2026, 1, 2),
                datetime(2026, 1, 3),
                datetime(2026, 1, 4),
                None,
            ],
            "text_col": [
                "This is a longer text paragraph that serves as a text column.",
                "Another sentence in the dataset to make it qualify as text.",
                "Short text here.",
                "   ",  # whitespace-only
                "",  # empty string
            ],
        }
    )


def test_logical_type_classification(
    sample_pandas_df: pd.DataFrame, sample_polars_df: pl.DataFrame
) -> None:
    """Test logical type classification for both backends."""
    ds_pd = fs.load(sample_pandas_df)
    ds_pl = fs.load(sample_polars_df)

    assert classify_logical_type(ds_pd, "num_col") == "numeric"
    assert classify_logical_type(ds_pl, "num_col") == "numeric"

    assert classify_logical_type(ds_pd, "cat_col") == "categorical"
    assert classify_logical_type(ds_pl, "cat_col") == "categorical"

    assert classify_logical_type(ds_pd, "date_col") == "datetime"
    assert classify_logical_type(ds_pl, "date_col") == "datetime"

    assert classify_logical_type(ds_pd, "text_col") == "text"
    assert classify_logical_type(ds_pl, "text_col") == "text"


def test_numeric_profiling_parity(
    sample_pandas_df: pd.DataFrame, sample_polars_df: pl.DataFrame
) -> None:
    """Test that numeric profiling computes correct stats and matches between backends."""
    res_pd = fs.profile(sample_pandas_df)
    res_pl = fs.profile(sample_polars_df)

    for res in (res_pd, res_pl):
        p = res.numeric_profiles["num_col"]
        assert p.count == 4
        assert p.missing_count == 1
        assert p.missing_percentage == 20.0
        assert p.unique_count == 4
        assert p.mean == 0.5
        assert p.median == 0.5
        assert p.minimum == -1.0
        assert p.maximum == 2.0
        assert p.range == 3.0
        assert p.sum == 2.0
        assert p.zero_count == 1
        assert p.negative_count == 1
        assert p.positive_count == 2
        # variance: mean=0.5. diffs: (0.5)^2 + (1.5)^2 + (-1.5)^2 + (-0.5)^2 = 0.25 + 2.25 + 2.25 + 0.25 = 5.0. ddof=1: 5.0 / 3 = 1.666...
        assert p.variance is not None and math.isclose(p.variance, 5.0 / 3)
        assert p.std_dev is not None and math.isclose(p.std_dev, math.sqrt(5.0 / 3))


def test_categorical_profiling_parity(
    sample_pandas_df: pd.DataFrame, sample_polars_df: pl.DataFrame
) -> None:
    """Test categorical column profiling."""
    res_pd = fs.profile(sample_pandas_df)
    res_pl = fs.profile(sample_polars_df)

    for res in (res_pd, res_pl):
        p = res.categorical_profiles["cat_col"]
        assert p.cardinality == 3
        assert p.missing_count == 1
        assert p.frequency_table == {"apple": 2, "banana": 1, "cherry": 1}
        assert p.top_values == [("apple", 2), ("banana", 1), ("cherry", 1)]
        assert p.most_common_category == "apple"

        # Entropy check: p1 = 0.5, p2 = 0.25, p3 = 0.25
        # - (0.5 * log2(0.5) + 0.25 * log2(0.25) * 2) = - (0.5 * -1 + 0.25 * -2 * 2) = - (-0.5 - 1.0) = 1.5
        assert p.entropy is not None and math.isclose(p.entropy, 1.5)


def test_datetime_profiling_parity(
    sample_pandas_df: pd.DataFrame, sample_polars_df: pl.DataFrame
) -> None:
    """Test datetime column profiling."""
    res_pd = fs.profile(sample_pandas_df)
    res_pl = fs.profile(sample_polars_df)

    for res in (res_pd, res_pl):
        p = res.datetime_profiles["date_col"]
        assert p.missing_count == 1
        assert (
            p.minimum == "2026-01-01T00:00:00"
            or p.minimum == "2026-01-01T00:00:00Z"
            or p.minimum.startswith("2026-01-01")
        )
        assert (
            p.maximum == "2026-01-04T00:00:00"
            or p.maximum == "2026-01-04T00:00:00Z"
            or p.maximum.startswith("2026-01-04")
        )
        assert p.range_days == 3.0


def test_text_profiling_parity(
    sample_pandas_df: pd.DataFrame, sample_polars_df: pl.DataFrame
) -> None:
    """Test text column profiling."""
    res_pd = fs.profile(sample_pandas_df)
    res_pl = fs.profile(sample_polars_df)

    for res in (res_pd, res_pl):
        p = res.text_profiles["text_col"]
        assert res.column_profiles["text_col"].missing_count == 0
        assert p.empty_strings == 1
        assert p.whitespace_only == 1
        # Word counts split on whitespace (\S+ tokens — punctuation stays attached):
        # Row 1: "This is a longer text paragraph that serves as a text column." -> 12 tokens
        # Row 2: "Another sentence in the dataset to make it qualify as text." -> 11 tokens
        # Row 3: "Short text here." -> 3 tokens
        # Row 4: "   " -> 0 tokens
        # Row 5: "" -> 0 tokens
        # Total = 12 + 11 + 3 = 26
        assert p.word_count == 26


def test_duplicates_and_constants() -> None:
    """Test duplicate row counts and constant columns detection."""
    df = pd.DataFrame(
        {
            "const": [1, 1, 1, 1],
            "empty": [None, None, None, None],
            "normal": [1, 2, 1, 2],
            "val": ["a", "b", "a", "b"],
        }
    )

    # Rows 0 and 2 are identical (1, None, 1, a)
    # Rows 1 and 3 are identical (1, None, 2, b)
    # So duplicate rows = 2
    res_pd = fs.profile(df)
    res_pl = fs.profile(
        pl.DataFrame(
            {
                "const": [1, 1, 1, 1],
                "empty": [None, None, None, None],
                "normal": [1, 2, 1, 2],
                "val": ["a", "b", "a", "b"],
            }
        )
    )

    for res in (res_pd, res_pl):
        assert res.duplicate_summary.duplicate_rows_count == 2
        assert res.duplicate_summary.duplicate_percentage == 50.0
        assert "const" in res.duplicate_summary.constant_columns
        assert "empty" in res.duplicate_summary.constant_columns
        assert "empty" in res.duplicate_summary.fully_empty_columns
        assert "normal" not in res.duplicate_summary.constant_columns


def test_correlations() -> None:
    """Test Pearson correlation matrix."""
    df = pd.DataFrame(
        {
            "a": [1.0, 2.0, 3.0, 4.0],
            "b": [2.0, 4.0, 6.0, 8.0],  # perfectly correlated with a (1.0)
            "c": [4.0, 3.0, 2.0, 1.0],  # perfectly anti-correlated with a (-1.0)
            "d": [1.0, 5.0, 2.0, 9.0],
        }
    )

    res = fs.profile(df)
    pearson = res.correlation_summary.pearson

    assert math.isclose(pearson["a"]["b"], 1.0)
    assert math.isclose(pearson["a"]["c"], -1.0)
    assert pearson["a"]["d"] is not None


def test_correlation_capping() -> None:
    """Test that correlation computation is capped correctly."""
    data = {f"col_{i}": list(range(5)) for i in range(10)}
    df = pd.DataFrame(data)

    # Cap at 5 columns
    dataset = fs.load(df)
    res = profile_dataset(dataset, max_correlation_columns=5)

    assert len(res.correlation_summary.pearson) == 5
    assert "col_0" in res.correlation_summary.pearson
    assert "col_4" in res.correlation_summary.pearson
    assert "col_5" not in res.correlation_summary.pearson


def test_empty_dataset() -> None:
    """Test profiling an empty dataset (0 rows)."""
    df = pd.DataFrame(columns=["a", "b"], dtype=float)
    res = fs.profile(df)

    assert res.dataset_summary.row_count == 0
    assert res.dataset_summary.column_count == 2
    assert res.dataset_summary.num_numeric_columns == 2
    assert res.numeric_profiles["a"].count == 0
    assert res.numeric_profiles["a"].mean is None


def test_single_column_dataset() -> None:
    """Test profiling a dataset with only one column."""
    df = pd.DataFrame({"a": [1, 2, 3]})
    res = fs.profile(df)

    assert res.dataset_summary.column_count == 1
    assert "a" in res.numeric_profiles
    assert res.correlation_summary.pearson == {"a": {"a": 1.0}}


def test_serialize_to_dict() -> None:
    """Test that ProfileResult serializes to a raw dictionary of primitives."""
    df = pd.DataFrame({"num": [1, 2, None], "cat": ["x", "y", "x"]})
    res = fs.profile(df)
    d = res.to_dict()

    assert isinstance(d, dict)
    assert "dataset_summary" in d
    assert d["dataset_summary"]["row_count"] == 3
    assert d["column_profiles"]["num"]["logical_type"] == "numeric"
    assert d["column_profiles"]["cat"]["logical_type"] == "categorical"
