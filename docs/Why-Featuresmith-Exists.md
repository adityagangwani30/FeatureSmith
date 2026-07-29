# Why Featuresmith Exists

## The problem: engineering discipline stops at the dataset's edge

Every serious codebase today has Git, pull requests, tests, CI/CD, linters, formatters, and static analysis. None of that is controversial anymore — it's just how software gets built. Datasets, which are just as load-bearing for an ML system as the code around them, get almost none of it. A column can go 40% missing, a categorical can silently leak the target, a distribution can drift out from under a model in production — and nothing stops it the way a failing test stops a bad commit, because nothing is running.

The tooling that does exist is fragmented by design, not by accident: one tool profiles, another validates, another detects drift, another documents, another engineers features, another monitors quality in production. Each is usually good at its one job. None of them talk to each other, so developers spend real time stitching together a workflow instead of using one — re-running disconnected tools by hand, copying findings between them, and losing whatever context existed in tool A by the time they're in tool B.

## Our answer: one toolkit, one loop

Featuresmith's premise is that this doesn't need to be five tools. **Understanding, validating, and improving a dataset is one continuous engineering workflow**, and it should be served by one extensible toolkit with one core, not a pile of point solutions:

- **Understand** — profile a dataset's shape, distributions, and relationships.
- **Validate** — catch data-quality and leakage issues with deterministic, testable rules.
- **Improve** — turn accepted findings into real, reviewable code (today: sklearn pipelines and notebooks).

Everything Featuresmith adds beyond this loop — AI narration and chat, drift detection, plugins, monitoring — is in service of making that same loop richer, never a separate product bolted on next to it. See `Architecture.md` §2 for how "one core, many thin surfaces" makes this a structural guarantee rather than a marketing claim: the CLI, the SDK, the dashboard, and the future editor integration all call the exact same engine, so there is only ever one workflow to learn.

## Why this has to be a developer tool, not a dashboard

Tools that developers actually adopt long-term look like `ruff`, `pytest`, or `pre-commit` — something you run, ideally automatically, not something you remember to open. Tools that don't get adopted look like reports: generated once, read once, forgotten. Featuresmith is built to be the former. `featuresmith analyze data.csv` is designed to sit in CI next to your other gates from day one (`Architecture.md` §13), and every other surface — the dashboard, the chat, the exported pipeline — exists to serve the moments a plain CLI check isn't enough, not to replace the check itself.

## Why AI is an assistant here, not the identity

An LLM is a good fit for exactly one part of this loop: turning a structured finding into a plain-language explanation, a ranked recommendation, or an answer to a follow-up question. It is a poor fit for computing the finding itself, so Featuresmith never lets it try — the AI layer only ever receives a precomputed, structured profile, never the raw dataset, and the deterministic engine produces a full report with the AI layer switched off entirely (`Architecture.md` §7.2, §7.4). AI makes the loop easier to use; it isn't what the loop is for.

## Where this goes

Today, that loop is profiling and rule-based validation, shipped as a Python SDK and CLI. The roadmap (`Phases.md`) grows it in the same direction: schema evolution and drift detection, deeper CI/CD integration, a plugin ecosystem for rules and connectors and exporters, feature intelligence (leakage detection, preprocessing recommendations), and continuous observability — dataset health tracked over time, not just per run. None of that is available yet, and this documentation says so plainly wherever it comes up (`Phases.md` marks every unreleased phase explicitly). See `Flagship-Capabilities.md` for the long-term, defining experiences — Dataset Review, ML Readiness Score, Dataset Diff, Intelligent Leakage Detection — that all of this is ultimately building toward. What's consistent from v0.1 through the last phase on the roadmap is the mission: **make data quality as routine as code quality**, one engineering-grade check at a time.
