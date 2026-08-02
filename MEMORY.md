# Featuresmith Development Memory

## Project Overview

- Current Version: 0.1.0
- Current Phase: Phase 1 — SDK + CLI MVP (complete) / Release Readiness
- Current Sprint: Review Engine — Dataset Diff (Sprint 5, complete)
- Repository: `D:\FeatureSmith`
- Last Updated: 2026-08-02

-------------------------------------------------

## Sprint Status

| Sprint | Status | Completion Date |
| --- | --- | --- |
| Sprint 1 — Foundations | Completed | 2026-07-25 |
| Sprint 2 — Dataset Foundation and Connector System | Completed | 2026-07-25 |
| Sprint 3 — Deterministic Data Profiling Engine | Completed | 2026-07-25 |
| Sprint 4 — Deterministic Rule Engine | Completed | 2026-07-25 |
| Sprint 5 — CLI MVP | Completed | 2026-07-26 |
| Release Readiness Sprint 1 (RR-1) — Repository Polish | Completed | 2026-07-26 |
| Release Readiness Sprint 2 (RR-2) — Documentation Website | Completed | 2026-07-26 |
| Release Readiness Sprint 3 (RR-3) — Examples & Tutorials | Completed | 2026-07-26 |
| Release Readiness Sprint 4 (RR-4) — Testing & Benchmarks | Completed | 2026-07-26 |
| Review Engine Foundation | Completed | 2026-08-02 |
| Review Engine — Built-in Reviewers (Sprint 2) | Completed | 2026-08-02 |
| Review Engine — ML Readiness Score (Sprint 3) | Completed | 2026-08-02 |
| Review Engine — Intelligent Leakage Detection (Sprint 4) | Completed | 2026-08-02 |
| Review Engine — Leakage Integration & Production Readiness (Sprint 4.1) | Completed | 2026-08-02 |
| Review Engine — Dataset Diff (Sprint 5) | Completed | 2026-08-02 |
| Sprint 6 — SDK Hardening & Exporter Layer | Deferred | — |

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

### Review Engine Foundation

- Objective: Build the Review Engine orchestration foundation inside
  `featuresmith-core` per `docs/features/Review-Engine-Architecture.md` —
  infrastructure only, shipping with zero built-in reviewers by design.
- Major Deliverables:
  - `featuresmith/review/schema.py` — `Severity`, `ReviewCategory`,
    `ReviewSection`, `ReviewResult` (frozen dataclasses with `to_dict()`).
  - `featuresmith/review/context.py` — `ReviewConfig` + frozen `ReviewContext`;
    no `ExecutionState` class, per the architecture decision that state lives on
    the context.
  - `featuresmith/review/base.py` — `BaseReviewer` ABC (`id`, `category`,
    `requires_previous_snapshot`, `applicable()`, `review()`).
  - `featuresmith/review/registry.py` — `ReviewerRegistry` +
    empty `default_registry()`; `reviewers/` subpackage placeholder.
  - `featuresmith/review/engine.py` — `ReviewEngine.run()` pipeline
    (`REVIEW_ENGINE_VERSION = "0.1.0"`): config validation → context
    construction → reviewer dispatch (enabled-reviewer/category filters,
    previous-snapshot gate, `applicable()` gate) → fault-isolated execution →
    aggregation.
  - `featuresmith/review/aggregator.py` — `ResultAggregator` (severity-sorted
    sections, templated overall summary, failed-reviewer warning).
  - `featuresmith/review/render.py` — `ConsoleRenderer` + `RendererRegistry` +
    `render()` facade (console only for now).
  - `featuresmith/review/__init__.py` — full public exports.
  - SDK: `fs.review(source)` in `featuresmith/api.py` (reuses `fs.analyze()`'s
    profile + rule findings); `review` added to root `__init__.py` exports;
    `render`, `ReviewCategory`, `ReviewResult`, `ReviewSection`, `Severity`
    re-exported from `featuresmith.api`.
  - CLI: `featuresmith review <source>` in
    `featuresmith_cli/commands/review.py` (table/json formats, `--output`,
    `--fail-on`, `--only`, `--quiet`, `--verbose`, `--version`).
  - Extended `featuresmith/core/profile_result.py::_asdict_custom` to serialize
    `datetime` (ISO-8601) and `Enum` (`.value`) so `ReviewResult.to_dict()` is
    JSON-clean.
  - Tests: `tests/review/` (schema, context, registry, aggregator, engine,
    render, sdk) and `tests/cli/test_cli_review.py` — 56 new tests.
  - Updated `docs/features/Review-Engine-Architecture.md` status to
    "Foundation implemented"; added §14 "Implemented Foundation" subsection.
- Files Modified: `featuresmith/api.py`; `featuresmith/__init__.py`;
  `featuresmith/core/profile_result.py`; `featuresmith_cli/main.py`;
  `pyproject.toml` (ruff `extend-exclude = ["*.md"]`; import-linter
  `ignore_imports` for review edges); `tests/test_imports.py`.
- Important Decisions:
  - The approved architecture docs are the source of truth; conflicting sprint
    brief details (a separate `ReviewFinding` type, an `INFO/WARNING/ERROR/
    CRITICAL` enum) were ignored — `ReviewSection.findings` reuses the existing
    `RuleFinding`, and `Severity` uses `critical | warning | info | passed`
    (lowercase values for backward compatibility).
  - Zero built-in reviewers ship with this sprint; `fs.review()` runs an empty
    reviewer set by design. `score`/`diff` fields exist only as reserved `None`
    attachment points. `fs.review(previous=...)` raises `NotImplementedError`.
  - Fault isolation mirrors the Rule Engine: one crashing reviewer degrades to
    a partial-result warning without aborting the run.
  - Added `extend-exclude = ["*.md"]` to `[tool.ruff]` so `ruff format --check .`
    passes without reformatting intentional alignment in README/design docs
    (pre-existing failure).
- Lessons Learned: Import-linter's transitive forbidden-contract chains need
  every new `featuresmith.api -> review -> core` edge listed in `ignore_imports`
  (same pattern as Sprint 5). `uv build --package <name>` builds a workspace
  member; `uv run build` is not a valid invocation.
- Known Limitations:
  - No built-in reviewers yet — future sprints fill `reviewers/`.
  - Diff-aware review (`previous=`) raises `NotImplementedError`; ML Readiness
    Score, AI narration, recommendations, and non-console renderers remain
    future work.
  - `render` is exported from `featuresmith.api`/`featuresmith.review`, not the
    package root.
  - `.pytest_cache` writes fail under Windows (WinError 5, pre-existing).

### Review Engine — Built-in Reviewers (Sprint 2)

- Objective: Implement the first built-in reviewer set so `featuresmith review
  dataset.csv` produces a meaningful engineering review, per the approved docs
  as contract. No score, no recommendations, no AI, no diff.
