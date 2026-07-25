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

Every supported source returns the same lightweight `Dataset` object. It
exposes `dataframe`, `backend`, `schema`, `metadata`, `row_count`,
`column_count`, `dtypes`, `source`, `file_size`, and `preview()`.

No profiling, rules, AI, exports, dashboard behavior, or feature engineering
is included in this loading API.

## Workspace Structure

```text
/
├── packages/
│   ├── featuresmith-core/
│   ├── featuresmith-cli/
│   └── featuresmith-dashboard/
├── tests/
├── docs/
├── examples/
├── .github/workflows/
├── pyproject.toml
├── .pre-commit-config.yaml
├── .gitignore
├── LICENSE
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
