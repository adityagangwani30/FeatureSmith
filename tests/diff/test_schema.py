"""Tests for the Dataset Diff output schemas."""

from __future__ import annotations

import json

from featuresmith.diff.schema import (
    DIFF_ENGINE_VERSION,
    ConstantColumnDiff,
    DatasetDiffResult,
    DatasetDiffSummary,
    DiffConfig,
    DuplicateDiff,
    LeakageColumnDiff,
    LeakageDiff,
    MissingValueDiff,
    SchemaDiff,
    StructureDiff,
)


def test_diff_config_defaults() -> None:
    """DiffConfig carries the documented default thresholds."""
    config = DiffConfig()

    assert config.distribution_shift_threshold == 0.10
    assert config.missing_change_threshold == 1.0
    assert config.duplicate_change_threshold == 1.0
    assert config.numeric_tolerance == 1e-9


def test_schema_diff_changed() -> None:
    """SchemaDiff.changed reflects any schema-level difference."""
    assert SchemaDiff().changed is False
    assert SchemaDiff(added_columns=("c",)).changed is True
    assert SchemaDiff(removed_columns=("b",)).changed is True
    assert SchemaDiff(type_changes=()).changed is False


def test_missing_value_diff_status_classification() -> None:
    """MissingValueDiff.status classifies the missingness delta."""
    assert MissingValueDiff("a", 0, 3, 0.0, 50.0).status == "new"
    assert MissingValueDiff("a", 3, 0, 50.0, 0.0).status == "resolved"
    assert MissingValueDiff("a", 1, 2, 20.0, 40.0).status == "regressed"
    assert MissingValueDiff("a", 2, 1, 40.0, 20.0).status == "improved"
    assert MissingValueDiff("a", 1, 1, 20.0, 20.0).status == "unchanged"


def test_duplicate_diff_status_classification() -> None:
    """DuplicateDiff.status classifies the duplicate-rate delta."""
    assert DuplicateDiff(1, 2, 10.0, 20.0).status == "regressed"
    assert DuplicateDiff(2, 1, 20.0, 10.0).status == "improved"
    assert DuplicateDiff(1, 1, 10.0, 10.0).status == "unchanged"


def test_constant_column_diff_changed() -> None:
    """ConstantColumnDiff.changed reflects any constant-column change."""
    assert ConstantColumnDiff().changed is False
    assert ConstantColumnDiff(newly_constant=("a",)).changed is True
    assert ConstantColumnDiff(no_longer_constant=("b",)).changed is True


def test_leakage_diff_collections() -> None:
    """LeakageDiff partitions column deltas by status."""
    new = LeakageColumnDiff("x", None, "critical", "new")
    removed = LeakageColumnDiff("y", "warning", None, "removed")
    escalated = LeakageColumnDiff("z", "info", "critical", "escalated")
    de_escalated = LeakageColumnDiff("w", "critical", "info", "de_escalated")
    unchanged = LeakageColumnDiff("v", "warning", "warning", "unchanged")

    diff = LeakageDiff(columns=(new, removed, escalated, de_escalated, unchanged))

    assert diff.new_findings == (new,)
    assert diff.removed_findings == (removed,)
    assert diff.escalated == (escalated,)
    assert diff.de_escalated == (de_escalated,)
    assert diff.changed is True

    assert LeakageDiff(columns=(unchanged,)).changed is False


def test_dataset_diff_result_to_dict_is_json_serializable() -> None:
    """DatasetDiffResult serializes to JSON without losing structure."""
    result = DatasetDiffResult(
        version=DIFF_ENGINE_VERSION,
        schema=SchemaDiff(added_columns=("c",), removed_columns=("b",)),
        structure=StructureDiff(
            previous_row_count=3,
            row_count=4,
            previous_column_count=2,
            column_count=2,
        ),
        missing_values=(MissingValueDiff("a", 0, 1, 0.0, 25.0),),
        duplicates=DuplicateDiff(0, 0, 0.0, 0.0),
        constant_columns=ConstantColumnDiff(),
        cardinality=(),
        statistics=(),
        distributions=(),
        leakage=None,
        summary=DatasetDiffSummary(
            rows_added=1,
            rows_removed=0,
            columns_added=1,
            columns_removed=1,
            columns_renamed=0,
            type_changes=0,
            schema_changed=True,
            missing_values_increased=1,
            missing_values_decreased=0,
            duplicate_rows_increased=False,
            duplicate_rows_decreased=False,
            newly_constant_columns=0,
            no_longer_constant_columns=0,
            leakage_new=0,
            leakage_removed=0,
            leakage_escalated=0,
            leakage_de_escalated=0,
            overall_health="regressed",
            recommendation="Review changes.",
        ),
        overall_summary="Rows 0 removed, 1 added.",
    )

    data = result.to_dict()

    assert data["version"] == "0.2.0"
    assert data["schema"]["added_columns"] == ["c"]
    assert data["missing_values"][0]["column"] == "a"
    assert data["missing_values"][0]["missing_count"] == 1
    assert data["summary"]["overall_health"] == "regressed"
    assert data["leakage"] is None
    json.dumps(data)
