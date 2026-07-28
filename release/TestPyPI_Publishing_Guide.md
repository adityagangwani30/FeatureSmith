# TestPyPI Publishing Guide

This guide documents how to publish Featuresmith packages to **TestPyPI** — the
pre-production package index used to validate the release pipeline before pushing
to the real PyPI.

---

## Prerequisites

- A [TestPyPI](https://test.pypi.org/) account
- A TestPyPI API token with upload scope
- Admin or maintainer access to the GitHub repository to configure secrets

---

## Creating a TestPyPI API Token

1. Go to [test.pypi.org](https://test.pypi.org/) and log in.
2. Navigate to **Account Settings** → **API tokens**.
3. Click **Add API token**.
4. Choose a name (e.g., `featuresmith-testpypi-ci`).
5. Select scope: **Entire account** (or limit to specific projects).
6. Copy the generated token immediately — you won't see it again.

---

## Adding the Token to GitHub Secrets

1. Go to the repository on GitHub:
   `https://github.com/adityagangwani30/FeatureSmith/settings/secrets/actions`
2. Click **New repository secret**.
3. Set **Name** to `TEST_PYPI_API_TOKEN`.
4. Paste the TestPyPI API token as the **Value**.
5. Click **Add secret**.

> The token value should look like `pypi-xxxxxxxxxxxxxxxxxxxx`.

The workflow reads this secret as `${{ secrets.TEST_PYPI_API_TOKEN }}` and passes
it to twine via the `TWINE_PASSWORD` environment variable with
`TWINE_USERNAME=__token__`.

---

## Triggering the Workflow

### Manual (workflow_dispatch)

1. Go to the repository on GitHub.
2. Click **Actions** → **Publish to TestPyPI**.
3. Click **Run workflow**.
4. Optionally enter a specific **Git ref** (branch, tag, or SHA) to publish.
   Leave blank to use the default branch.
5. Click **Run workflow**.

### Automatic (push)

The workflow also triggers automatically on push to the `release-testing` branch.
This is useful for iterative testing of the release pipeline before a manual
production release.

---

## Workflow Steps

| # | Step | Description |
|---|------|-------------|
| 1 | Environment Setup | Checks out code, sets up Python 3.11, uv, and caches |
| 2 | Dependency Installation | Runs `uv sync --locked --group dev --group test` |
| 3 | Format Check | `ruff format --check .` — aborts on failure |
| 4 | Lint | `ruff check .` — aborts on failure |
| 5 | Type Check | `mypy .` — aborts on failure |
| 6 | Tests | `pytest` — aborts on failure |
| 7 | Frontend Setup | Installs Node.js, pnpm, frontend dependencies |
| 8 | Frontend Type-Check | `tsc --noEmit` — aborts on failure |
| 9 | Frontend Build | `next build` — aborts on failure |
| 10 | Build Packages | Builds wheels + sdists for core and cli via `uv build` |
| 11 | Twine Check | Validates distribution metadata and rendering |
| 12 | Artifact Inspection | Verifies required files present, forbidden files absent |
| 13 | Artifact Upload | Uploads distributions as GitHub Action artifacts |
| 14 | Publish to TestPyPI | Uploads core and cli using twine |

Any failure **immediately aborts** the entire workflow. Partial or broken builds
are never published.

---

## Packages Published

| Package | Published | Notes |
|---------|-----------|-------|
| featuresmith-core | Yes | Core profiling + rules engine |
| featuresmith-cli | Yes | CLI surface |
| featuresmith-dashboard | **No** | Unreleased / internal only |

The dashboard package is deliberately excluded from both the build and publish
steps. Only `featuresmith_core-*` and `featuresmith_cli-*` distributions are
uploaded.

---

## Verifying a Successful Release

1. Open the workflow run in GitHub Actions and confirm all steps are green.
2. Visit [test.pypi.org/project/featuresmith-core](https://test.pypi.org/project/featuresmith-core/).
3. Verify the latest version (0.1.0) is listed with correct metadata.
4. Visit [test.pypi.org/project/featuresmith-cli](https://test.pypi.org/project/featuresmith-cli/).
5. Verify the CLI package is listed.
6. Confirm **featuresmith-dashboard does not appear** on TestPyPI.
7. (Optional) Install from TestPyPI in a clean environment:

   ```bash
   pip install --index-url https://test.pypi.org/simple/ featuresmith-core featuresmith-cli
   ```

---

## Troubleshooting

### "Invalid or non-existent authentication information"
- Ensure `TEST_PYPI_API_TOKEN` is set correctly in GitHub Secrets.
- Verify the token has not expired or been revoked on TestPyPI.
- Confirm `TWINE_USERNAME=__token__` is used (the literal string `__token__`).

### "File already exists"
- TestPyPI does not allow re-uploading the same version filename.
- Bump the package version before retrying, or delete the existing release on
  TestPyPI (TestPyPI allows deletion via the web UI).

### "No distributions found" at publish step
- Check that `uv build` succeeded for both packages.
- Verify the `dist/` directory contains `featuresmith_core-*.whl` and
  `featuresmith_cli-*.tar.gz`.

### "Twine check" fails
- Read the twine output carefully — it typically points to missing or malformed
  metadata fields in `pyproject.toml`.
- Run `twine check dist/*` locally to debug.

### Lint / type / test failures in CI but not locally
- Ensure your local environment matches CI: Python 3.11, latest uv, fresh
  `uv sync --locked`.
- Check for platform-specific test failures (CI is `ubuntu-latest`).

---

## Adapting for Production PyPI

When the team is ready to publish to real PyPI:

1. **Copy** this workflow to a new file (e.g., `publish-pypi.yml`).
2. **Change** the publish URL from `https://test.pypi.org/legacy/` to
   `https://upload.pypi.org/legacy/`.
3. **Change** the secret from `TEST_PYPI_API_TOKEN` to `PYPI_API_TOKEN`.
4. **Remove** the `workflow_dispatch` push-to-release-testing trigger.
5. **Add** a trigger on published GitHub Releases or version tags:
   ```yaml
   on:
     release:
       types: [published]
   ```
6. **Consider** using [Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
   (OIDC) instead of long-lived API tokens for production.
7. **Add** a GitHub Actions **environment** with required reviewers for
   production deployments.

The build, validation, and artifact inspection steps remain identical — they
are already production-grade.