- Major Deliverables:
  - `featuresmith/review/reviewers/base.py` — `SectionReviewer` abstract base
    (title + `_collect_findings`; `review()` builds the `ReviewSection`) and
    `section_severity()` helper (worst finding severity; `PASSED` when none).
  - Seven built-in reviewers (all `SectionReviewer` subclasses, all
    `requires_previous_snapshot = False`):
    - `schema_health.py` — `SchemaHealthReviewer`
      (`review.schema.health`, schema, "Schema Health"): fully empty columns
      (warning via `FullyEmptyColumnsRule`), zero rows (warning), zero columns
      (warning).
    - `missing_value.py` — `MissingValueReviewer`
      (`review.quality.missingness`, quality, "Missing Values"):
      `MissingValueThresholdRule` default threshold 20.0, configurable;
      excludes fully empty columns (owned by schema health).
    - `duplicates.py` — `DuplicateReviewer`
      (`review.quality.duplicates`, quality, "Duplicate Rows"):
      `DuplicateRowsRule` default threshold 10.0, configurable.
    - `constants.py` — `ConstantColumnReviewer`
      (`review.quality.constants`, quality, "Constant Columns"):
      `ConstantColumnsRule`; flags constant non-empty columns, including text
      columns whose `logical_type == "text"`.
    - `cardinality.py` — `CardinalityReviewer`
      (`review.quality.cardinality`, quality, "High Cardinality"):
      `HighCardinalityRule` threshold 0.50 / min_cardinality 20, configurable;
      categorical columns only.
    - `types.py` — `TypeReviewer` (`review.schema.types`, schema,
      "Data Types"): identifier-like numeric columns (all non-null values
      distinct, `identifier_min_count=10`), text-logical-type columns (info).
    - `basic_statistics.py` — `BasicStatisticsReviewer`
      (`review.quality.basic_statistics`, quality, "Basic Statistics"):
      skewness >= 2.0 (warning), kurtosis >= 10.0 (info), numeric constant
      columns, identifier-like numeric columns, text columns.
  - `featuresmith/review/reviewers/__init__.py` — exports all 7 + the
    `builtin_reviewers()` factory returning their tuple.
  - `featuresmith/review/registry.py` — `default_registry()` now registers the
    7 built-in reviewers.
  - Tests: `tests/review/test_reviewers.py` (per-reviewer unit tests) and
    `tests/review/test_review_integration.py` (empty/clean/missing/duplicates/
    constants/mixed-types/high-cardinality scenarios, JSON serialization,
    reviewer-config overrides); updated `test_registry.py`, `test_sdk.py`,
    `test_engine.py`, `tests/cli/test_cli_review.py` for the non-empty default
    registry.
  - Updated `docs/features/Review-Engine-Architecture.md` (status + §14
    "Implemented Built-in Reviewers (Sprint 2)") and
    `docs/features/Dataset-Review-PRD.md` (status + §7.1 progress note).
- Files Added: 7 reviewer modules, `reviewers/base.py`,
  `tests/review/test_reviewers.py`, `tests/review/test_review_integration.py`.
- Files Modified: `featuresmith/review/registry.py`,
  `featuresmith/review/reviewers/__init__.py`,
  `tests/review/{test_registry,test_sdk,test_engine}.py`,
  `tests/cli/test_cli_review.py`, `MEMORY.md`, architecture/PRD docs.
- Important Decisions:
  - Docs are the contract: reviewer IDs are namespaced
    (`review.schema.health`, `review.quality.missingness`, etc.);
    `ReviewCategory` enum; `Severity` lowercase with `.rank`; reviewers read
    only the frozen `ReviewContext` (profile + dataset + findings + config)
    and never re-read/re-profile data.
  - Fully empty columns are reported exactly once, by `SchemaHealthReviewer`;
    `MissingValueReviewer` excludes them.
  - `TypeReviewer` identifier-like findings folded into the Basic Statistics
    section output to avoid double-flagging; numeric constants reported under
    `basic_statistics` (not `constants`).
  - Severity assignment: schema-health (fully empty) warning; quality
    (missingness/cardinality/duplicates/false-constant) warning;
    basic-statistics (skew info-to-warning, identifier-like, text) info.
  - `ReviewConfig.reviewer_config` (reviewer id → mapping) drives configurable
    thresholds; validated against registered reviewer IDs by the engine.
  - Reviewer dispatch still runs with zero reviewers (explicit empty registry)
    as a foundation guarantee — covered by `test_engine.py`.
- Lessons Learned: default `--fail-on critical` means warning findings exit 0
  — CLI tests must pass `--fail-on warning` to gate on warnings; finding `id`
  UUIDs are volatile, so CLI/SDK surface-parity tests strip them before
  comparison; `skewed_df` kurtosis exceeds both skew and kurtosis thresholds,
  so threshold-config tests must raise both.
- Known Limitations: Outliers/Distribution/DuplicateColumn/FeatureQuality/
  Leakage/Diff reviewers remain future work; `review.quality.basic_statistics`
  currently absorbs the PRD's Outliers/Distribution/Basic-statistics sections.

### Review Engine — ML Readiness Score (Sprint 3)

- Objective: Implement the deterministic, explainable ML Readiness Score per
  `docs/features/ML-Readiness-Score.md` (contract), computed purely from Review
  Engine findings, surfaced through SDK and CLI. No AI scoring, no
  recommendations, no leakage detection, no diff, no plugins, no dashboard, no
  HTML reports.
- Major Deliverables:
  - `featuresmith/scoring/` — new module:
    - `schema.py` — frozen `DimensionScore` and `MLReadinessScore` dataclasses
      (`slots=True`, `to_dict()`); the latter carries `summary`,
      `positive_findings`, `negative_findings`.
    - `base.py` — `ScoreDimension` Protocol (`id`, `label`, `default_weight`,
      `applicable()`, `compute()`).
    - `dimensions/base.py` — `SectionScoreDimension` base; class attrs are
      instance-level; `SEVERITY_DEDUCTIONS` (`critical` 30, `warning` 15,
      `info` 5); `score_from_findings` (start 100, clamp [0,100], round 1),
      `build_rationale`, `build_actions`.
    - `dimensions/builtin.py` — 7 dimensions mapping 1:1 to Sprint-2
      reviewers: `score.schema_health`↔`review.schema.health`,
      `score.missing_values`↔`review.quality.missingness`,
      `score.duplicate_records`↔`review.quality.duplicates`,
      `score.data_types`↔`review.schema.types`,
      `score.constant_columns`↔`review.quality.constants`,
      `score.high_cardinality`↔`review.quality.cardinality`,
      `score.dataset_structure`↔`review.quality.basic_statistics`.
    - `registry.py` — explicit static `ScoreDimensionRegistry` +
      `default_registry()` (no plugin discovery yet).
    - `aggregator.py` — `WeightedAggregator`, `compute_score()`,
      `SCORING_VERSION = "0.1.0"`, `build_summary`,
      `build_positive_findings`, `build_negative_findings` (deduped by finding
      id, sorted critical→info then rule_id/column/title).
  - `featuresmith/review/scoring_adapter.py` — `ScoreAdapter.attach(result)`
    (sole bridge; `replace(result, score=score)` or original when `None`).
  - `featuresmith/review/engine.py` — `ReviewEngine.__init__`
    (`registry`/`aggregator`/`score_adapter`); `run()` attaches score after
    aggregation. `review/schema.py` types `score` as `MLReadinessScore | None`.
  - `featuresmith/review/render.py` — `_render_score()` block in
    `ConsoleRenderer` (conditional on `result.score`).
  - `featuresmith/api.py` + `featuresmith/__init__.py` — `fs.score(result)`
    accessor; `DimensionScore`/`MLReadinessScore` re-exports.
  - `packages/featuresmith-cli/.../review.py` — `--no-score` flag
    (`replace(result, score=None)` before rendering).
  - Tests: 178 total pass (was 151). New `tests/scoring/test_scoring.py` (22
    tests) + updated `tests/review/{test_sdk,test_render}.py` and
    `tests/cli/test_cli_review.py`.
- Files Added: `featuresmith/scoring/` (8 files), `review/scoring_adapter.py`,
  `tests/scoring/` (2 files).
