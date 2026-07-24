# Project Plan — Featuresmith
### An AI-Powered Feature Engineering & EDA Platform, built around one reusable Python core

This is the master reference document. It summarizes the full plan and links out to the detailed docs:

- [`PRD.md`](./PRD.md) — vision, problem, personas, goals/non-goals, success metrics
- [`Architecture.md`](./Architecture.md) — system design, modules, folder structure, plugin system
- [`Rules.md`](./Rules.md) — the development bible: standards, testing, PR/release process
- [`Phases.md`](./Phases.md) — roadmap from MVP to v5.0 with issues/milestones/labels
- [`Design.md`](./Design.md) — product design system, UI principles, tokens

---

## 1. Naming

The project is named **Featuresmith** — a craftsmanship metaphor (forging raw data into usable features) that's pronounceable, memorable, and scales cleanly into a company/brand name later. Package name: `featuresmith` (core), with thin surface packages `featuresmith-cli`, `featuresmith-dashboard`, and — from Phase 7 — `featuresmith-vscode`. Config file: `.featuresmith.yml`. Import: `import featuresmith as fs`. CLI binary: `featuresmith`.

## 2. One-Paragraph Summary

Featuresmith is not another EDA report generator. It's a closed loop, delivered from a single reusable Python core: it computes rigorous statistics deterministically, detects data-quality and leakage issues with a rule engine, uses a pluggable AI provider strictly as a *narrator, ranker, and conversational partner* (never a calculator) to explain findings in plain language, answer follow-up questions, and prioritize recommendations, and — critically — exports accepted recommendations as real, tested, production-grade code (sklearn pipelines, notebooks). Every one of these capabilities is exposed identically whether accessed as a Python import, a CLI command, a Streamlit dashboard, or (from Phase 7) a VS Code extension — because all four are thin clients over exactly one core library. See `PRD.md` §4 and §17 for the full competitive analysis.

## 3. System at a Glance

```mermaid
flowchart TB
    subgraph Surfaces["Four Equivalent Interfaces"]
        SDK["Python SDK\nimport featuresmith as fs"]
        CLI["CLI\nfeaturesmith analyze train.csv"]
        DASH["Streamlit Dashboard\nfeaturesmith dashboard"]
        VSC["VS Code Extension\n(future, Phase 7)"]
    end

    subgraph Core["Featuresmith Core (Python Library)"]
        direction TB
        PROF[Profiling Engine]
        RULES[Rule Engine]
        FEENG[Feature Engine]
        AI[AI Layer + Chat]
        EXPORT[Export Engine]
    end

    subgraph Providers["AI Providers (pluggable, config-only switch)"]
        OLLAMA["Ollama\n(default, local)"]
        OPENAI["OpenAI\n(BYO key)"]
        ANTH["Anthropic\n(BYO key)"]
    end

    CLI --> SDK
    DASH --> SDK
    VSC --> SDK
    SDK --> Core
    AI --> Providers
```

Full detail in `Architecture.md` §2. The core architectural commitment: **all business logic lives only inside `featuresmith-core`; every interface is a thin wrapper calling the same SDK — no duplicated logic, no duplicated APIs.**

## 4. Four Ways to Use Featuresmith

| Interface | Example | When to reach for it |
|---|---|---|
| **1. Python Library** | `import featuresmith as fs`<br>`profile = fs.analyze(df)` | Notebooks, scripts, programmatic pipelines — the foundation every other surface builds on |
| **2. CLI** | `featuresmith analyze train.csv` | CI gating, quick terminal checks, scripting outside Python |
| **3. Streamlit Dashboard** | `featuresmith dashboard` | Interactive review, stakeholder walkthroughs, the AI chat panel |
| **4. VS Code Extension** *(future, Phase 7)* | Inline findings + chat on file open | In-editor review without context-switching |

All four call `featuresmith.api` and return the same typed results for the same input — this "surface parity" is a tested, CI-enforced property, not a design aspiration (`Rules.md` §5, `PRD.md` §12).

## 5. AI Architecture at a Glance

```mermaid
flowchart TB
    ENGINE["Deterministic Engine\n(stats, rules, correlations,\nquality + leakage findings)"] -->|"structured JSON profile only\n— never the raw dataframe"| AI["AI Provider Interface"]
    AI --> OLLAMA[Ollama — default/local]
    AI --> OPENAI[OpenAI — BYO key]
    AI --> ANTHROPIC[Anthropic — BYO key]
    AI --> FUTURE[Future providers — plugin]
    AI --> CHAT["Interactive AI Chat"]
```

The deterministic engine computes everything numeric; the AI layer only ever receives that precomputed, structured profile and is responsible solely for explanations, ranking, and conversational answers — never computation. Provider selection is entirely config-driven (`ai.provider: ollama|openai|anthropic` in `.featuresmith.yml`); no code changes are ever required to switch. Full detail, including the `AIProvider` protocol and grounding contract, in `Architecture.md` §7.

