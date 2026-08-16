# PRD — Featuresmith

> **Scope note:** The goals in this document describe Featuresmith’s roadmap and product direction; they do not imply that every capability already exists in v0.2.0. For shipped implementation status, see `implementation/IMPLEMENTATION_STATUS.md`.

> The Dataset Contract layer for structured data — built around a single reusable Python core.

## 1. Vision

> The full case for why this exists, what category it's building, and its permanent boundaries lives in `VISION.md`. This section states, concretely, what that vision means as a product.

**"Every dataset deserves a code review" is Featuresmith's acquisition message** — the five words that explain the product to someone who has never heard of it. It is not the ceiling of what Featuresmith is building (`VISION.md` §1). Featuresmith's actual mission is broader: **make the state of a dataset as versioned, provable, and reviewable as the state of code.** Review is the entry point — the moment a user first sees Featuresmith catch something real. What Featuresmith becomes after that first review is a continuous lifecycle: a dataset is reviewed, a fix is recommended, a transformation is planned, that plan is applied through the tools a team already uses (pandas, Polars, scikit-learn, dbt), the result is reviewed again, the before/after is diffed, the change is documented, and the whole thing is locked into a versioned **Dataset Contract** — the artifact that lets a team, a CI pipeline, or a teammate six months from now answer "what exactly was this dataset, and is it safe to build on" without re-deriving the answer from scratch.

The end state: an engineer runs `featuresmith review` on a dataset the way they'd run a linter before a commit, gets a prioritized, evidence-backed verdict, accepts a plan to fix what's wrong, applies it with the dataframe library they already use, and walks away with a committed `featuresmith.lock` that is now part of the project's history — reviewable in a pull request exactly like a dependency-lockfile change is.

Critically, this experience must be **identical in substance no matter which surface it's accessed from**, because all surfaces are thin clients over one Python core. See `Architecture.md` §2 for the core-first architecture this PRD assumes throughout, and `features/Dataset-Contracts-And-Planning.md` for the full design of the Contract/Plan/Apply lifecycle referenced throughout this document.

## 2. Problem Statement

- EDA output today is descriptive, not diagnostic. Tools like `pandas-profiling`/`ydata-profiling`, `sweetviz`, and `autoviz` produce reports; a human still has to interpret them, spot leakage, and decide what to do.
- Feature engineering knowledge is tribal. Best practices (target encoding pitfalls, leakage from time-based joins, cardinality handling) live in senior engineers' heads, not in tools.
- The "understand → decide → code" loop is manual and slow. Nothing bridges a finding ("this column has 40% missing, correlated with target") to a generated, reviewable pipeline step, or lets a user simply *ask* why a finding matters.
- Existing profiling tools scale poorly on large data, rarely integrate with production pipeline code (sklearn `Pipeline`, `ColumnTransformer`, MLflow), and are almost always single-surface (a notebook cell or a CLI report) rather than a consistent experience across a script, a dashboard, and an editor.

## 3. Existing Solutions

| Tool | Strength | Gap |
|---|---|---|
| ydata-profiling | Rich single-report stats | No recommendations, no code output, slow on large data |
| Sweetviz | Fast visual comparison reports | Static HTML, no reasoning, no pipeline export |
| AutoViz | Automatic chart generation | Charts only, no data-quality reasoning |
| Great Expectations | Strong validation/testing | Not designed for exploratory discovery or feature engineering |
| Featuretools | Automated feature synthesis (DFS) | No EDA, no explanations, steep learning curve |
| DataPrep.eda | Fast, interactive EDA | No leakage detection, no NL explanation, no export, no conversational follow-up |

## 4. Why Existing Solutions Aren't Enough

They all stop at **description**. None of them close the loop from "here's a chart" to "here's why it matters, here's what to do, here's the code, and here's an answer to your follow-up question about it." None reason about *interactions between findings* — e.g., "this high-cardinality categorical is also a near-duplicate of the ID column, and encoding it naively will leak information forward." That reasoning step, and the ability to interrogate it conversationally, is exactly what an LLM-augmented system is suited for, and it's the gap Featuresmith fills — while keeping the LLM strictly out of the business of computing numbers (see §10, Core Features, and `Architecture.md` §7).

