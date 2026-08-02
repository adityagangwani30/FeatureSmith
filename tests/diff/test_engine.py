"""Tests for the Dataset Diff Engine."""

from __future__ import annotations

from typing import Any

import pandas as pd

import featuresmith as fs
from featuresmith.diff.engine import compute_diff


def _profile(df: pd.DataFrame) -> Any:
    """Profile a pandas dataframe through the SDK."""
    return fs.profile(df)


def _diff(old_df: pd.DataFrame, new_df: pd.DataFrame, **kwargs: Any) -> Any:
    """Compute a diff from two dataframes."""
    return compute_diff(_profile(old_df), _profile(new_df), **kwargs)


def test_identical_datasets_no_changes() -> None:
    """Two identical snapshots produce an unchanged, finding-free diff."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    new = old.copy()

    result = _diff(old, new)

    assert result.schema.changed is False
    assert result.structure.rows_added == 0
    assert result.structure.rows_removed == 0
    assert result.structure.columns_added == 0
    assert result.structure.columns_removed == 0
    assert result.missing_values == ()
    assert result.duplicates.status == "unchanged"
    assert result.constant_columns.changed is False
    assert result.statistics == ()
    assert result.distributions == ()
    assert result.summary.overall_health == "unchanged"
    assert result.leakage is None


def test_rows_added() -> None:
    """Additional rows surface as rows_added with no schema change."""
    old = pd.DataFrame({"a": [1, 2, 3]})
    new = pd.DataFrame({"a": [1, 2, 3, 4]})

    result = _diff(old, new)

    assert result.structure.rows_added == 1
    assert result.structure.rows_removed == 0
    assert result.schema.changed is False
    assert result.summary.rows_added == 1


def test_rows_removed() -> None:
    """Removed rows surface as rows_removed."""
    old = pd.DataFrame({"a": [1, 2, 3, 4]})
    new = pd.DataFrame({"a": [1, 2]})

    result = _diff(old, new)

    assert result.structure.rows_added == 0
    assert result.structure.rows_removed == 2
    assert result.summary.rows_removed == 2


def test_added_column() -> None:
    """A new column surfaces in schema.added_columns."""
    old = pd.DataFrame({"a": [1, 2, 3]})
    new = pd.DataFrame({"a": [1, 2, 3], "c": [4, 5, 6]})

    result = _diff(old, new)

    assert result.schema.added_columns == ("c",)
    assert result.schema.removed_columns == ()
    assert result.summary.columns_added == 1


def test_removed_column() -> None:
    """A dropped column surfaces in schema.removed_columns."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new = pd.DataFrame({"a": [1, 2, 3]})

    result = _diff(old, new)

    assert result.schema.removed_columns == ("b",)
    assert result.summary.columns_removed == 1
    assert result.summary.overall_health == "regressed"


