import os

import featuresmith as fs


def main():
    dataset_path = os.path.join("examples", "data", "processed", "customer_churn.csv")
    print(f"Reviewing Customer Churn dataset: {dataset_path}")

    # 1. Load dataset
    dataset = fs.load(dataset_path)
    print(f"Rows: {dataset.row_count} | Columns: {len(dataset.schema.names)}")

    # 2. Run review targeting 'churn_label' to catch target leakage
    review_result = fs.review(dataset, target_column="churn_label")

    # 3. Extract ML Readiness Score
    scorecard = fs.score(review_result)
    if scorecard:
        print(f"\nML Readiness Score: {scorecard.overall:.1f}/100")
        for dim in scorecard.dimensions:
            if "leakage" in dim.id:
                print(
                    f"  * Leakage Risk Dimension Score: {dim.score:.1f}/100 ({len(dim.contributing_findings)} leakage findings)"
                )

    # 4. Filter and print leakage findings
    all_findings = [f for s in review_result.sections for f in s.findings]
    print("\nIntelligent Leakage Detection Results:")
    leakage_findings = [
        f
        for f in all_findings
        if "leakage" in f.rule_id or "leakage" in f.title.lower()
    ]
    if leakage_findings:
        for finding in leakage_findings:
            print(
                f"  [{finding.severity.upper()}] Column '{finding.column_name}': {finding.title}"
            )
            print(f"     {finding.description}")
    else:
        print("  No target leakage detected.")


if __name__ == "__main__":
    main()