**Interactive AI Chat** (new capability): after any analysis, users can ask questions like "Why is this feature leakage?", "Explain this chart", "What encoding should I use?", "Explain this to a beginner", "Generate sklearn preprocessing", or "Compare two columns" — all answered from the already-computed profile, never by re-reading the dataset. Available identically from the SDK, CLI, and dashboard (`Architecture.md` §7.3).

## 6. Roadmap Overview

| Phase | Version | Focus |
|---|---|---|
| 0 | pre-release | Foundations — core library first |
| 1 | v0.1 | SDK + CLI MVP: EDA + rule engine |
| 2 | v0.3 | AI provider layer + narration |
| 3 | v0.4 | Interactive AI Chat |
| 4 | v0.5 | Export layer (sklearn/notebook/HTML) |
| 5 | v1.0 | Streamlit dashboard + multi-source connectors |
| 6 | v2.0 | Plugin ecosystem (rules, connectors, exporters, AI providers) + dataset diffing |
| 7 | v3.0 | VS Code extension + Feast export |
| 8 | v4.0 | Distributed scale + data warehouse tier |
| 9 | v5.0 | Optional hosted/cloud tier |

Full detail, acceptance criteria, and suggested GitHub issues per phase in `Phases.md`. Note the roadmap ordering change from earlier planning: the SDK/CLI now ship *before* AI narration, and the AI Chat is its own dedicated phase between narration and export — sequencing that reflects "core capability before AI enhancement before surface polish."

## 7. Tech Stack — Recommendations & Reasoning

| Area | Recommendation | Reasoning |
|---|---|---|
| Core language | Python 3.11+ | Ecosystem fit for ML audience; non-negotiable for adoption |
| DataFrame engine | **Polars (primary), Pandas (compat shim only)** | Polars' lazy execution and multi-threaded performance matter directly for the "size-tiered scalability" requirement in `Architecture.md` §17; pandas is kept only as an interop layer since much of the ecosystem (sklearn, some connectors) still expects it |
| Large-data query engine | **DuckDB** | Zero-infra SQL/analytical engine, exceptional for out-of-core aggregation and works beautifully as a pushdown layer for the SQL/warehouse connectors |
| Columnar interchange | **Apache Arrow** | Zero-copy interop between Polars, DuckDB, and Parquet — avoids redundant serialization at every layer boundary |
| Monorepo/workspace tooling | **uv workspaces** | Manages `featuresmith-core`, `featuresmith-cli`, `featuresmith-dashboard` as independently versioned packages sharing one lockfile-driven dev environment — directly supports the hard package-boundary requirement in `Architecture.md` §4 |
| API layer (future hosted tier) | **FastAPI** | Type-hint-driven, async-native, pairs naturally with Pydantic schemas already used internally; becomes just another thin surface over `featuresmith.api` |
| Dashboard (v1) | **Streamlit**, not Next.js | Fastest path to a Python-native, plugin-author-friendly interactive UI during early, fast-iterating phases (`Architecture.md` §14); a Next.js rewrite is explicitly deferred, not rejected — revisit once the product surface stabilizes (Phase 6+) |
| Charting | **Plotly/Altair (Vega-Lite specs)** | Declarative chart specs render consistently across CLI, dashboard, and static HTML report (`Architecture.md` §11) |
| Validation/schema | **Pydantic v2** | Already the contract layer for every internal stage boundary; validates config (`.featuresmith.yml`) too |
| Modeling utilities | **Scikit-learn** | Lowest-common-denominator export target; nearly every downstream framework can consume a sklearn-compatible pipeline |
| Feature engineering libs | **Feature-engine used selectively; Featuretools deferred** | Feature-engine's sklearn-compatible transformers integrate cleanly with the export layer today; Featuretools' automated deep feature synthesis is heavier and better suited as an optional plugin once the core recommendation loop is proven |
| Data validation | **Pandera now; Great Expectations later as an export target** | Pandera is lightweight and Pydantic-adjacent, a natural fit for validating generated pipeline outputs in tests; Great Expectations is heavier but valuable as a future *export format* for teams already standardized on it |
| Experiment/artifact tracking | **MLflow, optional integration only** | Not core — Featuresmith produces artifacts, it doesn't need to own experiment tracking |
| **AI provider abstraction** | **Custom lightweight `AIProvider` protocol (3 methods: narrate, rank, chat)** | A full agent framework (LangChain, LlamaIndex) would pull in far more surface area than three narrowly-scoped methods need, and would make the "AI never touches raw data" grounding guarantee harder to audit; a small, hand-rolled protocol keeps the contract auditable and keeps provider plugins trivially simple to write |
| Local LLM runner | **Ollama** (default) | Simplest, most widely adopted way to run local models with a stable HTTP API — no GPU-management complexity pushed onto the user; ships as the zero-config default experience |
| Cloud LLM providers | **OpenAI, Anthropic** (opt-in, BYO key) | The two most widely adopted hosted APIs; both added as optional `pyproject.toml` extras (`featuresmith[openai]`, `featuresmith[anthropic]`) so the core install stays dependency-light |
| Containerization | **Docker**, multi-stage build | Standard for reproducible dev environments and eventual hosted-tier deployment |
| CI/CD | **GitHub Actions** | Free for OSS, tight PyPI trusted-publishing integration; workflow matrix runs per-package (core/cli/dashboard) given the monorepo structure |
| Package distribution | **PyPI, trusted publishing (OIDC)**, independently per package | No long-lived API tokens to leak; independent versioning supports the "thin surface, stable core" principle (`Rules.md` §9) |
| Docs site | **MkDocs (Material theme), not Docusaurus** | Python-native tooling keeps the docs build in the same language as the project, lowering the barrier for contributors to fix docs |
| IDE integration | **VS Code extension (TypeScript, thin client) + Jupyter extension** | Deferred to Phase 7 — a thin client over the existing CLI/SDK rather than a reimplementation, per `Phases.md` Phase 7 |