def test_renamed_column_detected() -> None:
    """A column renamed with identical values is detected deterministically."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    new = pd.DataFrame({"c": [1, 2, 3], "b": ["x", "y", "z"]})

    result = _diff(old, new)

    renames = [
        (rename.previous_name, rename.name) for rename in result.schema.renamed_columns
    ]
    assert renames == [("a", "c")]
    assert result.schema.added_columns == ()
    assert result.schema.removed_columns == ()
    assert result.summary.columns_renamed == 1


def test_dtype_change_detected() -> None:
    """A shared column whose dtype changes surfaces as a type change."""
    old = pd.DataFrame({"a": [1, 2, 3]})
    new = pd.DataFrame({"a": ["1", "2", "3"]})

    result = _diff(old, new)

    assert result.schema.type_changes
    assert result.schema.type_changes[0].column == "a"
    assert result.summary.type_changes == 1


def test_missing_values_regression() -> None:
    """Newly-introduced missingness is a regression."""
    old = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0]})
    new = pd.DataFrame({"a": [1.0, None, None, 4.0]})

    result = _diff(old, new)

    assert result.missing_values
    assert result.missing_values[0].status == "new"
    assert result.summary.missing_values_increased == 1
    assert result.summary.overall_health == "regressed"


def test_missing_values_improvement() -> None:
    """Resolved missingness is an improvement."""
    old = pd.DataFrame({"a": [1.0, None, None, 4.0]})
    new = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0]})

    result = _diff(old, new)

    assert result.missing_values
    assert result.missing_values[0].status == "resolved"
    assert result.summary.missing_values_decreased == 1
    assert result.summary.overall_health == "improved"


def test_duplicates_regression() -> None:
    """A rising duplicate rate is a regression."""
    old = pd.DataFrame({"a": [1, 2, 3, 4], "b": ["w", "x", "y", "z"]})
    new = pd.DataFrame({"a": [1, 1, 1, 1], "b": ["w", "w", "w", "w"]})

    result = _diff(old, new)

    assert result.duplicates.status == "regressed"
    assert result.summary.duplicate_rows_increased is True
    assert result.summary.overall_health == "regressed"


def test_newly_constant_column() -> None:
    """A shared column that became constant is flagged."""
    old = pd.DataFrame({"a": [1, 2, 3, 4]})
    new = pd.DataFrame({"a": [5, 5, 5, 5]})

    result = _diff(old, new)

    assert result.constant_columns.newly_constant == ("a",)
    assert result.summary.newly_constant_columns == 1
    assert result.summary.overall_health == "regressed"


def test_no_longer_constant_column() -> None:
    """A constant column that gained variance is flagged as improved."""
    old = pd.DataFrame({"a": [5, 5, 5, 5]})
    new = pd.DataFrame({"a": [1, 2, 3, 4]})

    result = _diff(old, new)

    assert result.constant_columns.no_longer_constant == ("a",)
    assert result.summary.no_longer_constant_columns == 1


def test_statistics_and_distribution_changes() -> None:
    """Changed basic statistics and mean shifts are captured."""
    old = pd.DataFrame({"a": [1.0, 2.0, 3.0]})
    new = pd.DataFrame({"a": [100.0, 200.0, 300.0]})

    result = _diff(old, new)

    statistics = {entry.statistic: entry for entry in result.statistics}
    assert "mean" in statistics
    assert statistics["mean"].previous == 2.0
    assert statistics["mean"].current == 200.0
    assert result.distributions
    assert result.distributions[0].column == "a"
    assert result.distributions[0].significant is True


def test_empty_datasets() -> None:
    """Empty snapshots diff without errors and report no changes."""
    old = pd.DataFrame()
    new = pd.DataFrame()

    result = _diff(old, new)

    assert result.schema.changed is False
    assert result.structure.row_count == 0
    assert result.summary.overall_health == "unchanged"


def test_worse_dataset_is_regressed() -> None:
    """A dataset with more missingness and duplicates is a regression."""
    old = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0], "b": ["w", "x", "y", "z"]})
    new = pd.DataFrame({"a": [None, None, None, 4.0], "b": ["w", "w", "w", "w"]})

    result = _diff(old, new)

    assert result.summary.overall_health == "regressed"
    assert "regressed" in result.summary.recommendation


def test_better_dataset_is_improved() -> None:
    """A dataset with fewer duplicates and no missingness is an improvement."""
    old = pd.DataFrame({"a": [None, None, 3.0, 4.0], "b": ["w", "w", "y", "y"]})
    new = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0], "b": ["w", "x", "y", "z"]})

    result = _diff(old, new)

    assert result.summary.overall_health == "improved"
    assert "improved" in result.summary.recommendation


def test_leakage_new_removed_and_unchanged() -> None:
    """Leakage deltas classify new, removed, and unchanged columns."""
    old = pd.DataFrame({"target": [1, 2, 3, 4, 5], "a": [10, 20, 30, 40, 50]})
    new = pd.DataFrame({"target": [1, 2, 3, 4, 5], "leak": [1, 2, 3, 4, 5]})

    result = _diff(old, new, target_column="target")

    assert result.leakage is not None
    statuses = {entry.column: entry.status for entry in result.leakage.columns}
    assert statuses["leak"] == "new"
    assert statuses["a"] == "removed"
    assert result.summary.leakage_new == 1
    assert result.summary.leakage_removed == 1

    same = _diff(old, old, target_column="target")
    assert same.leakage is not None
    assert all(entry.status == "unchanged" for entry in same.leakage.columns)


def test_leakage_skipped_without_target() -> None:
    """No target column means no leakage comparison runs."""
    old = pd.DataFrame({"target": [1, 2, 3], "leak": [1, 2, 3]})
    new = pd.DataFrame({"target": [1, 2, 3], "leak": [1, 2, 3]})

    result = _diff(old, new)

    assert result.leakage is None


def test_unknown_target_column_is_ignored_by_leakage() -> None:
    """An absent target column does not crash the leakage comparison."""
    old = pd.DataFrame({"a": [1, 2, 3]})
    new = pd.DataFrame({"a": [1, 2, 3]})

    result = _diff(old, new, target_column="bogus")

    assert result.leakage is not None
    assert result.leakage.columns == ()


def test_diff_is_deterministic() -> None:
    """Repeated diffs over the same snapshots produce identical output."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    new = pd.DataFrame({"a": [1, 2, 3, 4], "c": [1, 2, 3, 4]})

    first = _diff(old, new)
    second = _diff(old, new)

    assert first.to_dict() == second.to_dict()


def test_renamed_column_is_deterministic() -> None:
    """Rename detection returns a stable result across repeated runs."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    new = pd.DataFrame({"c": [1, 2, 3], "b": ["x", "y", "z"]})

    first = _diff(old, new)
    second = _diff(old, new)

    assert first.schema.renamed_columns == second.schema.renamed_columns


def test_diff_config_thresholds_are_respected() -> None:
    """A tiny missingness delta stays below the configured threshold."""
    from featuresmith.diff.schema import DiffConfig

    old = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]})
    new = pd.DataFrame({"a": [1.0, None, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]})

    result = _diff(old, new, config=DiffConfig(missing_change_threshold=15.0))

    assert result.summary.missing_values_increased == 0


def test_default_config_detects_small_missingness_delta() -> None:
    """The default threshold still flags a meaningful missingness delta."""
    old = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]})
    new = pd.DataFrame({"a": [1.0, None, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]})

    result = _diff(old, new)

    assert result.summary.missing_values_increased == 1


def test_descriptive_summary_line() -> None:
    """The one-line roll-up summarizes rows, columns, and health."""
    old = pd.DataFrame({"a": [1, 2, 3]})
    new = pd.DataFrame({"a": [1, 2, 3, 4], "c": [1, 2, 3, 4]})

    result = _diff(old, new)

    assert "Rows 0 removed, 1 added" in result.overall_summary
    assert "columns 0 removed, 1 added" in result.overall_summary
    assert "overall health:" in result.overall_summary
