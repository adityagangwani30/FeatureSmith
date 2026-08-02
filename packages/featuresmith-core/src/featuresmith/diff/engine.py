"""Dataset Diff Engine that orchestrates profile comparisons.

The engine consumes two ``ProfileResult`` snapshots produced by the existing
profiling engine and computes a typed ``DatasetDiffResult``. It deliberately
reuses profiling outputs and the existing leakage reviewer rather than
re-implementing any statistic: no new analysis of raw data happens here.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from featuresmith.core.profile_result import ProfileResult
from featuresmith.diff.schema import (
    CardinalityDiff,
    ColumnRename,
    ColumnTypeChange,
    ConstantColumnDiff,
    DatasetDiffResult,
    DatasetDiffSummary,
    DiffConfig,
    DistributionDiff,
    DuplicateDiff,
    LeakageColumnDiff,
    LeakageDiff,
    MissingValueDiff,
    SchemaDiff,
    StatisticDiff,
    StructureDiff,
)

_SEVERITY_RANK = {"critical": 3, "warning": 2, "info": 1}

_STATISTICS = ("mean", "median", "std_dev", "minimum", "maximum")


class DatasetDiffEngine:
    """Computes a structured diff between two dataset profile snapshots."""

    def diff(
        self,
        previous: ProfileResult,
        current: ProfileResult,
        *,
        target_column: str | None = None,
        config: DiffConfig | None = None,
    ) -> DatasetDiffResult:
        """Diff two profile snapshots into a typed DatasetDiffResult.

        Args:
            previous: The profile of the older snapshot.
            current: The profile of the newer snapshot.
            target_column: Optional target column name; enables the leakage
                comparison by reusing the leakage reviewers.
            config: Optional thresholds; defaults to ``DiffConfig``.

        Returns:
            A frozen DatasetDiffResult summarizing every required comparison.
        """
        cfg = config or DiffConfig()
        schema_diff = _diff_schema(previous, current)
        structure = _diff_structure(previous, current)
        missing = _diff_missing(previous, current)
        duplicates = _diff_duplicates(previous, current)
        constants = _diff_constants(previous, current)
        cardinality = _diff_cardinality(previous, current)
        statistics = _diff_statistics(previous, current, cfg)
        distributions = _diff_distributions(previous, current, cfg)
        leakage = (
            _diff_leakage(previous, current, target_column)
            if target_column is not None
            else None
        )
        summary = _build_summary(
            schema_diff,
            structure,
            missing,
            duplicates,
            constants,
            leakage,
            cfg,
        )
        return DatasetDiffResult(
            version=_result_version(),
            schema=schema_diff,
            structure=structure,
            missing_values=missing,
            duplicates=duplicates,
            constant_columns=constants,
            cardinality=cardinality,
            statistics=statistics,
            distributions=distributions,
            leakage=leakage,
            summary=summary,
            overall_summary=_build_overall_summary(summary),
        )


def compute_diff(
    previous: ProfileResult,
    current: ProfileResult,
    *,
    target_column: str | None = None,
    config: DiffConfig | None = None,
) -> DatasetDiffResult:
    """Diff two profile snapshots into a typed DatasetDiffResult.

    This is a convenience wrapper over ``DatasetDiffEngine().diff()``.

    Args:
        previous: The profile of the older snapshot.
        current: The profile of the newer snapshot.
        target_column: Optional target column name; enables leakage comparison.
        config: Optional thresholds; defaults to ``DiffConfig``.

    Returns:
        A frozen DatasetDiffResult summarizing the comparison.
    """
    return DatasetDiffEngine().diff(
        previous,
        current,
        target_column=target_column,
        config=config,
    )


def _result_version() -> str:
    """Return the Dataset Diff result schema version."""
    from featuresmith.diff.schema import DIFF_ENGINE_VERSION

    return DIFF_ENGINE_VERSION


def _diff_schema(previous: ProfileResult, current: ProfileResult) -> SchemaDiff:
    """Compute schema-level differences between the snapshots."""
    previous_names = list(previous.column_profiles)
    current_names = list(current.column_profiles)
    previous_set = set(previous_names)
    current_set = set(current_names)

    removed = [name for name in previous_names if name not in current_set]
    added = [name for name in current_names if name not in previous_set]

    renames = _detect_renames(previous, current, removed, added)
    renamed_previous = {rename.previous_name for rename in renames}
    renamed_new = {rename.name for rename in renames}
    removed = [name for name in removed if name not in renamed_previous]
    added = [name for name in added if name not in renamed_new]

    shared = [
        name
        for name in previous_names
        if name in current_set and name not in renamed_previous
    ]
    type_changes = [
        ColumnTypeChange(
            column=name,
            previous_dtype=previous.column_profiles[name].dtype,
            dtype=current.column_profiles[name].dtype,
            previous_logical_type=previous.column_profiles[name].logical_type,
            logical_type=current.column_profiles[name].logical_type,
        )
        for name in shared
        if _type_changed(previous, current, name)
    ]
    return SchemaDiff(
        added_columns=tuple(added),
        removed_columns=tuple(removed),
        renamed_columns=tuple(renames),
        type_changes=tuple(type_changes),
    )


def _type_changed(previous: ProfileResult, current: ProfileResult, column: str) -> bool:
    """Return whether a shared column's dtype or logical type changed."""
    before = previous.column_profiles[column]
    after = current.column_profiles[column]
    return before.dtype != after.dtype or before.logical_type != after.logical_type


