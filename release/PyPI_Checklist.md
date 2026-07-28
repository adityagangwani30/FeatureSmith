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

- [x] Exclude `featuresmith-dashboard` from v0.1.0 publish jobs.
- [x] Run `twine check dist/*` in CI (handled by publish-testpypi.yml).

## TestPyPI Validation

- [ ] Trigger the **Publish to TestPyPI** workflow via `workflow_dispatch`.
- [ ] Confirm all validation, build, twine check, and publish steps pass.
- [ ] Visit [test.pypi.org/project/featuresmith-core](https://test.pypi.org/project/featuresmith-core/) and verify metadata.
- [ ] Visit [test.pypi.org/project/featuresmith-cli](https://test.pypi.org/project/featuresmith-cli/) and verify metadata.
- [ ] Install from TestPyPI in a clean environment:
      ```bash
      pip install --index-url https://test.pypi.org/simple/ featuresmith-core featuresmith-cli
      ```
- [ ] Run `featuresmith --help` to confirm CLI entry point works.
- [ ] Confirm `featuresmith-dashboard` is NOT present on TestPyPI.

## Production Upload

- [ ] Upload `featuresmith-core` and `featuresmith-cli` to PyPI only after TestPyPI validation passes. See `release/TestPyPI_Publishing_Guide.md` for the adaptation checklist.
