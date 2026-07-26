# Contributing to Featuresmith

Thank you for your interest in contributing! Featuresmith is built to be a genuinely contributor-friendly codebase — every extension point (rules, connectors, exporters, and AI providers) is designed so a first-time contributor can make a meaningful change without reading the entire codebase.

---

## Table of Contents

1. [Development Setup](#1-development-setup)
2. [Project Structure](#2-project-structure)
3. [Coding Standards](#3-coding-standards)
4. [Testing](#4-testing)
5. [Adding an Extension](#5-adding-an-extension)
6. [Pull Requests](#6-pull-requests)
7. [Commit Convention](#7-commit-convention)
8. [Code of Conduct](#8-code-of-conduct)

---

## 1. Development Setup

**Prerequisites:** Python 3.11+, [uv](https://docs.astral.sh/uv/)

```bash
# Clone the repository
git clone https://github.com/adityagangwani30/FeatureSmith.git
cd FeatureSmith

# Create the virtual environment and install all workspace packages
uv sync

# Install pre-commit hooks (runs ruff + mypy before every commit)
pre-commit install

# Verify your setup — all checks should pass
uv run ruff format .
uv run ruff check .
uv run mypy .
uv run lint-imports
uv run pytest
```

---

## 2. Project Structure

```
featuresmith/
├── packages/
│   ├── featuresmith-core/       # ALL business logic — rules, connectors, profiling
│   │   └── src/featuresmith/
│   │       ├── core/            # Shared data models: Dataset, ProfileResult, RuleFinding
│   │       ├── connectors/      # Data source connectors
│   │       ├── profiling/       # Profiling engine
│   │       ├── rules/           # Rule Engine + seed rules
│   │       └── api.py           # The only public entrypoint
│   ├── featuresmith-cli/        # Thin CLI wrapper (Typer) — imports api.py only
│   └── featuresmith-dashboard/  # Thin Streamlit wrapper — imports api.py only
├── tests/                       # Mirrors source structure 1:1
├── docs/                        # Architecture, PRD, Rules, Phases, Design
└── pyproject.toml               # uv workspace root
```

**The most important rule:** all business logic lives in `featuresmith-core`. The CLI and Dashboard may only import `featuresmith.api`. This boundary is enforced by `import-linter` on every PR. If you add logic to the CLI, the CI will fail.

---

## 3. Coding Standards

See [`docs/Rules.md`](./docs/Rules.md) for the full development bible. Key points:

- **Python 3.11+** only. Type hints are mandatory on all public functions.
- **Formatting:** `uv run ruff format .` — Black-compatible, no debates.
- **Linting:** `uv run ruff check .` — shared config in `pyproject.toml`, no per-module overrides.
- **Type checking:** `uv run mypy .` — `--strict` mode, zero ignored errors.
- **Docstrings:** Google-style, required on every public class and function.
- **No bare `except:`** — always catch specific exceptions.
- **No file over ~400 lines** — split by responsibility.

---

## 4. Testing

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run a specific module
uv run pytest tests/rules/

# Check coverage (85% minimum on core/, rules/, feature_engine/)
uv run pytest --cov=packages/featuresmith-core/src
```

**Testing requirements for new contributions:**

- Every new rule must include at least one positive fixture test (triggers the rule) and one negative test (does not trigger).
- New connectors must include tests with real fixture files.
- Tests mirror source structure 1:1: `src/featuresmith/rules/missing.py` → `tests/rules/test_missing.py`.
- Do not skip or ignore tests without a documented `# TODO(issue-link)` justification.

---

## 5. Adding an Extension

Featuresmith has four extension points. Each has its own README with a step-by-step walkthrough:

### New Rule

1. Read [`packages/featuresmith-core/src/featuresmith/rules/README.md`](./packages/featuresmith-core/src/featuresmith/rules/README.md)
2. Subclass `BaseRule` from `featuresmith.rules.base`
3. Implement `id`, `name`, `description`, `category`, `severity`, `enabled_by_default`, and `evaluate(profile)`
4. Register in `featuresmith.rules.registry.default_registry()`
5. Add tests with positive and negative fixtures
6. Open a PR

### New Connector

1. Read [`packages/featuresmith-core/src/featuresmith/connectors/README.md`](./packages/featuresmith-core/src/featuresmith/connectors/README.md)
2. Subclass `BaseConnector` from `featuresmith.connectors.base`
3. Implement `can_handle(source)` and `load(source) -> Dataset`
4. Register in `featuresmith.connectors.registry`
5. Add tests with fixture files

### New Exporter (Phase 4+)

See `featuresmith/exporters/README.md` (available from Phase 4).

### New AI Provider (Phase 2+)

See `featuresmith/ai/providers/README.md` (available from Phase 2).

---

## 6. Pull Requests

- **One logical change per PR.** A new rule + a registry refactor = two PRs.
- **Fill in the PR template** — describe what changed, why, how you tested it, and which section of `PRD.md`/`Architecture.md` it relates to.
- **Draft PRs are welcome** for early feedback. Mark ready-for-review only when CI is green.
- **All PRs require** at least one core-team approval. Changes to `Base*` interfaces or `featuresmith.api` require two approvals.
- **Branch naming:** `feat/<short-desc>`, `fix/<short-desc>`, `docs/<short-desc>`

**PR checklist (also in the PR template):**

- [ ] Type hints complete; `mypy --strict` passes
- [ ] Tests added/updated, including a negative case for new rules
- [ ] Docs updated in the same PR
- [ ] No new dependency without an ADR in `docs/adr/`
- [ ] No surface package imports anything beyond `featuresmith.api`
- [ ] Follows naming conventions and folder rules
- [ ] Conventional Commit messages

---

## 7. Commit Convention

Featuresmith uses [Conventional Commits](https://www.conventionalcommits.org/), scoped by package:

```
feat(rules): add near-duplicate row detection rule
fix(cli): correct exit code when target column is invalid
docs(architecture): clarify AI provider plugin discovery
test(profiling): add edge case for all-null numeric column
chore(deps): bump ruff to 0.12.1
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`

Breaking changes: `feat(core)!: rename ProfileResult.column_stats to column_profiles`

---

## 8. Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you agree to uphold it. Please report unacceptable behavior to the project maintainers.