## 5. Goals

- Provide automatic, statistically rigorous EDA across tabular data of any reasonable size (local-first, scaling to distributed later).
- Detect data-quality issues (missingness patterns, drift, skew, cardinality problems, target leakage, duplicate/near-duplicate rows, outliers) with explanations, not just flags — the shipped Review Engine (`features/Review-Engine-Architecture.md`).
- Compare two dataset snapshots the way `git diff` compares two commits, and make that comparison a persistable, git-native artifact — not just a one-off CLI report.
- Recommend concrete transformations for accepted findings, each with a rationale and confidence, and represent every recommendation as an inspectable, deterministic **Plan** before anything is applied (`features/Dataset-Contracts-And-Planning.md`).
- Turn an accepted Plan into real, readable code for the ecosystem the user already runs — a `sklearn.Pipeline`, a Polars expression, a dbt model — by default generating that code rather than running it, and never by executing anything inside a Featuresmith-owned runtime (`features/Dataset-Contracts-And-Planning.md` §7.2).
- Re-review and diff a dataset after a transformation is applied, so "did this fix actually work" is answered by the same deterministic engine that found the problem, not by trust.
- Persist dataset state — schema fingerprint, readiness score, leakage findings, transformation lineage — into a versioned, diffable **Dataset Contract** (`featuresmith.lock`) that a team commits to git and a CI pipeline gates on, the same way a dependency lockfile is committed and diffed today.
- Let a natural-language instruction populate a Plan the same way a rule-based recommendation would, so the deterministic Plan/Export loop has exactly one shape regardless of how the plan was authored.
- Ship one Python core library that every interface — SDK, CLI, dashboard, IDE extension — calls identically, with zero duplicated business logic (`Architecture.md` §2). **The dashboard is a surface over this core, not the product itself** — every capability ships as an SDK call and a CLI command first (or alongside), the deterministic core and CI/CD workflows never depend on the dashboard existing, and a future hosted/team tier extends the dashboard as a surface without turning `featuresmith-core` itself into a hosted/backend architecture (`Design-Principles.md`, `Architecture.md` §25.2).
- **Remain simple enough for a new contributor to understand the whole system, while providing extension points that can evolve as real user or contributor demand emerges** — across the analysis engine, the export/apply layer, and the AI provider layer. This explicitly rejects designing today's architecture around hypothetical future scale: build for today's demonstrated problems, keep interfaces clean and small, and let a proven extension point (one with a real external contributor actually blocked by it) evolve into something more elaborate — never the reverse. Maintainability, modularity, and a healthy open-source contributor base remain the goal; the architecture that gets there is decided by evidence as it arrives, not architected in advance for a contributor base that doesn't exist yet (`Architecture.md` §23.3, §25.1).

## 6. Non-Goals

These are not phase-limited caveats — they are permanent boundaries, restated here at product-spec level; the philosophy behind them is in `VISION.md` §3. Featuresmith's core differentiation is *proof*, not *execution*; every non-goal below exists to keep the product from drifting into infrastructure categories it has no structural advantage in. See `Architecture.md` §20 for the corresponding integration model (how Featuresmith cooperates with the tools it deliberately does not replace).

