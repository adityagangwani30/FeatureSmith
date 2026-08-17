# Implementation Status Tracker

> Authoritative implementation tracker for Featuresmith v0.4.0. This document records what is implemented, what is intentionally deferred, and what is planned future work. It does not duplicate architecture — it only records implementation status.

Last Updated: 2026-08-17 (v0.4.0)

---

## Review Engine

### Implemented
- **Review Pipeline** (`ReviewEngine.run`) — 5-stage orchestration in `featuresmith/review/engine.py`
- **Reviewer Registry** (`ReviewerRegistry`) — explicit registration in `featuresmith/review/registry.py`
- **Result Aggregator** (`ResultAggregator`) — `featuresmith/review/aggregator.py`
- **BaseReviewer interface** — `featuresmith/review/base.py`
- **Built-in Reviewers (10/12)**:
  - `SchemaHealthReviewer` (`review.schema.health`)
  - `TypeReviewer` (`review.schema.types`)
  - `MissingValueReviewer` (`review.quality.missingness`)
  - `DuplicateReviewer` (`review.quality.duplicates`) — covers duplicate rows
  - `ConstantColumnReviewer` (`review.quality.constants`)
  - `CardinalityReviewer` (`review.quality.cardinality`)
  - `BasicStatisticsReviewer` (`review.quality.basic_statistics`)
  - `LeakageReviewer` (`review.leakage`) — 6 pattern detectors merged per column
  - `DiffReviewer` (`review.diff`) — diff-aware review, active only when a previous snapshot is provided (added v0.3.0)
  - `FeatureQualityReviewer` (`review.quality.feature_quality`) — near-constant, redundant, and low-signal columns (added v0.4.0)
- **Review Categories** (`ReviewCategory` enum) — 6 categories: `schema`, `quality`, `leakage`, `diff`, `feature_quality`, `custom`
- **Centralized Recommendation Engine** (`featuresmith.recommendation`):
  - `RecommendationEngine` — merges findings from all review sections into a single ranked, explainable list of `Recommendation` objects
  - `Recommendation` dataclass with traceability (`originating_findings`, `originating_reviewers`)
  - Replaces the minimal severity-ranked fallback formatter; fallback formatter removed
- **Recommendation Adapter** — bridges Review Engine to centralized Recommendation Engine
- **Score Adapter** — bridges Review Engine to `featuresmith.scoring` in `featuresmith/review/scoring_adapter.py`
- **Console Renderer** (`ConsoleRenderer` + `RendererRegistry`) — `featuresmith/review/render.py`
- **Plan Renderer** (`PlanRenderer`) — `featuresmith/review/render.py`, renders `Plan` objects via `plan_console` target
- **SDK Entrypoints** — `fs.review()`, `fs.plan()` in `featuresmith/api.py`
- **CLI Commands** — `featuresmith review` and `featuresmith plan` with full flag sets
- **CI Exit Codes** — 0 (clean), 1 (findings ≥ threshold), 2 (usage/unknown category), 3 (source missing/parse), 4 (unexpected error)

### Deferred (Intentionally Not Yet Implemented)
- **CategoryRegistry** with entry-point discovery — explicit registration only for now
- **Plugin Architecture** (entry_points for reviewers) — same pattern as rules/connectors, deferred
- **Dashboard / HTML / JSON Renderers** — only `ConsoleRenderer` and `PlanRenderer` implemented
- **AI Integration** (narration, AI-enhanced ranking) — Phase 6

### Future Work (Planned)
- **DuplicateColumnReviewer** (`review.quality.duplicate_columns`)
- **OutlierReviewer** (`review.statistics.outliers`)
- **DistributionReviewer** (`review.distribution`)
- **Reviewer priority/ordering config** in `.featuresmith.yml`
- **Custom review profiles** (e.g., `--profile pre-training`)
- **Cross-reviewer dependencies**
- **Streaming/partial rendering** for large datasets

