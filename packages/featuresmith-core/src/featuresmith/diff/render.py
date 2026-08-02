"""Render pipeline that turns a DatasetDiffResult into surface-native output.

Following the same pattern as ``featuresmith.review.render``, the renderer is a
pure, read-only transformation over the frozen ``DatasetDiffResult``: it never
recomputes or reinterprets a delta.
"""

from __future__ import annotations

import abc
from collections.abc import Iterable

from featuresmith.diff.schema import (
    DatasetDiffResult,
    DatasetDiffSummary,
    SchemaDiff,
)


class BaseDiffRenderer(abc.ABC):
    """Base class for rendering a DatasetDiffResult into one output format."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Return the target identifier this renderer produces."""
        pass

    @abc.abstractmethod
    def render(self, result: DatasetDiffResult) -> str:
        """Render the diff result into the target format.

        Args:
            result: The frozen DatasetDiffResult.

        Returns:
            The rendered output as a string.
        """
        pass


class DiffConsoleRenderer(BaseDiffRenderer):
    """Render a DatasetDiffResult as a deterministic plain-text terminal report."""

    @property
    def name(self) -> str:
        """Return the target identifier "console"."""
        return "console"

    def render(self, result: DatasetDiffResult) -> str:
        """Render the diff result as a plain-text terminal report.

        Args:
            result: The frozen DatasetDiffResult.

        Returns:
            The plain-text report.
        """
        structure = result.structure
        lines: list[str] = ["Featuresmith Dataset Diff"]
        lines.append(
            f"Rows: {structure.previous_row_count:,} -> {structure.row_count:,} "
            f"(+{structure.rows_added:,} / -{structure.rows_removed:,}) | "
            f"Columns: {structure.previous_column_count:,} -> {structure.column_count:,}"
        )
        lines.append(f"Engine: v{result.version}")
        lines.append("")
        lines.append(result.overall_summary)
        lines.append("")
        lines.extend(self._render_summary(result.summary))
        lines.append("")
        lines.append(f"Recommendation: {result.summary.recommendation}")
        lines.append("")

        details = self._render_details(result)
        if details:
            lines.extend(details)
        else:
            lines.append("No significant changes detected.")
        return "\n".join(lines)

    def _render_summary(self, summary: DatasetDiffSummary) -> list[str]:
        """Render the Dataset Comparison Summary block."""
        return [
            "Dataset Comparison Summary",
            f"  Rows Added: {summary.rows_added:,}",
            f"  Rows Removed: {summary.rows_removed:,}",
            f"  Columns Added: {summary.columns_added:,}",
            f"  Columns Removed: {summary.columns_removed:,}",
            f"  Columns Renamed: {summary.columns_renamed:,}",
            f"  Schema Changed: {'Yes' if summary.schema_changed else 'No'}",
            f"  Type Changes: {summary.type_changes:,}",
            f"  Missing Values Increased: {summary.missing_values_increased:,} column(s)",
            f"  Missing Values Improved: {summary.missing_values_decreased:,} column(s)",
            "  Duplicate Rows Increased: "
            f"{'Yes' if summary.duplicate_rows_increased else 'No'}",
            "  Duplicate Rows Improved: "
            f"{'Yes' if summary.duplicate_rows_decreased else 'No'}",
            f"  Newly Constant Columns: {summary.newly_constant_columns:,}",
            f"  No Longer Constant Columns: {summary.no_longer_constant_columns:,}",
            f"  Leakage New: {summary.leakage_new:,}",
            f"  Leakage Escalated: {summary.leakage_escalated:,}",
            f"  Leakage Removed: {summary.leakage_removed:,}",
            f"  Leakage De-escalated: {summary.leakage_de_escalated:,}",
            f"  Overall Dataset Health: {summary.overall_health}",
        ]

    def _render_details(self, result: DatasetDiffResult) -> list[str]:
        """Render the per-comparison detail sections."""
        lines: list[str] = []
        lines.extend(self._render_schema(result.schema))
        lines.extend(self._render_missing(result))
        lines.extend(self._render_duplicates(result))
        lines.extend(self._render_constants(result))
        lines.extend(self._render_cardinality(result))
        lines.extend(self._render_statistics(result))
        lines.extend(self._render_distributions(result))
        lines.extend(self._render_leakage(result))
        return lines

    def _render_schema(self, schema: SchemaDiff) -> list[str]:
        """Render the schema-change detail section."""
        lines: list[str] = []
        if not schema.changed:
            return lines
        lines.append("Schema Changes")
        if schema.added_columns:
            lines.append("  Added: " + ", ".join(schema.added_columns))
        if schema.removed_columns:
            lines.append("  Removed: " + ", ".join(schema.removed_columns))
        if schema.renamed_columns:
            lines.append(
                "  Renamed: "
                + ", ".join(
                    f"{rename.previous_name} -> {rename.name}"
                    for rename in schema.renamed_columns
                )
            )
        if schema.type_changes:
            lines.append(
                "  Type Changes: "
                + ", ".join(
                    f"{change.column} ({change.previous_dtype} -> {change.dtype})"
                    for change in schema.type_changes
                )
            )
        lines.append("")
        return lines

    def _render_missing(self, result: DatasetDiffResult) -> list[str]:
        """Render the missing-value detail section."""
        if not result.missing_values:
            return []
        lines = ["Missing Values"]
        for diff in result.missing_values:
            lines.append(
                f"  [{diff.status}] {diff.column}: "
                f"{diff.previous_missing_percentage:g}% -> {diff.missing_percentage:g}% "
                f"({diff.delta_count:+d} missing)"
            )
        lines.append("")
        return lines

    def _render_duplicates(self, result: DatasetDiffResult) -> list[str]:
        """Render the duplicate-record detail section."""
        duplicates = result.duplicates
        if (
            duplicates.previous_duplicate_count == duplicates.duplicate_count
            and duplicates.delta_percentage == 0.0
        ):
            return []
        return [
            "Duplicate Records",
            f"  {duplicates.previous_duplicate_percentage:g}% -> "
            f"{duplicates.duplicate_percentage:g}% "
            f"({duplicates.delta_percentage:+g} points)",
            "",
        ]

    def _render_constants(self, result: DatasetDiffResult) -> list[str]:
        """Render the constant-column detail section."""
        constants = result.constant_columns
        if not constants.changed:
            return []
        lines = ["Constant Columns"]
        if constants.newly_constant:
            lines.append("  Newly constant: " + ", ".join(constants.newly_constant))
        if constants.no_longer_constant:
            lines.append(
                "  No longer constant: " + ", ".join(constants.no_longer_constant)
            )
        lines.append("")
        return lines

    def _render_cardinality(self, result: DatasetDiffResult) -> list[str]:
        """Render the high-cardinality detail section."""
        if not result.cardinality:
            return []
        lines = ["Cardinality"]
        for diff in result.cardinality:
            lines.append(
                f"  {diff.column}: {diff.previous_cardinality} -> {diff.cardinality} "
                f"({diff.delta:+d} unique values)"
            )
        lines.append("")
        return lines

    def _render_statistics(self, result: DatasetDiffResult) -> list[str]:
        """Render the basic-statistics detail section."""
        if not result.statistics:
            return []
        lines = ["Statistics"]
        for diff in result.statistics:
            delta = f" ({diff.delta:+g})" if diff.delta is not None else ""
            lines.append(
                f"  {diff.column}.{diff.statistic}: "
                f"{_fmt(diff.previous)} -> {_fmt(diff.current)}{delta}"
            )
        lines.append("")
        return lines

    def _render_distributions(self, result: DatasetDiffResult) -> list[str]:
        """Render the distribution-shift detail section."""
        if not result.distributions:
            return []
        lines = ["Distribution Shifts"]
        for diff in result.distributions:
            relative = (
                f" ({diff.mean_relative_shift:+g} relative)"
                if diff.mean_relative_shift is not None
                else ""
            )
            lines.append(
                f"  [significant] {diff.column}: "
                f"{_fmt(diff.previous_mean)} -> {_fmt(diff.mean)}{relative}"
            )
        lines.append("")
        return lines

    def _render_leakage(self, result: DatasetDiffResult) -> list[str]:
        """Render the leakage-comparison detail section."""
        if result.leakage is None or not result.leakage.columns:
            return []
        lines = ["Leakage"]
        for diff in result.leakage.columns:
            lines.append(
                f"  [{diff.status}] {diff.column}: "
                f"{diff.previous_severity or 'none'} -> {diff.severity or 'none'}"
            )
        lines.append("")
        return lines


