import os

import featuresmith as fs


def main():
    # Construct path to the processed dataset
    dataset_path = os.path.join("examples", "data", "processed", "iris.csv")
    print(f"Analyzing Iris dataset: {dataset_path}")

    # Load dataset using Featuresmith Load Connector
    dataset = fs.load(dataset_path)
    print(f"Row count: {dataset.row_count}")
    print(f"Schema columns: {dataset.schema.names}")

    # Profile the dataset (computes stats, nulls, cardinality, correlations)
    profile = fs.profile(dataset)
    print("\nColumn Profiles:")
    for col_name, col_prof in profile.column_profiles.items():
        print(
            f"- {col_name}: Type={col_prof.logical_type}, Missing={col_prof.missing_count}"
        )

    # Run analysis (loads dataset, computes profiles, evaluates rules)
    result = fs.analyze(dataset)
    print(f"\nRule evaluation complete. Total findings: {len(result.findings)}")
    for finding in result.findings:
        print(
            f"[{finding.severity.upper()}] Column: {finding.column_name} - Rule: {finding.rule_id}"
        )
        print(f"  Title: {finding.title}")
        print(f"  Detail: {finding.description}")

    # Print serialization summary
    print("\nSerialized findings count:", len(result.to_dict()["findings"]))


if __name__ == "__main__":
    main()
