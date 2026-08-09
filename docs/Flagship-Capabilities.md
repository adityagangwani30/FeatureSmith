# Flagship Capabilities — Future Vision

> **Capabilities 1-4 below are shipped, as of v0.2.0** — `featuresmith review`, the ML Readiness Score, `featuresmith diff`, and Intelligent Leakage Detection all exist today; see `features/Review-Engine-Architecture.md`, `features/ML-Readiness-Score.md`, and `features/Dataset-Diff-And-Leakage-Detection.md` for their exact implementation status. **Capability 5 does not exist yet** — see `features/Dataset-Contracts-And-Planning.md` for its design. Current, shipped functionality generally is described in `PRD.md` §10 and `Phases.md`; where a capability below is still partial or future, this page says so explicitly.

The rest of this documentation describes Featuresmith phase by phase: what ships, in what order, and why. This page answers a different question — **what is Featuresmith ultimately trying to become?** These five experiences are the concrete, product-level form of the North Star in `VISION.md` §4, and every phase in `Phases.md` is, in one way or another, building toward them. They exist to give contributors a destination, not just a backlog.

---

## 1. Dataset Review — `featuresmith review <dataset>`

**Shipped.** One command that performs a comprehensive engineering review of a dataset — not a pile of disconnected charts, but the same kind of thorough, structured pass a senior engineer would give a pull request. Running it is already as natural as running a test suite before a merge.

A review draws together: missing values, duplicates, schema issues, outliers, target leakage, class imbalance, feature quality (partial), an overall data-quality score, and (from Phase 4 onward) recommended preprocessing — ending in actionable suggestions, not just observations. See `features/Dataset-Review-PRD.md` for the full spec and `implementation/IMPLEMENTATION_STATUS.md` for exactly which sections are live today.

**This is the idea we want people to remember Featuresmith by: every dataset deserves a code review.** Code review didn't happen because code was assumed untrustworthy — it happened because catching problems before they ship is cheaper than catching them after. Datasets deserve that same discipline, run automatically, every time, before they touch a model. It's also, deliberately, just the *first* discipline software engineering has that Featuresmith is bringing to data — see Capability 5 for the next one.

## 2. ML Readiness Score

**Shipped.** A single, legible number — `ML Readiness: 91/100` — that answers the question "is this dataset ready for machine learning?" at a glance, backed by 8 component dimensions a developer can drill into: schema health, missing values, feature quality, distribution health, class balance, leakage risk, data quality, and consistency.

This is never shown as a standalone number a team could rally around without understanding what's behind it — every score ships with its underlying findings (`features/ML-Readiness-Score.md`, "Evidence before recommendations" in `Design-Principles.md`). It is also, unmodified, the score a Dataset Contract locks in and the signal Apply's validation step checks for improvement (`features/Dataset-Contracts-And-Planning.md` §7.3).

## 3. Dataset Diff — `featuresmith diff train_v1.parquet train_v2.parquet`

**Shipped.** Compare two versions of a dataset the way you'd diff two versions of code, surfacing added/removed columns, schema changes, distribution shifts, new missing values, changed categories, and quality regressions — so a team can see, before retraining, exactly what changed and whether that change is safe.

`fs.diff()` and `featuresmith diff` ship today (`features/Dataset-Diff-And-Leakage-Detection.md`) as a standalone engine, with schema, structure, quality, distribution, and leakage comparison. This same primitive is reused, unmodified, twice in Capability 5: to validate that an applied transformation improved a dataset, and to diff two `featuresmith.lock` files.

## 4. Intelligent Leakage Detection

**Shipped.** Goes beyond correlation-threshold rules to recognize the *shapes* target leakage tends to take — label-derived columns, features that encode information only available after the prediction point, identifier leakage, duplicate target information, and suspicious correlation patterns a simple threshold would miss or over-flag.

Featuresmith treats leakage as a first-class rule category, not an afterthought — 6 named pattern detectors ship today (`features/Dataset-Diff-And-Leakage-Detection.md`). AI-assisted pattern recognition (Phase 7) will sit on top of this deterministic set later, never replacing it — every flagged column still traces back to a concrete, inspectable reason. Target leakage is one of the most common and most expensive mistakes in applied ML, precisely because it's invisible until a model looks too good to be true; this is the capability most directly responsible for preventing that.

## 5. Dataset Contracts & the Plan/Apply Lifecycle

**Not yet built — design complete.** The evolution the first four capabilities exist to set up. A review that finds a problem should end somewhere better than a report: an inspectable **Plan** for fixing it, an **Apply** step that generates real code for the ecosystem the user already runs (never a Featuresmith-owned runtime), an automatic re-review that proves the fix worked, and a versioned **Dataset Contract** (`featuresmith.lock`) that persists the result — committed to git, diffed in a pull request, gated in CI, and referenceable later by a teammate, a dataset card, or a training run's metadata.

**Retraining without a contract is like deploying without a lockfile.** A dependency lockfile doesn't reimplement `pip`; it pins what actually got resolved so a build is reproducible. `featuresmith.lock` does the same for dataset state: it doesn't reimplement pandas or scikit-learn, it pins what a dataset's reviewed, transformed state actually was, so a team can answer "what exactly was this dataset, and is it safe to build on" without re-deriving the answer from scratch. Full design in `features/Dataset-Contracts-And-Planning.md`; roadmap placement in `Phases.md` Phases 4-6.

---

## Why this page exists

A roadmap tells you what ships next. It doesn't always tell you what all of it adds up to. These five experiences are that "adds up to" — the concrete, buildable form of the North Star in `VISION.md` §4, translated into things a contributor can actually pick up and build. If a future feature doesn't move Featuresmith closer to one of these, it's worth asking why it's being built at all.
