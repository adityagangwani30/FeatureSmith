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