class DiffRendererRegistry:
    """Registry of named renderers for dataset diff output targets."""

    def __init__(self, renderers: Iterable[BaseDiffRenderer] = ()) -> None:
        """Initialize the registry with an optional set of initial renderers.

        Args:
            renderers: Iterable of renderer instances to register.
        """
        self._renderers: dict[str, BaseDiffRenderer] = {}
        for renderer in renderers:
            self.register(renderer)

    def register(self, renderer: BaseDiffRenderer) -> None:
        """Register a new renderer instance.

        Args:
            renderer: An instance of a BaseDiffRenderer subclass.
        """
        self._renderers[renderer.name] = renderer

    def get(self, name: str) -> BaseDiffRenderer | None:
        """Retrieve a registered renderer by name.

        Args:
            name: The renderer name.

        Returns:
            The registered BaseDiffRenderer instance, or None if not found.
        """
        return self._renderers.get(name)

    def render(self, name: str, result: DatasetDiffResult) -> str:
        """Render the diff result with a named renderer.

        Args:
            name: The renderer name.
            result: The frozen DatasetDiffResult.

        Returns:
            The rendered output as a string.

        Raises:
            ValueError: If no renderer is registered under the name.
        """
        renderer = self.get(name)
        if renderer is None:
            raise ValueError(f"Unknown diff renderer: '{name}'")
        return renderer.render(result)


def render_diff(result: DatasetDiffResult, target: str = "console") -> str:
    """Render a DatasetDiffResult into the requested target format.

    Args:
        result: The frozen DatasetDiffResult.
        target: Output target name. Only "console" ships in this sprint.

    Returns:
        The rendered output as a string.

    Raises:
        ValueError: If the target renderer is not registered.
    """
    return DiffRendererRegistry((DiffConsoleRenderer(),)).render(target, result)


def _fmt(value: float | None) -> str:
    """Format a float for console output (None renders as 'n/a')."""
    if value is None:
        return "n/a"
    return f"{value:g}"