- **Not an orchestration or scheduling engine.** No DAG runner, no job scheduler for its own sake. Featuresmith plans and validates transformations; Airflow, Dagster, Prefect, and dbt's own scheduler run them.
- **Not a distributed execution engine.** No Featuresmith-branded Spark/Ray runtime. Large-scale compute is delegated to backends Featuresmith pushes down to (DuckDB, Spark, Snowflake, BigQuery — Phase 8), never reimplemented.
- **Not a proprietary transformation runtime or DSL.** Recommended transformations compile to real, readable Polars expressions or a real `sklearn.Pipeline` — code a user can run, read, and own outside Featuresmith entirely — never a Featuresmith-only mini-language.
- **Not a feature store.** Featuresmith does not serve features online or manage feature versioning at serving time; it exports to feature stores (Feast) that already own that job.
- **Not an AutoML or model-training system.** It recommends and validates data fixes; it never selects, tunes, or trains a model. The moment a recommendation is about hyperparameters instead of data, it's out of scope.
- **Not a no-code/low-code platform.** Every capability is developer-first: importable, scriptable, and pipeable before it has a UI (`Design-Principles.md`).
- **Not a data warehouse or storage product** — it connects to and certifies existing sources, it doesn't replace them.
- **Not a real-time streaming analytics tool** in early phases.
- **Not a replacement for domain expertise** — recommendations and transformation plans are advisory, always reviewable/rejectable, never silently applied without an explicit `apply` step.
- **Not initially multi-modal** (image/text/audio) — tabular-first, with NLP-column support as a stretch goal.
- **The AI layer is not a general-purpose data-analysis chatbot with live dataframe access** — it narrates, ranks, and translates natural language into an inspectable Plan grounded in the precomputed profile only; it never computes a number and never executes a transformation directly (see §10, `Architecture.md` §7, `features/Dataset-Contracts-And-Planning.md` §7).

## 7. Target Users

- **ML Engineers** who need a fast, trustworthy first pass on a new dataset, from whichever surface fits their current workflow.
- **Data Scientists** doing iterative feature engineering for modeling, often from a notebook via the SDK.
- **Data Engineers** validating pipeline outputs and catching schema drift, often via CLI in CI.
- **MLOps Engineers** who need reproducible, testable preprocessing artifacts, not notebook-only logic.
- **Open Source Contributors** who want a well-scoped, well-documented codebase to build a career-visible portfolio on — including contributing new AI providers, not just rules and connectors.

## 8. User Personas

**Priya, Senior ML Engineer (primary)**
Joins a new project, is handed a 40-column CSV. Wants: leakage/quality flags in minutes, a defensible narrative for a design doc, and pipeline code she doesn't have to rewrite by hand. Uses the CLI in CI and the SDK in notebooks interchangeably, expecting identical results.

**Marcus, Data Scientist at a mid-size startup**
Iterates on features daily from a Jupyter notebook. Wants: `import featuresmith as fs`, a couple of lines to profile a dataframe already in memory (`fs.review(df)` — Current), and the ability to ask the AI chat "why did you flag this column?" without re-running anything (**[Future]**, v1.x).

**Elena, MLOps Engineer**
Owns the path from notebook to production. Wants: everything Featuresmith outputs to be a real, testable, versioned Python artifact — not throwaway notebook cells (**[Future]**, v0.4-v0.5 for export/apply) — and wants her org's OpenAI key used instead of the default local model, configured once, with zero code changes (**[Future]**, v1.x).

**Sam, Open Source Contributor**
Wants a plugin architecture with clear extension points (a new connector, a new rule, a new export target, or a new AI provider) and a codebase that doesn't require reading the whole repo to contribute meaningfully.

## 9. User Stories

Several stories below describe **[Future]** capability (AI chat, `fs.analyze()`, AI provider switching, AI-provider plugin authoring) — marked inline; these are the target experience once the AI layer and unified `analyze()` entrypoint ship, not v0.2.0 behavior today.

