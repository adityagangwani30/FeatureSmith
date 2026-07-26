# Installation Guide

## Public Packages

Install the SDK:

```bash
pip install featuresmith-core
```

Install the SDK and CLI:

```bash
pip install featuresmith-core featuresmith-cli
```

Using uv:

```bash
uv add featuresmith-core featuresmith-cli
```

## Source Development

```bash
git clone https://github.com/adityagangwani30/FeatureSmith.git
cd FeatureSmith
uv sync
```

## Verified Artifact Installs

The following release-artifact checks passed in disposable virtual environments:

- `pip install dist/featuresmith_core-0.1.0-py3-none-any.whl dist/featuresmith_cli-0.1.0-py3-none-any.whl`
- `uv pip install --python <venv-python> dist/featuresmith_core-0.1.0-py3-none-any.whl dist/featuresmith_cli-0.1.0-py3-none-any.whl`
- `import featuresmith as fs`
- `fs.__version__`
- `featuresmith --version`
- `featuresmith --help`
- `featuresmith analyze <csv> --target target --format json`

## Environment Note

In this local sandbox, `uv sync` failed because uv could not access `C:\Users\ASUS\AppData\Local\uv\cache`. This is a machine permission issue, not a packaging metadata failure. Earlier elevated `uv build` and `uv pip install` checks succeeded.