def _detect_renames(
    previous: ProfileResult,
    current: ProfileResult,
    removed: Sequence[str],
    added: Sequence[str],
) -> list[ColumnRename]:
    """Detect renamed columns using a deterministic profile-level signature.

    A removed column is considered renamed to an added column when they share
    the same dtype, missing count, and value-shape signature (top categories,
    numeric mean, datetime bounds, or text length). The match is deterministic:
    the first added column with an identical signature wins, and ambiguous
    columns (zero or multiple matches) are left as added/removed.
    """
    signatures = {name: _rename_signature(current, name) for name in added}
    renames: list[ColumnRename] = []
    for removed_name in removed:
        previous_sig = _rename_signature(previous, removed_name)
        candidates = [name for name in signatures if signatures[name] == previous_sig]
        if len(candidates) == 1:
            renames.append(ColumnRename(previous_name=removed_name, name=candidates[0]))
            signatures.pop(candidates[0])
    return renames


def _rename_signature(profile: ProfileResult, column: str) -> Any:
    """Return a deterministic signature describing a column's value shape."""
    overview = profile.column_profiles[column]
    if overview.logical_type == "numeric":
        numeric = profile.numeric_profiles.get(column)
        return (
            overview.dtype,
            overview.missing_count,
            _round(numeric.unique_count) if numeric else None,
            _round(numeric.mean) if numeric else None,
        )
    if overview.logical_type == "categorical":
        categorical = profile.categorical_profiles.get(column)
        if categorical is None:
            return (overview.dtype, overview.missing_count)
        top = tuple(sorted(categorical.top_values))
        return (overview.dtype, overview.missing_count, categorical.cardinality, top)
    if overview.logical_type == "datetime":
        datetime = profile.datetime_profiles.get(column)
        if datetime is None:
            return (overview.dtype, overview.missing_count)
        return (
            overview.dtype,
            overview.missing_count,
            datetime.minimum,
            datetime.maximum,
        )
    if overview.logical_type == "text":
        text = profile.text_profiles.get(column)
        if text is None:
            return (overview.dtype, overview.missing_count)
        return (
            overview.dtype,
            overview.missing_count,
            _round(text.avg_length),
            text.max_length,
        )
    return (overview.dtype, overview.missing_count)


def _round(value: Any) -> Any:
    """Round a numeric value to six decimals (None stays None)."""
    if value is None:
        return None
    return round(value, 6)


def _diff_structure(previous: ProfileResult, current: ProfileResult) -> StructureDiff:
    """Compute row and column count differences."""
    before = previous.dataset_summary
    after = current.dataset_summary
    return StructureDiff(
        previous_row_count=before.row_count,
        row_count=after.row_count,
        previous_column_count=before.column_count,
        column_count=after.column_count,
    )


