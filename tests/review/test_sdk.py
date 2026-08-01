"""Tests for the public fs.review() SDK entrypoint."""

from __future__ import annotations

import json

import pandas as pd
import polars as pl
import pytest

import featuresmith as fs
from featuresmith.review.schema import ReviewResult


def test_review_dataframe_returns_review_result() -> None:
    """fs.review() works on an in-memory dataframe with zero reviewers."""
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": [1.0, 2.0, 3.0, 4.0, 5.0]})

    result = fs.review(df)

    assert isinstance(result, ReviewResult)
    assert result.sections == ()
    assert result.overall_summary == "Review complete: no reviewers ran."
    assert result.dataset_summary.row_count == 5
    assert result.dataset_summary.column_count == 2


def test_review_polars_dataframe() -> None:
    """fs.review() accepts a Polars dataframe."""
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    result = fs.review(df)

    assert result.dataset_summary.row_count == 3
    assert result.sections == ()


def test_review_dataset_object() -> None:
    """fs.review() accepts a pre-loaded Dataset."""
    df = pd.DataFrame({"a": [1, 2, 3]})
    dataset = fs.load(df)

    result = fs.review(dataset)

    assert result.dataset_summary.row_count == 3


def test_review_result_is_json_serializable() -> None:
    """ReviewResult serializes to clean JSON through the SDK."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    data = fs.review(df).to_dict()

    serialized = json.dumps(data)
    parsed = json.loads(serialized)
    assert parsed["engine_version"] == "0.1.0"
    assert parsed["sections"] == []
    assert "overall_summary" in parsed


def test_review_previous_not_implemented() -> None:
    """Diff-aware review raises NotImplementedError for now."""
    df = pd.DataFrame({"a": [1, 2, 3]})

    with pytest.raises(NotImplementedError, match="not available yet"):
        fs.review(df, previous="train_v1.csv")
