import os

import featuresmith as fs


def main():
    dataset_path = os.path.join("examples", "data", "processed", "customer_churn.csv")
    print(f"Analyzing Customer Churn dataset: {dataset_path}")

    # Load dataset
    dataset = fs.load(dataset_path)
    print(f"Row count: {dataset.row_count}")
    print(f"Schema columns: {dataset.schema.names}")

    # Run analysis targeting 'churn_label' to check for target leakage
    # We choose churn_label (the numeric column) to trigger the leakage rule
    result = fs.analyze(dataset, target_column="churn_label")
    print(f"\nRule evaluation complete. Total findings: {len(result.findings)}")
    for finding in result.findings:
        print(
            f"[{finding.severity.upper()}] Column: {finding.column_name} - Rule: {finding.rule_id}"
        )
        print(f"  Title: {finding.title}")
        print(f"  Detail: {finding.description}")

    # Print execution metadata
    print(f"\nExecuted rules: {len(result.executed_rules)}")
    print(f"Failed rules: {len(result.failed_rules)}")
    print(f"Execution time: {result.execution_time_ms:.2f} ms")


if __name__ == "__main__":
    main()
