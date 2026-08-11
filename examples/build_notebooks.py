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

    # Clean out deprecated notebook names if present
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
        description="Learn the fundamentals of Featuresmith — loading tabular datasets, inspecting Dataset descriptors, deterministic statistical profiling, automated dataset code reviews, and ML readiness scoring.",
        sections=[
            {
                "markdown": [
                    "## 1. Problem Statement & Why This Capability Matters\n",
                    "Machine learning failure modes often originate from dataset quality rather than model architecture choices. ",
                    "Featuresmith brings developer-first code review discipline to tabular datasets before training begins.\n\n",
                    "### Objectives\n",
                    "1. Understand Featuresmith's package structure (`featuresmith-core` and `featuresmith-cli`).\n",
                    "2. Load tabular data from CSV, Parquet, Excel, or DataFrames using `fs.load()`.\n",
                    "3. Inspect `Dataset` properties (`row_count`, `column_count`, `dtypes`, `source`, `preview()`).\n",
                    "4. Profile datasets deterministically with `fs.profile()`.\n",
                    "5. Perform an automated dataset code review with `fs.review()`.\n",
                    "6. Extract an explainable 0–100 ML Readiness Score with `fs.score()`.",
                ]
            },
            {
                "markdown": ["### Step 1: Import Featuresmith & Verify Version"],
                "code": [
                    "import featuresmith as fs\n",
                    "import os\n",
                    "import pandas as pd\n\n",
                    'print(f"Featuresmith Version: {fs.__version__}")',
                ],
            },
            {
                "markdown": [
                    "### Step 2: Load Tabular Datasets & Inspect Dataset Objects\n",
                    "`fs.load()` normalizes local files (`.csv`, `.parquet`, `.xlsx`) and in-memory DataFrames into a shallowly immutable `Dataset` contract without copying memory buffers.",
                ],
                "code": [
                    'data_path = os.path.join("..", "data", "processed", "titanic.csv")\n',
                    "dataset = fs.load(data_path)\n\n",
                    'print(f"Dataset Source : {dataset.source}")\n',
                    'print(f"Backend Engine : {dataset.backend}")\n',
                    'print(f"Row Count      : {dataset.row_count}")\n',
                    'print(f"Column Count   : {dataset.column_count}")\n',
                    'print(f"Columns        : {dataset.schema.names}")\n\n',
                    "# Preview first 3 rows\n",
                    "print('\\nData Preview:')\n",
                    "print(dataset.preview(3))",
                ],
            },
            {
                "markdown": [
                    "### Step 3: Load In-Memory DataFrame using `from_dataframe` or `load`"
                ],
                "code": [
                    'df = pd.DataFrame({"age": [25, 30, 35], "income": [50000.0, 65000.0, 80000.0]})\n',
                    "ds_mem = fs.load(df)\n",
                    'print(f"In-Memory Dataset Row Count: {ds_mem.row_count}, Columns: {ds_mem.column_count}")',
                ],
            },
            {
                "markdown": [
                    "### Step 4: Run Vectorized Deterministic Profiling\n",
                    "`fs.profile()` computes statistical descriptors (min, max, mean, quantiles, missingness, cardinality, correlations) deterministically.",
                ],
                "code": [
                    "profile = fs.profile(dataset)\n",
                    'print(f"Overall Missingness: {profile.dataset_summary.missing_percentage:.2f}%")\n',
                    'print("\\nSample Column Profiles:")\n',
                    "for col, col_prof in list(profile.column_profiles.items())[:5]:\n",
                    '    print(f"  - {col:<15}: logical_type={col_prof.logical_type:<12} missing={col_prof.missing_count}")',
                ],
            },
            {
                "markdown": [
                    "### Step 5: Run Automated Dataset Review & Scorecard\n",
                    "`fs.review()` evaluates dataset health across 8 specialized reviewers, while `fs.score()` extracts an overall ML Readiness Scorecard.",
                ],
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
                    "### Key Takeaways & Connection to Next Tutorial\n",
                    "- `fs.load()` normalizes files and DataFrames into a standard schema contract.\n",
                    "- `fs.profile()` executes ultra-fast computations to extract shape and column descriptors.\n",
                    "- `fs.review()` runs 8 automated reviewers to inspect missingness, data types, and target leakage risk.\n",
                    "- `fs.score()` transforms review findings into an explainable 0–100 quality scorecard.\n\n",
                    "**Next Tutorial**: In `02_dataset_review.ipynb`, we explore the Review Engine's 8 automated reviewers, category filtering, reviewer configuration, and text output rendering.",
                ]
            },
        ],
    )

    # =========================================================================
    # Notebook 2: Complete Dataset Review Walkthrough
    # =========================================================================
    nb2 = create_notebook(
        title="02 — Complete Dataset Review Walkthrough",
        description="Deep dive into Featuresmith's Review Engine — exploring the 8 automated reviewers, category filtering, finding severities, reviewer configuration, and formatted text report rendering.",
        sections=[
            {
                "markdown": [
                    "## 1. Why Automated Dataset Code Reviews Matter\n",
                    "Just as software engineers perform code reviews before merging pull requests, ML engineers must perform dataset code reviews before training models. ",
                    "Featuresmith's Review Engine runs 8 specialized reviewers to evaluate dataset health deterministically.\n\n",
                    "### The 8 Automated Reviewers in v0.2.0\n",
                    "1. **Schema Health Reviewer**: Evaluates structural consistency and column naming.\n",
                    "2. **Data Types Reviewer**: Detects text types, numeric types, and type mismatches.\n",
                    "3. **Missing Values Reviewer**: Identifies column missingness ratios and null spikes.\n",
                    "4. **Duplicate Records Reviewer**: Checks for duplicate row entries.\n",
                    "5. **Constant Columns Reviewer**: Finds zero-variance and empty columns.\n",
                    "6. **High Cardinality Reviewer**: Flags categorical columns with excessive unique values.\n",
                    "7. **Basic Statistics Reviewer**: Analyzes distribution skewness and kurtosis anomalies.\n",
                    "8. **Leakage Risk Reviewer**: Evaluates target correlations, identifier shapes, timestamp anomalies, and duplicate targets.",
                ]
            },
            {
                "markdown": [
                    "### Prerequisite: Prepare the Sales Dataset\n",
                    "This notebook loads `examples/data/processed/sales.csv`, which `examples/prepare_datasets.py` generates deterministically (no network). From the repository root, run:\n\n",
                    "```bash\n",
                    "python examples/prepare_datasets.py\n",
                    "```\n",
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
                    "### Step 3: Filter Review Categories & Configure Reviewers\n",
                    "You can pass `enabled_categories` as a list of the public `fs.ReviewCategory` enum members (e.g. `[fs.ReviewCategory.QUALITY, fs.ReviewCategory.LEAKAGE]`) or configure specific reviewer thresholds via `reviewer_config`.\n\n",
                    "Filtering to the `QUALITY` and `LEAKAGE` categories runs the 5 quality reviewers plus the leakage reviewer, for 6 sections total.",
                ],
                "code": [
                    "custom_review = fs.review(\n",
                    "    dataset,\n",
                    "    enabled_categories=[\n",
                    "        fs.ReviewCategory.QUALITY,\n",
                    "        fs.ReviewCategory.LEAKAGE,\n",
                    "    ],\n",
                    "    reviewer_config={\n",
                    '        "review.quality.missingness": {"threshold": 10.0}\n',
                    "    }\n",
                    ")\n",
                    'print(f"Filtered Review Sections Count: {len(custom_review.sections)}")',
                ],
            },
            {
                "markdown": [
                    "### Step 4: Render Formatted Text Report with `fs.render()`"
                ],
                "code": [
                    'report_text = fs.render(review_res, target="console")\n',
                    'print("=== Formatted Text Report Preview ===")\n',
                    'print(report_text[:600] + "\\n...")',
                ],
            },
            {
                "markdown": [
                    "### Key Takeaways & Connection to Next Tutorial\n",
                    "- `fs.review()` evaluates dataset health across 8 reviewers deterministically.\n",
                    "- Category filtering (`enabled_categories`) and reviewer threshold overrides (`reviewer_config`) allow custom validation rules.\n",
                    "- `fs.render(review_res)` generates formatted console text reports.\n\n",
                    "**Next Tutorial**: In `03_ml_readiness_score.ipynb`, we explore the 0–100 ML Readiness Scorecard, health dimension weights, deduction math, and actionable fix suggestions.",
                ]
            },
        ],
    )

    # =========================================================================
    # Notebook 3: Understanding the ML Readiness Score
    # =========================================================================
    nb3 = create_notebook(
        title="03 — Understanding the ML Readiness Score",
        description="Learn how Featuresmith computes an explainable 0–100 ML Readiness Score across 8 health dimensions with transparent mathematical weighting, deduction rules, and actionable fix suggestions.",
        sections=[
            {
                "markdown": [
                    "## 1. What is the ML Readiness Score?\n",
                    "The ML Readiness Score answers a fundamental question: *'Is this dataset ready for model training?'*\n\n",
                    "It translates complex statistical findings into a single, explainable 0–100 score supported by 8 health dimensions:\n",
                    "- **Schema Health**\n",
                    "- **Missing Values**\n",
                    "- **Duplicate Records**\n",
                    "- **Data Types**\n",
                    "- **Constant Columns**\n",
                    "- **High Cardinality**\n",
                    "- **Dataset Structure**\n",
                    "- **Leakage Risk**\n\n",
                    "In v0.2.0 every dimension carries the same default weight of `1.0`, so the overall score is the plain arithmetic mean of the applicable dimension scores. (Per-dimension weight configuration is a documented future capability, not yet configurable.)\n\n",
                    "### Deduction Rules\n",
                    "Base score per dimension starts at 100. Findings deduct points based on severity:\n",
                    "- **CRITICAL finding**: -30 points\n",
                    "- **WARNING finding**: -15 points\n",
                    "- **INFO finding**: -5 points\n",
                    "Scores are clamped to [0, 100] and rounded to one decimal place.",
                ]
            },
            {
                "markdown": [
                    "### Prerequisite: Prepare the California Housing Dataset\n",
                    "This notebook loads `examples/data/processed/california_housing.csv`, which the example scripts generate and which is **not** bundled in the repository. From the repository root, run the two preparation steps first:\n\n",
                    "```bash\n",
                    "python examples/download_datasets.py  # network fetch (requires scikit-learn)\n",
                    "python examples/prepare_datasets.py\n",
                    "```\n",
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
                    "### Key Takeaways & Connection to Next Tutorial\n",
                    "- The ML Readiness Score is completely deterministic and reproducible.\n",
                    "- Dimensions currently use uniform `1.0` weights, so the overall score is a simple mean of the applicable dimension scores.\n",
                    "- Fix suggestions provide exact data pipeline remedies.\n\n",
                    "**Next Tutorial**: In `04_leakage_detection.ipynb`, we dive deep into Intelligent Leakage Detection and the 6 pattern detectors that prevent target leakage bugs.",
                ]
            },
        ],
    )

    # =========================================================================
    # Notebook 4: Detecting Data Leakage
    # =========================================================================
    nb4 = create_notebook(
        title="04 — Detecting Data Leakage with Intelligent Leakage Detection",
        description="Master Intelligent Leakage Detection — discovering target correlations, timestamp anomalies, identifier shapes, post-outcome feature names, and duplicate target copies before model training.",
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
                    "4. **Future Information Detector**: Identifies features named like outcome labels (e.g., `refund_date`, `is_cancelled`).\n",
                    "5. **Duplicate Target Detector**: Detects near-identical transformed copies of the target.\n",
                    "6. **Suspicious Correlation Detector**: Flags unexpected strong correlations (>= 0.95).",
                ]
            },
            {
                "markdown": [
                    "### Prerequisite: Prepare the Customer Churn Dataset\n",
                    "This notebook loads `examples/data/processed/customer_churn.csv`, which the example scripts generate and which is **not** bundled in the repository. From the repository root, run the two preparation steps first:\n\n",
                    "```bash\n",
                    "python examples/download_datasets.py  # network fetch (requires scikit-learn)\n",
                    "python examples/prepare_datasets.py\n",
                    "```\n",
                ]
            },
            {
                "markdown": [
                    "### Step 1: Analyze Customer Churn Dataset with Leakage Columns"
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
                    "### Key Takeaways & Connection to Next Tutorial\n",
                    "- Always declare your target column when invoking `fs.review(dataset, target_column=...)`.\n",
                    "- Never deploy a model trained on features triggering `CRITICAL` target leakage findings.\n\n",
                    "**Next Tutorial**: In `05_dataset_diff.ipynb`, we explore the Dataset Diff Engine (`fs.diff`) to compare dataset snapshot versions.",
                ]
            },
        ],
    )

    # =========================================================================
    # Notebook 5: Comparing Dataset Versions with Dataset Diff
    # =========================================================================
    nb5 = create_notebook(
        title="05 — Comparing Dataset Versions with Dataset Diff Engine",
        description="Learn how to compare dataset snapshot versions with `fs.diff()`, `fs.diff_findings()`, and `fs.render_diff()` to prevent silent schema drift, missingness spikes, and quality regressions.",
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
                    "### Prerequisite: Prepare the Sales Dataset\n",
                    "This notebook loads `examples/data/processed/sales.csv`, which `examples/prepare_datasets.py` generates deterministically (no network). From the repository root, run:\n\n",
                    "```bash\n",
                    "python examples/prepare_datasets.py\n",
                    "```\n",
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
                    "### Step 3: Extract Diff Findings & Render Diff Text Report\n",
                    "Use `fs.diff_findings()` to extract `RuleFinding` objects from a diff result, and `fs.render_diff()` for terminal output.",
                ],
                "code": [
                    "findings = fs.diff_findings(diff_result)\n",
                    'print(f"Derived Diff Findings Count: {len(findings)}")\n',
                    "for f in findings[:3]:\n",
                    '    print(f"  - [{f.severity.upper()}] {f.title}")\n\n',
                    'diff_report = fs.render_diff(diff_result, target="console")\n',
                    'print("\\n=== Formatted Diff Text Report Preview ===")\n',
                    'print(diff_report[:500] + "\\n...")',
                ],
            },
            {
                "markdown": [
                    "### Key Takeaways & Connection to Next Tutorial\n",
                    "- `fs.diff()` gives an immediate pass/fail verdict for dataset snapshot updates.\n",
                    "- It tracks structural, schema, quality, distribution, and leakage deltas in one canonical object.\n",
                    "- `fs.diff_findings()` converts diff deltas into standard `RuleFinding` objects for CI exit code gating.\n\n",
                    "**Next Tutorial**: In `06_end_to_end_workflow.ipynb`, we build a production pre-training pipeline gate that integrates review, scoring, and error handling.",
                ]
            },
        ],
    )

    # =========================================================================
    # Notebook 6: End-to-End ML Dataset Validation Workflow
    # =========================================================================
    nb6 = create_notebook(
        title="06 — End-to-End ML Dataset Validation Workflow",
        description="Build a production-ready ML dataset validation pipeline connecting dataset loading, automated review, readiness gating, error handling, and JSON export.",
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
                    "from featuresmith.core.exceptions import ConnectorError\n",
                    "import json\n",
                    "import os\n",
                    "import sys\n\n",
                    "def validate_and_gate_dataset(file_path: str, target_col: str, min_score: float = 80.0) -> bool:\n",
                    '    print(f"=== Validating Dataset: {file_path} ===")\n',
                    "    try:\n",
                    "        dataset = fs.load(file_path)\n",
                    "    except ConnectorError as err:\n",
                    '        print(f"❌ GATE FAILED: Connector Error loading {file_path}: {err}")\n',
                    "        return False\n\n",
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
                    "### Key Takeaways & Connection to Next Tutorial\n",
                    "- Featuresmith enables programmatic dataset quality gating in production pipelines.\n",
                    "- Zero external network dependencies ensure data remains 100% private and secure.\n\n",
                    "**Next Tutorial**: In `07_custom_rules_and_extensions.ipynb`, we learn how to extend `BaseRule` to write custom domain-specific validation rules.",
                ]
            },
        ],
    )

    # =========================================================================
    # Notebook 7: Custom Rules and Advanced Extensions
    # =========================================================================
    nb7 = create_notebook(
        title="07 — Custom Rules and Advanced Extensions",
        description="Learn how to extend `BaseRule` to create custom quality rules, register them in `RuleRegistry`, and execute them via `RuleEngine` or `fs.analyze()`.",
        sections=[
            {
                "markdown": [
                    "## 1. Custom Rule Engineering\n",
                    "Featuresmith is designed to be fully extensible. While built-in rules cover standard statistical quality and leakage checks, business-specific constraints (e.g., negative balances, invalid transaction ranges, proprietary schema rules) can be implemented by inheriting from `BaseRule`.\n\n",
                    "### The `BaseRule` Interface\n",
                    "Custom rules implement six required properties/methods:\n",
                    "- `id`: Unique dot-separated rule identifier (e.g. `custom.zero_variance`).\n",
                    "- `name`: Human-readable title.\n",
                    "- `description`: Summary of rule check.\n",
                    "- `category`: Category string (`quality`, `statistical`, `leakage`, or `custom`).\n",
                    "- `severity`: Default severity (`critical`, `warning`, `info`).\n",
                    "- `enabled_by_default`: Boolean flag.\n",
                    "- `evaluate(profile: ProfileResult) -> list[RuleFinding]`: Evaluation logic consuming a precomputed `ProfileResult`.",
                ]
            },
            {
                "markdown": [
                    "### Prerequisite: Prepare the Sales Dataset\n",
                    "This notebook loads `examples/data/processed/sales.csv`, which `examples/prepare_datasets.py` generates deterministically (no network). From the repository root, run:\n\n",
                    "```bash\n",
                    "python examples/prepare_datasets.py\n",
                    "```\n",
                ]
            },
            {
                "markdown": ["### Step 1: Implement a Custom `ZeroVarianceRule`"],
                "code": [
                    "from featuresmith.core.profile_result import ProfileResult\n",
                    "from featuresmith.core.rule_finding import RuleFinding\n",
                    "from featuresmith.rules.base import BaseRule\n",
                    "import featuresmith as fs\n",
                    "import os\n\n",
                    "class ZeroVarianceRule(BaseRule):\n",
                    '    """Detect numeric columns with zero standard deviation."""\n',
                    "    @property\n",
                    "    def id(self) -> str:\n",
                    '        return "custom.zero_variance"\n\n',
                    "    @property\n",
                    "    def name(self) -> str:\n",
                    '        return "Zero Variance Numeric Columns"\n\n',
                    "    @property\n",
                    "    def description(self) -> str:\n",
                    '        return "Flags numeric columns with zero observed standard deviation."\n\n',
                    "    @property\n",
                    "    def category(self) -> str:\n",
                    '        return "custom"\n\n',
                    "    @property\n",
                    "    def severity(self) -> str:\n",
                    '        return "warning"\n\n',
                    "    @property\n",
                    "    def enabled_by_default(self) -> bool:\n",
                    "        return True\n\n",
                    "    def evaluate(self, profile: ProfileResult) -> list[RuleFinding]:\n",
                    "        findings: list[RuleFinding] = []\n",
                    "        for col_name, num_prof in profile.numeric_profiles.items():\n",
                    "            if num_prof.std_dev == 0.0:\n",
                    "                findings.append(\n",
                    "                    RuleFinding(\n",
                    "                        rule_id=self.id,\n",
                    "                        rule_name=self.name,\n",
                    "                        category=self.category,\n",
                    "                        severity=self.severity,\n",
                    "                        column_name=col_name,\n",
                    '                        title="Zero Variance Detected",\n',
                    "                        description=f\"Numeric column '{col_name}' has standard deviation of 0.0.\",\n",
                    '                        evidence={"std_dev": num_prof.std_dev}\n',
                    "                    )\n",
                    "                )\n",
                    "        return findings\n\n",
                    'print("Custom ZeroVarianceRule defined successfully.")',
                ],
            },
            {
                "markdown": [
                    "### Step 2: Register & Evaluate Custom Rule Against Profile"
                ],
                "code": [
                    "from featuresmith.rules.registry import default_registry\n\n",
                    "# Instantiate the custom rule and add it to a RuleRegistry\n",
                    "custom_rule = ZeroVarianceRule()\n",
                    "registry = default_registry()\n",
                    "registry.register(custom_rule)\n\n",
                    'data_path = os.path.join("..", "data", "processed", "sales.csv")\n',
                    "dataset = fs.load(data_path)\n",
                    "profile = fs.profile(dataset)\n\n",
                    "# Evaluate the custom rule directly\n",
                    "findings = custom_rule.evaluate(profile)\n\n",
                    'print(f"Rule ID             : {custom_rule.id}")\n',
                    'print(f"Registered Rules    : {len(registry.list_rules())}")\n',
                    'print(f"Direct Findings     : {len(findings)}")\n',
                    "for f in findings:\n",
                    '    print(f"  - [{f.severity.upper()}] Column: {f.column_name} | {f.title}")',
                ],
            },
            {
                "markdown": [
                    "### Key Takeaways\n",
                    "- `BaseRule` allows developers to add custom, business-specific quality checks.\n",
                    "- Custom rules operate deterministically on precomputed `ProfileResult` descriptors.\n",
                    "- `RuleRegistry` maintains registered rule instances for execution engines.",
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
        "07_custom_rules_and_extensions.ipynb": nb7,
    }

    for name, content in notebooks.items():
        out_path = nb_dir / name
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2)
        print(f"Generated notebook: {out_path}")


if __name__ == "__main__":
    build_all_notebooks()
