# Changelog

All notable changes to Featuresmith are documented here.

This project adheres to [Semantic Versioning](https://semver.org/) and
[Conventional Commits](https://www.conventionalcommits.org/).

---

## [0.3.0] - 2026-08-15

Closes the v0.2.0/design gap (`Architecture.md` §21.4): Dataset Diff is now integrated into the Review Engine as `DiffReviewer`, and the project governance baseline is published.

### Added
- **`DiffReviewer`** (`review.diff`) — diff-aware review integrated into the Review Engine:
  - `fs.review(source, previous=...)` now succeeds instead of raising `NotImplementedError`; it loads and profiles the previous snapshot once at the SDK boundary and passes `previous_profile` to the engine
  - `featuresmith review <source> --previous <snapshot>` activates the diff section; exit 3 on a missing/unparseable previous source, exit 2 on an unknown target column in either snapshot
  - `ReviewResult.diff` attaches the `DatasetDiffResult` when a previous snapshot is provided; `None` otherwise
  - `DiffReviewer` reuses the standalone diff engine (`compute_diff()` + `findings_from_diff()`) — no second diffing code path, no re-profiling of the previous snapshot when a previous profile is available
  - Single-dataset review is unchanged: 8 sections, no diff section, `result.diff is None`
- **`GOVERNANCE.md`** — project governance baseline (decision process, roadmap governance, contribution standards)

### Changed
- Version bumped to `0.3.0` across all packages (core, cli, workspace)
- `REVIEW_ENGINE_VERSION` bumped to `"0.3.0"`; `default_registry()` now ships 9 built-in reviewers
- `fs.review(previous=...)` no longer raises `NotImplementedError` (the standalone `fs.diff()`/`featuresmith diff` path remains unchanged)

### Fixed
- `featuresmith review --previous` previously errored; it now produces a diff-aware review

---

## [0.2.0] - 2026-08-02

Completes Phase 2 of the roadmap: Review Engine, ML Readiness Score, Dataset Diff, and Intelligent Leakage Detection.

### Added
- **Review Engine** (`featuresmith.review`) — orchestration layer with 8 built-in reviewers:
  - `SchemaHealthReviewer` (schema health, dtype consistency)
  - `TypeReviewer` (data type appropriateness)
  - `MissingValueReviewer` (missingness ratios and patterns)
  - `DuplicateReviewer` (duplicate row detection)
  - `ConstantColumnReviewer` (zero/near-zero variance columns)
  - `CardinalityReviewer` (high-cardinality categorical columns)
  - `BasicStatisticsReviewer` (distribution statistics)
  - `LeakageReviewer` (6 pattern detectors merged per column)
- **ML Readiness Score** (`featuresmith.scoring`) — deterministic, explainable 0-100 score with 8 dimensions:
  - Schema Health, Missing Values, Duplicate Records, Data Types, Constant Columns, High Cardinality, Dataset Structure, Leakage Risk
  - Per-dimension breakdown with rationale, contributing findings, and suggested actions
  - `scoring_version = "0.2.0"` (bumped from `0.1.0` with Leakage Risk addition)
- **Dataset Diff Engine** (`featuresmith.diff`) — standalone comparison engine:
  - `fs.diff(old, new)` SDK and `featuresmith diff` CLI
  - Schema, structure, missing values, duplicates, constants, cardinality, statistics, distribution shifts, and leakage deltas
  - Overall health verdict: regressed / improved / unchanged
  - Plain-language engineering recommendation
- **Intelligent Leakage Detection** — 6 named pattern detectors in `featuresmith.rules.leakage`:
  - `TargetCorrelationDetector`, `IdentifierShapeDetector`, `TimestampLeakageDetector`, `FutureInfoDetector`, `DuplicateTargetDetector`, `SuspiciousCorrelationDetector`
  - Findings merged per column, confidence levels, rationale
  - Legacy `LeakageRuleTargetCorrelation` preserved for backward compatibility
- **CLI Commands**:
  - `featuresmith review` — with `--target`, `--format`, `--output`, `--fail-on`, `--only`, `--no-score`, `--quiet`, `--verbose`, `--version`
  - `featuresmith diff` — with `--target`, `--format`, `--output`, `--fail-on`, `--quiet`, `--verbose`, `--version`
- **SDK Entrypoints** in `featuresmith.api`:
  - `fs.review()`, `fs.diff()`, `fs.diff_findings()`, `fs.score()`
- **Implementation Status Tracker** — `docs/implementation/IMPLEMENTATION_STATUS.md`

### Changed
- Version bumped to `0.2.0` across all packages (core, cli, workspace)
- `ReviewCategory` enum: 6 categories (schema, quality, leakage, diff, feature_quality, custom)
- `fs.review(previous=...)` raises `NotImplementedError` with guidance to use `fs.diff()`
- Leakage Risk dimension integrated into ML Readiness Score (scoring version bumped)

### Fixed
- `DatasetDiffSummary.columns_added/removed` now correctly derive from `SchemaDiff.added_columns/removed_columns` (not structure counts)

---

## [0.1.0] - 2026-07-27

The first public release. Completes Phase 1 of the roadmap: SDK + CLI MVP with deterministic profiling, a rule engine, and robust engineering validations.

### Added
- `featuresmith-core` — production-grade core library.
- `featuresmith-cli` — Typer-based CLI wrapper (`featuresmith analyze`).
- Unified `Dataset` abstraction with normalized schema across all sources.
- Built-in connectors: CSV (Polars), Excel (pandas), Parquet (Polars), pandas DataFrame, and Polars DataFrame.
- Deterministic Profiling Engine (`fs.profile()`) computing numeric stats, categorical cardinality/entropy, datetime range, text metrics, and Pearson correlation matrices.
- Deterministic Rule Engine (`fs.analyze()`) with 8 seed rules covering missingness, duplicates, constant columns, fully empty columns, high cardinality, outliers, high correlations, and potential target leakage.
- Strong typing — `frozen=True` dataclasses throughout (`Dataset`, `ProfileResult`, `RuleFinding`, `RuleResult`) with full type annotations.
- Full serialization support via `.to_dict()` and standard primitives.
- PEP 561 support (`py.typed` markers) for downstream type checking.
- Package boundary enforcement via `import-linter` contract (CLI may only import `featuresmith.api`).
- Comprehensive GitHub Actions CI: Ruff lint/format, MyPy strict type checks, pytest unit/integration test suite, and pip-audit scans.

### Fixed
- Enforced explicit rule thresholds by removing ambiguous ratio-to-percentage auto-coercion.
- Added eager `RuleEngine` configuration checking of types and keys using signature binding to fail early.
- Capped `frequency_table` size in categorical profiling (default 1000) to prevent memory and payload bloat on high-cardinality columns.
- Introduced specific typed exceptions (`SourceNotFoundError`, `UnsupportedFormatError`, `SourceParseError`) inheriting from `ConnectorError` in loaders and CLI exit codes.
- Frozen collection fields using `MappingProxyType` and `tuple` to ensure strict runtime immutability.
- Corrected package installation references and unified versions across repository to `0.1.0`.
- Expanded CI matrix to cover Windows/Ubuntu and Python 3.11, 3.12, and 3.13.
- Isolated JIT compilation noise from performance benchmarks, and documented native memory caveats.
- Cleaned up example directories from being polluted by test output.
