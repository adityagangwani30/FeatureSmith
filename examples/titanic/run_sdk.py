import os

import featuresmith as fs


def main():
    dataset_path = os.path.join("examples", "data", "processed", "titanic.csv")
    print(f"Analyzing Titanic dataset: {dataset_path}")

    # Load dataset
    dataset = fs.load(dataset_path)
    print(f"Row count: {dataset.row_count}")
    print(f"Schema columns: {dataset.schema.names}")

    # Run analysis
    # We specify 'survived' as the target column to check target leakage (though titanic features are mostly valid, we'll see rules run)
    result = fs.analyze(dataset, target_column="survived")
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
