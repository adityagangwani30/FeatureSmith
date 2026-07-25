# Featuresmith

Featuresmith is an AI-powered feature engineering and EDA platform organized as one reusable Python core with thin client surfaces.

## Project Overview

The repository is structured as a uv workspace with three installable Python distributions:

- `featuresmith-core` for the reusable core library
- `featuresmith-cli` for the command-line surface
- `featuresmith-dashboard` for the Streamlit dashboard surface

The CLI and dashboard are intentionally thin clients that depend only on the public `featuresmith.api` module.

## Installation

```bash
uv sync
```

## Load a Dataset

Sprint 2 provides the normalized dataset foundation. Load a local CSV, Excel,
or Parquet file, or pass an in-memory pandas or Polars DataFrame directly:

```python
import featuresmith as fs

dataset = fs.load("customers.csv")
print(dataset.row_count)
print(dataset.schema.names)
print(dataset.preview())
```

## Profile a Dataset

Sprint 3 provides the deterministic profiling engine. The `profile()` function
accepts the same sources as `load()` — a file path, an in-memory dataframe,
or a pre-loaded `Dataset` — and returns a strongly-typed `ProfileResult`:

```python
import featuresmith as fs

# From a file path
profile = fs.profile("customers.csv")

# From an in-memory dataframe
import pandas as pd

df = pd.read_csv("customers.csv")
profile = fs.profile(df)

# Explore the results
print(profile.dataset_summary.row_count)
print(profile.dataset_summary.num_numeric_columns)
print(profile.numeric_profiles["age"].mean)
print(profile.numeric_profiles["age"].std_dev)
print(profile.categorical_profiles["country"].top_values)
print(profile.categorical_profiles["country"].entropy)
print(profile.missing_value_summary.dataset_missing_percentage)
print(profile.duplicate_summary.duplicate_rows_count)
print(profile.correlation_summary.pearson["age"]["income"])

# Full serialization
import json

data = profile.to_dict()
print(json.dumps(data, indent=2, default=str))
```

### ProfileResult structure at a glance

```
ProfileResult
├── dataset_summary         → row/column counts, type counts, missing/duplicate rates
├── column_profiles         → per-column logical type, missing count, constant/empty flags
├── numeric_profiles        → mean, median, std, quartiles, skewness, kurtosis, …
├── categorical_profiles    → cardinality, frequency table, entropy, top/bottom values
├── datetime_profiles       → min date, max date, range in days
├── text_profiles           → avg/min/max length, word count, empty/whitespace counts
├── missing_value_summary   → per-column and dataset-wide missing analysis
├── duplicate_summary       → duplicate rows, constant columns, fully empty columns
├── correlation_summary     → Pearson matrix (Spearman/Kendall reserved for future)
├── dataset_metadata        → source path, file size, backend
└── execution_metadata      → start time, duration, version
```

`ProfileResult` is the canonical interface between the Profiling Engine and
every downstream module: the Rule Engine (Sprint 4), the AI Layer (Phase 2),
the Recommendation Engine, and the Exporters all consume only this object —
never the raw dataframe.

## Workspace Structure

```text
/
├── packages/
│   ├── featuresmith-core/
│   │   └── src/featuresmith/
│   │       ├── core/           # Dataset, schemas, ProfileResult
│   │       ├── connectors/     # CSV, Excel, Parquet, DataFrame connectors
│   │       ├── profiling/      # Deterministic profiling engine (Sprint 3)
│   │       └── api.py          # Public SDK: fs.load(), fs.profile()
│   ├── featuresmith-cli/
│   └── featuresmith-dashboard/
├── tests/
│   ├── connectors/
│   ├── core/
│   └── profiling/
├── docs/
├── examples/
├── .github/workflows/
├── pyproject.toml
└── README.md
```

## Developer Setup

```bash
uv sync
pre-commit install
```

## Running Tests

```bash
pytest
# or verbose
pytest -v
```

## Formatting

```bash
ruff format
```

## Linting

```bash
ruff check
```

## Type Checking

```bash
mypy .
```

## Contributing

1. Create a branch.
2. Make changes in the appropriate package.
3. Run formatting, linting, type checking, and tests locally.
4. Open a pull request.

Before contributing, read [MEMORY.md](./MEMORY.md) and the project documents in
[`docs/`](./docs/).
