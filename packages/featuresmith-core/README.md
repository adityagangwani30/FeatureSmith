# featuresmith-core

`featuresmith-core` is the public Python SDK and deterministic analysis engine for Featuresmith.

It provides:

- `featuresmith.load()` for local CSV, Excel, Parquet, pandas, and Polars sources.
- `featuresmith.profile()` for reproducible tabular profiling.
- `featuresmith.analyze()` for data quality and leakage rule findings.
- Typed, serializable result dataclasses and a PEP 561 `py.typed` marker.

Install the staged pre-release version from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ featuresmith-core
```

*(Note: Upon final release, standard installation from public PyPI will be enabled: `pip install featuresmith-core`)*

For source development and full project documentation, see the repository README:
<https://github.com/adityagangwani30/FeatureSmith>
