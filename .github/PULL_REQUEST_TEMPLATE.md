## Summary

<!-- What does this PR do? One or two sentences. -->

## Motivation

<!-- Why is this change needed? Link to an issue if applicable: Closes #XX -->

## Related

<!-- Section of PRD.md / Architecture.md this change relates to (if applicable). -->
<!-- Example: Implements PRD.md §10 Feature #4 (Rule-based data quality engine) -->

---

## Changes

<!-- List the key changes in this PR. Group by package if touching multiple. -->

### `featuresmith-core` / `featuresmith-cli` / other:

- 

---

## Testing

<!-- Describe how you tested this change. -->

- [ ] Ran `uv run pytest` — all tests pass
- [ ] Ran `uv run ruff check .` — no lint errors
- [ ] Ran `uv run mypy .` — no type errors
- [ ] Ran `uv run lint-imports` — import boundary intact
- [ ] Added tests for new behavior (positive + negative case for new rules)
- [ ] Manual verification: <!-- describe what you ran and what you observed -->

---

## PR Checklist

- [ ] Type hints complete on all public functions
- [ ] Google-style docstrings on all public classes/functions
- [ ] No business logic added outside `featuresmith-core`
- [ ] No surface package imports anything beyond `featuresmith.api`
- [ ] Docs updated in this PR (if behavior changed)
- [ ] No new dependency without an ADR in `docs/adr/`
- [ ] Conventional Commit messages used
- [ ] No file exceeds ~400 lines (split if needed)
- [ ] `CHANGELOG.md` entry added (if user-facing change)

---

## For New Rules

*(Delete this section if not applicable)*

- [ ] Rule has a stable, namespaced `id` (e.g. `quality.my_new_rule`)
- [ ] Rule registered in `featuresmith.rules.registry.default_registry()`
- [ ] Positive fixture test (triggers the rule) added
- [ ] Negative fixture test (does not trigger) added
- [ ] Rule documented in `packages/featuresmith-core/src/featuresmith/rules/README.md`

---

## For New Connectors

*(Delete this section if not applicable)*

- [ ] Connector registered in `featuresmith.connectors.registry`
- [ ] Tests include fixture files (CSV/Excel/Parquet as appropriate)
- [ ] `can_handle()` tested with both matching and non-matching inputs
- [ ] ADR added in `docs/adr/` if new dependency introduced