- Files Modified: `review/engine.py`, `review/schema.py`,
  `review/__init__.py`, `review/render.py`, `api.py`, `__init__.py`, CLI
  `review.py`, `tests/review/*`, `tests/cli/test_cli_review.py`,
  `pyproject.toml` (import-linter ignores), `docs/features/*.md`, `MEMORY.md`.
- Important Decisions:
  - Score is derived only from aggregated `ReviewSection` findings; `fs.score()`
    never re-runs analysis and returns the attached score when present.
  - `MLReadinessScore`/`DimensionScore` are frozen dataclasses (not Pydantic),
    consistent with every other core schema.
  - Weighted-mean overall with inapplicable-dimension renormalization; uniform
    default weights (1.0); per-dimension weight overrides supported.
  - All deduction amounts, weights, and the formula are versioned under
    `scoring_version = "0.1.0"`.
  - `--no-score` sets `score` to `None` in JSON output (not `0`), so "not
    scored" is distinct from "scored poorly".
- Lessons Learned: mypy Protocol conformance requires dimension class attrs to
  be instance-level; import-linter needs explicit `ignore_imports` edges for
  the new CLI→api→scoring→core chain; `1.0`-scale vs 0-100 scale must be kept
  consistent between doc formula and implementation (shipped: `sum(score*w) /
  sum(w)` on a 0-100 scale).
- Known Limitations: `--fail-below`/`--fail-below-dimension` CI gating, Feature
  Quality/Distribution/Class Balance dimensions, and non-weighted/custom
  formulas remain future work.

### Review Engine — Intelligent Leakage Detection (Sprint 4)

- Objective: Implement pattern-based intelligent leakage detection per
  `docs/features/Dataset-Diff-And-Leakage-Detection.md` (contract): six named
  pattern detectors matured from Phase 1's single naive threshold rule, an
  orchestration `LeakageReviewer`, and integration into the default reviewer
  set. No Dataset Diff, no AI, no detector registry refactor.
- Major Deliverables:
  - `featuresmith/rules/leakage/` — new package: `base.py`
    (`LeakagePatternDetector` ABC + `LeakageFinding` protocol members),
    `schema.py` (`LeakageFinding` frozen dataclass, `confidence_label`),
    `target_correlation.py` (also re-exports the legacy
    `LeakageRuleTargetCorrelation`, id `leakage.potential_leakage`, for
    backward compatibility with `fs.analyze`), `future_info.py`,
    `identifier.py`, `duplicate_target.py`, `timestamp.py`, `suspicious.py`,
    `__init__.py` (`builtin_detectors()`).
  - `featuresmith/review/reviewers/leakage.py` — `LeakageReviewer`
    (`review.leakage`, category `leakage`, "Leakage Detection") dispatching all
    detectors against `context.profile` with `context.config.target_column` and
    per-reviewer config; merges findings per column into one `RuleFinding`
    (`leakage.multiple_patterns`) citing every contributing pattern, or a
    single `leakage.<pattern>` finding.
  - Registered in `review/registry.py` `default_registry()` (8th built-in
    reviewer); exported from `review/reviewers/__init__.py`.
  - Tests: `tests/review/test_leakage_reviewer.py` (30 tests: per-detector
    positive/negative fixtures, dedup/merge, severity, CLI `--only` category).
- Files Modified: `review/registry.py`, `review/reviewers/__init__.py`;
  deleted single-file `rules/leakage.py` (replaced by the package);
  `tests/cli/test_cli_review.py`, `tests/review/test_registry.py`,
  `tests/review/test_review_integration.py`, `tests/review/test_sdk.py`.
- Important Decisions:
  - Detectors live under `rules/leakage` (matured rules, per the doc §8.2) and
    expose `detect(profile, *, target_column, config)` rather than the doc's
    `detect(context)` sketch, avoiding a `rules`→`review` dependency.
  - The legacy naive rule is preserved as a re-export so `fs.analyze` behavior
    is unchanged.
  - Merged findings carry every contributing pattern's rationale; severity is
    the worst contributing finding's.
- Lessons Learned: no target column means correlation-based detectors stay
  silent by design (explicit target only, no inference); finding `id`s are
  volatile UUIDs so CLI/SDK parity tests strip them.
- Known Limitations: known-leaky benchmark suite (§13 of the doc) not yet
  built; categorical targets silently skip correlation-based detectors; finding
  IDs are non-deterministic (uuid4).

### Review Engine — Leakage Integration & Production Readiness (Sprint 4.1)

- Objective: Close the integration/consistency gaps found in the Sprint 4
  verification audit — make leakage findings affect the ML Readiness Score, add
  CLI target-column support, fix lint issues, sync docs, and strengthen tests.
  Not a feature sprint; no benchmark suite, diff, AI, or refactors.
- Major Deliverables:
  - `featuresmith/scoring/dimensions/builtin.py` — new `LeakageRiskDimension`
    (`score.leakage_risk`, label "Leakage Risk", `section_id = "review.leakage"`)
    added to `builtin_dimensions()` (eight built-in dimensions); `registry.py`
    docstring updated.
  - `featuresmith/scoring/aggregator.py` — `SCORING_VERSION` bumped `0.1.0` →
    `0.2.0` (dimension-list change per `ML-Readiness-Score.md` §7.4); formula
    shape and weights unchanged.
  - `featuresmith_cli/commands/review.py` — new `--target <column>` option
    mirroring `analyze` (validates presence against the dataset schema, forwards
    `target_column=` to `fs.review`).
  - Lint fixes: removed unused `Any` import and added `strict=True` to the
    `zip()` in `review/reviewers/leakage.py`.
  - Tests: leakage-scoring integration + score stability in
    `tests/scoring/test_scoring.py`; CLI `--target` and leakage-findings output
    tests in `tests/cli/test_cli_review.py`; dimension-count/version updates
    across scoring/sdk/render/cli tests.
  - Docs synchronized: `ML-Readiness-Score.md` (§16: eight dimensions,
    `scoring_version` 0.2.0, Leakage Risk mapping, `--target` surface),
    `Review-Engine-Architecture.md` (§14: leakage reviewer + scoring status,
    reviewer count), `Dataset-Diff-And-Leakage-Detection.md` (status + `--target`
    example), `Dataset-Review-PRD.md` (status + §7.1 note), `MEMORY.md`.
- Important Decisions:
  - Leakage Risk uses the shared `SectionScoreDimension` formula (start 100,
    deduct critical 30 / warning 15 / info 5) — no bespoke scoring logic, per
    the versioned formula in `ML-Readiness-Score.md` §16.2.
  - CLI uses `--target` (same name as `analyze`) rather than a separate flag,
    keeping SDK/CLI consistent.
- Known Limitations: deferred items from the audit remain documented future work
  (stable finding IDs, detector registry refactor, benchmark suite, advanced
  heuristics, polars-specific enhancements).

### Review Engine — Dataset Diff (Sprint 5)

- Objective: Ship dataset-to-dataset comparison as a standalone **Diff Engine**
  (`featuresmith.diff`) exposed via `fs.diff(old, new)` and
  `featuresmith diff old.csv new.csv`, reusing the profiling engine and the
  leakage reviewer. Scope decision: the experimental `DiffReviewer` integration
  was reverted — the Review Engine keeps its exact 8-reviewer
  `default_registry()`, `fs.review(previous=...)` stays `NotImplementedError`,
  and single-dataset review vs two-dataset diff remain separate workflows.