- As an ML engineer, I want to point the CLI at a CSV/Parquet/SQL table and get a structured quality report so I can decide if the data is modeling-ready. **(Current for CSV/Parquet via `featuresmith review`; SQL is [Future], v0.3.)**
- **[Future]** As a data scientist, I want to `import featuresmith` and call `fs.analyze(df)` directly on an in-memory dataframe, without shelling out to a CLI. (v0.2.0 today: `fs.review(df)` works on an in-memory dataframe already; `fs.analyze()` as a unifying name is the future target, `Architecture.md` §5.)
- **[Future]** As a data scientist, I want the tool to flag likely target leakage with an explanation, and then let me ask "why is this leakage?" in a follow-up chat message, so I don't ship a model that looks too good to be true. (Leakage flagging with explanation is Current, v0.2.0; the follow-up chat is v1.x.)
- **[Future]** As an MLOps engineer, I want to export accepted feature engineering steps as a versioned `sklearn.Pipeline` (or equivalent) with unit tests, so it's CI-testable. (v0.4-v0.5.)
- **[Future]** As an MLOps engineer, I want to switch the AI provider from local Ollama to our org's Anthropic key by changing one config value, with no code or CLI-flag changes required anywhere in our scripts. (v1.x.)
- **[Future]** As a contributor, I want to add a new "rule" (Current — rules are a real, static-registration extension point today) or a new AI provider (**[Future]**, v1.x) by implementing a small interface, without touching the core engine or any specific surface (CLI/dashboard/extension).
- As a data engineer, I want to diff two snapshots of the same dataset and get a plain-language summary of what changed (schema, distributions, missingness). **(Current — `fs.diff()`/`featuresmith diff`.)**
- **[Future]** As a product stakeholder, I want a narrative report I can read without knowing pandas, summarizing what the data says and where it's risky, and to be able to ask it a plain-language question if something is unclear. (The narrative/chat portions are v1.x; a structured, readable report already exists today via `featuresmith review`.)

## 10. Core Features

Ordered by where each capability sits in the lifecycle (`VISION.md` §2), not by release date. Status is tracked per-feature in each feature's own document and in `implementation/IMPLEMENTATION_STATUS.md` — this list is the product surface, not a delivery schedule (see `Phases.md` for sequencing). **Current (v0.2.0, shipped)** items are marked; everything else is **[Future]** design this PRD commits to building, not something a v0.2.0 install already does.

1. **Featuresmith Core**: a single, importable Python library (`import featuresmith as fs`) containing all business logic — profiling, rules, review, scoring, diffing shipped today; planning and export are **[Future]**. Every other interface is a thin wrapper over this library (`Architecture.md` §2).
2. **Current**: CSV, Excel, Parquet ingestion, plus in-memory Polars/pandas dataframes passed directly through the SDK. **[Future]**: SQL (via SQLAlchemy), planned v0.3 (`Architecture.md` §4, `implementation/IMPLEMENTATION_STATUS.md`).
3. **Current**: statistical profiling engine — univariate/bivariate stats, correlations, distributions, missingness patterns — deterministic, Polars-first.
4. **Current**: **Review Engine** — deterministic, rule-based reviewers (schema, quality, leakage; statistics reviewers **[Future]**, v0.3) orchestrated into one structured, prioritized `ReviewResult` (`features/Review-Engine-Architecture.md`) — the deterministic core every other capability below builds on.
5. **Current**: **ML Readiness Score** — a 0–100 composite score with a per-dimension breakdown, always shown with its underlying findings, never as a standalone number (`features/ML-Readiness-Score.md`).
6. **Current**: **Intelligent Leakage Detection** — named, inspectable leakage patterns (target correlation, identifier shape, timestamp anomalies, duplicate targets) rather than a single correlation threshold (`features/Dataset-Diff-And-Leakage-Detection.md`).
7. **Current**: **Dataset Diff** — compare two dataset snapshots — schema, distributions, missingness, quality — the way `git diff` compares two commits (`features/Dataset-Diff-And-Leakage-Detection.md`). Ships as a standalone engine (`fs.diff()`/`featuresmith diff`) AND integrated into the Review Engine as `DiffReviewer` since v0.3.0 (`Architecture.md` §21.4) — `fs.review(source, previous=...)` produces a diff section in the same review.
8. **[Future]** — v0.4: **Recommendation & Plan Engine** — rule findings and (later) AI-ranked suggestions merge into a single ranked, explainable list; each accepted item compiles into an inspectable, deterministic **Plan** before anything runs (`features/Dataset-Contracts-And-Planning.md` §7-8).
9. **[Future]** — v0.4-v0.5: **Export/Apply layer** — turns an accepted Plan into real, generated code for an ecosystem the user already runs — `sklearn.Pipeline`/`ColumnTransformer`, a Polars expression chain, a Jupyter notebook, or a dbt model stub — defaulting to code generation rather than execution, and never a Featuresmith-owned execution engine (`features/Dataset-Contracts-And-Planning.md` §7.2, §9).
10. **[Future]** — v0.5: **Dataset Contract (`featuresmith.lock`)** — the versioned, diffable artifact recording a dataset's schema fingerprint, readiness score, leakage state, and transformation lineage — committed to git, diffed in PRs, gated in CI (`features/Dataset-Contracts-And-Planning.md` §5-6).
11. **[Future]** — v1.x: **AI Provider Interface** *(thin, optional layer — see `Design-Principles.md` "AI assists, never replaces")* — a pluggable abstraction (Ollama default/local, OpenAI and Anthropic as opt-in, bring-your-own-key) supplying plain-language narration of findings, ranking rationale, and translation of natural-language instructions into an inspectable Plan. Provider switching is designed to be config-only, never a code change (`Architecture.md` §7).
12. **Current, in part**: two of a planned four equivalent interfaces exist today — the Python SDK and the CLI (`featuresmith review data.csv`), all calling the same core with no duplicated logic. The Streamlit dashboard (**[Future]**, v0.3) and a future VS Code extension (**[Future]**, v2.0+) are planned additions on the same model (`Architecture.md` §2, §13-14).
13. **Current**: **CI/CD gating** — deterministic exit codes and machine-readable JSON output, so `featuresmith review` sits in CI next to a project's other gates from day one. A contract-diff check is **[Future]**, v0.5+.
14. **Current, in part; [Future] for most categories**: config-driven, plugin-based architecture spanning connectors and rules today (static registration, `Architecture.md` §25.1); reviewers, exporters, and AI providers are **[Future]** categories, each earning external plugin discovery independently on demonstrated demand.

