# Retail Sales Dataset Example

This example demonstrates how Featuresmith profiles structured retail transactions, analyzing dates and categories while flagging constant columns. It also demonstrates the dataset **diff** workflow (v0.3.0): the lower-level `fs.diff()` snapshot comparison and the integrated `fs.review(..., previous=...)` DiffReviewer review.

## Dataset Description
This dataset represents transactional order lines for a retail store. It contains transaction details (order ID, order date, customer ID, product category), numeric performance metrics (sales amount, quantity ordered, discount applied), and geographic details (region).

- **Size**: 1,000 rows × 10 columns
- **Columns**: `order_id`, `order_date`, `customer_id`, `category`, `sales_amount`, `quantity`, `discount`, `region`, `store_version`, `return_reason`

## Original Source
- **Origin**: Generative retail sales simulation, designed to mirror common formats like the Tableau Superstore sales dataset.
- **Source**: Generated reproducibly using `examples/prepare_datasets.py`.
- **License**: Public Domain (Creative Commons CC0).

## Why This Dataset Was Chosen
A real retail sales dataset is typically very large and contains hundreds of megabytes of transaction history, making it unsuitable for repository distribution. This dataset is simulated programmatically to provide the same structure, containing:
1. Datetime fields (`order_date`) to show datetime column profiling.
2. Constant columns (`store_version`) and fully empty columns (`return_reason`) to showcase the **Rule Engine's constant and empty column rules**.
3. Categories with missing values (`discount`) to show numeric missing values profiling.

## How to Get the Data
Run the workspace downloader script from the project root:
```bash
python examples/download_datasets.py
python examples/prepare_datasets.py
```
This writes the processed CSV file to `examples/data/processed/sales.csv`.

## Featuresmith SDK Example
You can run the SDK example script `run_sdk.py` to see the programmatic workflow:
```bash
python examples/sales/run_sdk.py
```

Code summary (run_sdk.py):
```python
import os

import pandas as pd
import featuresmith as fs

dataset_path = os.path.join("examples", "data", "processed", "sales.csv")

# Load base dataset (v1) - the "previous" snapshot
sales_v1 = pd.read_csv(dataset_path)

# Simulate dataset evolution (v2): schema drift, missingness spike, new rows
sales_v2 = sales_v1.copy()
sales_v2.drop(columns=["store_version"], inplace=True)   # Column dropped
sales_v2["promo_code"] = "SUMMER2026"                    # New column added
sales_v2.loc[:50, "discount"] = None                     # Missingness spike

# 1. Lower-level primitive: standalone snapshot comparison
diff_res = fs.diff(sales_v1, sales_v2)

# 2. Integrated DiffReviewer: review current vs previous snapshot (v0.3.0)
review_res = fs.review(sales_v2, previous=sales_v1)
# review_res.diff is the DatasetDiffResult;
# review_res.sections includes the "review.diff" section
```

## CLI Example
Run the Featuresmith CLI from your terminal:
```bash
featuresmith review examples/data/processed/sales.csv
```

To output results as machine-readable JSON:
```bash
featuresmith review examples/data/processed/sales.csv --format json
```

To compare against a previous snapshot (v0.3.0, DiffReviewer):
```bash
featuresmith review sales_v2.csv --previous sales_v1.csv
```

## Expected Findings
- **Fully Empty Columns Rule (`quality.fully_empty_columns`)**: Flags `return_reason` as **critical** because it contains 100% missing values (all rows are null).
- **Constant Columns Rule (`quality.constant_columns`)**: Flags `store_version` as a warning because it contains exactly one unique value (`v1.4`) for all non-null records.
- **Missing Value Threshold Rule (`quality.missing_value_threshold`)**: Flags `discount` as a warning if the missingness ratio exceeds 20% (our default generation is around 10%, but this demonstrates threshold checks).
- **Exit Code**: The CLI will exit with code `1` due to the critical empty column finding.

## Learning Points
1. **Datetime Column Profiling**: Observe how Featuresmith identifies datetime stamps and calculates date ranges and spans.
2. **Pruning Empty and Constant Features**: Learn how constant features (which provide zero statistical variance) and empty features (which contain no information) are detected so they can be dropped from modeling pipelines.
3. **Missing Value Proportions**: Review how numeric missingness is tracked, showing exactly which features need imputation.
