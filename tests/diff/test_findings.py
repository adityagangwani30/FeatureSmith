"""Tests for converting a DatasetDiffResult into RuleFindings."""

from __future__ import annotations

from typing import Any

import pandas as pd

import featuresmith as fs
from featuresmith.api import diff_findings
from featuresmith.diff.engine import compute_diff


def _findings(
    old_df: pd.DataFrame, new_df: pd.DataFrame, **kwargs: Any
) -> dict[str, str]:
    """Compute the diff findings keyed by rule ID."""
    old_profile = fs.profile(old_df)
    new_profile = fs.profile(new_df)
    result = compute_diff(old_profile, new_profile, **kwargs)
    return {finding.rule_id: finding.severity for finding in diff_findings(result)}


def test_identical_datasets_have_no_findings() -> None:
    """Two identical snapshots produce no findings."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    findings = _findings(df, df.copy())

    assert findings == {}


def test_added_and_removed_columns_findings() -> None:
    """Added columns are informational; removed columns are warnings."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new = pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]})

    findings = _findings(old, new)

    assert findings["diff.schema.added_columns"] == "info"
    assert findings["diff.schema.removed_columns"] == "warning"


def test_renamed_columns_finding() -> None:
    """Renamed columns surface as an informational finding."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    new = pd.DataFrame({"c": [1, 2, 3], "b": ["x", "y", "z"]})

    findings = _findings(old, new)

    assert findings["diff.schema.renamed_columns"] == "info"


def test_type_change_finding() -> None:
    """A dtype change surfaces as a warning finding."""
    old = pd.DataFrame({"a": [1, 2, 3]})
    new = pd.DataFrame({"a": ["1", "2", "3"]})

    findings = _findings(old, new)

    assert findings["diff.schema.type_changes"] == "warning"


def test_missing_increased_finding() -> None:
    """New missingness surfaces as a warning finding."""
    old = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0]})
    new = pd.DataFrame({"a": [1.0, None, None, 4.0]})

    findings = _findings(old, new)

    assert findings["diff.quality.missing_increased"] == "warning"


def test_newly_constant_finding() -> None:
    """A newly constant column surfaces as a warning finding."""
    old = pd.DataFrame({"a": [1, 2, 3, 4]})
    new = pd.DataFrame({"a": [5, 5, 5, 5]})

    findings = _findings(old, new)

    assert findings["diff.quality.newly_constant"] == "warning"


def test_distribution_shift_finding() -> None:
    """A significant mean shift surfaces as an informational finding."""
    old = pd.DataFrame({"a": [1.0, 2.0, 3.0]})
    new = pd.DataFrame({"a": [100.0, 200.0, 300.0]})

    findings = _findings(old, new)

    assert findings["diff.distribution.mean_shift"] == "info"


def test_leakage_new_finding_is_critical() -> None:
    """Newly introduced leakage surfaces as a critical finding."""
    old = pd.DataFrame({"target": [1, 2, 3, 4, 5], "a": [10, 20, 30, 40, 50]})
    new = pd.DataFrame({"target": [1, 2, 3, 4, 5], "leak": [1, 2, 3, 4, 5]})

    findings = _findings(old, new, target_column="target")

    assert findings["diff.leakage.new"] == "critical"


def test_no_leakage_findings_without_target() -> None:
    """No target column means no leakage findings are emitted."""
    old = pd.DataFrame({"target": [1, 2, 3], "leak": [1, 2, 3]})
    new = pd.DataFrame({"target": [1, 2, 3], "leak": [1, 2, 3]})

    findings = _findings(old, new)

    assert not any(rule_id.startswith("diff.leakage") for rule_id in findings)
