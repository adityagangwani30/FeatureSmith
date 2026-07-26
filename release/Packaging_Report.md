# Packaging Report

## Scope

RR-5 audited the repository's Python packaging state for the v0.1.0 release.

Public release packages:

- `featuresmith-core`
- `featuresmith-cli`

Internal package:

- `featuresmith-dashboard` remains unreleased/internal for v0.1.0.

## Metadata Results

`featuresmith-core` and `featuresmith-cli` now include PyPI-ready metadata:

- Version: `0.1.0`
- Python requirement: `>=3.11`
- SPDX license expression: `Apache-2.0`
- Packaged license files
- Package-local README files
- Authors and maintainers
- Keywords
- Classifiers
- Homepage, documentation, repository, issue tracker, and changelog URLs

`featuresmith-dashboard` includes internal/planning metadata, packaged license, and a PEP 561 marker, but should not be uploaded for v0.1.0.

## Package Data

All Python packages include `py.typed` markers. Package discovery is scoped to each package's `src/` tree.

## Release Decision

`featuresmith-core` and `featuresmith-cli` are ready for TestPyPI packaging validation. `featuresmith-dashboard` should stay excluded from public publishing automation until its implementation phase.
