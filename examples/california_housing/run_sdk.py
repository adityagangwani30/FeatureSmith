import os

import featuresmith as fs


def main():
    dataset_path = os.path.join(
        "examples", "data", "processed", "california_housing.csv"
    )
    print(f"Reviewing California Housing dataset: {dataset_path}")

    # 1. Load dataset
    dataset = fs.load(dataset_path)
    print(f"Rows: {dataset.row_count} | Columns: {len(dataset.schema.names)}")

    # 2. Run review with regression target
    review_result = fs.review(dataset, target_column="median_house_value")
    scorecard = fs.score(review_result)
    if scorecard:
        print(f"\nML Readiness Score: {scorecard.overall:.1f}/100")
        for dim in scorecard.dimensions:
            print(
                f"  - {dim.label:<20}: {dim.score:5.1f}/100 ({len(dim.contributing_findings)} findings)"
            )

    # 3. List findings
    findings = [f for s in review_result.sections for f in s.findings]
    print(f"\nTotal Findings Identified: {len(findings)}")
    for finding in findings:
        print(
            f"[{finding.severity.upper()}] Column: {finding.column_name or 'dataset'} - {finding.title}"
        )


if __name__ == "__main__":
    main()
