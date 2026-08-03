import os

import featuresmith as fs


def main():
    dataset_path = os.path.join("examples", "data", "processed", "iris.csv")
    print(f"Reviewing Iris dataset: {dataset_path}")

    # 1. Load dataset
    dataset = fs.load(dataset_path)
    print(f"Rows: {dataset.row_count} | Columns: {len(dataset.schema.names)}")

    # 2. Run profile
    profile = fs.profile(dataset)
    print("\nColumn logical types & missingness:")
    for col_name, col_prof in profile.column_profiles.items():
        print(
            f"  - {col_name:<15}: Type={col_prof.logical_type:<10} Missing={col_prof.missing_count}"
        )

    # 3. Run dataset review
    review_res = fs.review(dataset, target_column="species")
    scorecard = fs.score(review_res)
    if scorecard:
        print(f"\nIris ML Readiness Score: {scorecard.overall:.1f}/100")

    findings = [f for s in review_res.sections for f in s.findings]
    print(f"Total Findings Identified: {len(findings)}")


if __name__ == "__main__":
    main()
