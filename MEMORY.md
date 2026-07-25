# Featuresmith Development Memory

## Project Overview

- Current Version: 0.1.0-dev
- Current Phase: Phase 1 — SDK + CLI MVP
- Current Sprint: Sprint 5 — CLI MVP
- Repository: `D:\FeatureSmith`
- Last Updated: 2026-07-25

-------------------------------------------------

## Sprint Status

| Sprint | Status | Completion Date |
| --- | --- | --- |
| Sprint 1 — Foundations | Completed | 2026-07-25 |
| Sprint 2 — Dataset Foundation and Connector System | Completed | 2026-07-25 |
| Sprint 3 — Deterministic Data Profiling Engine | Completed | 2026-07-25 |
| Sprint 4 — Deterministic Rule Engine | Completed | 2026-07-25 |
| Sprint 5 — CLI MVP | Current | — |

-------------------------------------------------

## Completed Work

### Sprint 1 — Foundations

- Objective: Establish the workspace, package boundaries, quality tooling, and
  documentation skeleton.
- Major Deliverables: uv workspace; installable core, CLI, and dashboard
  packages; CI; Ruff; MyPy; pytest; pre-commit; import-linter; documentation
  skeleton.
- Files Added: Foundation package and tooling files already present in the
  repository.
- Files Modified: None recorded by this implementation journal.
- Important Decisions: Business logic lives only in `featuresmith-core`; the
  CLI and dashboard may import only `featuresmith.api`.
- Lessons Learned: The workspace-level quality configuration is the source of
  truth for implementation checks.
- Known Limitations: No user-facing analysis capability was shipped.

### Sprint 2 — Dataset Foundation and Connector System

- Objective: Normalize supported local tabular sources into one reusable
  `Dataset` contract.
- Major Deliverables: Immutable dataset descriptors; schema contracts; typed
  connector failures; CSV, Excel, Parquet, pandas, and Polars connectors;
  explicit registry; public `fs.load()`.
- Files Added: Core dataset/schema/exception modules; connector modules;
  connector and core module READMEs; connector documentation; ADR 0001;
  connector and dataset tests.
- Files Modified: Core package metadata and lockfile; public SDK exports;
  repository README.
- Important Decisions: Polars is used for CSV and Parquet; pandas is used for
  Excel and pandas DataFrame interop; no connector discovery or dynamic loading
  is included.
- Lessons Learned: File-source errors remain typed and actionable without
  exposing raw data.
- Known Limitations: Excel loads the first worksheet only; SQL, cloud, plugin
  discovery, profiling, rules, AI, exports, dashboard, and CLI commands remain
  out of scope.

### Sprint 3 — Deterministic Data Profiling Engine

- Objective: Build a production-grade, deterministic profiling engine that
  analyses a `Dataset` and produces a structured `ProfileResult`.
- Major Deliverables:
  - `featuresmith/core/profile_result.py` — strongly-typed `ProfileResult` and
    all inner schema classes (11 dataclasses total).
  - `featuresmith/profiling/profiler.py` — central orchestrator.
  - `featuresmith/profiling/numeric.py` — 23-metric numeric column profiler.
  - `featuresmith/profiling/categorical.py` — cardinality, frequency tables,
    entropy, top/bottom values.
  - `featuresmith/profiling/datetime.py` — min/max timestamps, range in days.
  - `featuresmith/profiling/text.py` — length statistics, word/char counts,
    empty/whitespace counts.
  - `featuresmith/profiling/correlation.py` — Pearson correlation matrix with
    column cap; Spearman/Kendall reserved.
  - `featuresmith/profiling/missing.py` — per-column and dataset-wide missing
    value analysis.
  - `featuresmith/profiling/duplicates.py` — duplicate row counts; constant
    and fully empty column detection.
  - `featuresmith/profiling/quality.py` — helper functions for quality flags.
  - `featuresmith/profiling/summary.py` — logical type classification
    heuristic and `DatasetMetadata` builder.
  - `featuresmith/profiling/README.md` — module documentation.
  - `featuresmith/core/README.md` — updated to document `ProfileResult`.
  - `README.md` — updated with profiling usage examples.
  - `tests/profiling/test_profiler.py` — 11 comprehensive test scenarios.
  - `tests/profiling/__init__.py` — test package init.
  - Public API: `fs.profile(source)` added to `api.py` and exported from the
    package root.
- Files Modified: `featuresmith/api.py`; `featuresmith/__init__.py`;
  `featuresmith/core/__init__.py`; `featuresmith/profiling/__init__.py`.
