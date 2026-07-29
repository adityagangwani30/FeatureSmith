# Flagship Capabilities — Future Vision

> **None of the capabilities on this page exist today.** Current, shipped functionality is described in `PRD.md` §10 and `Phases.md`; this page is intentionally forward-looking. Everything here is roadmap-adjacent — where individual pieces already have a home in `Phases.md`, this page says so — but nothing here should be read as available now.

The rest of this documentation describes Featuresmith phase by phase: what ships, in what order, and why. This page answers a different question — **what is Featuresmith ultimately trying to become?** These four experiences are the long-term, defining answer to that question, and every phase in `Phases.md` is, in one way or another, building toward them. They exist to give contributors a destination, not just a backlog.

Every one of them serves the same mission: **make data quality as routine as code quality.**

---

## 1. Dataset Review — `featuresmith review <dataset>`

**The idea:** one command that performs a comprehensive engineering review of a dataset — not a pile of disconnected charts, but the same kind of thorough, structured pass a senior engineer would give a pull request. Long-term, running it should feel as natural as running a test suite before a merge.

A review would draw together: missing values, duplicates, schema issues, outliers, target leakage, class imbalance, feature quality, an overall data-quality score, and recommended preprocessing — ending in actionable suggestions, not just observations. In practice, this is the capstone experience that the deterministic engine (Phase 1), diffing (Phase 2), feature intelligence (Phase 4), and the AI assistant (Phase 6) are all, eventually, in service of; `featuresmith review` is what it looks like when those pieces are used together instead of one at a time.

**This is the idea we want people to remember Featuresmith by: every dataset deserves a code review.** Code review didn't happen because code was assumed untrustworthy — it happened because catching problems before they ship is cheaper than catching them after. Datasets deserve that same discipline, run automatically, every time, before they touch a model.

## 2. ML Readiness Score

**The idea:** a single, legible number — `ML Readiness: 91/100` — that answers the question "is this dataset ready for machine learning?" at a glance, backed by component scores a developer can drill into: data quality, schema health, feature quality, leakage risk, distribution health, missing values, and class balance.

This isn't a new idea invented from nothing — Phase 2's deterministic quality score is the seed of it, and this is what that score is meant to grow into: a composite, multi-dimensional view rather than a single scalar, always shown with the underlying findings it's built from (never as a standalone number a team could rally around without understanding what's behind it — see `Design-Principles.md`, "Evidence before recommendations").

## 3. Dataset Diff — `featuresmith diff train_v1.parquet train_v2.parquet`

**The idea:** compare two versions of a dataset the way you'd diff two versions of code, surfacing added/removed columns, schema changes, distribution shifts, new missing values, changed categories, and quality regressions — so a team can see, before retraining, exactly what changed and whether that change is safe.

The foundational version of this already has a home on the roadmap: Phase 2 (`Phases.md`) ships `fs.diff()` and `featuresmith diff` with schema and missingness comparison. The flagship version described here is that same capability matured — deeper distribution-shift analysis, and quality-regression detection wired into Phase 5's observability so a regression a diff would catch manually gets caught automatically on a schedule instead.

## 4. Intelligent Leakage Detection

**The idea:** go beyond correlation-threshold rules to recognize the *shapes* target leakage tends to take — label-derived columns, features that encode information only available after the prediction point, identifier leakage, duplicate target information, and suspicious correlation patterns a simple threshold would miss or over-flag.

Featuresmith already treats leakage as a first-class rule category, not an afterthought (Phase 1's naive correlation-based checks, `Architecture.md` §9's leakage heuristics). This flagship capability is that category's long-term ceiling: pattern recognition informed by the AI assistant layer (Phase 6) sitting on top of the deterministic rule engine, never replacing it — every flagged column still traces back to a concrete, inspectable reason, per the AI grounding contract in `Architecture.md` §7.2. Target leakage is one of the most common and most expensive mistakes in applied ML, precisely because it's invisible until a model looks too good to be true; this is the capability most directly responsible for preventing that.

---

## Why this page exists

A roadmap tells you what ships next. It doesn't always tell you what all of it adds up to. These four experiences are that "adds up to" — the north star that should shape phase priorities for years, not just quarters. If a future feature doesn't move Featuresmith closer to one of these, it's worth asking why it's being built at all.
