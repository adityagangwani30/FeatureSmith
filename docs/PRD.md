# PRD — Featuresmith

> The Developer Toolkit for Trustworthy Structured Data — built around a single reusable Python core.

## 1. Vision

Software engineering has spent decades building discipline into the development loop — tests, linters, formatters, CI gates that catch problems before they reach production. Datasets have never gotten the same treatment, and the cost of that gap is paid quietly, in models trained on leakage or drift nobody caught. Featuresmith's mission is to **make data quality as routine as code quality** — because every dataset deserves a code review, run automatically, the way tests and linters run before every merge. See `Project_Plan.md` §0 for the full philosophy.

Every ML project starts the same way: a raw dataset and a blank notebook. Engineers spend 60-80% of project time on EDA, cleaning, and feature engineering — most of it repetitive, undocumented, and re-invented per project. Featuresmith's vision is to become **the engineering layer between raw datasets and trustworthy machine learning** — a tool that doesn't just compute statistics, but *understands* the dataset, explains what it means, answers follow-up questions about it, and produces reviewable, production-grade code to act on that understanding.

The end state: an engineer connects a dataset — from a Python script, the CLI, a dashboard, or an IDE — gets a structured report of what's wrong and what's promising, asks follow-up questions in natural language, and exports a versioned, testable preprocessing pipeline — not a wall of disconnected charts.

Critically, this experience must be **identical in substance no matter which surface it's accessed from**, because all surfaces are thin clients over one Python core. See `Architecture.md` §2 for the core-first architecture this PRD assumes throughout.

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
- Detect data-quality issues (missingness patterns, drift, skew, cardinality problems, target leakage, duplicate/near-duplicate rows, outliers) with explanations, not just flags.
- Generate natural-language narrative summaries of a dataset that a non-specialist stakeholder could read.
- Let users ask follow-up questions about the analysis in natural language (Interactive AI Chat), grounded entirely in the already-computed profile — never a fresh, ungrounded pass over the raw data.
- Recommend concrete feature engineering actions, each with a rationale and confidence.
- Generate production-ready, versioned preprocessing code (sklearn-compatible pipelines) and notebooks from the recommendations a user accepts.
- Ship one Python core library that every interface — SDK, CLI, dashboard, IDE extension — calls identically, with zero duplicated business logic (`Architecture.md` §2).
- Be modular and pluggable enough to sustain a large open-source contributor base for 5+ years, across both the analysis engine and the AI provider layer.

## 6. Non-Goals (v1–v2)

- Not a full AutoML system — it recommends and prepares features; it does not select/tune models.
- Not a data warehouse or storage product — it connects to existing sources, it doesn't replace them.
- Not a real-time streaming analytics tool in early phases.
- Not a replacement for domain expertise — recommendations are advisory, always reviewable/rejectable, never silently auto-applied in production paths.
- Not initially multi-modal (image/text/audio) — tabular-first, with NLP-column support as a stretch goal.
- The AI Chat is not a general-purpose data-analysis chatbot with live dataframe access — it answers questions grounded in the precomputed profile only (see §10 and `Architecture.md` §7).

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
Iterates on features daily from a Jupyter notebook. Wants: `import featuresmith as fs`, a couple of lines to profile a dataframe already in memory, and the ability to ask the AI chat "why did you flag this column?" without re-running anything.

**Elena, MLOps Engineer**
Owns the path from notebook to production. Wants: everything Featuresmith outputs to be a real, testable, versioned Python artifact — not throwaway notebook cells — and wants her org's OpenAI key used instead of the default local model, configured once, with zero code changes.

**Sam, Open Source Contributor**
Wants a plugin architecture with clear extension points (a new connector, a new rule, a new export target, or a new AI provider) and a codebase that doesn't require reading the whole repo to contribute meaningfully.

## 9. User Stories

- As an ML engineer, I want to point the CLI at a CSV/Parquet/SQL table and get a structured quality report so I can decide if the data is modeling-ready.
- As a data scientist, I want to `import featuresmith` and call `fs.analyze(df)` directly on an in-memory dataframe, without shelling out to a CLI.
- As a data scientist, I want the tool to flag likely target leakage with an explanation, and then let me ask "why is this leakage?" in a follow-up chat message, so I don't ship a model that looks too good to be true.
- As an MLOps engineer, I want to export accepted feature engineering steps as a versioned `sklearn.Pipeline` (or equivalent) with unit tests, so it's CI-testable.
- As an MLOps engineer, I want to switch the AI provider from local Ollama to our org's Anthropic key by changing one config value, with no code or CLI-flag changes required anywhere in our scripts.
- As a contributor, I want to add a new "rule" (e.g., a new leakage heuristic) or a new AI provider by implementing a small interface, without touching the core engine or any specific surface (CLI/dashboard/extension).
- As a data engineer, I want to diff two snapshots of the same dataset and get a plain-language summary of what changed (schema, distributions, missingness).
- As a product stakeholder, I want a narrative report I can read without knowing pandas, summarizing what the data says and where it's risky, and to be able to ask it a plain-language question if something is unclear.