- Important Decisions:
  - `ProfileResult` uses `frozen=True` dataclasses (not Pydantic) for
    consistency with Sprint 2 schemas (`ColumnSchema`, `DatasetSchema`) — keeps
    the dependency surface minimal.
  - Logical type classification uses a heuristic: avg string length ≥ 20 chars
    or > 50 % unique ratio with > 10 unique values → `text`; all others →
    `categorical`. This is intentionally simple and will be tunable later.
  - Text column `missing_count` is derived in the orchestrator via the shared
    `_get_missing_count` helper rather than stored on `TextProfile` (avoids
    duplicating the null-counting logic already in `missing.py`).
  - Correlation capping is enforced at `max_correlation_columns` (default 100)
    to prevent O(n²) blowup on wide datasets; the cap is configurable per call.
  - Polars columns use batched `select()` expression pipelines for performance;
    pandas columns use equivalent vectorized pandas APIs.
- Lessons Learned: Polars `n_unique()` inside `drop_nulls()` requires an
  expression-level call pattern; scalar extraction via `[0, 0]` indexing is
  idiomatic for single-row results.
- Known Limitations:
  - Text column `TextProfile` does not store `missing_count` directly (it is
    available via `column_profiles`). A future cleanup could unify this.
  - Correlation is Pearson only; Spearman and Kendall are structurally reserved
    but not yet implemented.
  - No sampling for very large datasets — the size-tiered execution strategy
    (`Architecture.md §17`) is deferred to a later sprint once the rule engine
    is in place.

### Sprint 4 — Deterministic Rule Engine

- Objective: Build a production-grade, deterministic Rule Engine that consumes
  `ProfileResult` and produces a typed `RuleResult` containing `RuleFinding[]`.
  No AI. No recommendations. No natural language generation.
- Major Deliverables:
  - `featuresmith/core/rule_finding.py` — strongly-typed frozen `RuleFinding`
    dataclass with `rule_id`, `rule_name`, `category`, `severity`,
    `column_name`, `title`, `description`, `evidence`, `confidence`, `id`,
    and `metadata`.
  - `featuresmith/core/rule_result.py` — `RuleResult` dataclass carrying
    the `ProfileResult`, findings list, executed rule IDs, execution time, and
    any failed rules with their tracebacks.
  - `featuresmith/rules/base.py` — `BaseRule` abstract class with abstract
    properties (`id`, `name`, `description`, `category`, `severity`,
    `enabled_by_default`) and method `evaluate(profile) -> list[RuleFinding]`.
  - `featuresmith/rules/registry.py` — `RuleRegistry` with `register`,
    `unregister`, `list_rules`; `default_registry()` factory pre-loading all
    8 seed rules.
  - `featuresmith/rules/engine.py` — `RuleEngine` orchestrator with
    configurable rule enabling/disabling, per-rule config injection, error
    isolation, and execution timing.
  - `featuresmith/rules/missing.py` — `MissingValueThresholdRule`
    (`quality.missing_value_threshold`, default threshold 20%).
  - `featuresmith/rules/duplicates.py` — `DuplicateRowsRule`
    (`quality.duplicate_rows`, default threshold 10%).
  - `featuresmith/rules/constants.py` — `ConstantColumnsRule`
    (`quality.constant_columns`) and `FullyEmptyColumnsRule`
    (`quality.fully_empty_columns`).
  - `featuresmith/rules/cardinality.py` — `HighCardinalityRule`
    (`statistical.high_cardinality`, default unique ratio > 50% with
    min_cardinality=20).
  - `featuresmith/rules/outliers.py` — `OutlierDetectionRule`
    (`statistical.outliers`, IQR factor=1.5).
  - `featuresmith/rules/correlation.py` — `HighCorrelationRule`
    (`statistical.high_correlation`, default Pearson threshold 0.90).
  - `featuresmith/rules/leakage.py` — `LeakageRuleTargetCorrelation`
    (`leakage.potential_leakage`, default Pearson threshold 0.99 with
    explicit `target_column`; skips silently if no target provided — no target
    inference per design).
  - `featuresmith/rules/README.md` — module documentation and contributor guide.
  - `tests/rules/test_rules.py` — 12 comprehensive test scenarios covering all
    8 rules (positive and negative cases), engine error isolation, rule
    disabling/enabling, empty datasets, single-column datasets, and mixed
    Polars/pandas fixtures.
  - `tests/rules/__init__.py` — test package init.
  - `README.md` — updated with `fs.analyze()` usage, full pipeline diagram,
    and rules table.
  - Public API: `fs.analyze(source, target_column, enabled_rules, rule_config)`
    added to `api.py` and exported from the package root.