---

## Dataset Review

### Implemented
- **SDK**: `fs.review(source, target_column, enabled_reviewers, enabled_categories, reviewer_config)`
- **CLI**: `featuresmith review <source>` with all flags above
- **9 of 11 required sections** (§7.1 table):
  - Schema health ✅
  - Missing values ✅
  - Duplicate rows ✅
  - Data types ✅
  - Constant columns ✅
  - High-cardinality columns ✅
  - Target leakage warnings ✅
  - Overall summary ✅
  - Feature quality ✅ (added v0.4.0)
- **ML Readiness Score** attached by default (`--no-score` to opt out)
- **Category filtering** via `--only schema,leakage` etc.
- **Severity-sorted output** (critical → warning → info → passed)
- **Surface parity** — SDK and CLI produce identical `ReviewResult`
- **Centralized Recommendation Engine** — `ReviewResult.recommendations` (flat, ranked list) and per-section `ReviewSection.recommendations` populated by `RecommendationAdapter` using `featuresmith.recommendation.RecommendationEngine`

### Deferred
- (None — centralized Recommendation Engine implemented in v0.4.0)

### Future Work
- **Duplicate columns** section (`DuplicateColumnReviewer`)
- **Outliers** section (`OutlierReviewer`)
- **Distribution issues** section (`DistributionReviewer`)
- **Dashboard "Review" tab**
- **HTML static report**
- **Named review profiles** (`--profile`)
- **Review history/trend view** — Phase 5

---

## ML Readiness Score

### Implemented
- **ScoreDimension Protocol** — `featuresmith/scoring/dimensions/base.py`
- **ScoreDimensionRegistry** — `featuresmith/scoring/registry.py`
- **WeightedAggregator** — `featuresmith/scoring/aggregator.py` (weighted mean, renormalizes for inapplicable dimensions)
- **MLReadinessScore / DimensionScore schemas** — `featuresmith/scoring/schema.py`
- **Score Adapter** — `featuresmith/review/scoring_adapter.py`
- **7 Built-in Dimensions** (mapping to reviewers, per spec §7.1 with reconciliation):
  - `SchemaHealthDimension` → `review.schema.health`
  - `MissingValuesDimension` → `review.quality.missingness`
  - `FeatureQualityDimension` → `review.quality.feature_quality` (added v0.4.0)
  - `DistributionHealthDimension` → `review.quality.basic_statistics` (stub — reads `BasicStatisticsReviewer` output; `DistributionReviewer`/`OutlierReviewer` not yet implemented)
  - `LeakageRiskDimension` → `review.leakage` (added Sprint 4.1)
  - `DataQualityDimension` → `review.quality.duplicates`, `review.quality.constants` (cardinality removed; no double-count with Consistency)
  - `ConsistencyDimension` → `review.schema.types`, `review.quality.cardinality`
- **fs.review()** automatically attaches score
- **CLI `--no-score`** — omits score section from output
- **`fs.score(result)`** convenience accessor — computes from existing result, never re-runs analysis
- **`scoring_version = "0.3.0"`** — bumped from `0.2.0` after dimension reconciliation (cardinality double-count fix, Class Balance omitted)

### Deferred
- **`.featuresmith.yml` weight configuration** — config system not yet built

### Future Work
- **ClassBalanceDimension** — target column minority class detection (detector not implemented; dimension omitted per spec §7.4)
- **DistributionHealthDimension** — replace `basic_statistics` stub with `DistributionReviewer` / `OutlierReviewer`
- **CLI `--fail-below <score>`** — CI gate on overall score
- **CLI `--fail-below-dimension <dim:id>`** — CI gate on per-dimension score
- **Non-linear aggregation options** (hard floor on critical dimensions)
- **Community-contributed dimensions** (fairness, temporal consistency, etc.)
- **Score trend visualization** — Phase 5
- **Per-column score contribution view**

---

## Leakage Detection

