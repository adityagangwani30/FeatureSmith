# featuresmith-core

[![PyPI Version](https://img.shields.io/pypi/v/featuresmith-core.svg)](https://pypi.org/project/featuresmith-core/)
[![Python Version](https://img.shields.io/pypi/pyversions/featuresmith-core.svg)](https://pypi.org/project/featuresmith-core/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

`featuresmith-core` is the Python SDK and deterministic analysis engine for **Featuresmith** — the open-source Dataset Review Platform for structured data.

It provides automated dataset code reviews, 0–100 ML readiness scores, target leakage detection, version snapshot diffing, and deterministic transformation planning.

## Key Capabilities

- **Dataset Ingestion (`fs.load()`)**: Native support for CSV, Excel, Parquet, pandas, and Polars DataFrames.
- **Automated Dataset Review (`fs.review()`)**: 10 built-in reviewers evaluating schema health, missingness, duplicates, constants, cardinality, statistics, target leakage, snapshot deltas, and feature quality.
- **ML Readiness Score (`fs.score()`)**: An explainable 0–100 quality scorecard calculated across 7 effective health dimensions.
- **Intelligent Leakage Detection**: 6 named pattern detectors recognizing target correlation, identifier shape, timestamp anomalies, and duplicate targets.
- **Dataset Diff Engine (`fs.diff()`)**: Version snapshot comparison engine surfacing schema drift, null spikes, and quality regressions between two datasets.
- **Recommendation Engine & Plan Primitive (`fs.plan()`)**: Centralized engine merging review findings into ranked fix recommendations and compiling accepted items into inspectable, deterministic `Plan` objects.

## Installation

```bash
pip install featuresmith-core
```

## Quick Start (Python SDK)

```python
import featuresmith as fs

# 1. Load dataset
dataset = fs.load("data/train.csv")

# 2. Run automated dataset code review
review_res = fs.review(dataset, target_column="target")

# 3. Extract 0-100 ML Readiness Scorecard
scorecard = fs.score(review_res)
if scorecard:
    print(f"ML Readiness Score: {scorecard.overall}/100")

# 4. Compile an inspectable Plan from accepted recommendations
plan = fs.plan(review_res, accept=["rec.quality.missingness.cabin"])
for item in plan.items:
    print(f"Plan Step: {item.title} (confidence {item.confidence})")
```

For comprehensive guides and API reference, visit the official website:
<https://featuresmith.adityagangwani.me>
