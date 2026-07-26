# Titanic Dataset Example

This example demonstrates how Featuresmith profiles a dirty real-world dataset and detects missing values and empty column flags.

## Dataset Description
The Titanic dataset contains survival logs for 1,309 passengers aboard the Titanic. It records passenger characteristics (e.g., age, class, sex, fare) alongside whether they survived the sinking.

- **Size**: 1,309 rows × 14 columns
- **Columns**: `pclass`, `survived`, `name`, `sex`, `age`, `sibsp`, `parch`, `ticket`, `fare`, `cabin`, `embarked`, `boat`, `body`, `home_dest`

## Original Source
- **Origin**: Compiled by Thomas Cason from various historical registers.
- **Source**: Retrieved programmatically from OpenML via `fetch_openml('titanic', version=1)` or high-availability mirrors.
- **License**: Public Domain (Creative Commons CC0).

## Why This Dataset Was Chosen
The Titanic dataset is famous for being "messy". It contains a large percentage of missing values (e.g., Cabin and Age) and several columns that are almost entirely empty or contain duplicate rows (such as passengers sharing tickets). It is chosen to demonstrate the **Rule Engine's data quality rules** in a realistic context.

## How to Get the Data
Run the workspace downloader script from the project root:
```bash
python examples/download_datasets.py
python examples/prepare_datasets.py
```
This writes the processed CSV file to `examples/data/processed/titanic.csv`.

## Featuresmith SDK Example
You can run the SDK example script `run_sdk.py` to see the programmatic workflow:
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
- **Missing Value Threshold Rule (`quality.missing_value_threshold`)**: Triggered as a warning on `cabin`, `boat`, `body`, and `home_dest` columns since they contain over 20% null values.
- **Duplicate Rows Rule (`quality.duplicate_rows`)**: Triggered as a warning since passenger details can contain duplicates or shared records.
- **Exit Code**: The CLI will exit with code `1` because findings were detected.

## Learning Points
1. **Dirty Data Profiling**: Observe how Featuresmith automatically handles mixed string/float columns, categorizing them cleanly.
2. **Missing Value Audits**: Learn how missing value rules warn developers about features that cannot be easily fed to machine learning estimators without imputation.
3. **CLI Exit Code Gating**: Understand how a dirty dataset triggers a non-zero exit code, which can block standard CI builds.