## 10. Core Features (v1 scope)

1. **Featuresmith Core**: a single, importable Python library (`import featuresmith as fs`) containing all business logic — profiling, rules, feature engineering, AI reasoning, export. Every other interface is a thin wrapper over this library (`Architecture.md` §2).
2. Multi-format ingestion: CSV, Excel, Parquet, SQL (via SQLAlchemy), plus in-memory Polars/pandas dataframes passed directly through the SDK.
3. Statistical EDA engine: univariate/bivariate stats, correlations, distributions, missingness patterns.
4. Rule-based data quality engine: leakage heuristics, cardinality issues, duplicate/near-duplicate detection, outlier detection, type-mismatch detection.
5. **AI Provider Interface**: a pluggable abstraction (Ollama default/local, OpenAI and Anthropic as opt-in, bring-your-own-key) that supplies two capabilities — narration/ranking of precomputed findings, and the Interactive AI Chat below. Provider switching is config-only, never a code change (`Architecture.md` §7).
6. AI narrative layer: LLM-generated plain-language summary grounded in the computed statistics (never hallucinated numbers — the LLM narrates facts the rule engine already computed).
7. **Interactive AI Chat**: after analysis, users can ask natural-language follow-up questions ("Why is this feature leakage?", "Explain this chart", "What encoding should I use?", "Explain this to a beginner", "Generate sklearn preprocessing for this column", "Compare these two columns") — all answered from the already-computed profile object, never by re-reading the raw dataset.
8. Feature engineering recommendation engine: ranked, explainable suggestions (encoding strategy, binning, interaction candidates, scaling needs).
9. Pipeline/code export: generates a runnable sklearn-compatible `Pipeline`/`ColumnTransformer` plus a Jupyter notebook.
10. **Four equivalent interfaces**, all calling the same core with no duplicated logic: the Python SDK, the CLI (`featuresmith analyze data.csv`), the Streamlit dashboard (`featuresmith dashboard`), and a future VS Code extension (`Architecture.md` §2, §13-14).
11. Config-driven, plugin-based architecture from day one (even if only 2-3 plugins ship in v1), spanning connectors, rules, exporters, *and* AI providers.

## 11. Nice-to-Have Features (v2+)

- Dataset diffing/drift detection across snapshots.
- VS Code / Jupyter extension for inline recommendations and inline AI chat (Phase 7).
- Data warehouse & cloud storage connectors (Snowflake, BigQuery, S3, GCS).
- Multi-framework export (PySpark, Polars-native pipelines, Feature Store schemas — Feast).
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

A long-term ecosystem where: connectors, rules, exporters, and AI providers are largely community-maintained; a hosted SaaS/dashboard tier funds core maintenance; Featuresmith reports and chat transcripts become a standard artifact attached to model cards and PRs, the way `README.md` is standard today.

## 15. Open Source Strategy

- License: **Apache 2.0** (patent grant matters for enterprise adoption; more permissive than GPL for a tool meant to be embedded in other pipelines).
- Governance: BDFL-lite for v1 (single maintainer/small core team), moving to a documented RFC + core-team-vote model once the contributor base passes ~15 active contributors.
- Public roadmap (GitHub Projects) and a `GOVERNANCE.md` published no later than v0.3.
- "Good first issue" pipeline maintained deliberately — see `Rules.md` and `Phases.md`.

## 16. Contributor Experience

- One-command dev setup (`make dev` / `uv sync`) — see `Rules.md`.
- Every module has its own README with a "how to add a new X" guide (new rule, new connector, new exporter, new AI provider).
- CI must pass in under 5 minutes for the core test suite to keep contributor feedback loops fast.
- Clear `CONTRIBUTING.md` with issue labels, PR template, and a Discord/GitHub Discussions channel.

## 17. Competitive Differentiation

Featuresmith is not a "prettier ydata-profiling." Its differentiation is the **closed loop, delivered identically from any surface**: statistically grounded finding → natural-language explanation → conversational follow-up → ranked, explainable recommendation → reviewable, production-grade code artifact — whether invoked as `fs.analyze(df)` in a notebook, `featuresmith analyze data.csv` in CI, or through the dashboard. No existing open-source tool spans that entire loop today, and none offer a conversational, grounded chat over an already-computed profile. Secondary differentiators: leakage detection as a first-class citizen (not an afterthought), a plugin architecture designed for community contributions across rules *and* AI providers, and pipeline export that produces CI-testable code rather than notebook-only output.
