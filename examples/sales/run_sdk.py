import os

import pandas as pd

import featuresmith as fs


def main():
    dataset_path = os.path.join("examples", "data", "processed", "sales.csv")
    print(f"Loading Sales dataset for Dataset Diff demonstration: {dataset_path}")

    # 1. Load base dataset (v1)
    sales_v1 = pd.read_csv(dataset_path)

    # 2. Simulate dataset evolution (v2) with schema drift, missingness spike, and new rows
    sales_v2 = sales_v1.copy()
    sales_v2.drop(columns=["store_version"], inplace=True)  # Column dropped
    sales_v2["promotional_code"] = "SUMMER2026"  # New column added
    sales_v2.loc[:50, "discount"] = None  # Missingness spike

    print(
        f"Comparing Snapshot v1 ({sales_v1.shape}) vs Snapshot v2 ({sales_v2.shape})..."
    )

    # 3. Run Dataset Diff Engine
    diff_res = fs.diff(sales_v1, sales_v2)

    # 4. Print Diff summary & verdict
    print(f"\nDataset Health Verdict : {diff_res.summary.overall_health.upper()}")
    print(f"Recommendation         : {diff_res.summary.recommendation}")
    print(
        f"Columns Added          : {diff_res.summary.columns_added} ({diff_res.schema.added_columns})"
    )
    print(
        f"Columns Removed        : {diff_res.summary.columns_removed} ({diff_res.schema.removed_columns})"
    )
    print(f"Missing Values Increased: {diff_res.summary.missing_values_increased}")
    print(f"Overall Summary        : {diff_res.overall_summary}")


if __name__ == "__main__":
    main()
