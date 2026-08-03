"""Generator script for Featuresmith v0.2.0 educational Jupyter Notebooks."""

import json
from pathlib import Path


def create_notebook(title: str, description: str, sections: list[dict]) -> dict:
    """Build a valid nbformat v4 Jupyter notebook dictionary structure."""
    cells = []

    # Title & Overview Cell
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# Featuresmith Tutorial: {title}\n\n",
                f"{description}\n\n",
                "---\n",
            ],
        }
    )

    # Add sections
    for sec in sections:
        if "markdown" in sec:
            cells.append(
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": sec["markdown"]
                    if isinstance(sec["markdown"], list)
                    else [sec["markdown"]],
                }
            )
        if "code" in sec:
            cells.append(
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": sec["code"]
                    if isinstance(sec["code"], list)
                    else [sec["code"]],
                }
            )

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.0",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }
    return nb


def build_all_notebooks():
    nb_dir = Path("examples/notebooks")
    nb_dir.mkdir(parents=True, exist_ok=True)

    # Clean out old v0.1.0 notebooks if present
    old_notebooks = [
        "02_exploring_datasets.ipynb",
        "03_understanding_rule_findings.ipynb",
        "04_data_science_workflows.ipynb",
    ]
    for old_name in old_notebooks:
        old_file = nb_dir / old_name
        if old_file.exists():
            old_file.unlink()
            print(f"Removed deprecated notebook: {old_file}")

    # =========================================================================
    # Notebook 1: Getting Started with Featuresmith
    # =========================================================================
    nb1 = create_notebook(
        title="01 — Getting Started with Featuresmith v0.2.0",
        description="Learn the fundamentals of Featuresmith — loading tabular datasets, deterministic statistical profiling, automated dataset code reviews, and ML readiness scoring.",
        sections=[
            {
                "markdown": [
                    "## 1. Problem Statement & Why This Capability Matters\n",
                    "Machine learning failure modes often originate from dataset quality rather than model architecture choices. ",
                    "Featuresmith brings developer-first code review discipline to tabular datasets before training begins.\n\n",
                    "### Objectives\n",
                    "1. Understand Featuresmith's package structure (`featuresmith-core` and `featuresmith-cli`).\n",
                    "2. Load tabular data from CSV, Parquet, Excel, or DataFrames using `fs.load()`.\n",
                    "3. Profile datasets deterministically with `fs.profile()`.\n",
                    "4. Perform an automated dataset code review with `fs.review()`.\n",
                    "5. Extract an explainable 0–100 ML Readiness Score with `fs.score()`.",
                ]
            },
            {
                "markdown": ["### Step 1: Import Featuresmith & Verify Version"],
                "code": [
                    "import featuresmith as fs\n",
                    "import os\n\n",
                    'print(f"Featuresmith Version: {fs.__version__}")',
                ],
            },
            {
                "markdown": ["### Step 2: Load the Titanic Dataset"],
                "code": [
                    'data_path = os.path.join("..", "data", "processed", "titanic.csv")\n',
                    "dataset = fs.load(data_path)\n\n",
                    'print(f"Dataset Source : {dataset.source}")\n',
                    'print(f"Row Count      : {dataset.row_count}")\n',
                    'print(f"Column Count   : {dataset.column_count}")\n',
                    'print(f"Columns        : {dataset.schema.names}")',
                ],
            },
            {
                "markdown": ["### Step 3: Run Vectorized Deterministic Profiling"],
                "code": [
                    "profile = fs.profile(dataset)\n",
                    'print(f"Overall Missingness: {profile.dataset_summary.missing_percentage:.2f}%")\n',
                    'print("\\nSample Column Profiles:")\n',
                    "for col, col_prof in list(profile.column_profiles.items())[:5]:\n",
                    '    print(f"  - {col:<15}: logical_type={col_prof.logical_type:<12} missing={col_prof.missing_count}")',
                ],
            },
            {
                "markdown": ["### Step 4: Run Automated Dataset Review & Scorecard"],
                "code": [
                    'review_result = fs.review(dataset, target_column="survived")\n',
                    "scorecard = fs.score(review_result)\n\n",
                    "if scorecard:\n",
                    '    print(f"ML Readiness Score: {scorecard.overall:.1f} / 100")\n',
                    '    print("\\nDimension Breakdown:")\n',
                    "    for dim in scorecard.dimensions:\n",
                    '        print(f"  - {dim.label:<20}: {dim.score:5.1f}/100 ({len(dim.contributing_findings)} findings)")',
                ],
            },
            {
                "markdown": [
                    "### Key Takeaways\n",
                    "- `fs.load()` normalizes files and DataFrames into a standard schema contract.\n",
                    "- `fs.profile()` executes ultra-fast Polars computations to extract shape and column descriptors.\n",
                    "- `fs.review()` runs 8 automated reviewers to inspect missingness, data types, and target leakage risk.\n",
                    "- `fs.score()` transforms review findings into an explainable 0–100 quality scorecard.",
                ]
            },
        ],
    )

    # =========================================================================
    # Notebook 2: Complete Dataset Review Walkthrough
    # =========================================================================
    nb2 = create_notebook(
        title="02 — Complete Dataset Review Walkthrough",
        description="Deep dive into Featuresmith's Review Engine — exploring the 8 automated reviewers, category filtering, finding severities, and remediation guidance.",
        sections=[
            {
                "markdown": [
                    "## 1. Why Automated Dataset Code Reviews Matter\n",
                    "Just as software engineers perform code reviews before merging pull requests, ML engineers must perform dataset code reviews before training models. ",
                    "Featuresmith's Review Engine runs 8 specialized reviewers to evaluate dataset health deterministically.\n\n",
                    "### The 8 Automated Reviewers\n",
                    "1. **Schema Health Reviewer**: Evaluates structural consistency and column naming.\n",
                    "2. **Data Types Reviewer**: Detects text types, numeric types, and type mismatches.\n",
                    "3. **Missing Values Reviewer**: Identifies column missingness ratios and null spikes.\n",
                    "4. **Duplicate Records Reviewer**: Checks for duplicate row entries.\n",
                    "5. **Constant Columns Reviewer**: Finds zero-variance and empty columns.\n",
                    "6. **High Cardinality Reviewer**: Flags categorical columns with excessive unique values.\n",
                    "7. **Basic Statistics Reviewer**: Analyzes distribution skewness and kurtosis anomalies.\n",
                    "8. **Leakage Risk Reviewer**: Evaluates target correlations, identifier shapes, and timestamp anomalies.",
                ]
            },
            {
                "markdown": ["### Step 1: Load Dataset & Run Complete Review"],
                "code": [
                    "import featuresmith as fs\n",
                    "import os\n\n",
                    'data_path = os.path.join("..", "data", "processed", "sales.csv")\n',
                    "dataset = fs.load(data_path)\n",
                    "review_res = fs.review(dataset)\n\n",
                    'print(f"Total Sections Evaluated : {len(review_res.sections)}")\n',
                    'print(f"Overall Summary          : {review_res.overall_summary}")',
                ],
            },
            {
                "markdown": ["### Step 2: Inspect Review Sections & Findings"],
                "code": [
                    "for section in review_res.sections:\n",
                    '    sev_str = section.severity.value if hasattr(section.severity, "value") else str(section.severity)\n',
                    '    print(f"[{sev_str.upper():<8}] {section.title} ({len(section.findings)} findings)")\n',
                    "    for finding in section.findings:\n",
                    "        print(f'     - Column: {finding.column_name or \"dataset\":<15} | {finding.title}')",
                ],
            },
            {
                "markdown": [
                    "### Best Practices & Common Mistakes\n",
                    "- **Best Practice**: Always run `fs.review()` before training baseline models to catch silent structural issues.\n",
                    "- **Common Mistake**: Ignoring `INFO` severity findings like text columns (`name`, `ticket`) that require specialized NLP tokenization or embedding preprocessing.",
                ]
            },
        ],
    )

    # =========================================================================
    # Notebook 3: Understanding the ML Readiness Score
    # =========================================================================
    nb3 = create_notebook(
        title="03 — Understanding the ML Readiness Score",
        description="Learn how Featuresmith computes an explainable 0–100 ML Readiness Score across 8 health dimensions with transparent mathematical weighting.",
        sections=[
            {
                "markdown": [
                    "## 1. What is the ML Readiness Score?\n",
                    "The ML Readiness Score answers a fundamental question: *'Is this dataset ready for model training?'*\n\n",
                    "It translates complex statistical findings into a single, explainable 0–100 score supported by 8 weighted health dimensions:\n",
                    "- **Schema Health** (Weight: 15%)\n",
                    "- **Missing Values** (Weight: 15%)\n",
                    "- **Duplicate Records** (Weight: 10%)\n",
                    "- **Data Types** (Weight: 10%)\n",
                    "- **Constant Columns** (Weight: 10%)\n",
                    "- **High Cardinality** (Weight: 10%)\n",
                    "- **Dataset Structure** (Weight: 10%)\n",
                    "- **Leakage Risk** (Weight: 20%)",
                ]
            },
            {
                "markdown": ["### Step 1: Compute Scorecard on California Housing"],
                "code": [
                    "import featuresmith as fs\n",
                    "import os\n\n",
                    'data_path = os.path.join("..", "data", "processed", "california_housing.csv")\n',
                    "dataset = fs.load(data_path)\n",
                    'review_res = fs.review(dataset, target_column="median_house_value")\n',
                    "scorecard = fs.score(review_res)\n\n",
                    "if scorecard:\n",
                    '    print(f"Overall ML Readiness Score: {scorecard.overall:.1f} / 100\\n")\n',
                    '    print(f\'{"Dimension":<22} | {"Score":<7} | {"Weight":<6} | Rationale\')\n',
                    '    print("-" * 70)\n',
                    "    for dim in scorecard.dimensions:\n",
                    '        print(f"{dim.label:<22} | {dim.score:5.1f}   | {dim.weight:4.2f}   | {dim.rationale[:35]}...")',
                ],
            },
            {
                "markdown": ["### Step 2: Extract Actionable Fix Suggestions"],
                "code": [
                    'print("Actionable Fix Suggestions to Improve Score:")\n',
                    "for dim in scorecard.dimensions:\n",
                    "    if dim.suggested_actions:\n",
                    '        print(f"\\n[{dim.label}]")\n',
                    "        for action in dim.suggested_actions:\n",
                    '            print(f"  -> {action}")',
                ],
            },
            {
                "markdown": [
                    "### Key Takeaways\n",
                    "- The ML Readiness Score is completely deterministic and reproducible.\n",
                    "- Dimensions use dedicated weights reflecting their operational impact on model training.\n",
                    "- Fix suggestions provide exact code and data pipeline remedies.",
                ]
            },
        ],
    )

    # =========================================================================
    # Notebook 4: Detecting Data Leakage
    # =========================================================================
    nb4 = create_notebook(
        title="04 — Detecting Data Leakage with Intelligent Leakage Detection",
        description="Master Intelligent Leakage Detection — discovering target correlations, timestamp anomalies, identifier shapes, and duplicate target copies before training.",
        sections=[
            {
                "markdown": [
                    "## 1. The High Cost of Data Leakage\n",
                    "Data leakage is one of the most dangerous bugs in applied machine learning. ",
                    "It occurs when information from the target variable or future state leaks into training features. ",
                    "Models achieve deceptively high validation metrics in development, only to fail completely in production.\n\n",
                    "### 6 Pattern Detectors in v0.2.0\n",
                    "1. **Target Correlation Detector**: Flags features with Pearson correlation >= 0.99 with the target.\n",
                    "2. **Identifier Shape Detector**: Flags near-unique numeric ID features correlated with the target.\n",
                    "3. **Timestamp Detector**: Identifies future timestamp columns encoding post-outcome information.\n",
                    "4. **Future Information Detector**: Identifies features named like outcome labels.\n",
                    "5. **Duplicate Target Detector**: Detects near-identical transformed copies of the target.\n",
                    "6. **Suspicious Correlation Detector**: Flags unexpected strong correlations (>= 0.95).",
                ]
            },
            {
                "markdown": [
                    "### Step 1: Analyze Customer Churn Dataset with Leakage Column"
                ],
                "code": [
                    "import featuresmith as fs\n",
                    "import os\n\n",
                    'data_path = os.path.join("..", "data", "processed", "customer_churn.csv")\n',
                    "dataset = fs.load(data_path)\n\n",
                    'review_res = fs.review(dataset, target_column="churn_label")\n\n',
                    "all_findings = [f for s in review_res.sections for f in s.findings]\n",
                    'leakage_findings = [f for f in all_findings if "leakage" in f.rule_id or "leakage" in f.title.lower()]\n\n',
                    'print(f"Total Leakage Findings Count: {len(leakage_findings)}\\n")\n',
                    "for finding in leakage_findings:\n",
                    '    print(f"[{finding.severity.upper()}] Column: {finding.column_name}")\n',
                    '    print(f"  Rule : {finding.rule_id}")\n',
                    '    print(f"  Title: {finding.title}")\n',
                    '    print(f"  Detail: {finding.description}\\n")',
                ],
            },
            {
                "markdown": [
                    "### Best Practices\n",
                    "- Always declare your target column when invoking `fs.review(dataset, target_column=...)`.\n",
                    "- Never deploy a model trained on features triggering `CRITICAL` target leakage findings.",
                ]
            },
        ],
    )

    # =========================================================================
    # Notebook 5: Comparing Dataset Versions with Dataset Diff
    # =========================================================================
    nb5 = create_notebook(
        title="05 — Comparing Dataset Versions with Dataset Diff Engine",
        description="Learn how to compare dataset snapshot versions with `fs.diff()` to prevent silent schema drift, missingness spikes, and quality regressions.",
        sections=[
            {
                "markdown": [
                    "## 1. Why Dataset Diffing Matters\n",
                    "In production ML pipelines, datasets evolve continuously. ",
                    "New snapshots arrive daily or weekly. Silent changes — such as dropped columns, renamed features, ",
                    "type shifts, or missing value spikes — can break model inference or corrupt retrained models.\n\n",
                    "Featuresmith's `fs.diff()` compares two dataset snapshots deterministically and provides an overall health verdict:\n",
                    "- **`unchanged`**: No material structural or quality changes.\n",
                    "- **`improved`**: Quality metrics improved (e.g., missingness decreased, leakage eliminated).\n",
                    "- **`regressed`**: Quality degraded (e.g., columns dropped, missingness spiked, schema broke).",
                ]
            },
            {
                "markdown": [
                    "### Step 1: Simulate Dataset Evolution (Snapshot v1 vs Snapshot v2)"
                ],
                "code": [
                    "import featuresmith as fs\n",
                    "import os\n",
                    "import pandas as pd\n\n",
                    'data_path = os.path.join("..", "data", "processed", "sales.csv")\n',
                    "v1 = pd.read_csv(data_path)\n\n",
                    "v2 = v1.copy()\n",
                    'v2.drop(columns=["store_version"], inplace=True)\n',
                    'v2["promo_code"] = "SUMMER2026"\n',
                    'v2.loc[:100, "discount"] = None\n\n',
                    'print(f"Snapshot v1 Shape: {v1.shape}")\n',
                    'print(f"Snapshot v2 Shape: {v2.shape}")',
                ],
            },
            {
                "markdown": ["### Step 2: Execute Dataset Diff Engine (`fs.diff`)"],
                "code": [
                    "diff_result = fs.diff(v1, v2)\n\n",
                    'print(f"Health Verdict : {diff_result.summary.overall_health.upper()}")\n',
                    'print(f"Recommendation : {diff_result.summary.recommendation}")\n',
                    'print(f"Added Columns  : {diff_result.schema.added_columns}")\n',
                    'print(f"Removed Columns: {diff_result.schema.removed_columns}")\n',
                    'print(f"Missingness Shift Count: {diff_result.summary.missing_values_increased}")',
                ],
            },
            {
                "markdown": [
                    "### Key Takeaways\n",
                    "- `fs.diff()` gives an immediate pass/fail verdict for dataset snapshot updates.\n",
                    "- It tracks structural, schema, quality, distribution, and leakage deltas in one canonical object.",
                ]
            },
        ],
    )

    # =========================================================================
    # Notebook 6: End-to-End ML Dataset Validation Workflow
    # =========================================================================
    nb6 = create_notebook(
        title="06 — End-to-End ML Dataset Validation Workflow",
        description="Build a production-ready ML dataset validation pipeline connecting dataset loading, automated review, readiness gating, and JSON export.",
        sections=[
            {
                "markdown": [
                    "## 1. Building a Production Pre-Training Gate\n",
                    "This notebook demonstrates how to build an end-to-end dataset validation pipeline in Python that can gate model training jobs automatically.",
                ]
            },
            {
                "markdown": ["### Step 1: Complete Pipeline Function"],
                "code": [
                    "import featuresmith as fs\n",
                    "import json\n",
                    "import os\n",
                    "import sys\n\n",
                    "def validate_and_gate_dataset(file_path: str, target_col: str, min_score: float = 80.0) -> bool:\n",
                    '    print(f"=== Validating Dataset: {file_path} ===")\n',
                    "    dataset = fs.load(file_path)\n",
                    "    review_res = fs.review(dataset, target_column=target_col)\n",
                    "    scorecard = fs.score(review_res)\n\n",
                    "    overall_score = scorecard.overall if scorecard else 0.0\n",
                    '    print(f"ML Readiness Score: {overall_score:.1f} / 100 (Threshold: {min_score:.1f})")\n\n',
                    "    all_findings = [f for s in review_res.sections for f in s.findings]\n",
                    '    critical_findings = [f for f in all_findings if f.severity == "critical" or (hasattr(f.severity, "value") and f.severity.value == "critical")]\n\n',
                    "    if critical_findings:\n",
                    '        print(f"❌ GATE FAILED: {len(critical_findings)} critical finding(s) detected!")\n',
                    "        for f in critical_findings:\n",
                    '            print(f"   - [{f.rule_id}] {f.title}")\n',
                    "        return False\n\n",
                    "    if overall_score < min_score:\n",
                    '        print(f"❌ GATE FAILED: Readiness score {overall_score:.1f} is below minimum threshold {min_score:.1f}.")\n',
                    "        return False\n\n",
                    '    print("✅ GATE PASSED: Dataset is clean and ready for model training.")\n',
                    "    return True\n\n",
                    'titanic_path = os.path.join("..", "data", "processed", "titanic.csv")\n',
                    'passed = validate_and_gate_dataset(titanic_path, target_col="survived", min_score=80.0)\n',
                    'print(f"Pipeline Gate Result: {passed}")',
                ],
            },
            {
                "markdown": [
                    "### Key Takeaways\n",
                    "- Featuresmith enables programmatic dataset quality gating in production pipelines.\n",
                    "- Zero external network dependencies ensure data remains 100% private and secure.",
                ]
            },
        ],
    )

    notebooks = {
        "01_getting_started.ipynb": nb1,
        "02_dataset_review.ipynb": nb2,
        "03_ml_readiness_score.ipynb": nb3,
        "04_leakage_detection.ipynb": nb4,
        "05_dataset_diff.ipynb": nb5,
        "06_end_to_end_workflow.ipynb": nb6,
    }

    for name, content in notebooks.items():
        out_path = nb_dir / name
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2)
        print(f"Generated notebook: {out_path}")


if __name__ == "__main__":
    build_all_notebooks()
