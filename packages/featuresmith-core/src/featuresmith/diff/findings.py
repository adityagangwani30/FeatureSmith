"""Convert a DatasetDiffResult into shared RuleFinding objects.

The Diff Review Engine surface (reviewer sections, CLI exit codes) consumes
findings that speak the same language as every other review finding. This
module is the single place that maps the typed ``DatasetDiffResult`` onto
``RuleFinding`` objects so no surface reinterprets the diff itself.
"""

from __future__ import annotations

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.diff.schema import (
    DatasetDiffResult,
    DiffConfig,
    DistributionDiff,
    MissingValueDiff,
)


def findings_from_diff(
    diff: DatasetDiffResult,
    config: DiffConfig | None = None,
) -> list[RuleFinding]:
    """Convert a DatasetDiffResult into a list of RuleFinding objects.

    Findings are emitted only for meaningful differences: neutral structural
    changes (added/renamed columns) are informational, while regressions
    (removed columns, type changes, missingness increases, new leakage) are
    warnings or criticals. Improvements are deliberately not emitted as
    findings — they are surfaced by the summary and renderer.

    Args:
        diff: The frozen DatasetDiffResult.
        config: Optional thresholds; defaults to ``DiffConfig``.

    Returns:
        The deterministic list of RuleFinding objects.
    """
    cfg = config or DiffConfig()
    findings: list[RuleFinding] = []

    schema = diff.schema
    if schema.added_columns:
        findings.append(
            RuleFinding(
                rule_id="diff.schema.added_columns",
                rule_name="Added Columns",
                category="diff",
                severity="info",
                column_name=None,
                title="Columns added to the dataset",
                description=(
                    f"{len(schema.added_columns)} column(s) added: "
                    f"{', '.join(schema.added_columns)}."
                ),
                evidence={"columns": list(schema.added_columns)},
            )
        )
    if schema.removed_columns:
        findings.append(
            RuleFinding(
                rule_id="diff.schema.removed_columns",
                rule_name="Removed Columns",
                category="diff",
                severity="warning",
                column_name=None,
                title="Columns removed from the dataset",
                description=(
                    f"{len(schema.removed_columns)} column(s) removed: "
                    f"{', '.join(schema.removed_columns)}."
                ),
                evidence={"columns": list(schema.removed_columns)},
            )
        )
    if schema.renamed_columns:
        renames = [
            f"{rename.previous_name} -> {rename.name}"
            for rename in schema.renamed_columns
        ]
        findings.append(
            RuleFinding(
                rule_id="diff.schema.renamed_columns",
                rule_name="Renamed Columns",
                category="diff",
                severity="info",
                column_name=None,
                title="Columns renamed between snapshots",
                description=f"{len(renames)} column(s) renamed: {', '.join(renames)}.",
                evidence={
                    "renames": [
                        {"previous_name": r.previous_name, "name": r.name}
                        for r in schema.renamed_columns
                    ]
                },
            )
        )
    if schema.type_changes:
        changes = [
            f"{change.column} ({change.previous_dtype} -> {change.dtype})"
            for change in schema.type_changes
        ]
        findings.append(
            RuleFinding(
                rule_id="diff.schema.type_changes",
                rule_name="Data Type Changes",
                category="diff",
                severity="warning",
                column_name=None,
                title="Column data types changed",
                description=(
                    f"{len(changes)} column(s) changed data type: {', '.join(changes)}."
                ),
                evidence={
                    "changes": [
                        {
                            "column": change.column,
                            "previous_dtype": change.previous_dtype,
                            "dtype": change.dtype,
                            "previous_logical_type": change.previous_logical_type,
                            "logical_type": change.logical_type,
                        }
                        for change in schema.type_changes
                    ]
                },
            )
        )

    missing_threshold = cfg.missing_change_threshold
    for missing_diff in diff.missing_values:
        if (
            missing_diff.status in ("new", "regressed")
            and abs(missing_diff.delta_percentage) >= missing_threshold
        ):
            findings.append(_missing_regression_finding(missing_diff))
        if (
            missing_diff.status in ("resolved", "improved")
            and abs(missing_diff.delta_percentage) >= missing_threshold
        ):
            findings.append(_missing_improvement_finding(missing_diff))

    duplicates = diff.duplicates
    if (
        duplicates.status == "regressed"
        and abs(duplicates.delta_percentage) >= cfg.duplicate_change_threshold
    ):
        findings.append(
            RuleFinding(
                rule_id="diff.quality.duplicates_increased",
                rule_name="Duplicate Rows Increased",
                category="diff",
                severity="warning",
                column_name=None,
                title="Duplicate-row rate increased",
                description=(
                    f"Duplicate rate rose from {duplicates.previous_duplicate_percentage:g}% "
                    f"to {duplicates.duplicate_percentage:g}% "
                    f"({duplicates.delta_percentage:g} points)."
                ),
                evidence={
                    "previous_duplicate_percentage": duplicates.previous_duplicate_percentage,
                    "duplicate_percentage": duplicates.duplicate_percentage,
                    "delta_percentage": duplicates.delta_percentage,
                },
            )
        )

    for column in diff.constant_columns.newly_constant:
        findings.append(
            RuleFinding(
                rule_id="diff.quality.newly_constant",
                rule_name="Column Became Constant",
                category="diff",
                severity="warning",
                column_name=column,
                title=f"Column '{column}' became constant",
                description=(
                    f"Column '{column}' now contains a single value; "
                    "it contributes no predictive signal."
                ),
                evidence={"column": column},
            )
        )

    for distribution in diff.distributions:
        findings.append(_distribution_shift_finding(distribution))

    if diff.leakage is not None:
        for column_diff in diff.leakage.new_findings:
            findings.append(
                RuleFinding(
                    rule_id="diff.leakage.new",
                    rule_name="New Leakage Detected",
                    category="diff",
                    severity="critical",
                    column_name=column_diff.column,
                    title=f"Leakage introduced in column '{column_diff.column}'",
                    description=(
                        f"Column '{column_diff.column}' was not flagged for leakage "
                        "in the previous snapshot but is now flagged "
                        f"(severity: {column_diff.severity})."
                    ),
                    evidence={
                        "column": column_diff.column,
                        "severity": column_diff.severity,
                    },
                )
            )
        for column_diff in diff.leakage.escalated:
            findings.append(
                RuleFinding(
                    rule_id="diff.leakage.escalated",
                    rule_name="Leakage Severity Escalated",
                    category="diff",
                    severity="critical",
                    column_name=column_diff.column,
                    title=f"Leakage escalated in column '{column_diff.column}'",
                    description=(
                        f"Column '{column_diff.column}' leakage severity rose from "
                        f"'{column_diff.previous_severity}' to '{column_diff.severity}'."
                    ),
                    evidence={
                        "column": column_diff.column,
                        "previous_severity": column_diff.previous_severity,
                        "severity": column_diff.severity,
                    },
                )
            )

    return findings