def _diff_missing(
    previous: ProfileResult, current: ProfileResult
) -> tuple[MissingValueDiff, ...]:
    """Compute per-column missingness deltas for shared columns."""
    previous_counts = previous.missing_value_summary.column_missing_counts
    current_counts = current.missing_value_summary.column_missing_counts
    previous_pcts = previous.missing_value_summary.column_missing_percentages
    current_pcts = current.missing_value_summary.column_missing_percentages

    diffs: list[MissingValueDiff] = []
    for name in _shared_columns(previous, current):
        prev_count = previous_counts.get(name, 0)
        cur_count = current_counts.get(name, 0)
        prev_pct = previous_pcts.get(name, 0.0)
        cur_pct = current_pcts.get(name, 0.0)
        if prev_count == cur_count and _float_equal(prev_pct, cur_pct):
            continue
        diffs.append(
            MissingValueDiff(
                column=name,
                previous_missing_count=prev_count,
                missing_count=cur_count,
                previous_missing_percentage=round(prev_pct, 6),
                missing_percentage=round(cur_pct, 6),
            )
        )
    return tuple(diffs)


def _diff_duplicates(previous: ProfileResult, current: ProfileResult) -> DuplicateDiff:
    """Compute the duplicate-row statistics delta."""
    before = previous.duplicate_summary
    after = current.duplicate_summary
    return DuplicateDiff(
        previous_duplicate_count=before.duplicate_rows_count,
        duplicate_count=after.duplicate_rows_count,
        previous_duplicate_percentage=round(before.duplicate_percentage, 6),
        duplicate_percentage=round(after.duplicate_percentage, 6),
    )


def _diff_constants(
    previous: ProfileResult, current: ProfileResult
) -> ConstantColumnDiff:
    """Compute constant-column changes for shared columns."""
    newly_constant: list[str] = []
    no_longer_constant: list[str] = []
    for name in _shared_columns(previous, current):
        before = previous.column_profiles[name].is_constant
        after = current.column_profiles[name].is_constant
        if not before and after:
            newly_constant.append(name)
        elif before and not after:
            no_longer_constant.append(name)
    return ConstantColumnDiff(
        newly_constant=tuple(newly_constant),
        no_longer_constant=tuple(no_longer_constant),
    )


def _diff_cardinality(
    previous: ProfileResult, current: ProfileResult
) -> tuple[CardinalityDiff, ...]:
    """Compute per-column cardinality deltas for shared columns."""
    diffs: list[CardinalityDiff] = []
    for name in _shared_columns(previous, current):
        before = _cardinality(previous, name)
        after = _cardinality(current, name)
        if before is None or after is None or before == after:
            continue
        diffs.append(
            CardinalityDiff(column=name, previous_cardinality=before, cardinality=after)
        )
    return tuple(diffs)


def _cardinality(profile: ProfileResult, column: str) -> int | None:
    """Return a column's unique-value cardinality when available."""
    categorical = profile.categorical_profiles.get(column)
    if categorical is not None:
        return categorical.cardinality
    numeric = profile.numeric_profiles.get(column)
    if numeric is not None:
        return numeric.unique_count
    return None


def _diff_statistics(
    previous: ProfileResult,
    current: ProfileResult,
    config: DiffConfig,
) -> tuple[StatisticDiff, ...]:
    """Compute changed basic statistics for shared numeric columns."""
    diffs: list[StatisticDiff] = []
    for name in _shared_columns(previous, current):
        before = previous.numeric_profiles.get(name)
        after = current.numeric_profiles.get(name)
        if before is None or after is None:
            continue
        for statistic in _STATISTICS:
            prev_value: float | None = getattr(before, statistic)
            cur_value: float | None = getattr(after, statistic)
            if prev_value is None or cur_value is None:
                continue
            if _float_equal(prev_value, cur_value, config.numeric_tolerance):
                continue
            diffs.append(
                StatisticDiff(
                    column=name,
                    statistic=statistic,
                    previous=round(prev_value, 6),
                    current=round(cur_value, 6),
                    delta=round(cur_value - prev_value, 6),
                    relative_delta=_relative_delta(prev_value, cur_value),
                )
            )
    return tuple(diffs)


def _diff_distributions(
    previous: ProfileResult,
    current: ProfileResult,
    config: DiffConfig,
) -> tuple[DistributionDiff, ...]:
    """Compute significant distribution (mean) shifts for shared numeric columns."""
    diffs: list[DistributionDiff] = []
    for name in _shared_columns(previous, current):
        before = previous.numeric_profiles.get(name)
        after = current.numeric_profiles.get(name)
        if before is None or after is None:
            continue
        prev_mean = before.mean
        cur_mean = after.mean
        if prev_mean is None or cur_mean is None:
            continue
        relative = _relative_delta(prev_mean, cur_mean)
        significant = _is_significant_shift(prev_mean, cur_mean, relative, config)
        if not significant:
            continue
        diffs.append(
            DistributionDiff(
                column=name,
                previous_mean=round(prev_mean, 6),
                mean=round(cur_mean, 6),
                mean_relative_shift=relative,
                significant=True,
            )
        )
    return tuple(diffs)