### Implemented (Fully)
- **LeakagePatternDetector base interface** — `featuresmith/rules/leakage/base.py`
- **6 Built-in Pattern Detectors** (all in `featuresmith/rules/leakage/`):
  - `TargetCorrelationDetector` — extreme correlation with target (matured from Phase 1)
  - `IdentifierShapeDetector` — ID-like shape + correlation (reduces false positives)
  - `TimestampLeakageDetector` — datetime columns after prediction cutoff
  - `FutureInfoDetector` — columns only knowable after prediction point
  - `DuplicateTargetDetector` — deterministic transform of target
  - `SuspiciousCorrelationDetector` — high correlation + secondary signal
- **LeakageReviewer** — dispatches all detectors, merges findings per column into one `RuleFinding`
- **LeakageFinding schema** — typed, detection-only: column, pattern, confidence, rationale, suggested_action
- **ML Readiness Score integration** — `LeakageRiskDimension` consumes `LeakageReviewer` output
- **CLI `--target`** — validates column exists, forwards to reviewers
- **Backward compatibility** — legacy `LeakageRuleTargetCorrelation` re-exported unchanged

### Future Work
- **Configurable leakage sensitivity profiles** (strict/permissive) via `.featuresmith.yml`
- **Cross-dataset leakage detection** (train/test overlap) — bridging Diff + Leakage
- **AI-assisted pattern recognition** (Phase 6) — narrates deterministic findings, never invents new ones

---

## Dataset Diff

### Implemented (Fully — as Standalone Engine)
- **DatasetDiffEngine / compute_diff()** — `featuresmith/diff/engine.py`
- **DatasetDiffResult schema** — `featuresmith/diff/schema.py` (frozen dataclasses, `DIFF_ENGINE_VERSION = "0.2.0"`)
- **fs.diff(old, new, target_column=None)** — `featuresmith/api.py`
- **featuresmith diff CLI** — `featuresmith_cli/commands/diff.py` with `--target`, `--format`, `--output`, `--fail-on`, `--quiet`, `--verbose`, `--version`
- **Comparisons**:
  - Schema: added/removed/renamed columns, type changes
  - Structure: row count, column count deltas
  - Missing values: per-column missingness delta
  - Duplicate rows: count/percentage delta
  - Constant columns: newly constant / no longer constant
  - Cardinality: per-column unique value delta
  - Basic statistics: mean/median/std/min/max deltas for numeric columns
  - Distribution shifts: significant mean shifts (configurable threshold)
  - Leakage deltas: new/removed/escalated/de-escalated per column (requires `--target`)
- **Overall health verdict**: `regressed` / `improved` / `unchanged`
- **Plain-language recommendation**: engineering-focused summary of blocking changes
- **CI Exit Codes**: 0 (clean), 1 (gated findings), 2 (usage/format/unknown target), 3 (source not found), 4 (unexpected error)
- **JSON output** — deterministic serialization via `_asdict_custom`

### Architectural Decision
Dataset Diff ships as a **standalone engine** (`featuresmith.diff` package) AND as a **`DiffReviewer`** in the Review Engine (added v0.3.0):
- The standalone `featuresmith diff` CLI and `fs.diff()` remain the primary two-dataset workflow
- `DiffReviewer` (`review.diff`) reuses the standalone engine — it calls `compute_diff()` and `findings_from_diff()` — it does not re-profile the previous snapshot when a previous profile is available
- `fs.review(source, previous=...)` profiles the previous snapshot once at the SDK boundary and passes `previous_profile` to the engine; the diff section is appended only when a previous snapshot is provided
- Single-dataset review (`fs.review(source)` without `previous`) is unchanged: 8 sections, no diff section, `result.diff is None`

### Deferred / Future Work
- **ProfileDiff extension fields** (`distribution_shifts`, `quality_regressions`) — standalone `DatasetDiffResult` used instead

---

## Connectors

