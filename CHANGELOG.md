# Changelog

All notable changes to Featuresmith are documented here.

This project adheres to [Semantic Versioning](https://semver.org/) and
[Conventional Commits](https://www.conventionalcommits.org/).

---

## [0.4.0] - 2026-08-17

Completes Phase 4 of the roadmap: the centralized Recommendation Engine, FeatureQualityReviewer, and the Plan primitive (`fs.plan()` / `featuresmith plan`), with ML Readiness Score dimension reconciliation.

### Added
- **Centralized Recommendation Engine** (`featuresmith.recommendation`):
  - `RecommendationEngine.generate(sections)` merges findings from all review sections into a single ranked, explainable list of recommendations with consistent confidence semantics.
  - `Recommendation` dataclass with stable ID (`rec.{rule_prefix}.{column}`), title, rationale, confidence (0–1), severity, affected columns, suggested action, `accepted` flag, and full traceability (`originating_findings`, `originating_reviewers`).
  - Ranking by severity (desc) → confidence (desc) → affected column count (desc).
  - Replaces the minimal severity-ranked fallback formatter previously used by the Review Engine; the fallback formatter is removed.
- **FeatureQualityReviewer** (`review.quality.feature_quality`):
  - Near-constant columns: numeric columns with variance below configurable threshold.
  - Redundant column pairs: numeric column pairs with Pearson correlation exceeding threshold.
  - Low-signal columns: high-cardinality categorical columns with low target correlation (requires `target_column`).
- **Plan Primitive** (`featuresmith.plan` / `featuresmith plan`):
  - `Plan` / `PlanItem` dataclasses with versioned schema (`PLAN_SCHEMA_VERSION = "0.1.0"`), deterministic item IDs (`plan.{rec_id}.{idx}`), full traceability back to originating findings and reviewers.
  - `fs.plan(result, accept=[...])` SDK function and `featuresmith plan` CLI command.
  - `compile_plan()` / `compile_plan_from_recommendations()` for programmatic Plan construction.
  - Plan rendering via `PlanRenderer` (`plan_console` target) and `render()` dispatch.
  - CLI: `featuresmith plan <source> --accept <rec_ids> [--target] [--previous] [--format table|json] [--fail-on] [--output] [--quiet]`.
- **ML Readiness Score Dimension Reconciliation**:
  - `DataQualityDimension` now reads only `review.quality.duplicates` and `review.quality.constants` (cardinality removed to eliminate double-count with `ConsistencyDimension`).
  - `ConsistencyDimension` reads `review.schema.types` and `review.quality.cardinality` (cardinality only here, per spec §7.1).
  - `ClassBalanceDimension` made never-applicable (minority-class detector not implemented); dimension omitted from aggregate per spec §7.4 ("an inapplicable dimension must never silently count as a perfect or zero score").
  - Effective scored dimensions: 7 (Schema Health, Missing Values, Feature Quality, Distribution Health, Leakage Risk, Data Quality, Consistency).
  - `SCORING_VERSION` bumped to `"0.3.0"`.
- **New Tests**: 38 focused Plan tests (`tests/cli/test_cli_plan.py`, `tests/review/test_plan_render.py`).

### Changed
- Version bumped to `0.4.0` across all packages (core, cli, workspace).
- `REVIEW_ENGINE_VERSION` bumped to `"0.4.0"`; `default_registry()` now ships 10 built-in reviewers (includes `FeatureQualityReviewer`).
- `fs.review()` now attaches `Recommendation[]` to `ReviewResult.recommendations` and distributes them to originating `ReviewSection.recommendations`.
- `SCORING_VERSION` bumped to `"0.3.0"`; effective scored dimensions reduced from 8 to 7 (Class Balance omitted).
- `PLAN_SCHEMA_VERSION = "0.1.0"` introduced.

### Fixed
- Cardinality double-counting eliminated: `review.quality.cardinality` findings no longer lower both `score.data_quality` and `score.consistency`.
- `ClassBalanceDimension` no longer silently inflates scores with a stub 100.0; dimension is now omitted from aggregate per spec §7.4.
- `tests/cli/test_cli_review.py` reference to old dimension IDs (`score.duplicate_records`, `score.constant_columns`) updated to current IDs (`score.data_quality`, `score.consistency`).

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
