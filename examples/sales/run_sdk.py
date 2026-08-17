"""Sales snapshot comparison: lower-level ``fs.diff()`` and the integrated
diff-aware review (``fs.review(..., previous=...)``, v0.3.0+).

This example shows the two levels of dataset comparison:

- ``fs.diff(old, new)``: the standalone, lower-level comparison primitive.
- ``fs.review(new, previous=old)``: a full dataset review with the dataset
  diff integrated through the ``DiffReviewer`` (a ``review.diff`` section).
"""

import os

import pandas as pd

import featuresmith as fs


def main():
    dataset_path = os.path.join("examples", "data", "processed", "sales.csv")
    print(f"Loading Sales dataset for snapshot comparison: {dataset_path}")

    # 1. Load base dataset (v1) - the "previous" snapshot
    sales_v1 = pd.read_csv(dataset_path)

    # 2. Simulate dataset evolution (v2) with schema drift, missingness spike, and new rows
    sales_v2 = sales_v1.copy()
    sales_v2.drop(columns=["store_version"], inplace=True)  # Column dropped
    sales_v2["promo_code"] = "SUMMER2026"  # New column added
    sales_v2.loc[:50, "discount"] = None  # Missingness spike

    print(
        f"Comparing Snapshot v1 ({sales_v1.shape}) vs Snapshot v2 ({sales_v2.shape})..."
    )

    # 3. Run Dataset Diff Engine (lower-level primitive)
    diff_res = fs.diff(sales_v1, sales_v2)

    print("\n=== fs.diff(sales_v1, sales_v2) - lower-level comparison ===")
    print(f"Dataset Health Verdict : {diff_res.summary.overall_health.upper()}")
    print(f"Recommendation         : {diff_res.summary.recommendation}")
    print(
        f"Columns Added          : {diff_res.summary.columns_added} ({diff_res.schema.added_columns})"
    )
    print(
        f"Columns Removed        : {diff_res.summary.columns_removed} ({diff_res.schema.removed_columns})"
    )
    print(f"Missing Values Increased: {diff_res.summary.missing_values_increased}")
    print(f"Overall Summary        : {diff_res.overall_summary}")

    # 4. Run the integrated diff-aware review (v0.3.0+)
    review_res = fs.review(sales_v2, previous=sales_v1)

    print("\n=== fs.review(sales_v2, previous=sales_v1) - DiffReviewer workflow ===")
    print(
        f"Review Sections        : {len(review_res.sections)} (10 built-in + review.diff)"
    )

    diff_section = next(
        section for section in review_res.sections if section.id == "review.diff"
    )
    print(f"Diff Section           : {diff_section.title} [{diff_section.severity}]")
    print("DiffReviewer Findings :")
    for finding in diff_section.findings:
        print(
            f"  - [{finding.severity.upper():<7}] {finding.title}"
            f"{f' (column: {finding.column_name})' if finding.column_name else ''}"
        )

    # 5. The diff result is also attached directly to the review result
    print(f"ReviewResult.diff Health: {review_res.diff.summary.overall_health.upper()}")
    print(
        f"ReviewResult.diff Columns Added/Removed: "
        f"{review_res.diff.schema.added_columns} / {review_res.diff.schema.removed_columns}"
    )

    # 6. The diff section does NOT change the ML Readiness Score dimensions
    if review_res.score:
        print(
            f"ML Readiness Score    : {review_res.score.overall:.1f}/100 "
            f"(still 7 dimensions - diff is informational)"
        )

    print(f"\nOverall Review Summary: {review_res.overall_summary}")


if __name__ == "__main__":
    main()
