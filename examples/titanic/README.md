# Titanic Dataset Example

> **Extended example.** This is a real-world, "dirty" dataset review that requires
> dataset preparation if you regenerate the data from scratch. It is **not** the
> primary Quick Start. For an immediately runnable, zero-setup introduction use the
> [Quick Start](../../README.md#quick-start), which ships with the bundled
> `examples/data/processed/titanic.csv` already checked into the repository.

This example demonstrates how Featuresmith profiles a dirty real-world dataset and detects missing values, distribution skewness, and identifier-like columns.

## Dataset Description

The repository bundles a processed **Titanic** survival dataset at `examples/data/processed/titanic.csv`:

- **Size**: 891 rows × 12 columns
- **Columns**: `passengerid`, `survived`, `pclass`, `name`, `sex`, `age`, `sibsp`, `parch`, `ticket`, `fare`, `cabin`, `embarked`

The bundled file is the standard 891-passenger version of the Titanic dataset and is committed directly to the repository, so **no download is required to run this example**. Regenerating the raw data via the download script instead produces the fuller Thomas Cason compilation (1,309 rows × 14 columns, adding `boat`, `body`, and `home_dest`), which is also valid input for the same scripts.

## Original Source

- **Origin**: Compiled by Thomas Cason from various historical registers; the bundled copy is the standard 891-row subset used across ML tutorials.
- **Source**: Retrieved programmatically from OpenML via `fetch_openml('titanic', version=1)` or high-availability mirrors.
- **License**: Public Domain (Creative Commons CC0).
- **Network requirement**: Fetching the raw dataset **requires internet access** (OpenML with a GitHub mirror fallback). It is only needed if you want to regenerate the data yourself; the bundled `examples/data/processed/titanic.csv` needs no network.

## Why This Dataset Was Chosen

The Titanic dataset is famous for being "messy". It contains a large percentage of missing values (e.g., `cabin` and `age`) and several columns that are almost entirely text or identifier-like (e.g., `name`, `ticket`, `passengerid`). It is chosen to demonstrate the **Review Engine's data quality rules** in a realistic context.

## How to Get the Data

### Option A — Use the bundled file (no setup)

The processed CSV is already committed at `examples/data/processed/titanic.csv`. Just run the example:

```bash
python examples/titanic/run_sdk.py
```

### Option B — Regenerate from raw (requires network)

Run the workspace downloader and preparation scripts from the project root:

```bash
python examples/download_datasets.py
python examples/prepare_datasets.py
```

This downloads the raw Titanic data from OpenML (with a GitHub mirror fallback) and writes the processed CSV to `examples/data/processed/titanic.csv`.

## Featuresmith SDK Example

```bash
python examples/titanic/run_sdk.py
```

Code summary:

```python
import featuresmith as fs

dataset = fs.load("examples/data/processed/titanic.csv")
result = fs.analyze(dataset, target_column="survived")
```

## CLI Example

Run the Featuresmith CLI from your terminal:

```bash
featuresmith analyze examples/data/processed/titanic.csv --target survived
```

To filter findings by severity threshold:

```bash
featuresmith analyze examples/data/processed/titanic.csv --target survived --severity warning
```

## Expected Findings

Against the bundled 891-row dataset, the review reports:

- **Missing Value Threshold Rule (`quality.missing_value_threshold`)**: Triggered as **critical** on `cabin` (77.1% missing, above the 20% threshold).
- **Basic Statistics (`review.quality.basic_statistics`)**: `sibsp`, `parch`, and `fare` exceed the skewness threshold (2.0); `sibsp` and `fare` exceed the kurtosis threshold (10.0).
- **Identifier-like / Text columns**: `passengerid` is flagged as identifier-like; `name`, `ticket`, and `cabin` are flagged as free-text columns requiring preprocessing.
- **Exit Code**: `featuresmith analyze` and `featuresmith review` exit with code `1` because findings were detected.

## Learning Points

1. **Dirty Data Profiling**: Observe how Featuresmith automatically handles mixed string/float columns, categorizing them cleanly.
2. **Missing Value Audits**: Learn how missing value rules warn developers about features that cannot be easily fed to machine learning estimators without imputation.
3. **Distribution Signals**: See skewness and kurtosis findings that flag columns unlikely to behave well under linear models.
4. **CLI Exit Code Gating**: Understand how a dirty dataset triggers a non-zero exit code, which can block standard CI builds.
