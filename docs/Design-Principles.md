# Design Principles

These are the principles that decide what Featuresmith builds and how, across every phase of `Phases.md`. When a design decision is ambiguous, these principles — alongside `Rules.md` — are what should settle it, for contributors and maintainers alike.

## Developer-first

Every capability ships as something a developer can call, script, or pipe — first as a Python import, then a CLI command — before it becomes a UI. A feature that only exists behind a dashboard click isn't finished (`Architecture.md` §2).

## Engineering over dashboards

Featuresmith is shaped like `ruff`, `pytest`, or `pre-commit` — a check that runs, ideally automatically in CI — not a report that gets opened once and forgotten. The dashboard and chat exist to serve the moments a plain CLI check isn't enough, never to replace the check itself.

## AI assists, never replaces

The deterministic engine — profiling, rules, quality scoring, feature engineering, export — works completely with the AI layer switched off. AI narrates, ranks, and answers questions about facts that engine already computed; it never computes a number itself, and it's never a hard dependency for a core capability (`Architecture.md` §7.2, §7.4).

## Local-first, cloud-optional

Full value with zero network calls: local files, a local model (Ollama by default). Cloud LLMs and cloud connectors are opt-in, switched entirely through configuration — never a code change, never a requirement.

## Composable by default

Connectors, rules, exporters, and AI providers are all plugins behind small, stable interfaces. The core should never need to know about a specific data source, output format, or LLM vendor, and a contributor should be able to add one of these without touching core engine code (`Architecture.md` §16).

## Evidence before recommendations

Every recommendation — rule-based or AI-enhanced — shows the underlying finding before any narrative or suggested action. Nothing is ever narrative-only, and nothing auto-applies without an explicit accept.

## Trust over hype

We ship what exists and label what doesn't. Every roadmap phase in `Phases.md` is marked with its status, and this documentation is written to be checked against the actual code, not the other way around. A feature described as available should be available; a feature described as roadmap should say so in the same sentence.
