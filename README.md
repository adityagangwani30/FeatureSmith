<div align="center">

<img src="media/github_banner.png" alt="Featuresmith Banner" width="100%" />

# Featuresmith

**Make data quality as routine as code quality.**

An open-source, developer-first toolkit for understanding, validating, and improving structured data.

[![Version](https://img.shields.io/badge/version-0.2.0-blue?style=flat-square)](https://github.com/adityagangwani30/FeatureSmith/releases)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green?style=flat-square)](./LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/adityagangwani30/FeatureSmith/ci.yml?branch=main&style=flat-square&label=CI)](https://github.com/adityagangwani30/FeatureSmith/actions)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)
[![MyPy](https://img.shields.io/badge/mypy-strict-blueviolet?style=flat-square)](https://mypy-lang.org/)
[![Tests](https://img.shields.io/badge/tests-pytest-yellow?style=flat-square&logo=pytest)](https://docs.pytest.org/)

<br />

[📖 Documentation Website](https://featuresmith.adityagangwani.me) · [🚀 Quick Start](#quick-start) · [💬 Discussions](https://github.com/adityagangwani30/FeatureSmith/discussions)

</div>

---

## Hero Message

> **Every dataset deserves a code review.**
>
> Make data quality as routine as code quality.

---

## Why Featuresmith Exists

### The problem: engineering discipline stops at the dataset's edge
Every serious codebase today has Git, pull requests, tests, CI/CD, linters, formatters, and static analysis. Datasets, which are just as load-bearing for a machine learning system as the code around them, get almost none of it. A column can go missing, a categorical can silently leak the target, a distribution can drift — and nothing stops it because no tests are running.

Tooling that does exist is fragmented: one tool profiles, another validates, another detects drift, another monitors. None of them talk to each other.

### Our answer: one toolkit, one loop
Understanding, validating, and improving a dataset is one continuous engineering workflow, served by one extensible toolkit:
- **Understand** — profile a dataset's shape, distributions, and relationships.
- **Validate** — catch data-quality and leakage issues with deterministic, testable rules.
- **Improve** — turn accepted findings into real, reviewable code.

### Why this is a developer tool, not a dashboard
Tools that developers adopt look like `ruff`, `pytest`, or `pre-commit` — something you run automatically in CI. Featuresmith is built to be run from your CLI or imported in python. The dashboard and chat exist only to serve the moments a plain CLI check isn't enough, not to replace the check itself.

### Why AI is an assistant here, not the identity
An LLM is used solely to turn structured findings into plain-language explanations or rationales. It never computes the findings themselves. The deterministic engine runs completely with the AI layer switched off, and raw dataset data is never sent to the network.

---

## Current Capabilities (v0.2.0)

- **Dataset Profiling**: Polars-driven deterministic profiling engine computing 23 numeric metrics, categorical frequencies, text lengths, datetime ranges, and Pearson correlation matrices.
- **Rule-Based Validation**: Deterministic rule engine running 8 built-in seed quality and leakage rules (missing value thresholds, constant columns, duplicate rows, target leakage).
- **Intelligent Leakage Detection**: 6 named pattern detectors (target correlation, identifier shape, timestamp, future info, duplicate target, suspicious correlation) with merged per-column findings.
- **Dataset Diff**: Standalone diff engine comparing two dataset snapshots — schema, structure, quality, distribution, and leakage deltas with overall health verdict.
- **Review Engine**: Orchestration layer with 8 built-in reviewers (schema health, types, missingness, duplicates, constants, cardinality, basic statistics, leakage), category filtering, and console rendering.
- **ML Readiness Score**: 8-dimension deterministic, explainable score (0-100) computed from review findings with per-dimension breakdown.
- **Python SDK**: Clean, fully type-annotated public API (`fs.load()`, `fs.profile()`, `fs.analyze()`, `fs.diff()`, `fs.review()`, `fs.score()`).
- **Command Line Interface (CLI)**: Thin wrapper client enabling terminal reports (styled Rich tables), JSON output, and exit-code gating for CI/CD integration (`featuresmith analyze`, `featuresmith diff`, `featuresmith review`).
- **Documentation**: Complete set of engineering guides, ADRs, API references, and implementation status tracker.

---

## Installation

Install Featuresmith from PyPI:

**Using pip**
```bash
pip install featuresmith-core featuresmith-cli
```

**Using uv**
```bash
uv add featuresmith-core featuresmith-cli
```

**From Source (Development)**
```bash
git clone https://github.com/adityagangwani30/FeatureSmith.git
cd FeatureSmith
uv sync
```

---

## Quick Start

```python
import featuresmith as fs

# 1. Load data normalized
dataset = fs.load("customers.csv")
print(f"Loaded {dataset.row_count} rows across columns: {dataset.schema.names}")

# 2. Run deterministic profiling
profile = fs.profile("customers.csv")
for col_name, col in profile.column_profiles.items():
    print(f"{col_name}: {col.missing_count} missing values")

# 3. Analyze against rules (with target leakage detection)
result = fs.analyze("customers.csv", target_column="churn")
for finding in result.findings:
    print(f"[{finding.severity.upper()}] {finding.title} on column '{finding.column_name}'")
    print(f"  Details: {finding.description}")
```

---

## Example Usage (CLI)

```bash
# Basic terminal analysis table
featuresmith analyze customers.csv

# Leakage detection targeting churn with exit-code gating for CI
featuresmith analyze customers.csv --target churn --severity warning

# Output as machine-readable JSON to a file
featuresmith analyze customers.csv --format json --output report.json

# Compare two dataset snapshots (schema, quality, distribution, leakage)
featuresmith diff train_v1.csv train_v2.csv --target churn

# Comprehensive dataset review with ML Readiness Score
featuresmith review train.csv --target churn

# Review with category filter and CI gating
featuresmith review train.csv --only leakage,schema --fail-on warning --no-score
```

### Exit Codes

All commands share a consistent exit-code convention:

| Code | Meaning |
|:---:|---|
| `0` | Clean — no findings detected at or above the severity threshold |
| `1` | Findings detected at or above the severity threshold (trips CI/CD gate) |
| `2` | Invalid input (bad flag, missing column, unsupported format) |
| `3` | File load / parse failure |
| `4` | Unexpected internal error |

---

## Flagship Vision (v0.2.0 — Partially Delivered)

The following flagship capabilities are **partially delivered** in v0.2.0 and will continue maturing:

- **Dataset Review (`featuresmith review <dataset>`)**: ✅ Implemented with 8/11 review sections, ML Readiness Score, category filtering, and CLI/SDK. Missing: recommendations, duplicate columns, outliers, distribution, feature quality sections; diff-aware review (`--previous`) uses standalone `fs.diff()` instead.
- **ML Readiness Score**: ✅ Implemented with 8 dimensions, per-dimension breakdown, CLI/SDK access. Missing: Class Balance, Feature Quality, Distribution Health dimensions; CI score gating (`--fail-below`).
- **Dataset Diff (`featuresmith diff <v1> <v2>`)**: ✅ Fully implemented as standalone engine with schema, structure, quality, distribution, and leakage deltas. Not integrated as a Review Engine reviewer (uses separate `fs.diff()` workflow).
- **Intelligent Leakage Detection**: ✅ Fully implemented with 6 pattern detectors, merged findings, and scoring integration.

---

## Documentation

Visit [featuresmith.adityagangwani.me](https://featuresmith.adityagangwani.me) for comprehensive guides.

### Local Documentation Files
- [`docs/Architecture.md`](./docs/Architecture.md) — System design, JIT scaling constraints, AI providers
- [`docs/PRD.md`](./docs/PRD.md) — Product requirements, metrics, scope
- [`docs/Rules.md`](./docs/Rules.md) — Testing requirements, coding standards, and PR guidelines
- [`docs/Phases.md`](./docs/Phases.md) — Acceptance criteria per phase
- [`docs/Design.md`](./docs/Design.md) — Design system, typography, accessibility tokens
- [`docs/Why-Featuresmith-Exists.md`](./docs/Why-Featuresmith-Exists.md) — Detailed philosophy rationale
- [`docs/Flagship-Capabilities.md`](./docs/Flagship-Capabilities.md) — Deeper future capability specs

---

## Roadmap

| Phase | Version | Focus | Status |
|:---:|:---:|---|:---:|
| **Phase 0** | pre-release | Monorepo foundations, CI/CD, Pydantic schemas, Base interfaces | ✅ Complete |
| **Phase 1** | v0.1 | EDA & Rule Engine, SDK, CLI, CSV/DataFrame connectors | ✅ Complete |
| **Phase 2** | v0.2 | Review Engine, ML Readiness Score, Dataset Diff, Leakage Detection | ✅ Complete |
| **Phase 3** | v0.3 | Dashboard UI, SQL connectors, plugins registry, GitHub Action | 🔜 Planned |
| **Phase 4** | v0.4 | Feature Engineering Engine, Recommendation Engine, Exporters | 🔜 Planned |
| **Phase 5** | v0.5 | Observability history, scheduled re-profiling, alerts | 🔜 Planned |
| **Phase 6** | v1.0 | AI Provider layer, chat Q&A, plain-text narration | 🔜 Planned |
| **Phase 7** | v2.0 | VS Code extension, Jupyter magic, natural-language commands | 🔜 Planned |
| **Phase 8** | v3.0+ | Snowflake/BigQuery pushdown, Spark/Ray backend, hosted SaaS | 🔜 Planned |

---

## Contributing

We welcome community contributions. The best entry points are custom rules and connectors, which are completely pluggable.

1. Fork the repo and clone locally.
2. Run `uv sync` to configure the workspace environment.
3. Install git hooks: `pre-commit install`.
4. Ensure tests and formatting pass: `uv run pytest` & `uv run ruff check .`
5. Refer to [`CONTRIBUTING.md`](./CONTRIBUTING.md) and [`docs/Rules.md`](./docs/Rules.md) before opening a PR.

---

## License

Featuresmith is licensed under the Apache 2.0 License. See [`LICENSE`](./LICENSE) for details.
