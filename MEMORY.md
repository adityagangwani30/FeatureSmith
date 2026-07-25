# Featuresmith Development Memory

## Project Overview

- Current Version: 0.1.0 (development)
- Current Phase: Phase 1 — SDK + CLI MVP
- Current Sprint: Sprint 2 — Dataset Foundation and Connector System
- Repository: `D:\FeatureSmith`
- Last Updated: 2026-07-25

-------------------------------------------------

## Sprint Status

| Sprint | Status | Completion Date |
| --- | --- | --- |
| Sprint 1 — Foundations | Completed | 2026-07-25 |
| Sprint 2 — Dataset Foundation and Connector System | Completed | 2026-07-25 |

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

-------------------------------------------------

## Current Architecture Status

| Area | Status |
| --- | --- |
| Core | Completed |
| Connectors | Completed |
| Profiling | Not Started |
| Rules | Not Started |
| Recommendation Engine | Not Started |
| AI Layer | Not Started |
| Exporters | Not Started |
| CLI | Not Started |
| Dashboard | Not Started |
| Plugin System | Not Started |

-------------------------------------------------

## Public APIs Implemented

- `fs.load(source)`
- `Dataset.preview(rows=5)`

-------------------------------------------------

## Technical Decisions

| Date | Sprint | Decision | Reason |
| --- | --- | --- | --- |
| 2026-07-25 | Sprint 1 | Enforce thin surfaces through package boundaries and import-linter. | Keep all business logic in the reusable core. |
| 2026-07-25 | Sprint 2 | Use Polars for CSV/Parquet and pandas for Excel/pandas interoperability. | Match the architecture's Polars-first direction while preserving pandas compatibility. |
| 2026-07-25 | Sprint 2 | Keep connector registration explicit and static. | Establish the extension boundary without implementing future plugin discovery. |

-------------------------------------------------

## Known Technical Debt

- [ ] Add entry-point connector discovery only in its scheduled plugin-system phase.
- [ ] Add multi-sheet Excel selection only in its scheduled connector phase.

-------------------------------------------------

## Upcoming Sprint

- Sprint Number: Not recorded in the current implementation brief.
- Objective: Not recorded in the current implementation brief.
- Major Tasks: Not recorded in the current implementation brief.
- Dependencies: Sprint 2 dataset and connector foundation.
- Expected Deliverables: Not recorded in the current implementation brief.

-------------------------------------------------

## Changelog

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
