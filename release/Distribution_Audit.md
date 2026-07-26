# Distribution Audit

## Build Artifacts

Fresh artifacts were generated with:

```bash
uv build --all-packages
```

Generated files:

- `featuresmith_core-0.1.0-py3-none-any.whl` - 46,614 bytes
- `featuresmith_core-0.1.0.tar.gz` - 30,780 bytes
- `featuresmith_cli-0.1.0-py3-none-any.whl` - 13,241 bytes
- `featuresmith_cli-0.1.0.tar.gz` - 11,622 bytes
- `featuresmith_dashboard-0.1.0-py3-none-any.whl` - 5,965 bytes
- `featuresmith_dashboard-0.1.0.tar.gz` - 5,648 bytes

## Contents

Artifact inspection confirmed:

- Wheels contain source modules, package metadata, `py.typed`, and license files.
- Source distributions contain package source, package README, `pyproject.toml`, `py.typed`, and license files.
- No tests, caches, screenshots, temporary files, or editor files were found in generated artifacts.

## Notes

The dashboard artifacts build successfully but are internal-only for v0.1.0 and should not be uploaded to PyPI.
