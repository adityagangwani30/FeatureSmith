# IBM Customer Churn Dataset Example

This example demonstrates how Featuresmith detects **target leakage** in machine learning workflows.

## Dataset Description
This dataset contains customer logs from IBM's Telco Customer Churn project. It maps customer demographic characteristics (gender, partners, dependents), services signed up for (phone, internet, tech support), account metrics (tenure, contract, payment method, charges), and whether the customer churned.

- **Size**: 7,043 rows × 24 columns
- **Columns**: `customer_id`, `gender`, `senior_citizen`, `partner`, `dependents`, `tenure`, `phone_service`, `multiple_lines`, `internet_service`, `online_security`, `online_backup`, `device_protection`, `tech_support`, `streaming_tv`, `streaming_movies`, `contract`, `paperless_billing`, `payment_method`, `monthly_charges`, `total_charges`, `churn`, `customer_status`, `churn_label`, `leakage_score`

## Original Source
- **Origin**: IBM Telco Customer Churn dataset, widely hosted on Kaggle and OpenML.
- **Source**: Retrieved programmatically from OpenML via `fetch_openml('Telco-Customer-Churn', version=1)` or high-availability mirrors.
- **License**: Public Domain (Creative Commons CC0 / IBM terms).

## Why This Dataset Was Chosen
Target leakage occurs when columns in the training dataset contain information about the target that is unavailable during inference. In this example, the raw dataset was programmatically processed to add two leakage indicators:
1. `customer_status`: Mapped 100% to the target `churn` (Customers who churned have status = 'Inactive').
2. `leakage_score`: A continuous variable highly correlated with `churn_label` (Pearson correlation >= 0.99).
This is the perfect dataset to showcase Featuresmith's **Target Leakage Rule**.

## How to Get the Data
Run the workspace downloader script from the project root:
```bash
python examples/download_datasets.py
python examples/prepare_datasets.py
```
This writes the processed CSV file to `examples/data/processed/customer_churn.csv`.

## Featuresmith SDK Example
You can run the SDK example script `run_sdk.py` to see the programmatic workflow:
```bash
python examples/customer_churn/run_sdk.py
```

Code summary:
```python
import featuresmith as fs

dataset = fs.load("examples/data/processed/customer_churn.csv")
# Analyze targeting the numeric churn_label column to detect target leakage
result = fs.analyze(dataset, target_column="churn_label")
```

## CLI Example
Run the Featuresmith CLI from your terminal:
```bash
featuresmith analyze examples/data/processed/customer_churn.csv --target churn_label
```

To output results directly to a JSON file:
```bash
featuresmith analyze examples/data/processed/customer_churn.csv --target churn_label --format json --output churn_report.json
```

## Expected Findings
- **Target Leakage Rule (`leakage.potential_leakage`)**: Flags `leakage_score` as a **critical** target leakage finding because its Pearson correlation coefficient to the target column (`churn_label`) is >= 0.99.
- **High Cardinality Rule (`statistical.high_cardinality`)**: Warns that `customer_id` contains too many unique categories relative to dataset size.
- **Exit Code**: The CLI exits with code `1` (findings detected).

## Learning Points
1. **Target Leakage Gating**: Understand how Featuresmith evaluates correlations to target labels and flags leaking columns before they can bias your model training.
2. **High Cardinality Warnings**: Learn how high cardinality columns (like IDs) are flagged, prompting developers to drop them or apply target encoding.
3. **CI Pipeline Safety**: Gating your builds against leakage findings protects against shipping models with artificially inflated train/validation scores that perform poorly in production.
