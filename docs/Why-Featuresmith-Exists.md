# Why Featuresmith Exists

> The full case for why Featuresmith exists, what category it's building, what it will never become, and its North Star now lives in `VISION.md` — read that first. This page exists for a narrower purpose: it answers a few practical "why did we design it *this* way" questions that follow from that vision but aren't among its four fixed questions.

## Why this has to be a developer tool, not a dashboard

Tools that developers actually adopt long-term look like `ruff`, `pytest`, `git`, or `pre-commit` — something you run, ideally automatically, not something you remember to open. Tools that don't get adopted look like reports: generated once, read once, forgotten. Featuresmith is built to be the former. `featuresmith review data.csv` is designed to sit in CI next to your other gates from day one (`Architecture.md` §13), and a `featuresmith.lock` committed to git is designed to be diffed in a pull request exactly the way a dependency-lockfile change is today — every other surface (the dashboard, the chat, the exported pipeline) exists to serve the moments a plain CLI check isn't enough, not to replace the check itself.

## Why AI is an assistant here, not the identity

An LLM is a good fit for exactly one part of Featuresmith's lifecycle (`VISION.md` §2): turning a structured finding into a plain-language explanation, a ranked recommendation, or a natural-language instruction into an inspectable plan. It is a poor fit for computing the finding itself and a poor fit for being trusted to execute a transformation unsupervised, so Featuresmith never lets it try either — the AI layer only ever receives a precomputed, structured profile, never the raw dataset, and never executes a plan directly; the deterministic engine produces a full report and a fully rule-based Plan with the AI layer switched off entirely (`Architecture.md` §7.2, §7.4, §20.3). AI makes the lifecycle easier to use; it isn't what the lifecycle is for.

## Where this goes

Today, the lifecycle in `VISION.md` §2 is review, scoring, leakage detection, and diffing — deterministic, shipped, and usable with zero AI involvement (v0.2.0). The roadmap (`Phases.md`) closes the rest of it in the same spirit: recommendation and planning, apply and validation, the Dataset Contract itself, certification and continuous observability, and only then an AI layer that narrates and assists rather than leads. None of the later phases are available yet, and this documentation says so plainly wherever it comes up (`Phases.md` marks every unreleased phase explicitly). See `Flagship-Capabilities.md` for the long-term, defining experiences — Dataset Review, ML Readiness Score, Dataset Diff, Intelligent Leakage Detection, and Dataset Contracts — that all of this is ultimately building toward.
