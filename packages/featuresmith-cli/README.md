# featuresmith-cli

[![PyPI Version](https://img.shields.io/pypi/v/featuresmith-cli.svg)](https://pypi.org/project/featuresmith-cli/)
[![Python Version](https://img.shields.io/pypi/pyversions/featuresmith-cli.svg)](https://pypi.org/project/featuresmith-cli/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

`featuresmith-cli` is the command-line interface for **Featuresmith** — the open-source Dataset Review Platform for structured data.

It exposes terminal commands for automated dataset code reviews, snapshot diffing, remediation plan compilation, and CI/CD quality gating, delegating all engine work to `featuresmith-core`.

## Installation

```bash
pip install featuresmith-cli
```

*(This automatically installs `featuresmith-core` as a dependency).*

## CLI Workflows

```bash
# Run automated dataset review report with ML Readiness Scorecard
featuresmith review train.csv --target survived

# Diff two dataset snapshots to catch schema drift and quality regressions
featuresmith diff train_v1.csv train_v2.csv --target survived

# Compile an inspectable Plan from accepted recommendations
featuresmith plan train.csv --target survived --accept rec.quality.missingness.cabin

# Run quality & leakage rule analysis
featuresmith analyze train.csv --target survived

# Output machine-readable JSON for CI/CD gating (exit code 0 = clean, 1 = findings)
featuresmith review train.csv --target survived --format json --output report.json
```

For comprehensive guides and CLI reference, visit the official website:
<https://featuresmith.adityagangwani.me>