- Major Deliverables:
  - `featuresmith/diff/schema.py` — frozen models: `DiffConfig`,
    `ColumnDiff`, `RowCountDiff`, `DatasetDiffSummary`, `SchemaDiff`,
    `DatasetDiffResult`, `StructureDiff`, `DataQualityDiff`,
    `DistributionDiff`, `LeakageDiff`, `DiffFindingsResult`;
    `DIFF_ENGINE_VERSION = "0.1.0"`.
  - `featuresmith/diff/engine.py` — `DatasetDiffEngine.diff(old, new)`
    (pandas/Polars/Dataset sources) + `compute_diff()` facade; schema/dtype/
    missing/duplicate/constant/statistics/distribution comparisons, threshold
    gating, deterministic output.
  - `featuresmith/diff/findings.py` — `findings_from_diff()` converting diff
    deltas into `RuleFinding`s with stable rule IDs
    (`diff.schema.*`, `diff.quality.*`, `diff.distribution.*`,
    `diff.leakage.*`); leakage deltas reuse the existing `LeakageReviewer`.
  - `featuresmith/diff/render.py` — `BaseDiffRenderer`,
    `DiffConsoleRenderer`, `DiffRendererRegistry`, `render_diff()` (reuses
    Rich; empty sections omitted; deterministic).
  - `featuresmith/diff/__init__.py` — package exports; `featuresmith/__init__.py`
    exports `diff` at the root.
  - `api.py` — `diff(old, new, *, target_column=None)` and
    `diff_findings(result)` (the latter imports from `featuresmith.api`, not the
    root); `review()` reverted to raise `NotImplementedError` when `previous` is
    passed (message points callers to `fs.diff()`).
  - CLI `featuresmith diff` in `featuresmith_cli/commands/diff.py` (registered
    in `main.py`): flags `--target`, `--format {table,json}`, `--output`,
    `--fail-on`, `--quiet`, `--verbose`, `--version`; exit codes 0 (no gated
    findings), 1 (gated findings, e.g. removed-column warning / leakage
    critical), 2 (load/format/unknown-target), 3 (source not found), 4
    (unexpected error).
  - Tests: `tests/diff/` (schema, engine, findings, render, SDK) and
    `tests/cli/test_cli_diff.py` — 69 new tests.
  - `pyproject.toml` — import-linter `ignore_imports` edges for
    `featuresmith.api -> featuresmith.diff.*` and diff→core/review transitive
    paths; `ruff` files formatted.
- Important Decisions:
  - Diff ships as an independent engine, not a registered reviewer, per the
    confirmed scope decision; a diff-aware review is documented as future work.
  - Fixed semantics: `DatasetDiffSummary.columns_added/columns_removed` derive
    from `SchemaDiff.added_columns/removed_columns` (not structure counts).
  - `DatasetDiffResult` carries health at `summary.overall_health`, not on the
    result directly; JSON serialization goes through `_asdict_custom`.
- Full Validation: pytest (284 passed), ruff format/check clean, mypy strict
  clean on packages (89 files), mypy tests back to only the 6 pre-existing
  errors, lint-imports contract kept, wheels for featuresmith-core and
  featuresmith-cli build, and CLI/SDK smoke tests (leakage section renders,
  exit-code gating works, JSON serializes, `fs.review(previous=...)` still
  raises as designed).

### Release Readiness Sprint 3 (RR-3) — Examples & Tutorials

- Objective: Produce standard examples and tutorial materials demonstrating the full SDK & CLI workflows across common industry patterns.
- Major Deliverables:
  - Dataset ingestion and cleanup utilities (`examples/download_datasets.py` and `examples/prepare_datasets.py`) storing processed records in `examples/data/processed/` using high-availability GitHub mirror fallbacks to bypass OpenML time-outs.
  - Complete SDK runner scripts and descriptive markdown guides under `examples/` (`iris/`, `titanic/`, `california_housing/`, `customer_churn/`, `sales/`).
  - Four educational Jupyter notebooks (`01_getting_started.ipynb`, `02_exploring_datasets.ipynb`, `03_understanding_rule_findings.ipynb`, `04_data_science_workflows.ipynb`) under `examples/notebooks/`.
- Files Added: Download and preparation scripts, example runner scripts, dataset READMEs, and Jupyter notebooks under `examples/`.
- Files Modified: None.
- Important Decisions:
  - Use real-world datasets where possible (Iris via scikit-learn, California Housing via scikit-learn, Titanic and Churn via OpenML with mirrors).
  - Use a simulated transaction log for Sales to model dates and constant column rules without committing multi-megabyte CSVs.
- Lessons Learned:
  - Public OpenML services frequently experience gateway timeouts; implementing automatic raw file HTTP fallbacks ensures reproducible examples setup.
- Known Limitations:
  - Notebooks are static documents and require the developer to download datasets prior to execution.

### Release Readiness Sprint 4 (RR-4) — Testing, Benchmarks & Performance

- Objective: Implement automated stress tests, integration checks, and a benchmark framework to measure time complexity and peak memory scaling.
- Major Deliverables:
  - Benchmark utility `benchmarks/run_benchmarks.py` and final report `docs/benchmarks.md` containing measured speeds and memory profiles across 10K, 100K, and 500K rows.
  - Stress testing suite `tests/test_stress.py` checking wide datasets (500 columns), tall datasets (100K rows), empty headers, single columns, and backend dataframes.
  - Integration suite `tests/test_integration.py` verifying SDK/CLI parity, JSON serialization, and error conditions.
- Files Added: `benchmarks/run_benchmarks.py`, `docs/benchmarks.md`, `tests/test_stress.py`, `tests/test_integration.py`.
- Files Modified: `frontend/lib/constants.ts` and `frontend/app/docs/[...slug]/page.tsx` (integrated benchmarks/custom rules docs into frontend site).
- Important Decisions:
  - Track peak memory allocations using python standard library's `tracemalloc` to keep the dependency footprint cross-platform and light.
  - Specify CLI `--severity warning` in parity tests to bypass default critical-level gating.
- Lessons Learned:
  - Click's standard `CliRunner` fails to inspect Typer modules directly; utilizing `typer.testing.CliRunner` correctly resolves the CLI command wrappers.
- Known Limitations:
  - Benchmarks do not cover non-local connectors.

### Sprint 5 — CLI MVP

- Objective: Build a production-grade CLI wrapper (`featuresmith-cli`) over the existing Featuresmith SDK, following the core-first architecture.
- Major Deliverables:
  - `featuresmith_cli/main.py` — top-level application wrapper using `typer`.
  - `featuresmith_cli/commands/analyze.py` — implementation of the main `analyze` command.
  - `featuresmith_cli/output.py` — dispatcher choosing between styled Rich text and JSON serializers.
  - `featuresmith_cli/rich_output.py` — human-readable formatting using `rich.table.Table`.
  - `featuresmith_cli/json_output.py` — machine-readable JSON representation.
  - `featuresmith_cli/utils.py` — helpers for colors, severity levels, and text processing.
  - `docs/adr/0002-cli-dependencies.md` — ADR documenting cli dependencies.
  - `tests/cli/test_cli.py` — integration and surface-parity tests.
- Files Modified: `featuresmith/api.py`, `pyproject.toml` (workspace-level configuration), `README.md`, `MEMORY.md`.
- Important Decisions:
  - All command actions and validation steps invoke `featuresmith.api` rather than duplicate core engine behaviors.
  - Expose `--severity` to function as both a finding visual filter and exit-code gating threshold.
  - Console width in the renderer set to 200 to prevent mid-word wrapping and truncations during testing.
- Lessons Learned:
  - Custom Click types are deprecated in modern Typer; using standard `Annotated` + `Literal` type hints creates correct options metadata while remaining fully compliant with MyPy.
  - Direct import contract checks can trigger transitive failures across internal dependencies; configure the `ignore_imports` list under workspace contract definitions to skip transitive edges.
