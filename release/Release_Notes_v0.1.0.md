# Release Notes v0.1.0

Featuresmith v0.1.0 is the first public release candidate.

## Highlights

- Deterministic Python SDK for tabular data loading, profiling, and rule analysis.
- CLI command: `featuresmith analyze`.
- Connectors for CSV, Excel, Parquet, pandas DataFrames, and Polars DataFrames.
- Profiling engine for numeric, categorical, datetime, text, missingness, duplicate, and correlation summaries.
- Rule engine with eight deterministic quality, statistical, and leakage checks.
- Typed serializable result dataclasses.
- PEP 561 type markers.
- PyPI-ready packaging metadata for `featuresmith-core` and `featuresmith-cli`.

## Distribution Scope

Publish for v0.1.0:

- `featuresmith-core`
- `featuresmith-cli`

Do not publish for v0.1.0:

- `featuresmith-dashboard`

## Upgrade Notes

This is the first release. There are no previous public versions to migrate from.
