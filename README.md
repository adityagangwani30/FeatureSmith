# Featuresmith

Featuresmith is an AI-powered feature engineering and EDA platform organized as one reusable Python core with thin client surfaces.

**Current Version:** `v0.0.4-dev`

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

## Analyze a Dataset (Rule Engine)

Sprint 4 provides the deterministic Rule Engine. The `analyze()` function
accepts the same sources as `load()` and `profile()`, runs the full pipeline
(`load → profile → rule_engine.run()`), and returns a strongly-typed
`RuleResult`:

```python
import featuresmith as fs

# From a file path
result = fs.analyze("customers.csv")

# From an in-memory dataframe
import pandas as pd

df = pd.read_csv("customers.csv")
result = fs.analyze(df)

# With a target column for leakage detection
result = fs.analyze(df, target_column="churn")

# Inspect findings
for finding in result.findings:
    print(f"[{finding.severity.upper()}] {finding.title}")
    print(f"  Column : {finding.column_name}")
    print(f"  Rule   : {finding.rule_id}")
    print(f"  Detail : {finding.description}")

# Execution metadata
print(f"Rules executed : {result.executed_rules}")
print(f"Execution time : {result.execution_time_ms:.1f} ms")

# Full serialization
import json

data = result.to_dict()
print(json.dumps(data, indent=2, default=str))
```

### Rules implemented

| Rule ID | Category | Default severity | Description |
|---|---|---|---|
| `quality.missing_value_threshold` | quality | warning | Flags columns > 20% missing (configurable) |
| `quality.duplicate_rows` | quality | warning | Flags datasets with > 10% duplicate rows (configurable) |
| `quality.constant_columns` | quality | warning | Flags columns with exactly one unique non-null value |
| `quality.fully_empty_columns` | quality | critical | Flags columns with only null values |
| `statistical.high_cardinality` | statistical | warning | Flags categorical columns with unusually high unique ratios |
| `statistical.outliers` | statistical | warning | Detects numeric outliers via IQR method |
| `statistical.high_correlation` | statistical | warning | Flags numeric feature pairs with Pearson correlation ≥ 0.90 |
| `leakage.potential_leakage` | leakage | critical | Flags features with correlation ≥ 0.99 to the target column |

### Full pipeline

```
Raw Data
   │
   ▼
[Connector] → Dataset
                │
                ▼
         [Profiler] → ProfileResult
                          │
                          ▼
                   [Rule Engine] → RuleResult
                    (8 seed rules)     │
                                       ▼
                      findings: list[RuleFinding]
                                       │
                                       ▼
                   [Future Recommendation Engine]
```

## Command Line Interface (CLI)

Featuresmith CLI provides a fast, local-first terminal interface for dataset profiling and rule evaluation. It calls the public SDK to perform analysis, ensuring full consistency with programmatic SDK usage.

### Installation

To install the CLI in the workspace development environment:
```bash
uv sync --all-packages
```

### Usage Examples

**1. Basic Analysis (Styled Rich Table)**
```bash
uv run featuresmith analyze customers.csv
```

**2. Target Column for Leakage Detection**
Specify the target label column to check for potential feature leakage:
```bash
uv run featuresmith analyze customers.csv --target churn
```

**3. Format Outputs as JSON**
Output a standardized JSON structure for scripting or piping to other utilities:
```bash
uv run featuresmith analyze customers.csv --format json
```

**4. Filtering and Exit Gating by Severity**
Only display findings at or above a threshold (`info`, `warning`, `critical`). The CLI will return exit code `1` if any findings meet or exceed this threshold:
```bash
uv run featuresmith analyze customers.csv --severity warning
```

**5. Save the Report to a File**
Save the rendered report to disk. Text reports have ANSI escape sequences stripped automatically; JSON reports are saved as standard JSON:
```bash
uv run featuresmith analyze customers.csv --output report.txt
uv run featuresmith analyze customers.csv --format json --output report.json
```

**6. Quiet Mode**
Suppress all console outputs while writing the report directly to a file:
```bash
uv run featuresmith analyze customers.csv --output report.txt --quiet
```

### CLI Exit Codes

- `0` — Success (analysis completed, no findings met or exceeded the severity threshold).
- `1` — Analysis completed, but quality findings meeting or exceeding the threshold were detected.
- `2` — Invalid input (e.g. invalid target column name, bad option value).
- `3` — File loading/parsing failure (e.g. non-existent file, corrupted format).
- `4` — Unexpected internal error (pass `--verbose` to view full traceback).

## Workspace Structure

```text
/
├── packages/
│   ├── featuresmith-core/
│   │   └── src/featuresmith/
│   │       ├── core/           # Dataset, schemas, ProfileResult, RuleFinding, RuleResult
│   │       ├── connectors/     # CSV, Excel, Parquet, DataFrame connectors
│   │       ├── profiling/      # Deterministic profiling engine (Sprint 3)
│   │       ├── rules/          # Rule Engine + 8 seed rules (Sprint 4)
│   │       └── api.py          # Public SDK: fs.load(), fs.profile(), fs.analyze()
│   ├── featuresmith-cli/
│   └── featuresmith-dashboard/
├── tests/
│   ├── connectors/
│   ├── core/
│   ├── profiling/
│   └── rules/                  # Rule Engine tests (Sprint 4)
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

## Project Roadmap

Featuresmith is being built incrementally. See [Phases.md](./docs/Phases.md) for the detailed execution plan:

*   **Phase 0 (Foundations):** Workspace, packages, CI/CD, and schema definitions. (Completed)
*   **Phase 1 (SDK & CLI MVP):** Local data connectors, statistical profiling, and rule engine. (Completed)
*   **Phase 2 (AI Narration):** Grounded dataset summary and explainable recommendations.
*   **Phase 3 (Interactive AI Chat):** Contextual natural-language exploration of findings.
*   **Phase 4 (Export Layer):** Production-grade pipeline code generation (scikit-learn).
*   **Phase 5 (Dashboard):** Streamlit interactive UI.

## Contributing

1. Create a branch.
2. Make changes in the appropriate package.
3. Run formatting, linting, type checking, and tests locally.
4. Open a pull request.

Before contributing, read [MEMORY.md](./MEMORY.md) and the project documents in
[`docs/`](./docs/).

