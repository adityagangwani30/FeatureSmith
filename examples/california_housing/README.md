# California Housing Dataset Example

This example demonstrates how Featuresmith profiles a large continuous dataset and triggers outlier detection and feature correlation rules.

## Dataset Description
This dataset contains housing metrics compiled from the 1990 California census. It lists details such as median income, house age, population, average occupancy, latitude, longitude, and median house value for 20,640 block groups in California.

- **Size**: 20,640 rows × 9 columns
- **Columns**: `median_income`, `house_age`, `average_rooms`, `average_bedrooms`, `population`, `average_occupancy`, `latitude`, `longitude`, `median_house_value`

## Original Source
- **Origin**: Pace, R. Kelley and Ronald Barry (1997), "Sparse Spatial Autoregressions," *Statistics and Probability Letters*.
- **Source**: Retrieved programmatically via `sklearn.datasets.fetch_california_housing`.
- **License**: Public Domain (Creative Commons CC0).

## Why This Dataset Was Chosen
The California Housing dataset contains continuous numeric variables with extreme outliers (e.g., block groups with abnormally high average rooms or average occupancy ratios) and strongly correlated dimensions (e.g., latitude/longitude coordinates and average rooms vs average bedrooms). It is chosen to showcase the **Rule Engine's statistical and outlier rules**.

## How to Get the Data
Run the workspace downloader script from the project root:
```bash
python examples/download_datasets.py
python examples/prepare_datasets.py
```
This writes the processed CSV file to `examples/data/processed/california_housing.csv`.

## Featuresmith SDK Example
You can run the SDK example script `run_sdk.py` to see the programmatic workflow:
```bash
python examples/california_housing/run_sdk.py
```

Code summary:
```python
import featuresmith as fs

dataset = fs.load("examples/data/processed/california_housing.csv")
result = fs.analyze(dataset, target_column="median_house_value")
```

## CLI Example
Run the Featuresmith CLI from your terminal:
```bash
featuresmith analyze examples/data/processed/california_housing.csv --target median_house_value
```

## Expected Findings
- **High Correlation Rule (`statistical.high_correlation`)**: Flags that `average_rooms` and `average_bedrooms` are highly correlated (Pearson correlation >= 0.90), suggesting redundancy.
- **Outlier Detection Rule (`statistical.outliers`)**: Detects block groups with outlier values in columns like `average_occupancy`, `average_rooms`, and `population` using the IQR method (factor=1.5).
- **Exit Code**: The CLI will exit with code `1` because warnings are reported.

## Learning Points
1. **Outlier Detection**: Understand how Featuresmith runs deterministic IQR checks across large continuous distributions to isolate extreme records.
2. **Correlation Redundancy**: Learn how identifying highly correlated feature pairs helps developers prune redundant inputs, saving training cycles and improving model interpretability.
3. **Continuous Data Profiling**: Observe the detailed statistical summaries (mean, standard deviation, quantiles) produced by the profiling engine.
