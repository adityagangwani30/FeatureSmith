# Core primitives

`featuresmith.core` contains typed contracts shared by the Featuresmith
pipeline. Sprint 2 introduces `Dataset`, `DatasetSchema`, and `ColumnSchema`.

`Dataset` is the canonical object returned by connectors and passed to future
pipeline stages. It deliberately offers only normalization and `preview()`;
profiling, rules, and source-specific behavior do not belong here.

## Sprint 3 additions — ProfileResult

`profile_result.py` defines the canonical output of the profiling engine:

| Class | Purpose |
|---|---|
| `ProfileResult` | Top-level container — the sole input to all downstream modules |
| `DatasetSummary` | Row/column counts, logical type counts, missing/duplicate rates |
| `ColumnProfile` | Per-column logical type, missing count, constant/empty flags |
| `NumericProfile` | Full numeric statistics for a single column |
| `CategoricalProfile` | Cardinality, frequency tables, entropy for a single column |
| `DatetimeProfile` | Min/max timestamps and day range for a single column |
| `TextProfile` | Length and word-count statistics for a single column |
| `MissingValueSummary` | Per-column and dataset-wide missing value analysis |
| `DuplicateSummary` | Duplicate rows, constant columns, fully empty columns |
| `CorrelationSummary` | Pearson correlation matrix (Spearman/Kendall reserved) |
| `DatasetMetadata` | Source path, file size, backend identifier |
| `ExecutionMetadata` | Profiling run timestamps and duration |

All classes are `frozen=True` dataclasses. `ProfileResult.to_dict()` produces a
serializable dict for future JSON export.