- Known Limitations:
  - No interactive chat functionality is supported (deferred to Phase 3).
  - No configuration file resolution for rule threshold overrides (deferred to Sprint 6).

### Release Readiness Sprint 1 (RR-1) — Repository Polish

- Objective: Transform the repository into a professional GitHub project ready for its first public release. No product features implemented.
- Major Deliverables:
  - `README.md` — complete rewrite following FastAPI/Polars/Ruff quality bar: badges, Mermaid architecture diagram, SDK + CLI quickstart, rule engine table, project structure, design philosophy, roadmap table, quality tooling table, docs links, contributing guide.
  - `LICENSE` — updated from MIT to Apache 2.0 per `PRD.md §15` (patent grant matters for enterprise adoption).
  - `CONTRIBUTING.md` — full contributor guide: dev setup, coding standards, testing, extension points (rules/connectors/exporters/AI providers), PR guidelines, commit convention.
  - `CODE_OF_CONDUCT.md` — Contributor Covenant v2.1.
  - `SECURITY.md` — responsible disclosure process, privacy design notes, scope definition.
  - `CHANGELOG.md` — v0.1.0 upcoming release, full sprint history, upcoming release table.
  - `CITATION.cff` — placeholder citation metadata for academic use.
  - `CODEOWNERS` — assigns repository owner to all paths.
  - `.github/ISSUE_TEMPLATE/bug_report.yml` — structured bug report template.
  - `.github/ISSUE_TEMPLATE/feature_request.yml` — structured feature request template.
  - `.github/ISSUE_TEMPLATE/question.yml` — structured question template.
  - `.github/PULL_REQUEST_TEMPLATE.md` — professional PR template with checklists for general PRs, new rules, and new connectors.
  - `docs/github_repository.md` — written recommendations for repository description, topics, social preview, labels, Discussions categories, branch protection, and community health.
