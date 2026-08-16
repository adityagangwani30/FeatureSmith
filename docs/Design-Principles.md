# Design Principles

> These principles operationalize `VISION.md` — most directly §3 (what Featuresmith will not become). They're the day-to-day decision rules that follow from that vision, not a restatement of it.

These are the principles that decide what Featuresmith builds and how, across every phase of `Phases.md`. When a design decision is ambiguous, these principles — alongside `Rules.md` — are what should settle it, for contributors and maintainers alike.

## A coherent lifecycle toolkit, not a collection of utilities

Featuresmith must remain a coherent developer-first structured-data lifecycle toolkit: Review → Findings → Recommendations → Plan → Human Approval → Export/Generated Transformation → External Execution → Re-review → Diff → Contract/Lock. Every future capability must strengthen this core lifecycle rather than introduce an independent subsystem that merely happens to live in the same package. Feature engineering, AI assistance, ecosystem integrations, and scale infrastructure are all evaluated against this test — do they deepen the lifecycle above, or do they stand beside it as a separate value proposition — before they're treated as roadmap-committed rather than candidate work (`Architecture.md` §23.3's roadmap governance questions are the concrete mechanism; `Phases.md`'s Phase 3 A/B/C tiering is a worked example).

## Developer-first

Every capability ships as something a developer can call, script, or pipe — first as a Python import, then a CLI command — before it becomes a UI. A feature that only exists behind a dashboard click isn't finished (`Architecture.md` §2).

## The dashboard is a surface over Featuresmith's core, not the product itself

Featuresmith is shaped like `ruff`, `pytest`, or `pre-commit` — a check that runs, ideally automatically in CI — not a report that gets opened once and forgotten. The architectural hierarchy is Core (`Dataset → Review → Findings → Recommendations → Plan → Export → Re-review → Diff → Contract/Lock`) with Surfaces (SDK, CLI, CI/CD, Dashboard, future integrations) as equal-standing clients of it, not a ladder with the dashboard on top. Concretely: the deterministic core remains fully useful with no dashboard running at all; SDK and CLI workflows are first-class, never legacy fallbacks; no CI/CD or programmatic workflow may depend on the dashboard existing; the dashboard may add visualization, exploration, history, and trends that the CLI/SDK aren't suited to render, but never as the *only* place a capability lives; and the dashboard consumes and renders core objects (`ReviewResult`, `Plan`, `DatasetContract`) — it is never their source of truth. A future hosted/team tier must not force `featuresmith-core` itself into a hosted/backend architecture (§18) — full detail and rationale in `Architecture.md` §25.2.

## AI assists, never replaces

The deterministic engine — profiling, rules, quality scoring, leakage detection, diffing, planning, export — works completely with the AI layer switched off. AI narrates, ranks, and translates natural language into an inspectable plan grounded in facts that engine already computed; it never computes a number itself, never executes a transformation, and it's never a hard dependency for a core capability (`Architecture.md` §7.2, §7.4).

## Prove state, don't own execution

Featuresmith's differentiation is proof — that a dataset's state is understood, has been reviewed, and can be trusted — not execution. Every capability that touches a transformation (recommend, plan, export/apply) generates real, readable code for an ecosystem the user already runs (Polars, pandas, scikit-learn, dbt); none of them run inside a Featuresmith-owned runtime. Two separate gates enforce this, not one: nothing is ever proposed as a Plan step and turned into generated code without an explicit, human-reviewed accept step (`PRD.md` §6), and separately, the default output of the export/apply step is code to read and run yourself — not an in-place mutation of the user's dataset. Controlled execution exists only as a distinct, explicitly-opted-into convenience, never the default of a bare export/apply call (`features/Dataset-Contracts-And-Planning.md` §7.2). This is the boundary that keeps Featuresmith from drifting into orchestration, distributed execution, feature-store, or AutoML territory it has no structural advantage in.

## Local-first, cloud-optional

Full value with zero network calls: local files, a local model (Ollama by default). Cloud LLMs and cloud connectors are opt-in, switched entirely through configuration — never a code change, never a requirement.

## Composable by default

Connectors, rules, exporters, and AI providers are all designed as plugin-shaped: small, stable interfaces the core never needs to know the specifics of. The core should never need to know about a specific data source, output format, or LLM vendor, and a contributor should be able to add one of these without touching core engine code (`Architecture.md` §16). Whether a given category is externally discoverable yet (via `entry_points`) or still statically registered in-repo is a separate, incremental decision made per category, on demonstrated demand — not a prerequisite for the interface itself being composable (`Architecture.md` §25.1).

## Evidence before recommendations

Every recommendation — rule-based or AI-enhanced — shows the underlying finding before any narrative or suggested action. Nothing is ever narrative-only, and nothing auto-applies without an explicit accept.

## Trust over hype

We ship what exists and label what doesn't. Every roadmap phase in `Phases.md` is marked with its status, and this documentation is written to be checked against the actual code, not the other way around. A feature described as available should be available; a feature described as roadmap should say so in the same sentence.

## Simple by default, complex only when earned

Featuresmith must stay simple to understand, extend, and maintain as capabilities grow — this is as permanent a constraint as any non-goal in `VISION.md` §3, not a code-quality aspiration. Concretely:

1. Prefer a simple, concrete solution over a speculative abstraction built for a feature that doesn't exist yet. Do not create infrastructure — engines, registries, managers, providers, orchestration layers, frameworks — for a hypothetical future requirement; build it when a demonstrated need exists (`Architecture.md` §23.3).
2. A new abstraction (factory, registry, provider, adapter, interface, service layer, config system) must solve a real, current problem — never "might need this later." Even `Architecture.md` §6/§16's plugin categories, `entry_points` registry, and `Base*` interfaces are not a blanket exception to this: the *interface shape* (a `Base*` protocol) is reused and justified today, but *external discoverability* for any given category is introduced incrementally, per category, only once that category has demonstrated external demand (`Architecture.md` §25.1) — not built out for all categories at once because the pattern exists for one.
3. Reuse the existing architecture before creating a new subsystem — a new top-level module requires the same bar Phase 4-5's Plan/Export/Contract design met: it's a thin new layer around existing engines (Review, Recommendation, Export, Diff), never a parallel implementation (`Architecture.md` §20.1).
4. Prefer composition over inheritance, small cohesive modules, and explicit typed data flow between stages (`Architecture.md` §5) over a clever generalized one. Prefer boring, readable Python over clever architecture — cleverness that requires explanation is a cost, not a virtue.
5. The public API (`fs.analyze`, `fs.review`, `fs.chat`, `fs.export`, `fs.diff`, and their future `fs.plan`/`fs.lock`/export-or-apply siblings — exact naming for the export/apply step is still an open, implementation-time decision, `features/Dataset-Contracts-And-Planning.md` §10) stays small and understandable even as internal implementation evolves — internal complexity is never an excuse to grow the public surface.
6. Every significant new abstraction should be able to answer, in the PR description: what concrete problem does this solve, why is the existing architecture insufficient, why is it needed now (not speculatively), what complexity does it add, and what complexity does it remove.
7. Complexity is fully acceptable when it clearly enables a real, shipping product capability — the goal is never fewer files or fewer lines for their own sake, only that every module, interface, and layer earns its place. Complexity is a finite budget (`Architecture.md` §24): every addition spends part of it, and the spend must be justified by user value, not merely be technically possible. See `Architecture.md` §21-25 for how this principle is applied to Featuresmith's actual v0.2.0 architecture and enforced going forward.