def _missing_regression_finding(diff: MissingValueDiff) -> RuleFinding:
    """Build the finding for a newly-introduced or worsened missingness."""
    label = "introduced" if diff.status == "new" else "increased"
    return RuleFinding(
        rule_id="diff.quality.missing_increased",
        rule_name="Missing Values Increased",
        category="diff",
        severity="warning",
        column_name=diff.column,
        title=f"Missing values {label} in column '{diff.column}'",
        description=(
            f"Missingness in column '{diff.column}' changed from "
            f"{diff.previous_missing_percentage:g}% to {diff.missing_percentage:g}% "
            f"({diff.delta_percentage:g} points)."
        ),
        evidence={
            "previous_missing_percentage": diff.previous_missing_percentage,
            "missing_percentage": diff.missing_percentage,
            "delta_percentage": diff.delta_percentage,
            "status": diff.status,
        },
    )


def _missing_improvement_finding(diff: MissingValueDiff) -> RuleFinding:
    """Build the finding for missingness that improved between snapshots."""
    label = "resolved" if diff.status == "resolved" else "reduced"
    return RuleFinding(
        rule_id="diff.quality.missing_decreased",
        rule_name="Missing Values Improved",
        category="diff",
        severity="info",
        column_name=diff.column,
        title=f"Missing values {label} in column '{diff.column}'",
        description=(
            f"Missingness in column '{diff.column}' changed from "
            f"{diff.previous_missing_percentage:g}% to {diff.missing_percentage:g}% "
            f"({diff.delta_percentage:g} points)."
        ),
        evidence={
            "previous_missing_percentage": diff.previous_missing_percentage,
            "missing_percentage": diff.missing_percentage,
            "delta_percentage": diff.delta_percentage,
            "status": diff.status,
        },
    )


def _distribution_shift_finding(distribution: DistributionDiff) -> RuleFinding:
    """Build the finding for a significant distribution shift."""
    return RuleFinding(
        rule_id="diff.distribution.mean_shift",
        rule_name="Distribution Shift",
        category="diff",
        severity="info",
        column_name=distribution.column,
        title=f"Mean shifted in column '{distribution.column}'",
        description=(
            f"Column '{distribution.column}' mean changed from "
            f"{distribution.previous_mean:g} to {distribution.mean:g}"
            + (
                f" ({distribution.mean_relative_shift:g} relative)."
                if distribution.mean_relative_shift is not None
                else "."
            )
        ),
        evidence={
            "previous_mean": distribution.previous_mean,
            "mean": distribution.mean,
            "mean_relative_shift": distribution.mean_relative_shift,
            "significant": distribution.significant,
        },
    )
