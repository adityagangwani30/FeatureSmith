# Rules.md — The Development Bible (Featuresmith)

Every contributor, including AI coding assistants, must follow this document. When in doubt, this file wins over personal preference.

## 1. Coding Standards

- Python 3.11+ only. Type hints are **mandatory** on all public functions; `mypy --strict` runs in CI.
- Formatting: `ruff format` (Black-compatible) — no manual formatting debates, no config bikeshedding.
- Linting: `ruff check` with a shared `pyproject.toml` config; no per-module overrides without a documented reason in the PR.
- Docstrings: Google-style, required on every public class/function. Private (`_prefixed`) helpers are exempt but encouraged.
- No bare `except:` — always catch specific exceptions; custom exceptions live in `featuresmith.core.exceptions`.
- Prefer composition over inheritance except for the explicit `Base*`/`AIProvider` extension-point classes defined in `Architecture.md`.

## 2. Naming Conventions

- Modules: `snake_case`. Classes: `PascalCase`. Functions/vars: `snake_case`. Constants: `UPPER_SNAKE_CASE`.
- Every `Base*` interface subclass is named `<Thing><Category>`, e.g. `CsvConnector`, `LeakageRuleTargetCorrelation`, `OpenAIProvider` — no ambiguous names like `Helper` or `Utils2`.
- Rule IDs are stable, namespaced strings (`quality.missingness.high_null_ratio`), never renamed once released — treat them like a public API.
- AI provider IDs follow the same rule: `ollama`, `openai`, `anthropic` are stable config values (`ai.provider: <id>`) — never renamed once released.
- Package names follow the pattern `featuresmith-<surface>` for anything outside core (`featuresmith-cli`, `featuresmith-dashboard`, `featuresmith-vscode`); the core library is published as `featuresmith-core` (and imported as `featuresmith`).

## 3. Folder Rules

- Never add a new top-level package under `packages/` without an ADR (see §11) — new interfaces should happen *inside* `featuresmith-core`'s existing extension points, and new surfaces are rare, deliberate additions.
- **No business logic (profiling, rules, feature engineering, AI calls, export generation) may live outside `packages/featuresmith-core`.** `featuresmith-cli`, `featuresmith-dashboard`, and `featuresmith-vscode` may only import `featuresmith.api` — a linter rule (`import-linter`) enforces this boundary in CI on every PR touching a surface package.
- Test files mirror source structure 1:1: `packages/featuresmith-core/src/featuresmith/rules/quality/missingness.py` → `packages/featuresmith-core/tests/rules/quality/test_missingness.py`.
- No file should exceed ~400 lines; split by responsibility, not by convenience.

## 4. Documentation Rules — Documentation-First Development (Mandatory)

The `docs/` folder is the project's source of truth, not the codebase. Any contributor — human or AI coding assistant — should be able to understand the entire project's philosophy, architecture, roadmap, design decisions, and in-flight work by reading the documentation alone, without reading code.

This means a strict Documentation-First workflow for all work on Featuresmith, no exceptions:

1. **Define** the idea or feature.
2. **Update the relevant documentation** — explain the motivation, describe the user experience, explain how it fits the architecture, update the roadmap in `Phases.md` if it changes, and update any other affected page (`PRD.md`, `Architecture.md`, `Design.md`, `Flagship-Capabilities.md`, CLI/SDK references, etc.).
3. **Review and refine the design** in the documentation itself, before any implementation exists to anchor the discussion.
4. **Only then begin implementation.**

Nothing should be implemented unless it already exists in the documentation first. If a new idea arises mid-development, the same sequence applies retroactively: stop, document, review, then resume implementation.

Whenever code changes in a way that affects behavior — a feature, module, CLI command, API, architecture decision, or workflow — the documentation update ships **in the same change**, never a follow-up. Documentation and implementation are never allowed to diverge; this is the concrete workflow enforcement of the "docs updated in the same PR" rule below and the Code Review Checklist (§17).

- Every module directory has a `README.md` explaining its purpose and, if it's an extension point, a "how to add a new X" walkthrough — this now explicitly includes `featuresmith/ai/providers/README.md` ("how to add a new AI provider").
- Every public-facing behavior change requires a corresponding docs update in the same PR — docs and code are never allowed to drift, enforced via a CI checklist item.
- Mermaid diagrams preferred over prose for anything describing flow/sequence.

## 5. Testing Rules

