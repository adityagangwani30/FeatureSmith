"""Serializable schemas for Dataset Diff output models.

The Dataset Diff Engine produces one canonical, fully serializable artifact
(``DatasetDiffResult``) that every surface — CLI, dashboard, HTML report, JSON
— consumes identically. The models mirror ``Dataset-Diff-And-Leakage-Detection.md``
and reuse the existing ``ProfileResult`` schemas unchanged so every delta is
traceable back to the profiling engine that produced the two snapshots.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from featuresmith.core.profile_result import _asdict_custom

DIFF_ENGINE_VERSION = "0.2.0"


@dataclass(frozen=True, slots=True)
class DiffConfig:
    """Tunable thresholds for the Dataset Diff Engine.

    Attributes:
        distribution_shift_threshold: Relative mean shift (0.10 = 10%) above
            which a distribution change is flagged as significant.
        missing_change_threshold: Absolute missing-percentage-point change
            above which a missingness delta counts as a meaningful regression
            or improvement (default 1.0 percentage point).
        duplicate_change_threshold: Absolute duplicate-percentage-point change
            above which a duplicate-rate delta counts as meaningful.
        numeric_tolerance: Absolute tolerance used for floating-point equality.
    """

    distribution_shift_threshold: float = 0.10
    missing_change_threshold: float = 1.0
    duplicate_change_threshold: float = 1.0
    numeric_tolerance: float = 1e-9


@dataclass(frozen=True, slots=True)
class ColumnRename:
    """A column present in both snapshots under two different names.

    Attributes:
        previous_name: The column name in the older snapshot.
        name: The column name in the newer snapshot.
    """

    previous_name: str
    name: str


@dataclass(frozen=True, slots=True)
class ColumnTypeChange:
    """A data type change for a column present in both snapshots.

    Attributes:
        column: The column name.
        previous_dtype: The backend dtype string in the older snapshot.
        dtype: The backend dtype string in the newer snapshot.
        previous_logical_type: The logical type in the older snapshot.
        logical_type: The logical type in the newer snapshot.
    """

    column: str
    previous_dtype: str
    dtype: str
    previous_logical_type: str
    logical_type: str


@dataclass(frozen=True, slots=True)
class SchemaDiff:
    """Schema-level differences between the two snapshots.

    Attributes:
        added_columns: Columns present only in the newer snapshot.
        removed_columns: Columns present only in the older snapshot.
        renamed_columns: Columns detected as renamed between snapshots.
        type_changes: Per-column data type changes.
    """

    added_columns: tuple[str, ...] = ()
    removed_columns: tuple[str, ...] = ()
    renamed_columns: tuple[ColumnRename, ...] = ()
    type_changes: tuple[ColumnTypeChange, ...] = ()

    def __post_init__(self) -> None:
        """Freeze tuple fields to keep the diff immutable."""
        object.__setattr__(self, "added_columns", tuple(self.added_columns))
        object.__setattr__(self, "removed_columns", tuple(self.removed_columns))
        object.__setattr__(self, "renamed_columns", tuple(self.renamed_columns))
        object.__setattr__(self, "type_changes", tuple(self.type_changes))

    @property
    def changed(self) -> bool:
        """Return whether any schema-level difference exists."""
        return bool(
            self.added_columns
            or self.removed_columns
            or self.renamed_columns
            or self.type_changes
        )


@dataclass(frozen=True, slots=True)
class StructureDiff:
    """Row and column count changes between the snapshots.

    Attributes:
        previous_row_count: Row count of the older snapshot.
        row_count: Row count of the newer snapshot.
        previous_column_count: Column count of the older snapshot.
        column_count: Column count of the newer snapshot.
    """

    previous_row_count: int
    row_count: int
    previous_column_count: int
    column_count: int

    @property
    def rows_added(self) -> int:
        """Return the number of rows added (never negative)."""
        return max(self.row_count - self.previous_row_count, 0)

    @property
    def rows_removed(self) -> int:
        """Return the number of rows removed (never negative)."""
        return max(self.previous_row_count - self.row_count, 0)

    @property
    def columns_added(self) -> int:
        """Return the number of columns added (never negative)."""
        return max(self.column_count - self.previous_column_count, 0)

    @property
    def columns_removed(self) -> int:
        """Return the number of columns removed (never negative)."""
        return max(self.previous_column_count - self.column_count, 0)


@dataclass(frozen=True, slots=True)
class MissingValueDiff:
    """Per-column missingness delta between the snapshots.

    Attributes:
        column: The column name.
        previous_missing_count: Missing count in the older snapshot.
        missing_count: Missing count in the newer snapshot.
        previous_missing_percentage: Missing percentage in the older snapshot.
        missing_percentage: Missing percentage in the newer snapshot.
    """

    column: str
    previous_missing_count: int
    missing_count: int
    previous_missing_percentage: float
    missing_percentage: float

    @property
    def delta_count(self) -> int:
        """Return the signed change in missing count."""
        return self.missing_count - self.previous_missing_count

    @property
    def delta_percentage(self) -> float:
        """Return the signed change in missing percentage (points)."""
        return round(self.missing_percentage - self.previous_missing_percentage, 6)

    @property
    def status(self) -> str:
        """Classify the missingness change.

        Returns:
            "new" when missingness was introduced, "resolved" when it
            disappeared, "regressed" when it increased, "improved" when it
            decreased, or "unchanged" otherwise.
        """
        if self.previous_missing_percentage == 0.0 and self.missing_percentage > 0.0:
            return "new"
        if self.previous_missing_percentage > 0.0 and self.missing_percentage == 0.0:
            return "resolved"
        if self.delta_percentage > 0.0:
            return "regressed"
        if self.delta_percentage < 0.0:
            return "improved"
        return "unchanged"


@dataclass(frozen=True, slots=True)
class DuplicateDiff:
    """Duplicate-row statistics delta between the snapshots.

    Attributes:
        previous_duplicate_count: Duplicate row count in the older snapshot.
        duplicate_count: Duplicate row count in the newer snapshot.
        previous_duplicate_percentage: Duplicate percentage in the older snapshot.
        duplicate_percentage: Duplicate percentage in the newer snapshot.
    """

    previous_duplicate_count: int
    duplicate_count: int
    previous_duplicate_percentage: float
    duplicate_percentage: float

    @property
    def delta_percentage(self) -> float:
        """Return the signed change in duplicate percentage (points)."""
        return round(self.duplicate_percentage - self.previous_duplicate_percentage, 6)

    @property
    def status(self) -> str:
        """Classify the duplicate-rate change as regressed, improved, or unchanged."""
        if self.delta_percentage > 0.0:
            return "regressed"
        if self.delta_percentage < 0.0:
            return "improved"
        return "unchanged"


@dataclass(frozen=True, slots=True)
class ConstantColumnDiff:
    """Constant-column changes between the snapshots.

    Attributes:
        newly_constant: Shared columns that became constant in the newer snapshot.
        no_longer_constant: Shared columns that stopped being constant.
    """

    newly_constant: tuple[str, ...] = ()
    no_longer_constant: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Freeze tuple fields to keep the diff immutable."""
        object.__setattr__(self, "newly_constant", tuple(self.newly_constant))
        object.__setattr__(self, "no_longer_constant", tuple(self.no_longer_constant))

    @property
    def changed(self) -> bool:
        """Return whether any constant-column difference exists."""
        return bool(self.newly_constant or self.no_longer_constant)