- Files Modified: `featuresmith/api.py`; `featuresmith/__init__.py`;
  `featuresmith/core/__init__.py`; `featuresmith/rules/__init__.py`.
- Important Decisions:
  - `RuleFinding` and `RuleResult` are `frozen=True` dataclasses (consistent
    with all other core schemas) — serializable via `asdict()` / `to_dict()`.
  - `RuleEngine` isolates individual rule failures in `failed_rules` dict so a
    single crashing rule never aborts the entire analysis run.
  - `LeakageRuleTargetCorrelation` requires an explicit `target_column` — no
    target inference, per the sprint constraint "No AI, No target inference."
  - Rule configuration is injected by re-instantiating the rule class with
    keyword arguments (e.g. `MissingValueThresholdRule(threshold=30.0)`);
    this keeps rules stateless and independently testable.
  - `HighCardinalityRule` only evaluates columns classified as `"categorical"`
    by the existing profiling heuristic; columns with > 50% unique ratio and
    > 10 unique values are classified as `"text"` by the profiler and are
    intentionally excluded.
- Lessons Learned: The profiling engine's logical-type heuristic (avg length ≥
  20 or unique_ratio > 0.5 with > 10 unique values → `text`) means high-
  cardinality string columns frequently land in `"text"` rather than
  `"categorical"`. Test fixtures for the cardinality rule must use columns with
  ≤ 10 unique values repeated over many rows (so the unique-count threshold is
  not exceeded and the column remains categorical).
- Known Limitations:
  - `LeakageRuleTargetCorrelation` requires the target column to be numeric
    (present in the Pearson correlation matrix). Categorical targets are not
    yet supported.
  - Rule severity escalation in `MissingValueThresholdRule` (`> 50%` → critical)
    is hard-coded; in a future sprint this should be driven by configuration.
  - No rule configuration persistence (e.g. `.featuresmith.yml` loading) yet —
    rule configs are passed directly at call time.

-------------------------------------------------

## Current Architecture Status

| Area | Status |
| --- | --- |
| Core | In Progress |
| Connectors | Completed |
| Profiling | Completed |
| Rules | Completed |
| Recommendation Engine | Not Started |
| AI Layer | Not Started |
| Exporters | Not Started |
| CLI | Not Started |
| Dashboard | Not Started |
| Plugin System | Not Started |

Note: "Core" is marked In Progress because it will continue to grow throughout
Phase 1 with configuration models, exception types, and additional shared
primitives.

-------------------------------------------------

## Public APIs Implemented

- `fs.load(source)` — load any supported source into a `Dataset`.
- `Dataset.preview(rows=5)` — return the first N rows.
- `fs.profile(source)` — profile any supported source and return a `ProfileResult`.
- `fs.analyze(source, *, target_column, enabled_rules, rule_config)` — run the
  full pipeline (load → profile → rule_engine.run()) and return a `RuleResult`.
- `profile_dataset(dataset, max_correlation_columns=100)` — internal orchestrator,
  importable from `featuresmith.profiling` for advanced callers.

-------------------------------------------------

## Technical Decisions

| Date | Sprint | Decision | Reason |
| --- | --- | --- | --- |
| 2026-07-25 | Sprint 1 | Enforce thin surfaces through package boundaries and import-linter. | Keep all business logic in the reusable core. |
| 2026-07-25 | Sprint 2 | Use Polars for CSV/Parquet and pandas for Excel/pandas interoperability. | Match the architecture's Polars-first direction while preserving pandas compatibility. |
| 2026-07-25 | Sprint 2 | Keep connector registration explicit and static. | Establish the extension boundary without implementing future plugin discovery. |
| 2026-07-25 | Sprint 3 | Use `frozen=True` dataclasses for `ProfileResult` schemas instead of Pydantic. | Consistent with Sprint 2 core schemas; no extra dependency. |
| 2026-07-25 | Sprint 3 | Cap correlation columns at `max_correlation_columns=100` by default. | Prevent O(n²) blowup on wide datasets; configurable per call. |
| 2026-07-25 | Sprint 3 | Logical type heuristic: avg string length ≥ 20 → `text`. | Simple, deterministic; tunable in a later phase if needed. |
| 2026-07-25 | Sprint 4 | Use `frozen=True` dataclasses for `RuleFinding` and `RuleResult`. | Consistent with all other core schemas; serializable via `asdict()`. |
| 2026-07-25 | Sprint 4 | Rule configuration injected via re-instantiation (`Rule(**config)`). | Keeps rules stateless and independently testable without a global config object. |
| 2026-07-25 | Sprint 4 | `LeakageRuleTargetCorrelation` requires explicit `target_column`. | No target inference per design; deterministic heuristic only. |
| 2026-07-25 | Sprint 4 | `RuleEngine` isolates rule failures in `failed_rules` dict. | One crashing rule must never abort the analysis pipeline. |