- Minimum 85% coverage on `core/`, `rules/`, `feature_engine/` (the deterministic, trust-critical layers). The AI layer (narration, ranking, chat) is tested via a mocked `AIProvider` implementation, not live LLM calls, in CI.
- Every rule ships with at least one fixture dataset that triggers it and one that doesn't (positive + negative case) — prevents false-positive drift over time.
- Every `AIProvider` implementation ships a conformance test suite run against the shared `AIProvider` protocol (narrate/rank/chat) using a mocked HTTP layer, so a community-contributed provider can prove correctness without needing a real API key in CI.
- `ChatSession` tests assert, structurally, that no code path in `featuresmith.ai.chat` has access to the raw `Dataset`/dataframe object — only `ProfileResult`/`RuleFinding[]` — enforced as an explicit unit test, not just a design intent.
- Golden-file tests for exporters: generated pipeline code is diffed against a checked-in expected output; intentional changes require updating the golden file in the same PR with justification.
- **Surface parity tests**: a dedicated integration suite runs the same fixture dataset through the SDK, the CLI, and the dashboard's underlying calls, asserting identical `ProfileResult` output — this is the automated enforcement of `PRD.md` §12's "surface parity" success metric.
- No PR merges with failing or skipped tests without an explicit, reviewed `# TODO(issue-link)` justification.

## 6. PR Guidelines

- One logical change per PR. A new rule + a refactor of the registry = two PRs.
- PR description must state: what changed, why, how it was tested, and which section of `PRD.md`/`Architecture.md` it relates to (if applicable).
- Draft PRs welcome for early feedback; mark ready-for-review only once CI is green.
- All PRs require at least one core-team approval before merge; two for changes to `featuresmith-core`'s `core/`, any `Base*` interface, or the `AIProvider` protocol (interface changes ripple to every plugin and every surface).

## 7. Git Branch Strategy

- `main` is always releasable.
- Feature branches: `feat/<short-desc>`, fixes: `fix/<short-desc>`, docs: `docs/<short-desc>`.
- No direct commits to `main`; squash-merge only, to keep history readable.

## 8. Commit Convention

