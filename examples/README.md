# Featuresmith Examples & Educational Tutorials (v0.2.0)

Welcome to the Featuresmith examples repository! This collection provides production-ready example scripts and educational Jupyter Notebooks demonstrating how to use Featuresmith for dataset code reviews, ML readiness scoring, intelligent leakage detection, and dataset version diffing.

---

## 📚 Educational Jupyter Notebooks

Located in [`examples/notebooks/`](./notebooks/):

| Notebook | Topic | Description |
| :--- | :--- | :--- |
| [**`01_getting_started.ipynb`**](./notebooks/01_getting_started.ipynb) | Getting Started | Loading data (`fs.load`), profiling shapes (`fs.profile`), running reviews (`fs.review`), and extracting scorecards (`fs.score`). |
| [**`02_dataset_review.ipynb`**](./notebooks/02_dataset_review.ipynb) | Dataset Review Engine | In-depth walkthrough of the 8 automated reviewers, finding severities, and category filtering. |
| [**`03_ml_readiness_score.ipynb`**](./notebooks/03_ml_readiness_score.ipynb) | ML Readiness Scorecard | Understanding the 0–100 score across 8 health dimensions and actionable fix suggestions. |
| [**`04_leakage_detection.ipynb`**](./notebooks/04_leakage_detection.ipynb) | Intelligent Leakage Detection | Catching target correlations, timestamp anomalies, identifier shapes, and duplicate target copies. |
| [**`05_dataset_diff.ipynb`**](./notebooks/05_dataset_diff.ipynb) | Dataset Diff Engine | Comparing snapshot versions (`fs.diff`) to prevent silent schema drift and quality regressions. |
| [**`06_end_to_end_workflow.ipynb`**](./notebooks/06_end_to_end_workflow.ipynb) | End-to-End Pipeline Gate | Building a production Python validation function to gate ML model training jobs. |

---

## 🚀 Standalone Python Example Scripts

Executable scripts using real-world datasets:

- **[Titanic Classification](./titanic/run_sdk.py)**: Dataset code review targeting `survived` classification outcome.
- **[Customer Churn & Leakage](./customer_churn/run_sdk.py)**: Detecting hidden target leakage vectors on churn prediction datasets.
- **[California Housing Regression](./california_housing/run_sdk.py)**: Data quality review and missingness analysis for regression.
- **[Iris Classification](./iris/run_sdk.py)**: Clean baseline review demonstrating a 100/100 ML Readiness Score.
- **[Sales Snapshot Diff](./sales/run_sdk.py)**: Demonstrating `fs.diff()` snapshot comparisons across evolving datasets.

---

## ⚙️ Running the Examples

### 1. Prepare Data

```bash
python examples/prepare_datasets.py
```

### 2. Run Example Script

```bash
python examples/titanic/run_sdk.py
```

### 3. Run Notebooks

```bash
jupyter lab examples/notebooks/
```

---

## 🔗 Related Resources

- [📖 Main Documentation Website](https://featuresmith.adityagangwani.me)
- [📦 Installation Guide](../README.md#installation)
- [⚡ CLI Reference](https://featuresmith.adityagangwani.me/docs/cli/review)