- Files Modified: `README.md`, `LICENSE`, `MEMORY.md`.
- Files Added: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`, `CITATION.cff`, `CODEOWNERS`, `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/ISSUE_TEMPLATE/feature_request.yml`, `.github/ISSUE_TEMPLATE/question.yml`, `.github/PULL_REQUEST_TEMPLATE.md`, `docs/github_repository.md`.
- Important Decisions:
  - LICENSE updated from MIT to Apache 2.0 — this was already specified in `PRD.md §15` and the change was flagged and confirmed before execution.
  - Version bumped to `0.0.5-dev` to reflect post-RR-1 state.
- Known Limitations: None. This sprint contains no code changes.

### Release Readiness Sprint 2 (RR-2) — Documentation Website

- Objective: Build the official Featuresmith documentation website and landing page using Next.js, replacing placeholders with repository-driven content.
- Major Deliverables:
  - catch-all dynamic docs routing (`frontend/app/docs/[...slug]/page.tsx`) mapping all concepts (Dataset, Profiling, Rules), SDK APIs, and CLI flag settings.
  - Interactive Examples showcase gallery (`frontend/app/examples/page.tsx`) detailing CI/CD pipeline gating and custom validation rule creation.
  - Landing page featuring technical attribute highlights, Core-first philosophy, open-source references, and Apache 2.0 license tags.
  - Sidebar routing systems and option descriptors mapping in `frontend/lib/constants.ts`.
- Files Added: `frontend/app/docs/[...slug]/page.tsx`, `frontend/app/examples/page.tsx`.
- Files Modified: `frontend/lib/constants.ts`, `frontend/features/home/hero.tsx`, `frontend/features/home/philosophy-section.tsx`, `frontend/features/home/open-source-section.tsx`, `frontend/components/navbar.tsx`, `frontend/components/footer.tsx`.
- Important Decisions:
  - Implement catch-all route mapping in Next.js to dynamically serve structured documentation without heavy page boilerplate.
  - Add a styled "Under Construction" fallback page in the docs layout for planned features (e.g. plugins, exporters) to provide a premium user experience and clear expectations.
- Known Limitations: None.

-------------------------------------------------

## Current Architecture Status

| Area | Status |
| --- | --- |
| Core | In Progress |
| Connectors | Completed |
| Profiling | Completed |
| Rules | Completed |
| Review Engine | Built-in Reviewer Set Implemented |
| Dataset Diff | Implemented |
| Recommendation Engine | Not Started |
| AI Layer | Not Started |
| Exporters | Not Started |
| CLI | Completed |
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
- `featuresmith analyze <source>` — CLI command; thin Typer wrapper over `fs.analyze()`.
  Flags: `--target`, `--format {table,json}`, `--output`, `--severity {info,warning,critical}`,
  `--max-correlation-columns`, `--quiet`, `--verbose`, `--version`.
  Exit codes: 0 (clean), 1 (findings above threshold), 2 (invalid input), 3 (file load failure), 4 (unexpected error).
- `fs.review(source, *, previous, target_column, enabled_reviewers,
  enabled_categories, reviewer_config)` — run the Review Engine pipeline
  (load → profile → rules → reviewers → aggregate) and return a `ReviewResult`.
  `previous=` raises `NotImplementedError` for now. Also exported: `render`,
  `ReviewCategory`, `ReviewSection`, `Severity`, `ReviewResult`.
- `featuresmith review <source>` — CLI command; thin Typer wrapper over `fs.review()`.
  Flags: `--target <column>`, `--previous`, `--format {table,json}`, `--output`, `--fail-on {info,warning,critical}`,
  `--only <categories>`, `--no-score`, `--quiet`, `--verbose`, `--version`.
  Exit codes: 0 (clean), 1 (finding ≥ `--fail-on`), 2 (usage / unknown category / `--previous`),
  3 (source missing/parse), 4 (unexpected error).
- `fs.diff(old, new, *, target_column=None)` — compare two datasets and return a
  `DatasetDiffResult` (schema, structure, data-quality, distribution, and
  leakage deltas with `summary.overall_health`); accepts pandas, Polars, or
  `Dataset` sources. Also exported: `render_diff`, `DiffFindingsResult`,
  `DatasetDiffResult`, `DatasetDiffSummary`.
- `diff_findings(result)` — convert a `DatasetDiffResult` into
  `RuleFinding[]` (imported from `featuresmith.api`).
- `featuresmith diff <old> <new>` — CLI command; thin Typer wrapper over
  `fs.diff()`. Flags: `--target`, `--format {table,json}`, `--output`, `--fail-on`,
  `--quiet`, `--verbose`, `--version`. Exit codes: 0 (clean), 1 (gated findings),
  2 (usage/format/unknown target), 3 (source missing), 4 (unexpected error).

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
| 2026-07-26 | Sprint 5 | CLI is a thin Typer wrapper — all logic flows through `featuresmith.api`. | Enforce the core-first architecture; no business logic in the CLI package. |
| 2026-07-26 | Sprint 5 | Use `Annotated` + `Literal` types for constrained options, not `typer.types.Choice`. | Compatible with Typer 0.12+ (installed version) and generates correct type metadata. |
| 2026-07-26 | Sprint 5 | Use `import-linter` `ignore_imports` for transitive-only paths through `featuresmith.api`. | Prevent false positives from chains that route legitimately through the public API boundary. |
| 2026-07-26 | Sprint 5 | Set `Console(width=200)` to prevent mid-word Rich text wrapping in test environments. | Ensures rule IDs rendered in table cells are assertable without folding or truncation. |
| 2026-07-26 | Sprint 5 | Parquet fixture in CLI tests uses Polars `write_parquet()` not pandas. | Pandas Parquet requires pyarrow/fastparquet not installed; Polars writes natively. |
| 2026-08-02 | Review Engine | Architecture docs are the source of truth when they conflict with the sprint brief. | The sprint brief's `ReviewFinding` type and `INFO/WARNING/ERROR/CRITICAL` enum conflicted with the reviewed architecture; the latter wins. |
| 2026-08-02 | Review Engine | `Severity` uses lowercase string values `critical | warning | info | passed` with a `.rank`. | Backward compatible with existing `RuleFinding` severity strings and CLI `SEVERITY_LEVELS`. |
| 2026-08-02 | Review Engine | `ReviewSection.findings` reuses the existing `RuleFinding`; no separate `ReviewFinding` model. | Architecture requires traceability back to Rule Findings; no new model needed. |
| 2026-08-02 | Review Engine | Reviewers re-use `fs.analyze()` outputs; the engine never re-reads or re-profiles data. | Single profiling pass; reviewers are pure consumers of `ProfileResult` + `RuleFinding[]`. |
| 2026-08-02 | Review Engine | Zero built-in reviewers ship with the foundation; `fs.review(previous=...)` raises `NotImplementedError`. | Diff/scoring/AI are future phases; the pipeline must be correct with an empty reviewer set. |
| 2026-08-02 | Review Engine | Ruff formatter excludes `*.md` via `extend-exclude`. | Prevents `ruff format --check .` from rewriting intentional alignment in README and design docs. |
| 2026-08-02 | Review Engine (Sprint 2) | Seven built-in reviewers ship in `default_registry()`: schema health, types, missingness, duplicates, constants, cardinality, basic statistics. | `featuresmith review dataset.csv` must produce a meaningful review from the start; remaining PRD sections stay future work. |
| 2026-08-02 | Review Engine (Sprint 2) | Fully empty columns are reported by `SchemaHealthReviewer` only; `MissingValueReviewer` excludes them. | Every issue reported exactly once; no cross-reviewer double-flagging. |
| 2026-08-02 | Review Engine (Sprint 2) | Identifier-like/text findings folded into the Basic Statistics section (`review.quality.basic_statistics`); numeric constants reported there, not in `constants`. | Avoid output churn and duplicate "type" findings; a single owner per signal. |
| 2026-08-02 | Review Engine (Sprint 2) | Reviewer thresholds are configurable via `ReviewConfig.reviewer_config` keyed by reviewer ID. | Docs' configurable-threshold requirement without a global config object. |
| 2026-08-02 | Review Engine (Sprint 3) | ML Readiness Score is computed from aggregated `ReviewSection` findings only; `ScoreAdapter` is the sole bridge to `featuresmith.scoring`. | Structural guarantee behind the "not a black-box score" requirement. |
| 2026-08-02 | Review Engine (Sprint 3) | `MLReadinessScore`/`DimensionScore` are frozen dataclasses with `to_dict()`, not Pydantic `BaseModel`. | Consistent with every other core schema; no extra dependency. |
| 2026-08-02 | Review Engine (Sprint 3) | Seven score dimensions map 1:1 to the seven Sprint-2 reviewers; uniform default weights (1.0); weighted-mean overall with renormalization when a dimension is inapplicable. | Every shipped dimension must trace to a shipped reviewer; formula and weights versioned under `scoring_version = "0.1.0"`. |
| 2026-08-02 | Review Engine (Sprint 3) | Per-finding deductions: `critical` 30, `warning` 15, `info` 5; dimension starts at 100, clamped to [0, 100], rounded to 1 decimal. | Deterministic, explainable, and monotonic in findings. |
| 2026-08-02 | Review Engine (Sprint 3) | `--no-score` renders `"score": null` in JSON (not 0), and `fs.score()` returns the attached score, never re-running analysis. | Keeps "not scored" distinct from "scored poorly" and preserves one-pass review semantics. |
| 2026-08-02 | Dataset Diff (Sprint 5) | Dataset Diff ships as a standalone engine (`featuresmith.diff`), not a registered reviewer; `fs.review(previous=...)` stays `NotImplementedError`. | Confirmed scope decision — single-dataset review and two-dataset diff stay separate workflows; diff-aware review is future work. |
| 2026-08-02 | Dataset Diff (Sprint 5) | `DatasetDiffResult.to_dict()` goes through `_asdict_custom`; health lives at `summary.overall_health`. | Keeps diff output JSON-clean and consistent with `ReviewResult`/`ProfileResult` serialization. |

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
- [ ] Review Engine has eight built-in reviewers (schema health, types,
      missingness, duplicates, constants, cardinality, basic statistics, and
      leakage); outliers, distribution, duplicate-column, feature-quality, and
      diff reviewers are still future work in `reviewers/`.
- [ ] `fs.review(previous=...)` raises `NotImplementedError` — diff-aware review
      (and the reserved `ReviewResult.diff` field) is future work; the standalone
      `fs.diff()`/`featuresmith diff` covers the two-dataset workflow today.
- [ ] Diff findings rule IDs (`diff.schema.*`, `diff.quality.*`,
      `diff.distribution.*`, `diff.leakage.*`) are stable by construction but
      not yet versioned into a findings schema; revisit when a stable finding
      schema ships.
- [ ] `ReviewResult.score` is populated by the Score Adapter when a dimension
      applies and stays `None` otherwise; `--fail-below`/`--fail-below-dimension`
      CI gating on the score is future work.
- [ ] Leakage finding `id`s are volatile UUIDs; stable finding identifiers are
      deferred. The known-leaky benchmark suite
      (`Dataset-Diff-And-Leakage-Detection.md` §13) is not yet built.
- [ ] `review.quality.basic_statistics` currently absorbs the PRD's Outliers,
      Distribution, and Basic-statistics sections into one section; split into
      dedicated reviewers when Outlier/DistributionReviewer ship.
- [ ] `render` is not exported from the package root (only `featuresmith.api`
      and `featuresmith.review`); revisit if callers expect it at root.
- [ ] `ruff format --check .` excludes `*.md` via `extend-exclude` — reformatting
      Python code blocks inside docs is intentionally not enforced.

-------------------------------------------------

## Upcoming Sprint

- Sprint Number: Sprint 6 (deferred) — SDK Hardening & Exporter Layer
- Objective: SDK Hardening & Exporter Layer — improve SDK resilience, add JSON/CSV
  export helpers, and begin configuration loading from `.featuresmith.yml`.
  Deferred while the Review Engine foundation was built; still the next planned sprint.
- Major Tasks:
  - Add JSON and CSV export helpers to the SDK.
  - Implement `.featuresmith.yml` configuration loading for rule thresholds.
  - Extend SDK sampling strategy for very large datasets.
- Dependencies: Sprint 5 `featuresmith analyze` CLI; `RuleResult.to_dict()`; RR-1 repository polish.
- Expected Deliverables: `fs.export_json()`, `fs.export_csv()`; YAML config loader;
  size-tiered profiling strategy.

> Note: built-in Review Engine reviewers (schema/quality/leakage/diff) may take
> precedence over the deferred Sprint 6 items per `docs/features/Review-Engine-Architecture.md`.

-------------------------------------------------

## Changelog

### 2026-08-02 — Review Engine — Dataset Diff (Sprint 5)

- Implemented the standalone Dataset Diff Engine in `featuresmith/diff/`
  (`schema.py`, `engine.py`, `findings.py`, `render.py`, `__init__.py`) per
  `docs/features/Dataset-Diff-And-Leakage-Detection.md`; exposed `fs.diff()` and
  `diff_findings()` from `featuresmith.api` and `diff` at the package root.
- Added the `featuresmith diff old.csv new.csv` CLI command (mirrors
  analyze/review flags and exit codes); diff findings reuse the existing
  `LeakageReviewer` and profile data.
- Reverted the experimental `DiffReviewer` integration: `default_registry()`
  keeps exactly eight reviewers and `fs.review(previous=...)` remains
  `NotImplementedError`, per the confirmed scope decision; diff-aware review is
  documented future work.
- Added 69 tests (`tests/diff/` + `tests/cli/test_cli_diff.py`); full
  validation passes: ruff format/check, mypy strict (89 files), pytest
  (284 passed), lint-imports (1 kept, 0 broken), `uv build` for
  featuresmith-core and featuresmith-cli, and CLI/SDK smoke tests.
- Updated `Dataset-Diff-And-Leakage-Detection.md` and
  `Review-Engine-Architecture.md` to the standalone-engine status; synchronized
  `MEMORY.md`.

### 2026-08-02 — Review Engine — Leakage Integration & Production Readiness (Sprint 4.1)

- Registered the **Leakage Risk** scoring dimension (`score.leakage_risk` ↔
  `review.leakage`) in `scoring/dimensions/builtin.py` via the shared
  `SectionScoreDimension` base, so leakage findings now lower the ML Readiness
  Score; bumped `scoring_version` to `0.2.0` per the versioned-formula rule.
- Added CLI `--target <column>` to `featuresmith review` (mirrors `analyze`;
  validates the column against the dataset schema, forwards
  `target_column=` to `fs.review`), so target-aware leakage detection is
  available from the CLI and consistent with the SDK.
- Fixed lint issues: removed the unused `typing.Any` import and added
  `strict=True` to the `zip()` in `review/reviewers/leakage.py`.
- Added tests for leakage-scoring integration, score stability on leaky
  datasets, CLI target-column validation/behavior, and CLI rendering of
  leakage findings; updated scoring/sdk/render/cli tests for the 8-dimension
  set and `scoring_version` 0.2.0.
- Synchronized implementation status across `ML-Readiness-Score.md`,
  `Review-Engine-Architecture.md`, `Dataset-Diff-And-Leakage-Detection.md`,
  `Dataset-Review-PRD.md`, and `MEMORY.md`.
- Full validation passes: ruff format/check, mypy strict clean, pytest
  (215 passed), lint-imports clean, `uv build` for featuresmith-core and
  featuresmith-cli, and CLI/SDK smoke tests.

### 2026-08-02 — Review Engine — Intelligent Leakage Detection (Sprint 4)

- Implemented pattern-based intelligent leakage detection per
  `docs/features/Dataset-Diff-And-Leakage-Detection.md`: six built-in
  `LeakagePatternDetector`s in the new `featuresmith/rules/leakage/` package
  (future-information, target-correlation, identifier-shape, duplicate-target,
  timestamp, suspicious-correlation) plus a `LeakageReviewer`
  (`review.leakage`) that merges per-column findings into one `RuleFinding`.
- Preserved the legacy `LeakageRuleTargetCorrelation` rule
  (`leakage.potential_leakage`) as a re-export so `fs.analyze` behavior is
  unchanged; registered the reviewer as the 8th built-in in `default_registry()`.
- Added `tests/review/test_leakage_reviewer.py` (30 tests); full validation
  passes: ruff, mypy strict, pytest (208 passed), lint-imports, builds, CLI/SDK
  smoke tests.

### 2026-08-02 — Review Engine — Built-in Reviewers (Sprint 2)

- Implemented seven built-in reviewers in
  `packages/featuresmith-core/src/featuresmith/review/reviewers/` per the
  approved docs as contract: `SchemaHealthReviewer`
  (`review.schema.health`), `TypeReviewer` (`review.schema.types`),
  `MissingValueReviewer` (`review.quality.missingness`),
  `DuplicateReviewer` (`review.quality.duplicates`),
  `ConstantColumnReviewer` (`review.quality.constants`),
  `CardinalityReviewer` (`review.quality.cardinality`),
  `BasicStatisticsReviewer` (`review.quality.basic_statistics`), plus the
  shared `SectionReviewer` base (`reviewers/base.py`) and
  `section_severity()` helper.
- Wired `default_registry()` to the seven reviewers via
  `builtin_reviewers()`; `featuresmith review dataset.csv` now produces
  findings from all reviewers (deterministic, traceable `RuleFinding`s).
- Reviewers read only the frozen `ReviewContext`, reuse the existing rule
  engine where a matching rule exists (missingness/duplicates/constants/
  cardinality), set `requires_previous_snapshot = False`, and honor
  per-reviewer `reviewer_config` thresholds.
- Added `tests/review/test_reviewers.py` (per-reviewer unit tests) and
  `tests/review/test_review_integration.py` (empty/clean/missing/duplicates/
  constants/mixed-types/high-cardinality, JSON serialization, config
  overrides); updated `test_registry.py`, `test_sdk.py`, `test_engine.py`,
  and `tests/cli/test_cli_review.py` for the non-empty default registry.
- Updated `docs/features/Review-Engine-Architecture.md` (§14) and
  `docs/features/Dataset-Review-PRD.md` (§7.1) implementation status.
- Full validation passes: ruff format/check, mypy strict (89 files),
  pytest (151 passed), lint-imports (1 kept, 0 broken), `uv build` for
  featuresmith-core and featuresmith-cli, and an end-to-end CLI smoke test.

### 2026-08-02 — Review Engine — ML Readiness Score (Sprint 3)

- Implemented the deterministic, explainable ML Readiness Score in
  `packages/featuresmith-core/src/featuresmith/scoring/` per
  `docs/features/ML-Readiness-Score.md` as contract:
  `ScoreDimension` Protocol, `SectionScoreDimension` base, seven built-in
  dimensions (one per Sprint-2 reviewer), `ScoreDimensionRegistry` +
  `default_registry()`, `WeightedAggregator` with `SCORING_VERSION = "0.1.0"`,
  and frozen `DimensionScore`/`MLReadinessScore` schemas carrying `summary`,
  `positive_findings`, and `negative_findings`.
- Wired the `ScoreAdapter` (`review/scoring_adapter.py`) as the sole bridge:
  `ReviewEngine.run()` attaches `result.score` after aggregation; `ReviewResult`
  now types `score` as `MLReadinessScore | None`.
- Surfaced via `fs.score(result)` (returns the attached score, never re-runs
  analysis), the console renderer's "ML Readiness Score" block, and the CLI's
  `--no-score` flag (JSON output yields `"score": null`).
- Added `tests/scoring/test_scoring.py` (22 tests) and score assertions to
  `tests/review/test_sdk.py`, `tests/review/test_render.py`, and
  `tests/cli/test_cli_review.py`.
- Updated `docs/features/ML-Readiness-Score.md` (status + §16 "Implementation
  Status (Sprint 3)"), `Review-Engine-Architecture.md` (§14), and
  `Dataset-Review-PRD.md` (status).
- Full validation passes: ruff format/check, mypy strict (100 source files),
  pytest (178 passed), lint-imports (1 kept, 0 broken), `uv build` for
  featuresmith-core and featuresmith-cli, and an end-to-end CLI smoke test
  (`Overall: 97.9/100`, `--no-score` omits the block).

### 2026-08-02 — Review Engine Foundation

- Added the Review Engine orchestration foundation in
  `packages/featuresmith-core/src/featuresmith/review/` per the approved
  `docs/features/Review-Engine-Architecture.md`: `schema.py`, `context.py`,
  `base.py`, `registry.py`, `aggregator.py`, `engine.py`, `render.py`,
  `__init__.py`, and `reviewers/__init__.py` (empty placeholder).
- Added `Severity` (`critical | warning | info | passed`) and `ReviewCategory`
  enums; `ReviewSection` and `ReviewResult` schemas reusing the existing
  `RuleFinding` type; `ReviewConfig`/`ReviewContext`; `BaseReviewer` ABC;
  `ReviewerRegistry`; `ReviewEngine.run()` 5-stage pipeline with per-reviewer
  fault isolation; `ResultAggregator`; `ConsoleRenderer` + `RendererRegistry`.
- Extended `_asdict_custom` in `core/profile_result.py` to serialize `datetime`
  and `Enum` so `ReviewResult.to_dict()` is JSON-clean.
- Added SDK `fs.review()` (reusing `fs.analyze()`; `previous=` raises
  `NotImplementedError`) and exported `review` at the package root, plus
  `render`, `ReviewCategory`, `ReviewResult`, `ReviewSection`, `Severity` from
  `featuresmith.api`.
- Added `featuresmith review <source>` CLI command with table/json formats,
  `--output`, `--fail-on`, `--only`, `--quiet`, `--verbose`, `--version`;
  exit codes 0/1/2/3/4.
- Added 56 tests under `tests/review/` and `tests/cli/test_cli_review.py`.
- Added `extend-exclude = ["*.md"]` to `[tool.ruff]` and review edges to the
  import-linter `ignore_imports` list.
- Full validation passes: ruff format/check, mypy strict (79 files), pytest
  (121 passed), lint-imports (1 kept, 0 broken), `uv build` for all three
  packages, and CLI smoke tests.

### 2026-07-26 — Release Readiness Sprint 4 (RR-4)

- Added benchmark framework under `benchmarks/run_benchmarks.py` using stdlib `tracemalloc` to track peak memory cross-platform.
- Executed benchmarks for 10K, 100K, and 500K rows, compiling results inside `docs/benchmarks.md`.
- Added stress test suite under `tests/test_stress.py` covering wide datasets (500 columns), tall datasets (100K rows), empty headers, single-column data, and pandas/Polars parity.
- Added integration test suite under `tests/test_integration.py` checking CLI/SDK parity, JSON serialization, and ConnectorError handling.
- Integrated performance benchmarks table and custom rules guides dynamically into Next.js frontend website.

### 2026-07-26 — Release Readiness Sprint 3 (RR-3)

- Added dataset downloader (`examples/download_datasets.py`) fetching Iris, California Housing, Titanic, and Customer Churn datasets with high-availability GitHub mirror fallbacks for resilience.
- Added dataset preparer (`examples/prepare_datasets.py`) normalizing raw files, generating synthetic sales logs, and saving cleaned CSVs to `examples/data/processed/`.
- Created SDK runner examples (`run_sdk.py`) and detailed readme documentation for all 5 example datasets (`iris`, `titanic`, `california_housing`, `customer_churn`, `sales`).
- Created 4 Jupyter tutorial notebooks under `examples/notebooks/` illustrating getting started, profiling, rule configurations, and target leakage gating.

### 2026-07-26 — Release Readiness Sprint 2 (RR-2)

- Built official Featuresmith dynamic documentation website (`frontend/app/docs/[...slug]/page.tsx`) mapping all concepts (Dataset, Profiling, Rules), SDK APIs, and CLI flag settings.
- Built interactive Examples gallery (`frontend/app/examples/page.tsx`) detailing automated CI/CD pipeline gating and custom validation rule creation.
- Rewrote `constants.ts`, `hero.tsx`, `navbar.tsx`, and `footer.tsx` to display true repository-driven features and Apache 2.0 license indicators.
- Verified Next.js compiler correctness (`pnpm run build`).

### 2026-07-26 — Release Readiness Sprint 1 (RR-1)

- Rewrote `README.md` from scratch: badges, Mermaid diagram, SDK/CLI quickstart, rule engine table, roadmap table, design philosophy, quality tooling table, contributing section.
- Updated `LICENSE` from MIT to Apache 2.0 per `PRD.md §15`.
- Added `CONTRIBUTING.md` with full dev setup, coding standards, testing, extension points, and PR guidelines.
- Added `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1).
- Added `SECURITY.md` with responsible disclosure process and privacy design notes.
- Added `CHANGELOG.md` with v0.1.0 upcoming release and full sprint history.
- Added `CITATION.cff` with placeholder citation metadata.
- Added `CODEOWNERS` assigning all paths to repository owner.
- Added `.github/ISSUE_TEMPLATE/bug_report.yml`, `feature_request.yml`, `question.yml`.
- Added `.github/PULL_REQUEST_TEMPLATE.md`.
- Added `docs/github_repository.md` with GitHub repository setup recommendations.
- Version bumped to `0.0.5-dev`.

