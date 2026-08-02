# Implementation Status Tracker

> Authoritative implementation tracker for Featuresmith v0.2.0. This document records what is implemented, what is intentionally deferred, and what is planned future work. It does not duplicate architecture — it only records implementation status.

Last Updated: 2026-08-02 (v0.2.0)

---

## Review Engine

### Implemented
- **Review Pipeline** (`ReviewEngine.run`) — 5-stage orchestration in `featuresmith/review/engine.py`
- **Reviewer Registry** (`ReviewerRegistry`) — explicit registration in `featuresmith/review/registry.py`
- **Result Aggregator** (`ResultAggregator`) — `featuresmith/review/aggregator.py`
- **BaseReviewer interface** — `featuresmith/review/base.py`
- **Built-in Reviewers (8/12)**:
  - `SchemaHealthReviewer` (`review.schema.health`)
  - `TypeReviewer` (`review.schema.types`)
  - `MissingValueReviewer` (`review.quality.missingness`)
  - `DuplicateReviewer` (`review.quality.duplicates`) — covers duplicate rows
  - `ConstantColumnReviewer` (`review.quality.constants`)
  - `CardinalityReviewer` (`review.quality.cardinality`)
  - `BasicStatisticsReviewer` (`review.quality.basic_statistics`)
  - `LeakageReviewer` (`review.leakage`) — 6 pattern detectors merged per column
- **Review Categories** (`ReviewCategory` enum) — 7 categories: `schema`, `quality`, `leakage`, `diff`, `feature_quality`, `custom`
- **Score Adapter** — bridges Review Engine to `featuresmith.scoring` in `featuresmith/review/scoring_adapter.py`
- **Console Renderer** (`ConsoleRenderer` + `RendererRegistry`) — `featuresmith/review/render.py`
- **SDK Entrypoint** — `fs.review()` in `featuresmith/api.py`
- **CLI Command** — `featuresmith review` with `--target`, `--format`, `--output`, `--fail-on`, `--only`, `--no-score`, `--quiet`, `--verbose`, `--version`
- **CI Exit Codes** — 0 (clean), 1 (findings ≥ threshold), 2 (usage/unknown category/`--previous`), 3 (source missing/parse), 4 (unexpected error)

### Deferred (Intentionally Not Yet Implemented)
- **Recommendation Engine / Adapter** — centralized recommendation generation; reviewers produce findings only
- **CategoryRegistry** with entry-point discovery — explicit registration only for now
- **Plugin Architecture** (entry_points for reviewers) — same pattern as rules/connectors, deferred
- **Dashboard / HTML / JSON Renderers** — only `ConsoleRenderer` implemented
- **AI Integration** (narration, AI-enhanced ranking) — Phase 6

### Future Work (Planned)
- **DiffReviewer** — Dataset Diff ships as standalone engine (`featuresmith.diff`); Review Engine integration is future work
- **DuplicateColumnReviewer** (`review.quality.duplicate_columns`)
- **OutlierReviewer** (`review.statistics.outliers`)
- **DistributionReviewer** (`review.distribution`)
- **FeatureQualityReviewer** (`review.feature_quality`) — requires Phase 4 Feature Engineering Engine
- **`fs.review(previous=...)`** — currently raises `NotImplementedError`; use `fs.diff()` instead
- **Reviewer priority/ordering config** in `.featuresmith.yml`
- **Custom review profiles** (e.g., `--profile pre-training`)
- **Cross-reviewer dependencies**
- **Streaming/partial rendering** for large datasets

---

## Dataset Review

### Implemented
- **SDK**: `fs.review(source, target_column, enabled_reviewers, enabled_categories, reviewer_config)`
- **CLI**: `featuresmith review <source>` with all flags above
- **8 of 11 required sections** (§7.1 table):
  - Schema health ✅
  - Missing values ✅
  - Duplicate rows ✅
  - Data types ✅
  - Constant columns ✅
  - High-cardinality columns ✅
  - Target leakage warnings ✅
  - Overall summary ✅
