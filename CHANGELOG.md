# Changelog

All notable changes to Featuresmith are documented here.

This project adheres to [Semantic Versioning](https://semver.org/) and
[Conventional Commits](https://www.conventionalcommits.org/). Packages in this
workspace are versioned independently: `featuresmith` (core),
`featuresmith-cli`, and `featuresmith-dashboard`.

---

## [Unreleased] — v0.1.0 (Upcoming)

The first public release. Completes Phase 1 of the roadmap: SDK + CLI MVP with
deterministic profiling and a rule engine. No AI features in this release.

### Added

- `featuresmith-core` — production-grade core library
- `featuresmith-cli` — CLI wrapper (`featuresmith analyze`)
- Unified `Dataset` abstraction with normalized schema
- Connectors: CSV, Excel, Parquet, pandas DataFrame, Polars DataFrame
- Deterministic Profiling Engine (`fs.profile()`)
  - 23-metric numeric profiler
  - Categorical column profiler (cardinality, entropy, frequency tables)
  - Datetime column profiler (range, min/max)
  - Text column profiler (length stats, word/char counts)
  - Pearson correlation matrix (capped at configurable column count)
  - Missing value analysis (per-column and dataset-wide)
  - Duplicate and constant column detection
- Deterministic Rule Engine (`fs.analyze()`) with 8 seed rules:
  - `quality.missing_value_threshold`
  - `quality.duplicate_rows`
  - `quality.constant_columns`
  - `quality.fully_empty_columns`
  - `statistical.high_cardinality`
  - `statistical.outliers`
  - `statistical.high_correlation`
  - `leakage.potential_leakage`
- `featuresmith analyze <source>` CLI command with:
  - `--target` for leakage detection
  - `--format {table,json}` output modes
  - `--output` file export (ANSI-stripped for `.txt`, JSON for `.json`)
  - `--severity {info,warning,critical}` filter + exit-code gating
  - `--max-correlation-columns` correlation cap override
  - `--quiet` / `--verbose` modes
  - `--version` eager version display
  - Exit codes: 0 (clean), 1 (findings), 2 (invalid input), 3 (load failure), 4 (unexpected error)
- Strong typing — `frozen=True` dataclasses throughout (`Dataset`, `ProfileResult`, `RuleFinding`, `RuleResult`)
- Full serialization via `.to_dict()` / `asdict()`
- Import boundary enforcement via `import-linter` contract (CLI may only import `featuresmith.api`)
- CI with GitHub Actions: ruff, mypy, pytest, import-linter
- Pre-commit hooks
- ADR 0001: Connector dependency choices
- ADR 0002: CLI dependency choices

---

## Development History

### Sprint 5 — CLI MVP (2026-07-26)

- Built `featuresmith-cli` package with Typer entrypoint
- Implemented `featuresmith analyze` command
- Added Rich terminal report with Dataset Overview, Analysis Findings, and Execution Summary tables
- Added JSON output mode using `RuleResult.to_dict()` canonical serialization
- Added ANSI strip utility for plain-text file exports
- Added `tests/cli/test_cli.py` with 14 integration test scenarios
- Updated `featuresmith.api` to re-export types as explicit `as X` re-exports for mypy compliance
- Updated `import-linter` contract with `ignore_imports` list for transitive paths

### Sprint 4 — Deterministic Rule Engine (2026-07-25)

- Added `RuleFinding` and `RuleResult` frozen dataclasses
- Built complete Rule Engine: `BaseRule`, `RuleRegistry`, `RuleEngine`
- Implemented 8 seed rules
- Added `fs.analyze()` to the public SDK
- Added `tests/rules/test_rules.py` with 12 test scenarios
- Updated `featuresmith.api` with `max_correlation_columns` parameter

### Sprint 4 Quality Pass (2026-07-25)

- Updated all versions to `0.0.4-dev`
- Standardized Google-style docstrings across all public classes and functions
- Verified ruff, mypy, pytest, and import-linter on both pandas and Polars

### Sprint 3 — Deterministic Profiling Engine (2026-07-25)

- Added `ProfileResult` and 11 inner schema dataclasses
- Built complete profiling engine (11 modules)
- Added `fs.profile()` to the public SDK
- Added `tests/profiling/test_profiler.py` with 11 test scenarios

### Sprint 2 — Dataset Foundation & Connector System (2026-07-25)

- Added normalized `Dataset` and schema contracts
- Added CSV, Excel, Parquet, pandas, and Polars connectors
- Added `fs.load()` to the public SDK
- Added typed `ConnectorError` hierarchy
- Added ADR 0001

### Sprint 1 — Foundations (2026-07-25)

- Established uv workspace with three packages
- Configured Ruff, MyPy, pytest, import-linter, pre-commit
- Set up GitHub Actions CI
- Published documentation skeleton (Architecture, PRD, Rules, Phases, Design)

---

## Upcoming Releases

| Version | Focus |
|---------|-------|
| v0.1.0 | First public release (Phase 1 complete) |
| v0.3.0 | AI Provider Layer + narration (Phase 2) |
| v0.4.0 | Interactive AI Chat (Phase 3) |
| v0.5.0 | Export Layer — sklearn pipelines, notebooks (Phase 4) |
| v1.0.0 | Streamlit Dashboard + multi-source connectors (Phase 5) |