### 2026-07-26 — Sprint 5 (CLI MVP)

- Added `featuresmith-cli` package with Typer entrypoint registered as the `featuresmith` script.
- Added `featuresmith analyze <source>` CLI command — thin wrapper over `fs.analyze()`.
  - `--target` — target column for leakage rule.
  - `--format {table,json}` — output format using Literal type annotation.
  - `--output` — save rendered report to a file (ANSI-stripped for txt; JSON for json).
  - `--severity {info,warning,critical}` — severity threshold for display and exit-code gating.
  - `--max-correlation-columns` — configurable correlation cap.
  - `--quiet` — suppress console output; file output still written.
  - `--verbose` — print full Python traceback on unexpected error.
  - `--version` — print version and exit (eager).
- Added `packages/featuresmith-cli/src/featuresmith_cli/` package tree:
  `__init__.py`, `main.py`, `commands/__init__.py`, `commands/analyze.py`,
  `output.py`, `rich_output.py`, `json_output.py`, `utils.py`.
- Added Rich terminal report with Dataset Overview, Analysis Findings & Issues
  (including `rule_id` as dim subtitle), and Execution Summary tables.
- Added JSON output mode using `RuleResult.to_dict()` canonical serialization.
- Added ANSI strip utility for plain-text file exports.
- Added `tests/cli/test_cli.py` with 14 integration test scenarios:
  help display, version, CSV/Excel/Parquet analysis, severity thresholds, JSON format,
  missing file, unsupported format, invalid target column, file output (txt + JSON),
  quiet mode, and surface parity with SDK.
