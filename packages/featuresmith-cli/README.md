# featuresmith-cli

`featuresmith-cli` is the thin command-line interface for Featuresmith.

It exposes the `featuresmith` console command and delegates analysis work to
`featuresmith-core`.

Install the staged pre-release versions from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ featuresmith-core featuresmith-cli
```

*(Note: Upon final release, standard installation from public PyPI will be enabled: `pip install featuresmith-core featuresmith-cli`)*

Run an analysis:

```bash
featuresmith analyze customers.csv
featuresmith analyze customers.csv --target churn --format json
featuresmith --version
```

For source development and full project documentation, see the repository README:
<https://github.com/adityagangwani30/FeatureSmith>
