# Featuresmith Development Memory

## Project Overview

- Current Version: 0.0.3-dev
- Current Phase: Phase 1 — SDK + CLI MVP
- Current Sprint: Sprint 4 — Rule Engine
- Repository: `D:\FeatureSmith`
- Last Updated: 2026-07-25

-------------------------------------------------

## Sprint Status

| Sprint | Status | Completion Date |
| --- | --- | --- |
| Sprint 1 — Foundations | Completed | 2026-07-25 |
| Sprint 2 — Dataset Foundation and Connector System | Completed | 2026-07-25 |
| Sprint 3 — Deterministic Data Profiling Engine | Completed | 2026-07-25 |
| Sprint 4 — Deterministic Rule Engine | In Progress | — |

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

-------------------------------------------------

## Current Architecture Status

| Area | Status |
| --- | --- |
| Core | In Progress |
| Connectors | Completed |
| Profiling | Completed |
| Rules | In Progress |
| Recommendation Engine | Not Started |
| AI Layer | Not Started |
| Exporters | Not Started |
| CLI | Not Started |
| Dashboard | Not Started |
| Plugin System | Not Started |

Note: "Core" is marked In Progress because it will continue to grow throughout
Phase 1 with new modules: `rule_finding.py`, `rule_result.py`, and later
configuration models, exception types, and additional shared primitives.

-------------------------------------------------

## Public APIs Implemented

- `fs.load(source)` — load any supported source into a `Dataset`.
- `Dataset.preview(rows=5)` — return the first N rows.
- `fs.profile(source)` — profile any supported source and return a `ProfileResult`.
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

-------------------------------------------------

## Known Technical Debt

- [ ] Add entry-point connector discovery only in its scheduled plugin-system phase.
- [ ] Add multi-sheet Excel selection only in its scheduled connector phase.
- [ ] `TextProfile` does not carry `missing_count` directly — it is available via
      `column_profiles[name].missing_count`. Consider unifying in a future refactor.
- [ ] Spearman and Kendall correlation reserved but not implemented.
- [ ] Size-tiered profiling execution (`Architecture.md §17`) not yet implemented.

-------------------------------------------------

## Upcoming Sprint

- Sprint Number: Sprint 4
- Objective: Rule Engine — Deterministic data-quality and leakage checks that
  consume `ProfileResult` and produce `RuleFinding[]`.
- Major Tasks:
  - Implement `RuleFinding` and `RuleResult` core models in `featuresmith/core/`.
  - Implement `BaseRule` interface in `featuresmith/rules/base.py`.
  - Implement `RuleRegistry` in `featuresmith/rules/registry.py`.
  - Implement `RuleEngine` orchestrator in `featuresmith/rules/engine.py`.
  - Implement seed rules: `missing.py`, `duplicates.py`, `constants.py`,
    `cardinality.py`, `outliers.py`, `correlation.py`, `leakage.py`.
  - Export `fs.analyze()` as the combined profile + rules public API.
  - Write comprehensive tests for all rules and the engine.
  - Update documentation and README.
- Dependencies: Sprint 3 `ProfileResult`.
- Expected Deliverables: `RuleFinding[]` typed output; `RuleResult`; `RuleEngine`;
  seven seed rules; rule tests with positive and negative fixture cases.

-------------------------------------------------

## Changelog

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
