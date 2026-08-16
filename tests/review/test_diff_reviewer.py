"""Unit tests for the DiffReviewer."""

from __future__ import annotations

from typing import Any

import pandas as pd

import featuresmith as fs
from featuresmith.core.dataset import Dataset
from featuresmith.diff.schema import DatasetDiffResult
from featuresmith.review.context import ReviewConfig, ReviewContext
from featuresmith.review.reviewers.diff import DiffReviewer
from featuresmith.review.schema import ReviewCategory, Severity


def _context(
    current_df: pd.DataFrame,
    previous_df: pd.DataFrame | None,
    *,
    target_column: str | None = None,
) -> ReviewContext:
    """Build a ReviewContext with optional previous profile."""
    dataset: Dataset = fs.load(current_df)
    profile = fs.profile(dataset)
    previous_profile = fs.profile(previous_df) if previous_df is not None else None
    return ReviewContext(
        profile=profile,
        dataset=dataset,
        config=ReviewConfig(target_column=target_column),
        previous_profile=previous_profile,
    )


def test_diff_reviewer_identity() -> None:
    """DiffReviewer declares the diff category and requires a previous snapshot."""
    reviewer = DiffReviewer()

    assert reviewer.id == "review.diff"
    assert reviewer.category is ReviewCategory.DIFF
    assert reviewer.requires_previous_snapshot is True
    assert reviewer.title == "Dataset Diff"


def test_diff_reviewer_applicable_only_with_previous() -> None:
    """applicable() is True only when a previous profile exists."""
    reviewer = DiffReviewer()
    current = pd.DataFrame({"a": [1, 2, 3]})

    assert reviewer.applicable(_context(current, None)) is False
    assert reviewer.applicable(_context(current, current.copy())) is True


def test_diff_reviewer_identical_snapshots_pass() -> None:
    """Two identical snapshots produce a passed section with no findings."""
    reviewer = DiffReviewer()
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    section = reviewer.review(_context(df, df.copy()))

    assert section.id == "review.diff"
    assert section.category is ReviewCategory.DIFF
    assert section.severity is Severity.PASSED
    assert section.findings == ()


def test_diff_reviewer_flags_regressions() -> None:
    """A removed column surfaces as a warning finding in the diff section."""
    reviewer = DiffReviewer()
    old = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new = pd.DataFrame({"a": [1, 2, 3]})

    section = reviewer.review(_context(new, old))

    assert section.severity is Severity.WARNING
    rule_ids = {finding.rule_id for finding in section.findings}
    assert "diff.schema.removed_columns" in rule_ids
    assert all(finding.category == "diff" for finding in section.findings)


def test_diff_reviewer_exposes_diff_result() -> None:
    """The computed DatasetDiffResult is exposed for ReviewResult attachment."""
    reviewer = DiffReviewer()
    old = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new = pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]})

    assert reviewer.diff_result is None
    reviewer.review(_context(new, old))

    assert isinstance(reviewer.diff_result, DatasetDiffResult)
    assert reviewer.diff_result.schema.added_columns == ("c",)
    assert reviewer.diff_result.schema.removed_columns == ("b",)


def test_diff_reviewer_with_target_column() -> None:
    """A target column enables the leakage comparison in the diff."""
    reviewer = DiffReviewer()
    old = pd.DataFrame({"target": [1, 2, 3, 4, 5], "a": [10, 20, 30, 40, 50]})
    new = pd.DataFrame({"target": [1, 2, 3, 4, 5], "leak": [1, 2, 3, 4, 5]})

    section = reviewer.review(_context(new, old, target_column="target"))

    rule_ids = {finding.rule_id for finding in section.findings}
    assert "diff.leakage.new" in rule_ids
    assert reviewer.diff_result is not None
    assert reviewer.diff_result.leakage is not None
    assert reviewer.diff_result.summary.leakage_new == 1


def test_diff_reviewer_is_deterministic() -> None:
    """Repeated reviews over the same snapshots produce identical output."""
    reviewer = DiffReviewer()
    old = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    new = pd.DataFrame({"a": [1, 2, 3, 4], "c": [1, 2, 3, 4]})

    first = reviewer.review(_context(new, old))
    second = reviewer.review(_context(new, old))

    assert _without_finding_ids(first.to_dict()) == _without_finding_ids(
        second.to_dict()
    )
    assert reviewer.diff_result is not None
    assert reviewer.diff_result.to_dict() == reviewer.diff_result.to_dict()


def _without_finding_ids(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a deep copy with volatile finding IDs removed for comparison."""
    import copy

    cleaned = copy.deepcopy(payload)
    for finding in cleaned["findings"]:
        finding.pop("id", None)
    return cleaned


def test_diff_reviewer_never_reprofiles_previous() -> None:
    """The reviewer reads the previous profile from context, never re-profiles."""
    reviewer = DiffReviewer()
    old = pd.DataFrame({"a": [1, 2, 3]})
    new = pd.DataFrame({"a": [1, 2, 3, 4]})
    context = _context(new, old)

    # The previous profile is exactly the one supplied in the context.
    reviewer.review(context)

    assert reviewer.diff_result is not None
    assert reviewer.diff_result.structure.previous_row_count == 3
    assert reviewer.diff_result.structure.row_count == 4


def test_diff_reviewer_config_validation() -> None:
    """reviewer_config for the diff reviewer is accepted by the engine."""
    old = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]})
    new = pd.DataFrame({"a": [1.0, None, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]})

    result = fs.review(
        new,
        previous=old,
        reviewer_config={"review.diff": {"missing_change_threshold": 15.0}},
    )

    diff_section = next(
        section for section in result.sections if section.id == "review.diff"
    )
    assert diff_section.severity is Severity.PASSED