### Implemented
- **Local connector registry** (`fs.load()`, `featuresmith/connectors/`) — explicit, static registration; no entry-point discovery yet
- `CsvConnector` (Polars backend)
- `ExcelConnector` (`.xlsx`/`.xls`/`.xlsm`, pandas backend)
- `ParquetConnector` (`.pq`/`.parquet`, Polars backend)
- `DataFrameConnector` (accepts both pandas and Polars `DataFrame` in-memory, no file I/O)
- File-type/path validation with `featuresmith.core.ConnectorError` raised on invalid, corrupted, or unsupported sources with an actionable message
- File-backed `Dataset`s carry source path and byte size; in-memory `Dataset`s leave those fields `None`

### Deferred (Intentionally Not Yet Implemented)
- **Entry-point-based plugin discovery** for third-party connectors (`Architecture.md` §6, §16) — registry is static this release
- **SQL connector** (SQLAlchemy) — planned Phase 3
- Cloud/warehouse connectors (Snowflake, BigQuery, S3, GCS) — planned Phase 8

---

## Dataset Contracts & Plan/Apply Lifecycle

### Implemented (v0.4.0)
- **Plan Primitive** (`featuresmith.plan`):
  - `Plan` / `PlanItem` dataclasses with versioned schema (`PLAN_SCHEMA_VERSION = "0.1.0"`)
  - `compile_plan()` / `compile_plan_from_recommendations()` — deterministic compilation from accepted recommendation IDs
  - `PlanRenderer` (`plan_console` target) and `render()` dispatch for `Plan` objects
  - `fs.plan(result, accept=[...])` SDK function
  - `featuresmith plan` CLI command with `--accept`, `--target`, `--previous`, `--format table|json`, `--fail-on`, `--output`, `--quiet`
  - Full traceability: `PlanItem` → `Recommendation` → `originating_findings` + `originating_reviewers`

### Status: Plan Implemented — Design Complete for Contracts/Apply

Full specification for Dataset Contracts (`featuresmith.lock`), Apply/Export, and Validation in `features/Dataset-Contracts-And-Planning.md`; no code exists yet for Contracts/Apply. Roadmap placement: Phase 5 (Apply, Validation, `featuresmith.lock`), Phase 6 (Certification, Observability).

---

## Summary: v0.4.0 Release Readiness

| Capability | Implementation % | Release Ready |
|------------|------------------|---------------|
| Review Engine Core | ~85% | ✅ Yes (usable with 10 reviewers + Recommendation Engine) |
| Dataset Review | ~90% | ✅ Yes (10/11 sections, score, recommendations, CLI) |
| ML Readiness Score | ~85% | ✅ Yes (7 dims, CLI, SDK, dimension reconciliation) |
| Leakage Detection | 100% | ✅ Yes (6 detectors, reviewer, scoring) |
| Dataset Diff | 100% | ✅ Yes (standalone engine + DiffReviewer, CLI, SDK) |
| Connectors (CSV/Excel/Parquet/DataFrame) | 100% | ✅ Yes (static registry) |
| Dataset Contracts / Plan / Apply | ~25% | ✅ Plan shipped; Contracts/Apply design complete |

### Known Gaps for v0.4.0 (Documented, Not Blockers)
1. 2 of 11 Dataset Review sections missing (duplicate columns, outliers, distribution — feature quality now implemented)
2. No `.featuresmith.yml` config system
3. No dashboard, HTML report, or JSON renderer for review
4. No CI score gating (`--fail-below`, `--fail-below-dimension`)
5. Class Balance dimension omitted (minority-class detector not implemented)
6. DistributionHealthDimension uses `basic_statistics` stub (DistributionReviewer/OutlierReviewer not implemented)
7. Dataset Contracts / Apply / `featuresmith.lock` not started — design complete, Phase 5-6

All gaps are documented in the architecture documents as deferred/future work and do not block the v0.4.0 release.