@dataclass(frozen=True, slots=True)
class CardinalityDiff:
    """Unique-value cardinality delta for one shared column.

    Attributes:
        column: The column name.
        previous_cardinality: Unique-value count in the older snapshot.
        cardinality: Unique-value count in the newer snapshot.
    """

    column: str
    previous_cardinality: int
    cardinality: int

    @property
    def delta(self) -> int:
        """Return the signed change in cardinality."""
        return self.cardinality - self.previous_cardinality


@dataclass(frozen=True, slots=True)
class StatisticDiff:
    """A changed basic statistic for one shared numeric column.

    Only statistics that actually changed between snapshots are emitted, so the
    output stays focused on meaningful differences.

    Attributes:
        column: The column name.
        statistic: The statistic name ("mean", "median", "std_dev", "minimum", "maximum").
        previous: The statistic value in the older snapshot.
        current: The statistic value in the newer snapshot.
        delta: The signed absolute change (current - previous).
        relative_delta: The signed relative change; None when the previous
            value was zero.
    """

    column: str
    statistic: str
    previous: float | None
    current: float | None
    delta: float | None
    relative_delta: float | None


@dataclass(frozen=True, slots=True)
class DistributionDiff:
    """A significant distribution (mean) shift for one shared numeric column.

    Attributes:
        column: The column name.
        previous_mean: The mean in the older snapshot.
        mean: The mean in the newer snapshot.
        mean_relative_shift: The signed relative mean shift; None when the
            previous mean was zero.
        significant: Whether the shift exceeded the configured threshold.
    """

    column: str
    previous_mean: float | None
    mean: float | None
    mean_relative_shift: float | None
    significant: bool


