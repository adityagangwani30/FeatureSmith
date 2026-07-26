# Changelog

All notable changes to Featuresmith are documented here.

This project adheres to [Semantic Versioning](https://semver.org/) and
[Conventional Commits](https://www.conventionalcommits.org/).

---

## [0.1.0] - 2026-07-27

The first public release. Completes Phase 1 of the roadmap: SDK + CLI MVP with deterministic profiling, a rule engine, and robust engineering validations.

### Added
- `featuresmith-core` — production-grade core library.
- `featuresmith-cli` — Typer-based CLI wrapper (`featuresmith analyze`).
- Unified `Dataset` abstraction with normalized schema across all sources.
- Built-in connectors: CSV (Polars), Excel (pandas), Parquet (Polars), pandas DataFrame, and Polars DataFrame.
- Deterministic Profiling Engine (`fs.profile()`) computing numeric stats, categorical cardinality/entropy, datetime range, text metrics, and Pearson correlation matrices.
- Deterministic Rule Engine (`fs.analyze()`) with 8 seed rules covering missingness, duplicates, constant columns, fully empty columns, high cardinality, outliers, high correlations, and potential target leakage.
- Strong typing — `frozen=True` dataclasses throughout (`Dataset`, `ProfileResult`, `RuleFinding`, `RuleResult`) with full type annotations.
- Full serialization support via `.to_dict()` and standard primitives.
- PEP 561 support (`py.typed` markers) for downstream type checking.
- Package boundary enforcement via `import-linter` contract (CLI may only import `featuresmith.api`).
- Comprehensive GitHub Actions CI: Ruff lint/format, MyPy strict type checks, pytest unit/integration test suite, and pip-audit scans.

### Fixed
- Enforced explicit rule thresholds by removing ambiguous ratio-to-percentage auto-coercion.
- Added eager `RuleEngine` configuration checking of types and keys using signature binding to fail early.
- Capped `frequency_table` size in categorical profiling (default 1000) to prevent memory and payload bloat on high-cardinality columns.
- Introduced specific typed exceptions (`SourceNotFoundError`, `UnsupportedFormatError`, `SourceParseError`) inheriting from `ConnectorError` in loaders and CLI exit codes.
- Frozen collection fields using `MappingProxyType` and `tuple` to ensure strict runtime immutability.
- Corrected package installation references and unified versions across repository to `0.1.0`.
- Expanded CI matrix to cover Windows/Ubuntu and Python 3.11, 3.12, and 3.13.
- Isolated JIT compilation noise from performance benchmarks, and documented native memory caveats.
- Cleaned up example directories from being polluted by test output.
