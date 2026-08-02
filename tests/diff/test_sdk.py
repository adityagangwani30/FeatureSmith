"""Tests for the public fs.diff() SDK entrypoint."""

from __future__ import annotations

import json

import pandas as pd
import polars as pl

import featuresmith as fs
from featuresmith.diff.schema import DatasetDiffResult


def test_diff_pandas_dataframes() -> None:
    """fs.diff() works on two in-memory pandas dataframes."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new = pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]})

    result = fs.diff(old, new)

    assert isinstance(result, DatasetDiffResult)
    assert result.schema.added_columns == ("c",)
    assert result.schema.removed_columns == ("b",)


def test_diff_polars_dataframes() -> None:
    """fs.diff() accepts two Polars dataframes."""
    old = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    new = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    result = fs.diff(old, new)

    assert result.summary.overall_health == "unchanged"
    assert result.schema.changed is False


def test_diff_dataset_objects() -> None:
    """fs.diff() accepts pre-loaded Dataset objects."""
    old_df = pd.DataFrame({"a": [1, 2, 3]})
    new_df = pd.DataFrame({"a": [1, 2, 3, 4]})
    old = fs.load(old_df)
    new = fs.load(new_df)

    result = fs.diff(old, new)

    assert result.structure.rows_added == 1


def test_diff_result_is_json_serializable() -> None:
    """DatasetDiffResult serializes to JSON through the SDK."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new = pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]})

    data = fs.diff(old, new).to_dict()

    serialized = json.dumps(data)
    parsed = json.loads(serialized)
    assert parsed["version"] == "0.1.0"
    assert parsed["schema"]["added_columns"] == ["c"]
    assert parsed["summary"]["overall_health"] == "regressed"


def test_diff_with_target_column_runs_leakage() -> None:
    """Passing a target column enables the leakage comparison."""
    old = pd.DataFrame({"target": [1, 2, 3, 4, 5], "a": [10, 20, 30, 40, 50]})
    new = pd.DataFrame({"target": [1, 2, 3, 4, 5], "leak": [1, 2, 3, 4, 5]})

    result = fs.diff(old, new, target_column="target")

    assert result.leakage is not None
    assert result.leakage.changed is True
    assert result.summary.leakage_new == 1


def test_diff_findings_accessor() -> None:
    """diff_findings() maps a diff to shared RuleFinding objects."""
    from featuresmith.api import diff_findings

    old = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new = pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]})

    result = fs.diff(old, new)
    findings = diff_findings(result)

    assert any(finding.rule_id == "diff.schema.removed_columns" for finding in findings)
    assert all(finding.category == "diff" for finding in findings)


def test_diff_exports_from_root_package() -> None:
    """The root package exposes diff as a first-class SDK entrypoint."""
    assert callable(fs.diff)
