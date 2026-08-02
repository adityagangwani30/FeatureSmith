"""Dataset Diff Engine for comparing two dataset profile snapshots.

The Dataset Diff Engine reuses the profiling engine and the leakage reviewers
to produce a typed ``DatasetDiffResult`` describing exactly what changed between
two snapshots — the equivalent of a git diff for structured datasets. See
``docs/features/Dataset-Diff-And-Leakage-Detection.md`` for the design.
"""

from featuresmith.diff.engine import DatasetDiffEngine, compute_diff
from featuresmith.diff.findings import findings_from_diff
from featuresmith.diff.render import (
    BaseDiffRenderer,
    DiffConsoleRenderer,
    DiffRendererRegistry,
    render_diff,
)
from featuresmith.diff.schema import (
    DIFF_ENGINE_VERSION,
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

__all__ = [
    "DIFF_ENGINE_VERSION",
    "BaseDiffRenderer",
    "CardinalityDiff",
    "ColumnRename",
    "ColumnTypeChange",
    "ConstantColumnDiff",
    "DatasetDiffEngine",
    "DatasetDiffResult",
    "DatasetDiffSummary",
    "DiffConfig",
    "DiffConsoleRenderer",
    "DiffRendererRegistry",
    "DistributionDiff",
    "DuplicateDiff",
    "LeakageColumnDiff",
    "LeakageDiff",
    "MissingValueDiff",
    "SchemaDiff",
    "StatisticDiff",
    "StructureDiff",
    "compute_diff",
    "findings_from_diff",
    "render_diff",
]
