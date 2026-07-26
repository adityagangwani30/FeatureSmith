# featuresmith-cli

`featuresmith-cli` is the thin command-line interface for Featuresmith.

It exposes the `featuresmith` console command and delegates analysis work to
`featuresmith-core`.

Install it with:

```bash
pip install featuresmith-core featuresmith-cli
```

Run an analysis:

```bash
featuresmith analyze customers.csv
featuresmith analyze customers.csv --target churn --format json
featuresmith --version
```

For source development and full project documentation, see the repository README:
<https://github.com/adityagangwani30/FeatureSmith>
