# Featuresmith v0.1.0 Release Audit Fixes

Refer to fixes.txt to get a better context about each fix

## Sprint 1 — Release Blockers
- [x] C1 - Fix package installation instructions
- [x] C2 - Unify version numbers
- [x] H5 - Security documentation / pip-audit
- [x] H6 - Remove incorrect DuckDB claims
- [x] H8 - Dashboard package release decision

---

## Sprint 2 — Core Engineering
- [x] H1 - Threshold ambiguity bug
- [x] H2 - Rule config validation
- [x] H3 - Cap frequency_table
- [x] H4 - Add py.typed
- [x] H7 - CI matrix
- [x] M1 - ConnectorError subclasses
- [x] M2 - Immutability improvements

---

## Sprint 3 — Polish & Repository Quality
- [x] M3 - Dataset generation deduplication
- [x] M4 - Test output cleanup
- [x] M5 - Test dependency cleanup
- [x] M6 - Benchmark documentation accuracy
- [x] M7 - Benchmark methodology
- [x] M8 - Rename/add real stress tests
- [x] M9 - Move github_repository.md
- [x] Frontend package rename
- [x] README polish
- [x] CODEOWNERS comment cleanup
- [x] MEMORY.md documentation positioning
- [x] Rich output cleanup
- [x] CHANGELOG formatting
- [x] Placeholder asset cleanup

---

## Final Validation

- [x] Ruff
- [x] MyPy
- [x] Pytest
- [x] Build packages
- [x] Build frontend
- [x] GitHub Actions passing

---

## RR-5 — Packaging & Distribution
- [x] Audited publishable package metadata for `featuresmith-core` and `featuresmith-cli`.
- [x] Confirmed `featuresmith-dashboard` remains internal-only for v0.1.0.
- [x] Added PyPI-ready metadata: README, license, authors, maintainers, classifiers, keywords, and project URLs.
- [x] Added package type marker for `featuresmith-dashboard`.
- [x] Aligned architecture and release rules with the v0.1.0 public package scope.
- [x] Generated release-readiness reports under `release/`.