def _is_significant_shift(
    previous: float,
    current: float,
    relative: float | None,
    config: DiffConfig,
) -> bool:
    """Return whether a mean shift exceeds the configured significance threshold."""
    if relative is not None and abs(relative) >= config.distribution_shift_threshold:
        return True
    if previous == 0.0 and current != 0.0:
        return True
    return False


def _diff_leakage(
    previous: ProfileResult,
    current: ProfileResult,
    target_column: str,
) -> LeakageDiff:
    """Compare leakage findings between snapshots by reusing the leakage reviewer."""
    before = _leakage_by_column(previous, target_column)
    after = _leakage_by_column(current, target_column)
    columns = sorted(set(before) | set(after))
    diffs = [
        LeakageColumnDiff(
            column=column,
            previous_severity=before.get(column),
            severity=after.get(column),
            status=_leakage_status(before.get(column), after.get(column)),
        )
        for column in columns
    ]
    return LeakageDiff(columns=tuple(diffs))


def _leakage_by_column(profile: ProfileResult, target_column: str) -> Mapping[str, str]:
    """Return column name to worst leakage severity for a profile."""
    from featuresmith.review.context import ReviewConfig, ReviewContext
    from featuresmith.review.reviewers.leakage import LeakageReviewer

    context = ReviewContext(
        profile=profile,
        config=ReviewConfig(target_column=target_column),
    )
    section = LeakageReviewer().review(context)
    severities: dict[str, str] = {}
    for finding in section.findings:
        if finding.column_name is not None:
            severities[finding.column_name] = finding.severity
    return severities


def _leakage_status(previous_severity: str | None, current_severity: str | None) -> str:
    """Classify a column's leakage status change between snapshots."""
    if previous_severity is None and current_severity is not None:
        return "new"
    if previous_severity is not None and current_severity is None:
        return "removed"
    if previous_severity == current_severity:
        return "unchanged"
    previous_rank = _SEVERITY_RANK.get(previous_severity or "", 0)
    current_rank = _SEVERITY_RANK.get(current_severity or "", 0)
    if current_rank > previous_rank:
        return "escalated"
    return "de_escalated"


def _build_summary(
    schema_diff: SchemaDiff,
    structure: StructureDiff,
    missing: Sequence[MissingValueDiff],
    duplicates: DuplicateDiff,
    constants: ConstantColumnDiff,
    leakage: LeakageDiff | None,
    config: DiffConfig,
) -> DatasetDiffSummary:
    """Build the concise engineering-focused diff summary."""
    missing_increased = [
        diff
        for diff in missing
        if diff.status in ("new", "regressed")
        and abs(diff.delta_percentage) >= config.missing_change_threshold
    ]
    missing_decreased = [
        diff
        for diff in missing
        if diff.status in ("resolved", "improved")
        and abs(diff.delta_percentage) >= config.missing_change_threshold
    ]
    duplicate_increased = (
        duplicates.status == "regressed"
        and abs(duplicates.delta_percentage) >= config.duplicate_change_threshold
    )
    duplicate_decreased = (
        duplicates.status == "improved"
        and abs(duplicates.delta_percentage) >= config.duplicate_change_threshold
    )
    leakage_new = len(leakage.new_findings) if leakage else 0
    leakage_removed = len(leakage.removed_findings) if leakage else 0
    leakage_escalated = len(leakage.escalated) if leakage else 0
    leakage_de_escalated = len(leakage.de_escalated) if leakage else 0

    regressed = any(
        (
            bool(schema_diff.removed_columns),
            bool(schema_diff.type_changes),
            bool(missing_increased),
            duplicate_increased,
            bool(constants.newly_constant),
            bool(leakage_new or leakage_escalated),
        )
    )
    improved = any(
        (
            bool(missing_decreased),
            duplicate_decreased,
            bool(constants.no_longer_constant),
            bool(leakage_removed or leakage_de_escalated),
        )
    )
    if regressed:
        overall_health = "regressed"
    elif improved:
        overall_health = "improved"
    else:
        overall_health = "unchanged"

    return DatasetDiffSummary(
        rows_added=structure.rows_added,
        rows_removed=structure.rows_removed,
        columns_added=len(schema_diff.added_columns),
        columns_removed=len(schema_diff.removed_columns),
        columns_renamed=len(schema_diff.renamed_columns),
        type_changes=len(schema_diff.type_changes),
        schema_changed=schema_diff.changed,
        missing_values_increased=len(missing_increased),
        missing_values_decreased=len(missing_decreased),
        duplicate_rows_increased=duplicate_increased,
        duplicate_rows_decreased=duplicate_decreased,
        newly_constant_columns=len(constants.newly_constant),
        no_longer_constant_columns=len(constants.no_longer_constant),
        leakage_new=leakage_new,
        leakage_removed=leakage_removed,
        leakage_escalated=leakage_escalated,
        leakage_de_escalated=leakage_de_escalated,
        overall_health=overall_health,
        recommendation=_build_recommendation(
            schema_diff,
            missing_increased,
            missing_decreased,
            duplicate_increased,
            duplicate_decreased,
            constants,
            leakage_new,
            leakage_removed,
            leakage_escalated,
            leakage_de_escalated,
            regressed,
            improved,
        ),
    )


