# featuresmith-cli

`featuresmith-cli` is the thin command-line interface for Featuresmith.

It exposes the `featuresmith` console command and delegates analysis work to
`featuresmith-core`.

Install featuresmith-core and featuresmith-cli directly from PyPI:

```bash
pip install featuresmith-core featuresmith-cli
```

Run an analysis:

```bash
featuresmith analyze customers.csv
featuresmith analyze customers.csv --target churn --format json
featuresmith --version
```

For comprehensive guides and API reference, visit the official website:
<https://featuresmith.adityagangwani.me>