## 11. Nice-to-Have Features (later phases)

**Candidate examples, evidence-driven — not a commitment.** Everything below sits in Phase 8/v2.0+'s candidate pool (`Phases.md`); which of these actually get built, and when, is decided by real demand, adoption, contributor interest, ecosystem relevance, feasibility, maintenance cost, and core-lifecycle fit at the time — not by appearing on this list. See `Phases.md` Phase 8 for the full prioritization criteria.

- A "Featuresmith-verified" certification badge and portable artifact referencing a specific Dataset Contract, for READMEs, dataset cards, and model-registry metadata (`features/Dataset-Contracts-And-Planning.md` §11) — this one is scoped to v0.6, not v2.0+ (`Phases.md`).
- VS Code / Jupyter extension for inline findings and inline chat.
- Data warehouse & cloud storage connectors (Snowflake, BigQuery, S3, GCS).
- Deeper ecosystem exporters — a Feast feature-definition exporter, a dbt model exporter, an MLflow/Weights & Biases run-metadata attachment for a Dataset Contract's fingerprint (`Architecture.md` §20).
- Team dashboard with shareable, versioned reports and shared chat threads per dataset.
- Automated feature synthesis integration (Featuretools) as an optional heavy-compute plugin.
- Additional AI providers (Azure OpenAI, Google Gemini, self-hosted vLLM endpoints) contributed via the provider plugin interface.

## 12. Success Metrics

- **Time-to-insight**: median time from `featuresmith.analyze(...)` (any surface) to a reviewed report < 2 minutes for datasets under 1M rows.
- **Surface parity**: zero reported bugs where CLI, SDK, and dashboard produce different findings for the same dataset — tracked as a release-blocking bug class, not a normal priority-3 issue.
- **Adoption**: GitHub stars, PyPI weekly downloads, and — more importantly — issue/PR velocity from external contributors (a health signal, not a vanity one).
- **Trust**: % of AI-recommended features accepted by users, and chat-question resolution rate (opt-in anonymous telemetry) as proxies for recommendation and explanation quality.
- **Correctness**: leakage-detection precision/recall against a curated benchmark suite of known-leaky public datasets.
- **Contributor retention**: % of first-time contributors who open a second PR within 90 days.

## 13. Risks

