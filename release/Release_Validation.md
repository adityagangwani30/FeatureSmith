# Release Validation

## Passed

- `uv build --all-packages`
- Artifact inspection for wheels and source distributions
- `pip install` from built core and CLI wheels
- `uv pip install` from built core and CLI wheels
- SDK import/version/public exports check
- `featuresmith --version`
- `featuresmith --help`
- `featuresmith analyze <csv> --target target --format json`
- `.venv\Scripts\python.exe -m ruff format --check .`
- `.venv\Scripts\python.exe -m ruff check .`
- `.venv\Scripts\python.exe -m mypy .`
- `.venv\Scripts\python.exe -m pytest` with `TMP` and `TEMP` pointed to `.pytest_tmp`
- `npm run lint`
- `npm run build`

## Observed Environment Constraints

- Plain `uv sync` failed locally because uv could not access the user-profile cache path.
- Pytest required `TMP` and `TEMP` to point at the workspace because the default user temp pytest directory was not readable.
- The frontend build originally depended on remote Google Fonts fetches. This was fixed by using local font-family stacks.

## Result

The repository is ready to proceed to RR-6 for CI/CD and release automation, with one explicit automation requirement: RR-6 should run release validation in a clean CI environment and publish only `featuresmith-core` and `featuresmith-cli` for v0.1.0.