- Updated `featuresmith.api` to re-export `Dataset`, `ProfileResult`, `RuleResult`,
  and `ConnectorError` as explicit `as X` re-exports for mypy `attr-defined` compliance.
- Updated `pyproject.toml` `import-linter` contract with `ignore_imports` list
  to suppress legitimate transitive paths through `featuresmith.api`.
- Exit codes implemented: 0 (clean), 1 (findings ≥ threshold), 2 (invalid input),
  3 (file load failure), 4 (unexpected error).

### 2026-07-25 — Sprint 4 Quality & Release Preparation Pass

- Updated workspace and package versions across all `pyproject.toml` and metadata structures to `0.0.4-dev` pre-release.
- Completed comprehensive review of public SDK APIs (`fs.load()`, `fs.profile()`, `fs.analyze()`) to ensure consistent Google Style Docstrings with type hints, raises, parameter details, examples, and notes.
- Refined public API signatures by introducing and passing through `max_correlation_columns` parameter in `fs.profile()` and `fs.analyze()`.
- Standardized class, attribute, and method documentation across core models (`Dataset`, `ProfileResult`, `RuleResult`, `RuleFinding`) and base interfaces (`BaseConnector`, `BaseRule`, `RuleEngine`).
- Verified code formatting, linting, typing, and import boundary rules; verified tests on both pandas and Polars.

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