-------------------------------------------------

## Known Technical Debt

- [ ] Add entry-point connector discovery only in its scheduled plugin-system phase.
- [ ] Add multi-sheet Excel selection only in its scheduled connector phase.
- [ ] `TextProfile` does not carry `missing_count` directly — it is available via
      `column_profiles[name].missing_count`. Consider unifying in a future refactor.
- [ ] Spearman and Kendall correlation reserved but not implemented.
- [ ] Size-tiered profiling execution (`Architecture.md §17`) not yet implemented.
- [ ] `LeakageRuleTargetCorrelation` only supports numeric target columns (must be
      in the Pearson matrix). Categorical targets are not yet supported.
- [ ] Rule severity escalation thresholds are hard-coded in rule classes; should
      be configurable via `.featuresmith.yml` once the config system is built.
- [ ] No `.featuresmith.yml` config loading yet — rule configs are passed at call
      time only.

-------------------------------------------------

## Upcoming Sprint

- Sprint Number: Sprint 5
- Objective: CLI MVP — Expose `featuresmith analyze <source>` as a thin Typer
  wrapper over `fs.analyze()` so the same analysis is available from the
  terminal.
- Major Tasks:
  - Implement `featuresmith analyze <source>` CLI command in `featuresmith-cli`.
  - Implement human-readable table/rich output for findings.
  - Implement `--format json` flag for machine-consumption/piping.
  - Implement `--target` flag for `target_column`.
  - Surface `exit code 1` when findings above a configured severity threshold.
  - Write surface-parity tests asserting CLI and SDK produce the same findings.
- Dependencies: Sprint 4 `RuleResult` / `fs.analyze()`.
- Expected Deliverables: `featuresmith analyze` CLI command; rich table output;
  JSON output mode; surface-parity integration test.

-------------------------------------------------

## Changelog

### 2026-07-25 — Sprint 4

- Added `RuleFinding` dataclass in `core/rule_finding.py`.
- Added `RuleResult` dataclass in `core/rule_result.py`.
- Added complete Rule Engine under `featuresmith/rules/`:
  `base.py`, `registry.py`, `engine.py`, `missing.py`, `duplicates.py`,
  `constants.py`, `cardinality.py`, `outliers.py`, `correlation.py`,
  `leakage.py`.
- Added `fs.analyze()` to the public SDK and package root.
- Added `tests/rules/test_rules.py` with 12 test scenarios covering all 8 rules
  (positive + negative cases), engine error isolation, rule configuration,
  empty datasets, single-column datasets, and mixed Polars/pandas fixtures.
- Updated `README.md` with `fs.analyze()` usage, full pipeline diagram, and
  rules table.
- Added `featuresmith/rules/README.md` module documentation and contributor guide.
- Updated `featuresmith/core/__init__.py` to export `RuleFinding` and
  `RuleResult`.

### 2026-07-25 — Sprint 3

- Added `ProfileResult` and 11 inner schema dataclasses in `core/profile_result.py`.
- Added complete profiling engine under `featuresmith/profiling/`:
  `profiler.py`, `summary.py`, `numeric.py`, `categorical.py`, `datetime.py`,
  `text.py`, `correlation.py`, `missing.py`, `duplicates.py`, `quality.py`.
- Added `fs.profile()` to the public SDK and package root.
- Added `tests/profiling/test_profiler.py` with 11 test scenarios covering
  numeric, categorical, datetime, text, duplicates, correlations, empty datasets,
  single-column datasets, serialization, and pandas/Polars parity.
- Updated `README.md`, `core/README.md`, and added `profiling/README.md`.

### 2026-07-25 — Sprint 2

- Added normalized `Dataset` and schema contracts.
- Added local file and in-memory dataframe connectors with `fs.load()`.
- Added typed connector errors, tests, connector documentation, and ADR 0001.

### 2026-07-25 — Sprint 1

- Completed workspace foundations and quality-tooling setup.

-------------------------------------------------

## AI Instructions

Every AI contributing to this project MUST:

1. Read these files before writing code:

   - `MEMORY.md`
   - `Project_Plan.md`
   - `PRD.md`
   - `Architecture.md`
   - `Rules.md`
   - `Phases.md`
   - `Design.md`

2. Never redesign the architecture.
3. Never duplicate business logic.
4. Never skip roadmap phases.
5. Never implement future features early.
6. Update `MEMORY.md` immediately after every completed sprint.
7. Treat `MEMORY.md` as the project's implementation journal.
