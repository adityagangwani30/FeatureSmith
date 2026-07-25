# ADR 0001: Local tabular connector dependencies

## Status

Accepted — Sprint 2

## Context

Sprint 2 requires production-ready local CSV, Excel, Parquet, pandas DataFrame,
and Polars DataFrame connectors. The core package currently has no dataframe or
Excel reader dependencies.

## Decision

`featuresmith-core` depends on compatible releases of:

- `polars` for the primary in-memory backend and CSV/Parquet readers.
- `pandas` for pandas DataFrame interoperability and Excel loading.
- `openpyxl` as pandas' `.xlsx` reader engine.

The strict MyPy configuration skips third-party package implementation files;
the project targets Python 3.11 while the local development interpreter may be
newer than the versions supported by every dependency's inline stubs.

The connectors return the normalized `Dataset` contract, so these packages do
not leak into the public loading API. Cloud, SQL, and other heavy source
dependencies remain out of scope.

## Alternatives considered

- Standard-library CSV parsing: rejected because the project architecture names
  Polars as the primary dataframe engine and it would create inconsistent dtype
  handling.
- Making all readers optional extras: rejected for these Sprint 2 local formats;
  they are the supported foundation of `fs.load()`.
- Adding a separate Parquet dependency: rejected because Polars provides the
  required Parquet read/write support for this sprint.

## Consequences

The core install gains local tabular-data support while remaining free of cloud
SDKs and network-dependent functionality.
