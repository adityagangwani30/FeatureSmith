"""Edge-case and smoke test suite for Featuresmith profiling and rules engine."""

import numpy as np
import pandas as pd
import polars as pl
import pytest

import featuresmith as fs
from featuresmith.core.exceptions import ConnectorError


def test_edge_wide_dataset() -> None:
    """Edge-case test with a very wide dataset (500 columns)."""
    np.random.seed(42)
    num_cols = 500
    num_rows = 100

    # Generate wide data
    data = {f"col_{i}": np.random.randn(num_rows) for i in range(num_cols)}
    df = pd.DataFrame(data)

    # Analyze - should complete successfully (capping correlation columns)
    result = fs.analyze(df, max_correlation_columns=50)

    assert len(result.findings) >= 0
    assert result.profile.dataset_summary.column_count == num_cols
    assert result.profile.dataset_summary.row_count == num_rows


def test_edge_tall_dataset() -> None:
    """Edge-case test with a very tall dataset (100K rows)."""
    np.random.seed(42)
    num_rows = 100000

    df = pd.DataFrame(
        {
            "numeric_col": np.random.normal(size=num_rows),
            "cat_col": np.random.choice(["A", "B", "C"], size=num_rows),
            "const_col": ["static"] * num_rows,
        }
    )

    result = fs.analyze(df)

    assert len(result.findings) >= 0
    assert result.profile.dataset_summary.row_count == num_rows


def test_edge_empty_dataset() -> None:
    """Edge-case test with an empty dataset (0 rows, headers only)."""
    df = pd.DataFrame(columns=["a", "b", "c"])

    # Analyze empty dataset should not crash
    result = fs.analyze(df)

    assert result.profile.dataset_summary.row_count == 0
    assert result.profile.dataset_summary.column_count == 3


def test_edge_single_column() -> None:
    """Edge-case test with a single column dataset."""
    df = pd.DataFrame({"single": [1, 2, 3, 4, 5]})
    result = fs.analyze(df)

    assert result.profile.dataset_summary.column_count == 1
    assert "single" in result.profile.column_profiles


def test_edge_missing_heavy() -> None:
    """Edge-case test with 100% missing values in some columns."""
    df = pd.DataFrame(
        {
            "all_null": [None] * 100,
            "mostly_null": [1] + [None] * 99,
            "valid": list(range(100)),
        }
    )

    result = fs.analyze(df)
    findings_rule_ids = [f.rule_id for f in result.findings]

    # fully empty rule triggers critical on all_null
    assert "quality.fully_empty_columns" in findings_rule_ids
    # missing value threshold triggers warning on mostly_null
    assert "quality.missing_value_threshold" in findings_rule_ids


def test_edge_duplicate_heavy() -> None:
    """Edge-case test with extreme duplicates (99% duplicated rows)."""
    df = pd.DataFrame({"a": [1] * 100, "b": [2] * 100})

    result = fs.analyze(df)
    findings_rule_ids = [f.rule_id for f in result.findings]

    assert "quality.duplicate_rows" in findings_rule_ids
    assert "quality.constant_columns" in findings_rule_ids


def test_edge_mixed_dataframe_backends() -> None:
    """Edge-case test mixed pandas/Polars DataFrame loading."""
    df_pd = pd.DataFrame({"x": [1, 2, 3]})
    df_pl = pl.DataFrame({"x": [1, 2, 3]})

    dataset_pd = fs.load(df_pd)
    dataset_pl = fs.load(df_pl)

    assert dataset_pd.row_count == 3
    assert dataset_pl.row_count == 3


def test_edge_unsupported_excel_format() -> None:
    """Edge-case test invalid file extensions in load connector."""
    with pytest.raises(ConnectorError):
        fs.load("invalid_path.txt")
