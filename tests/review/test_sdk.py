"""Tests for the public fs.review() SDK entrypoint."""

from __future__ import annotations

import json

import pandas as pd
import polars as pl

import featuresmith as fs
from featuresmith.review.schema import ReviewResult


def test_review_dataframe_returns_review_result() -> None:
    """fs.review() works on an in-memory dataframe with the built-in reviewers."""
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": [2.0, 1.0, 3.0, 5.0, 4.0]})

    result = fs.review(df)

    assert isinstance(result, ReviewResult)
    assert len(result.sections) == 9
    assert result.overall_summary == (
        "9 of 9 sections passed with 0 finding(s) identified across the review."
    )
    assert result.dataset_summary.row_count == 5
    assert result.dataset_summary.column_count == 2
    assert result.score is not None
    assert result.score.overall == 100.0
    assert len(result.score.dimensions) == 7


def test_review_polars_dataframe() -> None:
    """fs.review() accepts a Polars dataframe."""
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    result = fs.review(df)

    assert result.dataset_summary.row_count == 3
    assert len(result.sections) == 9


def test_review_dataset_object() -> None:
    """fs.review() accepts a pre-loaded Dataset."""
    df = pd.DataFrame({"a": [1, 2, 3]})
    dataset = fs.load(df)

    result = fs.review(dataset)

    assert result.dataset_summary.row_count == 3


def test_review_result_is_json_serializable() -> None:
    """ReviewResult serializes to clean JSON through the SDK."""
    # Use a dataset that doesn't trigger feature quality warnings (no perfect correlation)
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 6, 5]})

    data = fs.review(df).to_dict()

    serialized = json.dumps(data)
    parsed = json.loads(serialized)
    assert parsed["engine_version"] == "0.4.0"
    assert len(parsed["sections"]) == 9
    assert all(section["severity"] == "passed" for section in parsed["sections"])
    assert "overall_summary" in parsed
    assert parsed["score"]["overall"] == 100.0
    assert len(parsed["score"]["dimensions"]) == 7


def test_review_previous_activates_diff_section() -> None:
    """Diff-aware review activates the diff section against a prior snapshot."""
    old_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new_df = pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]})

    result = fs.review(new_df, previous=old_df)

    assert isinstance(result, ReviewResult)
    assert len(result.sections) == 10
    diff_section = next(
        section for section in result.sections if section.category.value == "diff"
    )
    assert diff_section.id == "review.diff"
    assert diff_section.findings
    assert result.diff is not None
    assert result.diff.schema.added_columns == ("c",)
    assert result.diff.schema.removed_columns == ("b",)


def test_review_without_previous_has_no_diff_section() -> None:
    """A single-dataset review never includes a diff section or diff output."""
    df = pd.DataFrame({"a": [1, 2, 3]})

    result = fs.review(df)

    assert all(section.category.value != "diff" for section in result.sections)
    assert result.diff is None


def test_review_previous_polars_dataframe() -> None:
    """Diff-aware review accepts a Polars previous snapshot."""
    old_df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    new_df = pl.DataFrame({"a": [1, 2, 3, 4], "b": ["x", "y", "z", "w"]})

    result = fs.review(new_df, previous=old_df)

    assert result.diff is not None
    assert result.diff.structure.rows_added == 1