def _build_recommendation(
    schema_diff: SchemaDiff,
    missing_increased: Sequence[MissingValueDiff],
    missing_decreased: Sequence[MissingValueDiff],
    duplicate_increased: bool,
    duplicate_decreased: bool,
    constants: ConstantColumnDiff,
    leakage_new: int,
    leakage_removed: int,
    leakage_escalated: int,
    leakage_de_escalated: int,
    regressed: bool,
    improved: bool,
) -> str:
    """Synthesize a plain-language, engineering-focused recommendation."""
    if regressed:
        parts: list[str] = []
        if schema_diff.removed_columns:
            parts.append(f"{len(schema_diff.removed_columns)} column(s) removed")
        if schema_diff.type_changes:
            parts.append(f"{len(schema_diff.type_changes)} type change(s)")
        if missing_increased:
            parts.append(f"missingness increased in {len(missing_increased)} column(s)")
        if duplicate_increased:
            parts.append("duplicate rows increased")
        if constants.newly_constant:
            parts.append(f"{len(constants.newly_constant)} column(s) became constant")
        if leakage_new or leakage_escalated:
            parts.append(
                f"{leakage_new + leakage_escalated} leakage change(s) (new or escalated)"
            )
        return (
            f"Dataset regressed: {'; '.join(parts)}. "
            "Review the changes before retraining."
        )
    if improved:
        parts = []
        if missing_decreased:
            parts.append(f"missingness reduced in {len(missing_decreased)} column(s)")
        if duplicate_decreased:
            parts.append("duplicate rows reduced")
        if constants.no_longer_constant:
            parts.append(
                f"{len(constants.no_longer_constant)} column(s) are no longer constant"
            )
        if leakage_removed or leakage_de_escalated:
            parts.append(
                f"{leakage_removed + leakage_de_escalated} leakage change(s) removed "
                "or de-escalated"
            )
        return (
            f"Dataset improved: {'; '.join(parts)}. No blocking regressions detected."
        )
    return "No meaningful quality change detected between the two snapshots."


def _build_overall_summary(summary: DatasetDiffSummary) -> str:
    """Build the one-line templated roll-up of the diff."""
    return (
        f"Rows {summary.rows_removed} removed, {summary.rows_added} added; "
        f"columns {summary.columns_removed} removed, {summary.columns_added} added; "
        f"overall health: {summary.overall_health}."
    )


def _shared_columns(previous: ProfileResult, current: ProfileResult) -> list[str]:
    """Return the column names shared by both snapshots, in stable order."""
    return [
        name for name in previous.column_profiles if name in current.column_profiles
    ]


def _float_equal(left: float, right: float, tolerance: float = 1e-9) -> bool:
    """Return whether two floats are equal within a tolerance."""
    return abs(left - right) <= tolerance


def _relative_delta(previous: float, current: float) -> float | None:
    """Return the relative change from previous to current (None when previous is 0)."""
    if previous == 0.0:
        return None
    return round((current - previous) / abs(previous), 6)