@dataclass(frozen=True, slots=True)
class LeakageColumnDiff:
    """Leakage status delta for one column between the snapshots.

    Attributes:
        column: The column name.
        previous_severity: Leakage severity in the older snapshot, or None.
        severity: Leakage severity in the newer snapshot, or None.
        status: "new", "removed", "escalated", "de_escalated", or "unchanged".
    """

    column: str
    previous_severity: str | None
    severity: str | None
    status: str

    @property
    def changed(self) -> bool:
        """Return whether the leakage status differs between snapshots."""
        return self.status != "unchanged"


@dataclass(frozen=True, slots=True)
class LeakageDiff:
    """Leakage comparison between the snapshots (only when a target is given).

    Attributes:
        columns: Per-column leakage status deltas.
    """

    columns: tuple[LeakageColumnDiff, ...] = ()

    def __post_init__(self) -> None:
        """Freeze tuple fields to keep the diff immutable."""
        object.__setattr__(self, "columns", tuple(self.columns))

    @property
    def new_findings(self) -> tuple[LeakageColumnDiff, ...]:
        """Return columns where leakage was newly introduced."""
        return tuple(c for c in self.columns if c.status == "new")

    @property
    def removed_findings(self) -> tuple[LeakageColumnDiff, ...]:
        """Return columns where leakage disappeared."""
        return tuple(c for c in self.columns if c.status == "removed")

    @property
    def escalated(self) -> tuple[LeakageColumnDiff, ...]:
        """Return columns where leakage severity increased."""
        return tuple(c for c in self.columns if c.status == "escalated")

    @property
    def de_escalated(self) -> tuple[LeakageColumnDiff, ...]:
        """Return columns where leakage severity decreased."""
        return tuple(c for c in self.columns if c.status == "de_escalated")

    @property
    def changed(self) -> bool:
        """Return whether any leakage difference exists."""
        return any(column.changed for column in self.columns)


@dataclass(frozen=True, slots=True)
class DatasetDiffSummary:
    """Concise, engineering-focused summary of the dataset comparison.

    Mirrors the summary block described in
    ``Dataset-Diff-And-Leakage-Detection.md``: row/column deltas, schema-change
    flag, missing-value and leakage movement, and an overall health verdict.
    """

    rows_added: int
    rows_removed: int
    columns_added: int
    columns_removed: int
    columns_renamed: int
    type_changes: int
    schema_changed: bool
    missing_values_increased: int
    missing_values_decreased: int
    duplicate_rows_increased: bool
    duplicate_rows_decreased: bool
    newly_constant_columns: int
    no_longer_constant_columns: int
    leakage_new: int
    leakage_removed: int
    leakage_escalated: int
    leakage_de_escalated: int
    overall_health: str
    recommendation: str


@dataclass(frozen=True, slots=True)
class DatasetDiffResult:
    """The canonical, fully serializable output of a Dataset Diff run.

    Attributes:
        version: Version of the Dataset Diff result schema.
        schema: Schema-level differences.
        structure: Row and column count differences.
        missing_values: Per-column missingness deltas.
        duplicates: Duplicate-row statistics delta.
        constant_columns: Constant-column changes.
        cardinality: Per-column cardinality deltas.
        statistics: Changed basic statistics for shared numeric columns.
        distributions: Significant distribution shifts.
        leakage: Leakage comparison, or None when no target column was given.
        summary: The overall Dataset Diff Summary.
        overall_summary: A short, templated one-line roll-up of the diff.
    """

    version: str
    schema: SchemaDiff
    structure: StructureDiff
    missing_values: tuple[MissingValueDiff, ...]
    duplicates: DuplicateDiff
    constant_columns: ConstantColumnDiff
    cardinality: tuple[CardinalityDiff, ...]
    statistics: tuple[StatisticDiff, ...]
    distributions: tuple[DistributionDiff, ...]
    leakage: LeakageDiff | None
    summary: DatasetDiffSummary
    overall_summary: str

    def __post_init__(self) -> None:
        """Freeze tuple fields to keep the diff immutable."""
        object.__setattr__(self, "missing_values", tuple(self.missing_values))
        object.__setattr__(self, "cardinality", tuple(self.cardinality))
        object.__setattr__(self, "statistics", tuple(self.statistics))
        object.__setattr__(self, "distributions", tuple(self.distributions))

    def to_dict(self) -> dict[str, Any]:
        """Serialize the diff result to a dictionary of primitive values.

        Returns:
            A dictionary representation suitable for JSON serialization.
        """
        from typing import cast

        return cast(dict[str, Any], _asdict_custom(self))
