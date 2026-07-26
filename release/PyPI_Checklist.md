# PyPI Checklist

## Ready

- [x] Version set to `0.1.0`.
- [x] Public package metadata completed for `featuresmith-core`.
- [x] Public package metadata completed for `featuresmith-cli`.
- [x] SPDX license expression configured.
- [x] License files included in packages.
- [x] Package-local READMEs included.
- [x] `py.typed` markers included.
- [x] Wheels build successfully.
- [x] Source distributions build successfully.
- [x] Artifact contents inspected.
- [x] Wheel installation verified with pip.
- [x] Wheel installation verified with uv pip.
- [x] CLI entry point verified.

## Before Upload

- [ ] Exclude `featuresmith-dashboard` from v0.1.0 publish jobs.
- [ ] Run `twine check dist/*` in CI once RR-6 adds publishing dependencies.
- [ ] Upload first to TestPyPI.
- [ ] Install from TestPyPI in a clean environment.
- [ ] Upload `featuresmith-core` and `featuresmith-cli` to PyPI only after TestPyPI validation passes.