- **ML Readiness Score** attached by default (`--no-score` to opt out)
- **Category filtering** via `--only schema,leakage` etc.
- **Severity-sorted output** (critical → warning → info → passed)
- **Surface parity** — SDK and CLI produce identical `ReviewResult`

### Deferred
- **Centralized Recommendation Engine** — no recommendations generated; findings only

### Future Work
- **Duplicate columns** section (`DuplicateColumnReviewer`)
- **Outliers** section (`OutlierReviewer`)
- **Distribution issues** section (`DistributionReviewer`)
- **Feature quality** section (`FeatureQualityReviewer`) — Phase 4
- **Diff-aware review** (`--previous`) — use `fs.diff()` instead
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
- **8 Built-in Dimensions** (mapping to reviewers):
  - `SchemaHealthDimension` → `review.schema.health`
  - `MissingValuesDimension` → `review.quality.missingness`
  - `DuplicateRecordsDimension` → `review.quality.duplicates`
  - `DataTypesDimension` → `review.schema.types`
  - `ConstantColumnsDimension` → `review.quality.constants`
  - `HighCardinalityDimension` → `review.quality.cardinality`
  - `DatasetStructureDimension` → `review.quality.basic_statistics`
  - `LeakageRiskDimension` → `review.leakage` (added Sprint 4.1)
- **fs.review()** automatically attaches score
- **CLI `--no-score`** — omits score section from output
- **`fs.score(result)`** convenience accessor — computes from existing result, never re-runs analysis
- **`scoring_version = "0.2.0"`** — bumped from `0.1.0` when Leakage Risk added

### Deferred
- **`.featuresmith.yml` weight configuration** — config system not yet built

### Future Work
- **FeatureQualityDimension** — requires `FeatureQualityReviewer` (Phase 4)
- **DistributionHealthDimension** — requires `DistributionReviewer` / `OutlierReviewer`
- **ClassBalanceDimension** — target column minority class detection
- **ConsistencyDimension** (as single dimension) — currently split into `DataTypesDimension` + `HighCardinalityDimension`
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
- **DatasetDiffResult schema** — `featuresmith/diff/schema.py` (frozen dataclasses, `DIFF_ENGINE_VERSION = "0.1.0"`)
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
Dataset Diff is a **standalone engine** (`featuresmith.diff` package), NOT a `DiffReviewer` in the Review Engine. This was a deliberate scope decision (Sprint 5):
- Review Engine keeps its 8-reviewer `default_registry()`
- `fs.review(previous=...)` raises `NotImplementedError` with message pointing to `fs.diff()`
- Single-dataset review and two-dataset diff remain separate workflows

### Deferred / Future Work
- **DiffReviewer** — Review Engine integration of diff capability
- **ReviewResult.diff field** — reserved, always `None`
- **ProfileDiff extension fields** (`distribution_shifts`, `quality_regressions`) — standalone `DatasetDiffResult` used instead

---

## Summary: v0.2.0 Release Readiness

| Capability | Implementation % | Release Ready |
|------------|------------------|---------------|
| Review Engine Core | ~70% | ✅ Yes (usable with 8 reviewers) |
| Dataset Review | ~75% | ✅ Yes (8/11 sections, score, CLI) |
| ML Readiness Score | ~80% | ✅ Yes (8 dims, CLI, SDK) |
| Leakage Detection | 100% | ✅ Yes (6 detectors, reviewer, scoring) |
| Dataset Diff | 100% | ✅ Yes (standalone engine, CLI, SDK) |

### Known Gaps for v0.2.0 (Documented, Not Blockers)
1. No centralized Recommendation Engine — findings only, no actionable recommendations
2. 3 of 11 Dataset Review sections missing (duplicate columns, outliers, distribution, feature quality)
3. No `DiffReviewer` — diff is standalone only
4. No `fs.review(previous=...)` — use `fs.diff()`
5. No `.featuresmith.yml` config system
6. No dashboard, HTML report, or JSON renderer for review
7. No CI score gating (`--fail-below`)

All gaps are documented in the architecture documents as deferred/future work and do not block the v0.2.0 release.