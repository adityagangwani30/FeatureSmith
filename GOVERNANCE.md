# Governance

This document describes how Featuresmith is owned, decided, and released as an open-source project. It is deliberately proportional to the project's current size: lightweight rules now, with a documented path to a more formal model as the contributor base grows. See `docs/PRD.md` §15 for the product-level strategy this document operationalizes.

## 1. Ownership

Featuresmith is licensed under **Apache 2.0** (`LICENSE`). There is no corporate entity behind the project as of this writing; ownership of the codebase lives with the maintainer and the contributor community that maintains it.

For day-to-day maintenance, Featuresmith uses a **BDFL-lite** model: a single maintainer (or small core team) holds final say on decisions, but actively seeks input and delegates routine maintenance widely.

- The maintainer(s) are listed in `CODEOWNERS` and reflected in the GitHub "people" settings.
- Routine work (triaging issues, reviewing PRs, merging `good-first-issue` work, tending release notes) is delegated to any trusted contributor who wants it.
- Big, irreversible, or high-blast-radius decisions go through the significant-change process in §4.

## 2. Contribution and decision-making

- Anyone may open an issue, submit a PR, or start a discussion. Contributions are governed by `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.
- **Every merge happens through a PR with review**, per the branch-protection rules in `.github/github_repository.md`. No direct pushes to `main`.
- PRs touching `featuresmith-core` core/`api.py` require two approving reviews (`.github/github_repository.md` §7); everything else requires one.
- **Disagreements** are resolved by discussion first, then by the maintainer's decision. Decisions that are controversial, precedent-setting, or high-blast-radius are recorded (see §4) so the reasoning survives the people involved.
- **Scale trigger:** once the project has roughly **15 active contributors**, the BDFL-lite model is replaced by a documented **RFC + core-team-vote** model (per `docs/PRD.md` §15). Until then, the maintainer's call is the decision of record.

## 3. Significant changes

The following always go through the architecture-review process before being built, rather than landing reactively in a PR:

- New top-level modules or engines (e.g., a plan/export layer, a scheduler, a hosted tier).
- Changes to public API or documented schemas (see `docs/Rules.md` §9 for the versioning discipline).
- New flagship capabilities or changes to existing ones (`docs/Flagship-Capabilities.md`).
- Any change that would remove or weaken an existing architectural guarantee (e.g., "AI never touches raw data," "no silent execution").

Process: a design document is added under `docs/` (following `docs/Rules.md` §4's docs-before-code rule), the maintainer(s) review it against the roadmap governance questions in `docs/Architecture.md` §23, and the decision (adopt / revise / reject) is recorded. The v0.2.0 architecture review (`docs/Architecture.md` §21-25) is the standing template for how this works.

## 4. Release and versioning responsibility

- The maintainer(s) are responsible for release scheduling and for the decision to tag and publish a version.
- Each package is versioned independently and released through the process in `docs/Rules.md` §19 (Conventional Commits → changelog → version-bump PR → tag → trusted PyPI publish).
- **Breaking changes** follow `docs/Rules.md` §9: they are announced, versioned as a major (or minor with a documented deprecation cycle for the relevant package), and never landed silently. A breaking change to a public API requires a documented rationale and a migration path.
- `CHANGELOG.md` and release notes are the record of what changed and why.

## 5. Roadmap and prioritization

- The roadmap is public (`docs/Phases.md`) and tracked via GitHub Projects.
- Prioritization is **evidence-driven**, not order-of-appearance-driven: user feedback, GitHub issues/discussions, contributor demand, integration requirements, and demonstrated technical need gate what actually ships (`docs/Phases.md` Phase 3's A/B/C tiering is the standing example).
- Nothing is committed to a release simply by appearing on the roadmap; the maintainer makes the final scoping call each cycle, validated against real feedback.

## 6. Community expectations

- All community interaction — issues, PRs, discussions, and the badge/tag of "Featuresmith" — is governed by `CODE_OF_CONDUCT.md`.
- Contributors follow `CONTRIBUTING.md`: good-first-issue labels, one-command setup, and the docs-before-code rule.
- Security reports go through `SECURITY.md`.
- Maintainer behavior: decisions are explainable and recorded, contributions are acknowledged, and the "good first issue" pipeline is maintained deliberately so new contributors always have an on-ramp.

---

Nothing in this document is set in stone; like the codebase, it is meant to be revised when the project's reality requires it. Substantive changes to governance itself go through the significant-change process in §3.
