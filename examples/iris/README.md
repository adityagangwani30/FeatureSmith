# Iris Dataset Example

This example demonstrates how to load, profile, and analyze the famous Iris dataset using Featuresmith.

## Dataset Description
The Iris dataset consists of 150 samples from three species of Iris flowers (Setosa, Versicolor, and Virginica). Four features were measured from each sample: the length and the width of the sepals and petals, in centimeters.

- **Size**: 150 rows × 5 columns
- **Columns**: `sepal_length`, `sepal_width`, `petal_length`, `petal_width`, `species`

## Original Source
- **Origin**: Fisher, R.A. (1936). "The use of multiple measurements in taxonomic problems".
- **Source**: Retrieved programmatically via `sklearn.datasets.load_iris`.
- **License**: Public Domain (Creative Commons CC0).

## Why This Dataset Was Chosen
The Iris dataset is the canonical "clean" dataset in machine learning. It contains no missing values, duplicates, or extreme outliers. It is chosen for the Getting Started tutorial because it represents a "perfect" baseline where rule checks should pass cleanly, letting users observe profiling statistics on a simple dataset.

## How to Get the Data
Run the workspace downloader script from the project root:
```bash
python examples/download_datasets.py
python examples/prepare_datasets.py
```
This writes the cleaned CSV file to `examples/data/processed/iris.csv`.

## Featuresmith SDK Example
You can run the SDK example script `run_sdk.py` to see the programmatic workflow:
```bash
python examples/iris/run_sdk.py
```

Code summary:
```python
import featuresmith as fs

dataset = fs.load("examples/data/processed/iris.csv")
profile = fs.profile(dataset)
result = fs.analyze(dataset)
```

## CLI Example
Run the Featuresmith CLI from your terminal:
```bash
featuresmith analyze examples/data/processed/iris.csv
```

To format findings as JSON:
```bash
featuresmith analyze examples/data/processed/iris.csv --format json
```

## Expected Findings
Because the Iris dataset is clean:
- **Rule Findings**: `0 findings`.
- **Correlations**: High correlations will be computed (e.g., `petal_length` and `petal_width` are highly correlated with Pearson correlation >= 0.90), but since no target column was specified, no target leakage rule triggers.
- **Exit Code**: The CLI will exit with code `0` (clean).

## Learning Points
1. **Clean Baseline**: Shows that when a dataset has no statistical anomalies or missing elements, Featuresmith completes the audit cleanly with zero findings.
2. **Numeric Profiling**: Demonstrates 23 numeric profiling metrics on continuous dimensions like `sepal_length` and `petal_width`.
3. **Correlation Matrix**: Computes standard Pearson correlations across all numeric features.
