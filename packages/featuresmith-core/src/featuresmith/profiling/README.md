# Profiling Module — Featuresmith

The profiling module is the **deterministic analysis engine** of Featuresmith. It consumes a `Dataset` object and produces a strongly-typed `ProfileResult` — the canonical output that every downstream module (Rule Engine, AI Layer, Recommendation Engine, Dashboard, CLI, Exporters) will consume.

---

## Architecture

```
Dataset → profile_dataset() → ProfileResult
```

The profiler **never** mutates the dataset. It only reads from the underlying dataframe and computes statistics. No interpretation, no recommendations, no AI.

---

## Modules

| Module | Responsibility |
|---|---|
| `profiler.py` | Central orchestrator — calls all submodules and assembles `ProfileResult` |
| `summary.py` | Logical type classification, `DatasetMetadata` builder |
| `numeric.py` | Numeric column statistics (mean, std, quartiles, skewness, kurtosis, …) |
| `categorical.py` | Categorical column statistics (cardinality, frequency table, entropy, …) |
| `datetime.py` | Datetime column statistics (min, max, range in days) |
| `text.py` | Text column statistics (lengths, word count, empty/whitespace strings) |
| `correlation.py` | Pairwise Pearson correlation matrix (capped, extensible to Spearman/Kendall) |
| `missing.py` | Missing value analysis (per-column and dataset-wide) |
| `duplicates.py` | Duplicate row analysis; identifies constant and fully empty columns |
| `quality.py` | Helpers for extracting constant/empty columns from column profiles |

---

## Usage

```python
import featuresmith as fs

# From a file path
profile = fs.profile("customers.csv")

# From an in-memory dataframe
import pandas as pd

df = pd.read_csv("customers.csv")
profile = fs.profile(df)

# From a pre-loaded Dataset
dataset = fs.load("customers.csv")
profile = fs.profile(dataset)

# Access structured results
print(profile.dataset_summary.row_count)
print(profile.numeric_profiles["age"].mean)
print(profile.categorical_profiles["country"].top_values)
print(profile.correlation_summary.pearson["age"]["income"])
```

### Advanced: direct profiler call with options

```python
from featuresmith.profiling import profile_dataset

profile = profile_dataset(dataset, max_correlation_columns=50)
```

---

## ProfileResult Structure

```
ProfileResult
├── dataset_summary         → DatasetSummary (row/column counts, type counts, rates)
├── column_profiles         → dict[str, ColumnProfile] (logical type, missing counts)
├── numeric_profiles        → dict[str, NumericProfile] (all numeric statistics)
├── categorical_profiles    → dict[str, CategoricalProfile] (frequencies, entropy)
├── datetime_profiles       → dict[str, DatetimeProfile] (min, max, range)
├── text_profiles           → dict[str, TextProfile] (lengths, word/char counts)
├── missing_value_summary   → MissingValueSummary (per-column and dataset-wide)
├── duplicate_summary       → DuplicateSummary (counts, constant/empty columns)
├── correlation_summary     → CorrelationSummary (Pearson; reserved Spearman/Kendall)
├── dataset_metadata        → DatasetMetadata (source, backend, file_size)
└── execution_metadata      → ExecutionMetadata (start time, duration, version)
```

The `ProfileResult` is serializable via `.to_dict()` for JSON export in later phases.

---

## Logical Type Classification

Each column is classified into one of four logical types:

| Logical Type | Conditions |
|---|---|
| `datetime` | Pandas datetime64 types; Polars Date, Datetime, Time, Duration types |
| `numeric` | Integer or float dtypes (excluding boolean) |
| `categorical` | Boolean dtypes, or string columns with avg length < 20 and low unique ratio |
| `text` | String columns with avg non-null length ≥ 20 chars, or high unique ratio (> 50% and > 10 unique values) |

---

## Interface with Downstream Modules

> `ProfileResult` is the **sole interface** between the Profiling Engine and every downstream module.
>
> - The **Rule Engine** (Sprint 4) will receive `ProfileResult` as its only input.
> - The **AI Layer** (Phase 2) will receive `ProfileResult` serialized to JSON — it never touches the raw dataframe.
> - The **Recommendation Engine** merges `RuleFinding[]` (from the Rule Engine) with AI ranking; both are grounded in the `ProfileResult`.
> - The **Exporter** (Phase 4) and **Dashboard** (Phase 5) consume the `ProfileResult` directly.

---

## Extending the Correlations

The `CorrelationSummary` already reserves `spearman` and `kendall` fields. To add Spearman in a future sprint:

1. Add the computation in `correlation.py`'s `compute_correlations()`.
2. Populate `CorrelationSummary.spearman` — no API changes required.

---

## Performance Notes

- Polars columns are profiled using **batched expression pipelines** (single `select()` call per column where possible) to avoid redundant passes over the data.
- Correlation computation is **capped** at `max_correlation_columns` (default 100) to prevent O(n²) blowup on wide datasets — configurable per call.
- The profiler does **not copy** the underlying dataframe.
