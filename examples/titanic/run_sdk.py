import os

import featuresmith as fs


def main():
    dataset_path = os.path.join("examples", "data", "processed", "titanic.csv")
    print(f"Reviewing Titanic dataset: {dataset_path}")

    # 1. Load dataset
    dataset = fs.load(dataset_path)
    print(f"Rows: {dataset.row_count} | Columns: {len(dataset.schema.names)}")

    # 2. Run dataset review with target column
    review_result = fs.review(dataset, target_column="survived")
    print(f"\nReview complete across {len(review_result.sections)} sections.")

    # 3. Extract ML Readiness Score
    scorecard = fs.score(review_result)
    if scorecard:
        print(f"\nML Readiness Score: {scorecard.overall:.1f}/100")
        print("Dimension Breakdown:")
        for dim in scorecard.dimensions:
            print(
                f"  - {dim.label:<20}: {dim.score:5.1f}/100 ({len(dim.contributing_findings)} findings)"
            )

    # 4. Print findings
    findings = [f for s in review_result.sections for f in s.findings]
    print(f"\nTotal Findings Identified: {len(findings)}")
    for finding in findings:
        print(
            f"[{finding.severity.upper()}] Column: {finding.column_name or 'dataset'} - {finding.title}"
        )
        print(f"  Detail: {finding.description}")


if __name__ == "__main__":
    main()