Conventional Commits, enforced via a commit-lint CI check, scoped by package where relevant:
```
feat(rules): add near-duplicate row detection
feat(ai): add Anthropic provider implementation
fix(cli): correct exit code on chat session error
docs(architecture): clarify AI provider plugin discovery
```
Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`. Breaking changes flagged with `!` (`feat(core)!: ...`) and a `BREAKING CHANGE:` footer.

## 9. Versioning Strategy

- Semantic Versioning (`MAJOR.MINOR.PATCH`), applied **independently per release package** (`featuresmith-core`, `featuresmith-cli`, and future public surfaces). A CLI patch release must not force a core version bump and vice versa, though surface packages always declare a minimum compatible `featuresmith-core` version.
- `Base*`/`AIProvider` interface changes are MINOR at most pre-1.0, MAJOR post-1.0.
- Rule IDs, AI provider IDs, config schema keys, and CLI command names are part of the public API surface — changing them requires a deprecation cycle (warn for one MINOR release before removal).

## 10. Architecture Rules

- No module imports "up" the pipeline (see `Architecture.md` §5) — enforced via an `import-linter` CI check with explicit contract definitions.
- **No surface package (`featuresmith-cli`, `featuresmith-dashboard`, `featuresmith-vscode`) may import anything from `featuresmith-core` except `featuresmith.api`.** This is the structural enforcement of the "one core, many thin surfaces" principle and is checked by the same `import-linter` contract as the point above.
- The AI layer must never compute a statistic — it only narrates/ranks/answers questions using pre-computed, typed data. Any PR that has the AI provider producing a raw number instead of narrating one, or that gives `ChatSession` access to the raw dataframe, must be rejected in review.
- Every extension point (`connectors`, `rules`, `exporters`, `ai_providers`) must remain independently unit-testable without a live LLM or network call.

## 11. Dependency Rules

- New third-party dependencies require an **Architecture Decision Record** (ADR) in `docs/adr/`, even a short one — justify why, alternatives considered, and whether it's core or optional (`extras`).
- Heavy/optional deps (Featuretools, cloud SDKs, specific DB drivers, individual AI provider SDKs like `openai`/`anthropic`) go under `pyproject.toml` extras (`pip install featuresmith-core[openai]`, `pip install featuresmith-core[sql]`), never core dependencies. `featuresmith-core` with no extras must remain installable and fully functional (via Ollama + local rules) with zero cloud SDK dependencies.
- Pin direct dependencies with compatible-release specifiers (`~=`); avoid unpinned ranges that can silently break CI.

## 12. Performance Rules

- No rule or profiler function may load a full dataset into memory without checking the size-tier logic (`Architecture.md` §17) first.
- Any function operating on more than one column pairwise (e.g., correlation matrices, interaction candidates) must have a documented complexity bound and a config-driven cap to prevent combinatorial blowup on wide datasets.
- `ChatSession` responses must not trigger a re-profile of the dataset under any circumstance — a performance regression test asserts a bounded, small number of calls into `profiling/` per analysis, independent of how many chat messages follow.
- Benchmarks for `profiling/` and `rules/` run in CI on fixture datasets of 10K/1M/10M rows; a PR that regresses benchmark time by >20% requires justification.

## 13. Security Rules

- Never log or include raw data values in error messages, telemetry, or AI provider requests (narration, ranking, *or chat*) sent to a cloud provider by default — only schema, aggregate stats, and column names, per the grounding contract in `Architecture.md` §7.2.
- API keys for OpenAI/Anthropic are read from environment variables referenced by name in `.featuresmith.yml` (`api_key_env: OPENAI_API_KEY`) — never written directly into config files, never logged, never included in generated reports or exported notebooks.
- SQL connectors use parameterized queries exclusively; no string-interpolated SQL, ever.
- Dependency vulnerabilities scanned via `pip-audit` in CI on every PR touching any `pyproject.toml` in the workspace.

## 14. Privacy Rules

- Cloud AI provider usage is opt-in and requires an explicit config value (`ai.provider: openai`) — default is local (Ollama) or no-AI template mode.
- Telemetry (if enabled) is opt-in, anonymized, aggregate-only (e.g., "rule X fired," "chat used," never column names, values, or chat message content), and documented in a public `TELEMETRY.md`.
- Any connector reading from PII-likely sources should support column-level redaction/exclusion config before any profiling, AI narration, or chat step runs.

## 15. Logging Rules

- Structured logging (`structlog` or equivalent) — no bare `print()` in library code, ever (CLI output is a separate, deliberate presentation layer).
- Log levels: `DEBUG` for internal flow, `INFO` for user-relevant milestones ("profiled 42 columns", "chat session started"), `WARNING` for degraded-but-continuing states (e.g., "AI provider unreachable, using template narrator, chat disabled"), `ERROR` for failures.

## 16. Error Handling Rules

- User-facing errors must be actionable — never a raw stack trace as the only output in the CLI; wrap with a clear message and, where possible, a suggested fix (e.g., "AI provider 'openai' failed: missing OPENAI_API_KEY — set it or switch `ai.provider` to `ollama` in .featuresmith.yml").
- Library-level exceptions are typed and documented (`ConnectorError`, `RuleExecutionError`, `ExportError`, `AIProviderError`, `ChatSessionError`) so calling code can handle them specifically.
- A single failing rule, plugin, or AI provider call must never crash the whole analysis run — failures are isolated, logged, and surfaced as a partial-result warning; a failed AI narration still returns the full deterministic report.

## 17. Code Review Checklist

- [ ] Type hints complete; `mypy --strict` passes
- [ ] Tests added/updated, including a negative case for new rules and a conformance test for new AI providers
- [ ] Docs updated in the same PR
- [ ] No new hard dependency without an ADR
- [ ] No raw data in logs/prompts/chat context
- [ ] No surface package imports anything beyond `featuresmith.api`
- [ ] Follows naming conventions and folder rules
- [ ] Conventional Commit messages

## 18. Contributor Guidelines

- Start with issues labeled `good-first-issue` (see `Phases.md` for how these are seeded per phase).
- One-command setup: `make dev` (creates venv, installs all workspace packages + pre-commit hooks, runs a smoke test across SDK, CLI, and dashboard entrypoints).
- `CONTRIBUTING.md` links directly to the relevant extension-point README (`connectors/README.md`, `rules/README.md`, `exporters/README.md`, `ai/providers/README.md`) so new contributors don't need to read the whole architecture doc to make a first contribution.

## 19. Release Process

1. All PRs targeted for a release merged to `main`.
2. `CHANGELOG.md` auto-generated per package from Conventional Commits (`release-please` or equivalent, configured for the monorepo).
3. Version bump PR reviewed by core team, respecting per-package independent versioning (§9).
4. Tag → GitHub Release → PyPI publish via GitHub Actions (trusted publishing, no long-lived tokens) for each changed package.
5. Docs site (MkDocs) redeployed automatically on tag push.

## 20. Definition of Done

A feature is "done" when: code is merged to `main`, tests cover the happy path and at least one failure mode, docs are updated, it's included in the next release's `CHANGELOG.md`, it's exercised identically from at least the SDK and CLI (dashboard where applicable) per the surface-parity rule, and — for user-facing features — a CLI/dashboard example exists in `examples/`.

## 21. Anti-Patterns to Avoid

- Adding model-selection/training logic (scope creep into AutoML — explicitly a non-goal).
- Letting the AI layer touch raw data or compute statistics directly, in narration, ranking, **or chat**.
- Giving `ChatSession` a raw-dataframe tool/re-profiling capability "for convenience."
- Silent auto-application of any recommendation without explicit user acceptance.
- Implementing a feature in `featuresmith-cli` or `featuresmith-dashboard` first and "promoting it to core later" — logic is written in core from the start, even for a single-surface feature.
- God-objects: a `Dataset` class that grows connector-specific or rule-specific methods over time — extension belongs in plugins, not the core class.
- Breaking a `Base*`/`AIProvider` interface without a deprecation cycle.

## 22. Decision-Making Principles

When a design decision isn't covered by this document: prefer the option that (1) keeps the core package usable with zero network calls, (2) keeps an extension point testable in isolation, (3) keeps business logic inside `featuresmith-core` and out of any surface package, (4) is more boring/standard over more clever, and (5) can be explained in the PRD's "Why Existing Solutions Aren't Enough" framing — if it doesn't serve the closed-loop vision, it probably belongs in a plugin, not core.