### What to avoid early

- **Don't** build a custom plugin-discovery mechanism — Python entry_points already solve this for rules, connectors, exporters, *and* AI providers (`Architecture.md` §6).
- **Don't** adopt a heavyweight agent framework for the AI layer — the grounding guarantee (AI never computes, never sees raw data) is easiest to audit with a minimal, hand-rolled `AIProvider` protocol.
- **Don't** adopt Featuretools or Great Expectations as hard dependencies before v0.5 — both are excellent but heavy; make them optional extras.
- **Don't** start the Next.js dashboard in parallel with Streamlit — maintaining two UIs during early rapid iteration splits focus for no early benefit.
- **Don't** let the CLI or dashboard implement *any* logic beyond argument parsing and rendering — every capability, including the AI chat, is written once in `featuresmith-core` and only ever called, never duplicated (`Rules.md` §10, §21).

## 8. Product Thinking — Challenging the Plan Further

**What changed and why it's an improvement, not just a rename:**

- **Collapsing "CLI-first" into "core-first" is the single biggest architectural upgrade in this revision.** The previous plan treated the CLI as the primary interface with a dashboard bolted on later; that ordering quietly encourages logic to accrete in the CLI layer. Making the SDK the actual product — with CLI, dashboard, and (later) VS Code extension as equally thin, equally disposable clients — is what makes "no duplicated logic" enforceable rather than aspirational, and it's what makes a future hosted API tier (Phase 9) nearly free to add later.
- **Promoting AI providers to a first-class, symmetric plugin category** (alongside connectors/rules/exporters) rather than a single hardcoded LLM integration removes a real adoption blocker: teams with existing OpenAI or Anthropic contracts, or strict data-residency requirements favoring local Ollama, can now adopt Featuresmith without a fork.
- **Adding Interactive AI Chat as its own phase (Phase 3), before export (Phase 4)**, reflects that conversational drill-down is often *more* valuable early than code generation — users need to trust and understand findings before they're ready to accept and export them. Sequencing chat before export also means "generate sklearn preprocessing" as a chat capability and `fs.export()` as a direct call are built to share one code path from day one, rather than chat getting a second, divergent implementation bolted on later.
- **A monorepo of independently-versioned packages**, rather than one flat package, was not explicitly asked for but follows directly from "no duplicated logic, no duplicated APIs" taken seriously — it's the difference between a principle stated in prose and a boundary a linter enforces on every PR (`Rules.md` §10).

### Guardrails carried forward unchanged

The core trust boundary from the original plan — the AI layer never computes a statistic, only narrates and ranks precomputed, structured data — is not just preserved but *extended* to the new chat feature explicitly, since a conversational interface is the most tempting place for that boundary to quietly erode ("just let it peek at the dataframe to answer this one question better"). `Architecture.md` §7.2 and `Rules.md` §5/§21 make this an explicitly tested, reviewed boundary, not just a stated intention.

## 9. Contributor Onboarding Path (Summary)

```mermaid
flowchart LR
    A[Read CONTRIBUTING.md] --> B[make dev]
    B --> C[Pick a good-first-issue]
    C --> D{Which extension point?}
    D -->|New rule| E[rules/README.md]
    D -->|New connector| F[connectors/README.md]
    D -->|New exporter| G[exporters/README.md]
    D -->|New AI provider| H[ai/providers/README.md]
    E --> I[Open PR per Rules.md checklist]
    F --> I
    G --> I
    H --> I
```

Full contributor rules, PR checklist, and review process in `Rules.md` §17-20.

## 10. How to Use This Documentation Set

For a team (human or AI coding assistant) implementing this project: read `PRD.md` first for *why*, `Architecture.md` for *how it's structured* (especially §2 on the core-first architecture and §7 on the AI provider/chat design), `Rules.md` before writing any code for *how it must be written* (especially §3 and §10 on the core/surface package boundary), `Phases.md` for *what to build first*, and `Design.md` when touching any user-facing surface. This `Project_Plan.md` is the map — the other five files are the territory.