| Risk | Mitigation |
|---|---|
| LLM hallucinates numbers not backed by computed stats | Strict grounding: LLM (both narration and chat) only ever receives a structured JSON fact-object; never allowed to compute or invent numbers itself |
| Interactive AI Chat re-reads raw data on every question, leaking data or degrading performance | Chat is architecturally scoped to the precomputed `ProfileResult` + `RuleFinding[]` context only — no raw-dataframe tool access by default |
| Users blindly trust "AI recommendations" in production | Every recommendation ships with a confidence score, rationale, and requires explicit accept; nothing auto-applies silently |
| Scope creep into "AutoML platform" | Non-goals enforced in PRD and PR review checklist |
| Performance collapse on large datasets | Polars-first compute layer (DuckDB planned), sampling strategy for AI layer, explicit size-tiered code paths |
| Business logic duplicated across CLI/dashboard/extension, causing drift | Architectural rule: only `featuresmith-core` may contain business logic; enforced via import-linter contracts and the "surface parity" success metric above |
| Plugin architecture (rules, connectors, exporters, AI providers) becomes a maintenance burden | Small, versioned, stable interface contracts; core team owns the interfaces, not every plugin |
| PII/security exposure when sending data context to a cloud AI provider | Local-first LLM (Ollama) default; cloud LLM opt-in only, with schema/stat-only payloads (and chat context), never raw rows, by default |

## 14. Future Vision

A long-term ecosystem where: connectors, rules, reviewers, exporters, and AI providers are largely community-maintained; a hosted SaaS/dashboard tier funds core maintenance; and a `featuresmith.lock` file sits next to `pyproject.toml`/`package-lock.json` in every serious ML repo — diffed in every PR that touches training data, referenced from dataset cards and model-registry metadata, and gated in CI the same unremarkable way a type-check gate is today. Success looks like a team being able to answer "what changed in this data, and is it safe" in one command instead of an afternoon, and a "Featuresmith-verified" badge being as legible a trust signal on a dataset card as a green CI badge is on a repo. See `features/Dataset-Contracts-And-Planning.md` §12 for the concrete shape of that artifact and `Architecture.md` §20 for how it plugs into the wider ecosystem (MLflow, Weights & Biases, Hugging Face dataset cards) without Featuresmith owning any of them.

## 15. Open Source Strategy

- License: **Apache 2.0** (patent grant matters for enterprise adoption; more permissive than GPL for a tool meant to be embedded in other pipelines).
- Governance: BDFL-lite for v1 (single maintainer/small core team), moving to a documented RFC + core-team-vote model once the contributor base passes ~15 active contributors.
- Public roadmap (GitHub Projects) and a [`GOVERNANCE.md`](../GOVERNANCE.md) published no later than v0.3 (published with v0.3).
- "Good first issue" pipeline maintained deliberately — see `Rules.md` and `Phases.md`.

## 16. Contributor Experience

- One-command dev setup (`make dev` / `uv sync`) — see `Rules.md`.
- Every module has its own README with a "how to add a new X" guide (new rule, new connector, new exporter, new AI provider).
- CI must pass in under 5 minutes for the core test suite to keep contributor feedback loops fast.
- Clear `CONTRIBUTING.md` with issue labels, PR template, and a Discord/GitHub Discussions channel.

## 17. Competitive Differentiation

The category Featuresmith is building, and why it's evaluated against git/Terraform/dbt/Ruff rather than other profiling tools, is set out in `VISION.md` §2. At the product level, that translates into a concrete claim: Featuresmith's differentiation is the **closed loop, delivered identically from any surface, ending in a persisted artifact** — statistically grounded finding → ranked, explainable recommendation → an inspectable Plan → an applied transformation via the ecosystem the user already runs → re-review and diff → a versioned Dataset Contract — whether invoked as `fs.review(df)` in a notebook, `featuresmith review data.csv` in CI, or through the dashboard. No existing open-source tool spans that entire loop today. Secondary differentiators: leakage detection as a first-class citizen (not an afterthought), a plugin architecture designed for community contributions across rules, reviewers, exporters, *and* AI providers, and an apply layer that generates real, CI-testable code in ecosystems teams already trust rather than a proprietary transformation runtime.
