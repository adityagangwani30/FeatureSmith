import Link from "next/link"
import { notFound } from "next/navigation"
import { ChevronRight, Info, AlertTriangle, AlertCircle, CheckCircle2, Terminal as TerminalIcon } from "lucide-react"
import { CodeBlock } from "@/components/ui/code-block"

// Types for content mapping
interface DocContent {
  title: string
  subtitle: string
  category: string
  seoTitle: string
  seoDescription: string
  render: () => React.JSX.Element
}

// A dictionary mapping URL slugs to rich document structures
const DOCS_MAP: Record<string, DocContent> = {
  "installation": {
    title: "Installation",
    subtitle: "Install Featuresmith and set up your workspace",
    category: "Getting Started",
    seoTitle: "Installation",
    seoDescription: "Install Featuresmith via pip, uv, or build it from source.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Featuresmith is built for Python 3.11+. It can be installed as a library,
          as a CLI, or built directly from source for local development. We recommend using <code>uv</code> for package management.
        </p>

        <section className="mb-8" aria-labelledby="install-uv">
          <h3 id="install-uv" className="mb-3 text-lg font-semibold text-foreground">Using uv (Recommended)</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Add Featuresmith to your workspace dependencies:
          </p>
          <CodeBlock code="uv add featuresmith-core" language="bash" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="install-pip">
          <h3 id="install-pip" className="mb-3 text-lg font-semibold text-foreground">Using pip</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Install the latest version of the core library from PyPI:
          </p>
          <CodeBlock code="pip install featuresmith-core" language="bash" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="install-cli">
          <h3 id="install-cli" className="mb-3 text-lg font-semibold text-foreground">Installing the CLI</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            To use the command line tool, install the CLI surface wrapper:
          </p>
          <CodeBlock code="pip install featuresmith-core featuresmith-cli" language="bash" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="install-source">
          <h3 id="install-source" className="mb-3 text-lg font-semibold text-foreground">From Source (Development)</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            For local contribution or editing:
          </p>
          <CodeBlock code={`git clone https://github.com/adityagangwani30/FeatureSmith.git
cd FeatureSmith
uv sync --all-packages
pre-commit install`} language="bash" showCopy />
        </section>
      </>
    )
  },
  "quickstart": {
    title: "Quick Start",
    subtitle: "Get up and running with the SDK and CLI in under 5 minutes",
    category: "Getting Started",
    seoTitle: "Quick Start Guide",
    seoDescription: "Load, profile, and analyze a dataset in 3 lines using the Python SDK or CLI.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Featuresmith is designed to serve identical results whether you are running
          scripted pipelines in Python or triggering quick inspections in the terminal.
        </p>

        <section className="mb-8" aria-labelledby="qs-sdk">
          <h3 id="qs-sdk" className="mb-3 text-lg font-semibold text-foreground">Python SDK Quick Start</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Analyze a dataset and print quality findings:
          </p>
          <CodeBlock code={`import featuresmith as fs

# 1. Load a tabular dataset (CSV, Parquet, Excel, or DataFrames)
dataset = fs.load("customers.csv")
print(f"Loaded {dataset.row_count} rows.")

# 2. Extract deterministic statistical profiles
profile = fs.profile("customers.csv")

# 3. Perform rule-based data quality & target leakage checks
result = fs.analyze("customers.csv", target_column="churn")

for finding in result.findings:
    print(f"[{finding.severity.upper()}] {finding.title} in column '{finding.column_name}'")
    print(f"  Reason: {finding.description}")`} language="python" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="qs-cli">
          <h3 id="qs-cli" className="mb-3 text-lg font-semibold text-foreground">CLI Quick Start</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Verify dataset issues inside your shell:
          </p>
          <CodeBlock code={`# Analyze a local CSV dataset
featuresmith analyze customers.csv

# Run leakage checks targeting the 'churn' column
featuresmith analyze customers.csv --target churn

# Export findings to report.json in machine-readable format
featuresmith analyze customers.csv --format json --output report.json`} language="bash" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="qs-exitcodes">
          <h3 id="qs-exitcodes" className="mb-3 text-lg font-semibold text-foreground">CLI Exit Codes</h3>
          <p className="mb-4 text-sm text-muted-foreground">
            The CLI uses precise exit codes to facilitate pipeline integration and gating:
          </p>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="min-w-full divide-y divide-border text-left text-sm">
              <thead className="bg-muted/50 text-xs font-semibold uppercase tracking-wider text-foreground">
                <tr>
                  <th className="px-4 py-3">Exit Code</th>
                  <th className="px-4 py-3">Description</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-muted-foreground">
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground">0</td>
                  <td className="px-4 py-3">Clean — no rule violations detected at or above the threshold.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground">1</td>
                  <td className="px-4 py-3">Findings detected — one or more rules triggered at or above threshold.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground">2</td>
                  <td className="px-4 py-3">Invalid input — bad flags, missing arguments, or columns not in schema.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground">3</td>
                  <td className="px-4 py-3">File load failure — file does not exist, or parser error.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground">4</td>
                  <td className="px-4 py-3">Unexpected internal error (use <code>--verbose</code> for traceback).</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </>
    )
  },
  "concepts/dataset": {
    title: "Dataset Layer",
    subtitle: "Unified tabular dataset and schema representation",
    category: "Core Concepts",
    seoTitle: "Dataset Concept",
    seoDescription: "Learn how Featuresmith wraps CSV, Excel, Parquet, and in-memory DataFrames into a normalized Dataset descriptor.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Tabular data formats are fragmented. Columns might have different names, null indicators, or types depending on the file format or parsing engine. The **Dataset Layer** is a normalized layer that wraps tabular sources into an immutable, structured contract.
        </p>

        <section className="mb-8" aria-labelledby="ds-connectors">
          <h3 id="ds-connectors" className="mb-3 text-lg font-semibold text-foreground">Implemented Connectors</h3>
          <p className="mb-4 text-sm text-muted-foreground">
            Featuresmith Phase 1 implements five deterministic connectors out of the box:
          </p>
          <ul className="space-y-3 text-sm text-muted-foreground" role="list">
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>CSV Connector:</strong> High-performance CSV ingestion powered by <code>Polars</code>.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>Parquet Connector:</strong> Zero-copy columnar reader powered by <code>Polars</code>.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>Excel Connector:</strong> Reads tabular files (loads first worksheet only) powered by <code>pandas</code>.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>pandas DataFrame Connector:</strong> In-memory pandas interop, zero memory overhead.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>Polars DataFrame Connector:</strong> In-memory Polars interop, fully lazy-compatible.</span>
            </li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="ds-errors">
          <h3 id="ds-errors" className="mb-3 text-lg font-semibold text-foreground">Robust Ingestion & Errors</h3>
          <p className="mb-4 text-sm text-muted-foreground">
            Load errors are structured and do not expose raw table data, ensuring security and robust error gating. When loading fails, a typed <code>ConnectorError</code> is raised.
          </p>
          <CodeBlock code={`from featuresmith.core.exceptions import ConnectorError
import featuresmith as fs

try:
    dataset = fs.load("non_existent.csv")
except ConnectorError as e:
    print(f"Loading failed: {e}")`} language="python" showCopy />
        </section>
      </>
    )
  },
  "concepts/profiling": {
    title: "Profiling Engine",
    subtitle: "High-speed deterministic data profiling",
    category: "Core Concepts",
    seoTitle: "Profiling Concept",
    seoDescription: "Understand Featuresmith's deterministic profiling statistics and correlation matrices.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Most profiling tools generate heavy charts that are slow to load and hard to use programmatically. Featuresmith does not compute layout charts in core; it computes **deterministic statistical descriptors** returned as a typed, serializable <code>ProfileResult</code>.
        </p>

        <section className="mb-8" aria-labelledby="prof-metrics">
          <h3 id="prof-metrics" className="mb-3 text-lg font-semibold text-foreground">Statistical Coverage</h3>
          <p className="mb-4 text-sm text-muted-foreground">
            The profiling engine executes optimized, batched vectorized computations to compile:
          </p>
          <ul className="space-y-3 text-sm text-muted-foreground" role="list">
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>23 Numeric Metrics:</strong> Mean, median, min, max, standard deviation, variance, skewness, kurtosis, quantiles (IQR, 90th, 95th, 99th), sum, and range.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>Categorical Profiles:</strong> Cardinality, unique count, entropy, top frequency tables, and null/missing rates.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>Datetime Profiles:</strong> Minimum, maximum, and total datetime span in days.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>Text Profiles:</strong> String length statistics, character count, whitespace-only check, and missing rates.</span>
            </li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="prof-correlations">
          <h3 id="prof-correlations" className="mb-3 text-lg font-semibold text-foreground">Correlation Safeguard</h3>
          <p className="mb-4 text-sm text-muted-foreground">
            On wide tables, Pearson correlation matrix computation scales quadratically, which can crash memory or hang the execution. Featuresmith enforces a config-controlled correlation cap (<code>max_correlation_columns</code>, default 100) to ensure predictable execution.
          </p>
          <CodeBlock code={`# Customize the correlation column cutoff
profile = fs.profile("wide_table.csv", max_correlation_columns=50)`} language="python" showCopy />
        </section>
      </>
    )
  },
  "concepts/rules": {
    title: "Rule Engine",
    subtitle: "Deterministic quality and target leakage audits",
    category: "Core Concepts",
    seoTitle: "Rule Engine",
    seoDescription: "Examine Featuresmith's 8 deterministic rules for missing values, duplicates, empty columns, and target leakage.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Featuresmith separates profiling from auditing. The **Rule Engine** consumes a precomputed <code>ProfileResult</code> and evaluates a suite of deterministic, configurable rules. This allows rapid rules execution without re-scanning raw data.
        </p>

        <section className="mb-8" aria-labelledby="rules-list">
          <h3 id="rules-list" className="mb-4 text-lg font-semibold text-foreground">Implemented Seed Rules</h3>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="min-w-full divide-y divide-border text-left text-sm">
              <thead className="bg-muted/50 text-xs font-semibold uppercase tracking-wider text-foreground">
                <tr>
                  <th className="px-4 py-3">Rule ID</th>
                  <th className="px-4 py-3">Category</th>
                  <th className="px-4 py-3">Severity</th>
                  <th className="px-4 py-3">Description</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-muted-foreground">
                <tr>
                  <td className="px-4 py-3 font-mono text-foreground text-xs">quality.missing_value_threshold</td>
                  <td className="px-4 py-3">quality</td>
                  <td className="px-4 py-3 text-amber-500 font-semibold">warning</td>
                  <td className="px-4 py-3">Columns with &gt; 20% missing values.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-foreground text-xs">quality.duplicate_rows</td>
                  <td className="px-4 py-3">quality</td>
                  <td className="px-4 py-3 text-amber-500 font-semibold">warning</td>
                  <td className="px-4 py-3">Datasets with &gt; 10% duplicate rows.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-foreground text-xs">quality.constant_columns</td>
                  <td className="px-4 py-3">quality</td>
                  <td className="px-4 py-3 text-amber-500 font-semibold">warning</td>
                  <td className="px-4 py-3">Columns with exactly one unique non-null value.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-foreground text-xs">quality.fully_empty_columns</td>
                  <td className="px-4 py-3">quality</td>
                  <td className="px-4 py-3 text-red-500 font-semibold">critical</td>
                  <td className="px-4 py-3">Columns containing 100% null values.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-foreground text-xs">statistical.high_cardinality</td>
                  <td className="px-4 py-3">statistical</td>
                  <td className="px-4 py-3 text-amber-500 font-semibold">warning</td>
                  <td className="px-4 py-3">Categorical columns with &gt; 50% unique ratio.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-foreground text-xs">statistical.outliers</td>
                  <td className="px-4 py-3">statistical</td>
                  <td className="px-4 py-3 text-amber-500 font-semibold">warning</td>
                  <td className="px-4 py-3">Numeric outliers detected via the IQR method (factor=1.5).</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-foreground text-xs">statistical.high_correlation</td>
                  <td className="px-4 py-3">statistical</td>
                  <td className="px-4 py-3 text-amber-500 font-semibold">warning</td>
                  <td className="px-4 py-3">Numeric pairs with Pearson correlation &ge; 0.90.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-foreground text-xs">leakage.potential_leakage</td>
                  <td className="px-4 py-3">leakage</td>
                  <td className="px-4 py-3 text-red-500 font-semibold">critical</td>
                  <td className="px-4 py-3">Features with Pearson correlation &ge; 0.99 to target.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section className="mb-8" aria-labelledby="rules-isolation">
          <h3 id="rules-isolation" className="mb-3 text-lg font-semibold text-foreground">Rule Isolation</h3>
          <p className="mb-4 text-sm text-muted-foreground">
            A crash in a custom rule or internal rule evaluation must not block the rest of the profiling pipeline. Featuresmith handles exceptions internally per rule, listing rule failure stack traces in the final result metadata without terminating the execution.
          </p>
        </section>
      </>
    )
  },
  "sdk/load": {
    title: "fs.load()",
    subtitle: "SDK Reference: tabular ingestion",
    category: "Python SDK",
    seoTitle: "fs.load() API Reference",
    seoDescription: "API documentation and parameter reference for featuresmith.load().",
    render: () => (
      <>
        <CodeBlock code={`def load(source: object) -> Dataset:`} language="python" showCopy={false} />
        <p className="mt-4 mb-6 text-sm leading-relaxed text-muted-foreground">
          Load a supported local tabular file or in-memory DataFrame into a normalized immutable <code>Dataset</code> descriptor.
        </p>

        <section className="mb-8" aria-labelledby="load-args">
          <h3 id="load-args" className="mb-3 text-lg font-semibold text-foreground">Arguments</h3>
          <ul className="space-y-2 text-sm text-muted-foreground" role="list">
            <li><strong>source</strong>: <code>str</code> | <code>pandas.DataFrame</code> | <code>polars.DataFrame</code>. Local file path (<code>.csv</code>, <code>.xlsx</code>, <code>.parquet</code>) or loaded DataFrame.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="load-example">
          <h3 id="load-example" className="mb-3 text-lg font-semibold text-foreground">Example</h3>
          <CodeBlock code={`import featuresmith as fs
import polars as pl

# Load from file
ds = fs.load("train.parquet")
print(ds.row_count)

# Load from in-memory Polars DataFrame
df = pl.DataFrame({"x": [1, 2, 3]})
ds_mem = fs.load(df)`} language="python" showCopy />
        </section>
      </>
    )
  },
  "sdk/profile": {
    title: "fs.profile()",
    subtitle: "SDK Reference: statistical profiling",
    category: "Python SDK",
    seoTitle: "fs.profile() API Reference",
    seoDescription: "API documentation and parameter reference for featuresmith.profile().",
    render: () => (
      <>
        <CodeBlock code={`def profile(source: object, *, max_correlation_columns: int = 100) -> ProfileResult:`} language="python" showCopy={false} />
        <p className="mt-4 mb-6 text-sm leading-relaxed text-muted-foreground">
          Profile a Dataset or tabular source directly, executing vectorized summaries and returning a strongly-typed <code>ProfileResult</code>.
        </p>

        <section className="mb-8" aria-labelledby="profile-args">
          <h3 id="profile-args" className="mb-3 text-lg font-semibold text-foreground">Arguments</h3>
          <ul className="space-y-2 text-sm text-muted-foreground" role="list">
            <li><strong>source</strong>: <code>Dataset</code> | <code>str</code> | <code>DataFrame</code>. Pre-loaded Dataset or file/data source.</li>
            <li><strong>max_correlation_columns</strong>: <code>int</code> (default 100). Column cap for Pearson correlation computations.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="profile-example">
          <h3 id="profile-example" className="mb-3 text-lg font-semibold text-foreground">Example</h3>
          <CodeBlock code={`import featuresmith as fs

profile = fs.profile("customers.csv", max_correlation_columns=50)

# Inspect column summaries
print(profile.column_profiles["age"].missing_count)
print(profile.dataset_summary.row_count)`} language="python" showCopy />
        </section>
      </>
    )
  },
  "sdk/analyze": {
    title: "fs.analyze()",
    subtitle: "SDK Reference: comprehensive analysis",
    category: "Python SDK",
    seoTitle: "fs.analyze() API Reference",
    seoDescription: "API documentation and parameter reference for featuresmith.analyze().",
    render: () => (
      <>
        <CodeBlock code={`def analyze(
    source: object,
    *,
    target_column: str | None = None,
    enabled_rules: list[str] | None = None,
    rule_config: dict[str, Any] | None = None,
    max_correlation_columns: int = 100,
) -> RuleResult:`} language="python" showCopy={false} />
        <p className="mt-4 mb-6 text-sm leading-relaxed text-muted-foreground">
          Combines loading, profiling, and rules auditing into a single public SDK endpoint.
        </p>

        <section className="mb-8" aria-labelledby="analyze-args">
          <h3 id="analyze-args" className="mb-3 text-lg font-semibold text-foreground">Arguments</h3>
          <ul className="space-y-3 text-sm text-muted-foreground" role="list">
            <li><strong>source</strong>: <code>Dataset</code> | <code>str</code> | <code>DataFrame</code>. Input data or path.</li>
            <li><strong>target_column</strong>: <code>str | None</code> (default None). Target column name. Required for target leakage checks.</li>
            <li><strong>enabled_rules</strong>: <code>list[str] | None</code> (default None). Explicit rules to evaluate. If empty, runs all defaults.</li>
            <li><strong>rule_config</strong>: <code>dict[str, Any] | None</code>. Keyword argument config overrides for specific rules.</li>
            <li><strong>max_correlation_columns</strong>: <code>int</code> (default 100). Cap limit for correlation matrix computation.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="analyze-example">
          <h3 id="analyze-example" className="mb-3 text-lg font-semibold text-foreground">Example</h3>
          <CodeBlock code={`import featuresmith as fs

result = fs.analyze(
    "train.csv",
    target_column="churn",
    rule_config={
        "quality.missing_value_threshold": {"threshold": 30.0},
        "statistical.high_correlation": {"threshold": 0.85},
    }
)

print(f"Triggered {len(result.findings)} findings.")`} language="python" showCopy />
        </section>
      </>
    )
  },
  "cli/analyze": {
    title: "featuresmith analyze",
    subtitle: "CLI command reference and arguments",
    category: "CLI Reference",
    seoTitle: "CLI Command Reference",
    seoDescription: "Examine flags and options of featuresmith analyze command.",
    render: () => (
      <>
        <CodeBlock code={`featuresmith analyze <source> [options]`} language="bash" showCopy={false} />
        <p className="mt-4 mb-6 text-sm leading-relaxed text-muted-foreground">
          Analyze a local tabular dataset and run validation rules. Prints styled Rich tables or outputs structured JSON.
        </p>

        <section className="mb-8" aria-labelledby="cli-options">
          <h3 id="cli-options" className="mb-4 text-lg font-semibold text-foreground">Flags and Options</h3>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="min-w-full divide-y divide-border text-left text-sm">
              <tbody className="divide-y divide-border text-muted-foreground">
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--target TEXT</td>
                  <td className="px-4 py-3 text-sm">Name of the target column in the dataset for leakage evaluation.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--format [table|json]</td>
                  <td className="px-4 py-3 text-sm">Output format to display (default: <code>table</code>).</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--output PATH</td>
                  <td className="px-4 py-3 text-sm">Path to save the output report (JSON or txt depending on format).</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--severity [info|warning|critical]</td>
                  <td className="px-4 py-3 text-sm">Severity threshold for displayed findings and exit-code gating (default: <code>critical</code>).</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--max-correlation-columns INTEGER</td>
                  <td className="px-4 py-3 text-sm">Combinatorial cutoff limit for correlation profiling (default: 100).</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--quiet / --no-quiet</td>
                  <td className="px-4 py-3 text-sm">Suppress all standard console report output.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--verbose / --no-verbose</td>
                  <td className="px-4 py-3 text-sm">Show full Python tracebacks on error instead of generic messages.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--version</td>
                  <td className="px-4 py-3 text-sm">Show version info and exit.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </>
    )
  },
  "cli/config": {
    title: "Configuration",
    subtitle: "Understanding .featuresmith.yml schema",
    category: "CLI Reference",
    seoTitle: "Configuration Schema",
    seoDescription: "Detailed reference for .featuresmith.yml configurations.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Featuresmith uses a single <code>.featuresmith.yml</code> configuration file (analogous to <code>.pre-commit-config.yaml</code>) placed at your project root to handle settings layerings.
        </p>

        <section className="mb-8" aria-labelledby="cfg-schema">
          <h3 id="cfg-schema" className="mb-3 text-lg font-semibold text-foreground">Example Configuration</h3>
          <CodeBlock code={`# .featuresmith.yml
connectors:
  enabled:
    - csv
    - parquet
    - excel

rules:
  enabled:
    - quality.missing_value_threshold
    - quality.duplicate_rows
    - quality.fully_empty_columns
    - statistical.outliers
    - leakage.potential_leakage
  config:
    quality.missing_value_threshold:
      threshold: 15.0
    statistical.high_correlation:
      threshold: 0.85

ai:
  provider: ollama    # Default local provider. Options: ollama, openai, anthropic
  model: llama3
  max_correlation_columns: 100`} language="yaml" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="cfg-precedence">
          <h3 id="cfg-precedence" className="mb-3 text-lg font-semibold text-foreground">Configuration Precedence</h3>
          <p className="mb-4 text-sm text-muted-foreground">
            Configuration parameters resolve with the following precedence order:
          </p>
          <ol className="list-decimal pl-5 space-y-1.5 text-sm text-muted-foreground">
            <li>CLI command-line flags (highest precedence)</li>
            <li>Local <code>.featuresmith.yml</code> file settings</li>
            <li>Package defaults (lowest precedence)</li>
          </ol>
        </section>
      </>
    )
  },
  "benchmarks": {
    title: "Performance Benchmarks",
    subtitle: "Measured performance characteristics and memory profiles across dataset scales",
    category: "Getting Started",
    seoTitle: "Performance Benchmarks",
    seoDescription: "Review actual measured execution speeds and memory peaks for Featuresmith.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Featuresmith is optimized for fast, predictable execution. The following performance profiles were measured directly on our standard Windows 11 AMD64 host running Python 3.13.7.
        </p>

        <section className="mb-8" aria-labelledby="bench-specs">
          <h3 id="bench-specs" className="mb-3 text-lg font-semibold text-foreground">Hardware & Engine Specs</h3>
          <ul className="list-disc pl-5 space-y-1.5 text-sm text-muted-foreground" role="list">
            <li><strong>OS Platform</strong>: Windows 11 (Architecture: AMD64)</li>
            <li><strong>Runtime</strong>: Python 3.13.7</li>
            <li><strong>Vector Backends</strong>: Polars (vectorized lazy query planner) and pandas</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="bench-results">
          <h3 id="bench-results" className="mb-4 text-lg font-semibold text-foreground">Actual Performance Metrics</h3>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="min-w-full divide-y divide-border text-left text-sm">
              <thead className="bg-muted/50 text-xs font-semibold uppercase tracking-wider text-foreground">
                <tr>
                  <th className="px-4 py-3">Dataset Size (Rows)</th>
                  <th className="px-4 py-3">Ingestion / Load (ms)</th>
                  <th className="px-4 py-3">Profiling Engine (ms)</th>
                  <th className="px-4 py-3">Rule Engine (ms)</th>
                  <th className="px-4 py-3">End-to-End Audit (ms)</th>
                  <th className="px-4 py-3">Peak Memory (MB)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-muted-foreground">
                <tr>
                  <td className="px-4 py-3 font-semibold text-foreground">10,000</td>
                  <td className="px-4 py-3 font-mono">698.30</td>
                  <td className="px-4 py-3 font-mono">2,844.80</td>
                  <td className="px-4 py-3 font-mono">2.51</td>
                  <td className="px-4 py-3 font-semibold text-primary font-mono">416.85</td>
                  <td className="px-4 py-3 font-mono">1.22 MB</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-semibold text-foreground">100,000</td>
                  <td className="px-4 py-3 font-mono">231.23</td>
                  <td className="px-4 py-3 font-mono">2,487.63</td>
                  <td className="px-4 py-3 font-mono">4.36</td>
                  <td className="px-4 py-3 font-semibold text-primary font-mono">2,273.64</td>
                  <td className="px-4 py-3 font-mono">11.82 MB</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-semibold text-foreground">500,000</td>
                  <td className="px-4 py-3 font-mono">777.78</td>
                  <td className="px-4 py-3 font-mono">11,597.85</td>
                  <td className="px-4 py-3 font-mono">8.07</td>
                  <td className="px-4 py-3 font-semibold text-primary font-mono">10,806.48</td>
                  <td className="px-4 py-3 font-mono">62.01 MB</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p className="mt-3 text-xs text-muted-foreground">
            * Peak memory measures temporary heap allocations using <code>tracemalloc</code>. Rules execution operates instantly (under 10ms) because it audits statistical summaries already computed in memory.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="bench-conclusions">
          <h3 id="bench-conclusions" className="mb-3 text-lg font-semibold text-foreground">Key Observations</h3>
          <ul className="space-y-2.5 text-sm text-muted-foreground" role="list">
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>Linear Complexity:</strong> Execution times scale linearly with row count, taking ~11.5 seconds for half a million rows.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>Memory Gating:</strong> Memory footprint is extremely light, keeping peak consumption under 63 MB at 500K rows.</span>
            </li>
          </ul>
        </section>
      </>
    )
  },
  "guides/rules": {
    title: "Custom Rules Guide",
    subtitle: "Learn how to write custom deterministic data quality validation rules",
    category: "Guides",
    seoTitle: "Custom Validation Rules",
    seoDescription: "Step-by-step tutorial on extending BaseRule to create custom quality checks in Featuresmith.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Featuresmith is fully extensible. You can easily add your own deterministic rules by extending the <code>BaseRule</code> interface and defining rule parameters.
        </p>

        <section className="mb-8" aria-labelledby="rule-abstract">
          <h3 id="rule-abstract" className="mb-3 text-lg font-semibold text-foreground">The BaseRule Interface</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            All rules must extend <code>BaseRule</code> and implement the following properties and methods:
          </p>
          <ul className="list-disc pl-5 space-y-2 text-sm text-muted-foreground" role="list">
            <li><code>id</code>: A unique dotted identifier (e.g., <code>statistical.zero_variance</code>).</li>
            <li><code>name</code>: A descriptive rule title.</li>
            <li><code>category</code>: Group category (e.g., <code>quality</code>, <code>statistical</code>, <code>leakage</code>).</li>
            <li><code>severity</code>: Finding severity level (e.g., <code>RuleSeverity.INFO</code>, <code>WARNING</code>, or <code>CRITICAL</code>).</li>
            <li><code>evaluate(profile: ProfileResult) -&gt; list[RuleFinding]</code>: Core audit logic.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="rule-example">
          <h3 id="rule-example" className="mb-3 text-lg font-semibold text-foreground">Custom Rule Implementation</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Here is a complete example of a rule to detect numerical columns that have zero standard deviation (constant value columns):
          </p>
          <CodeBlock code={`from typing import Any
from featuresmith.rules.base import BaseRule
from featuresmith.core.rule_finding import RuleFinding, RuleSeverity
from featuresmith.core.profile_result import ProfileResult

class ZeroVarianceRule(BaseRule):
    """Custom rule to detect columns with zero variance."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__()
        self.enabled = kwargs.get("enabled", True)

    @property
    def id(self) -> str:
        return "statistical.zero_variance"

    @property
    def name(self) -> str:
        return "Zero Variance Columns"

    @property
    def category(self) -> str:
        return "statistical"

    @property
    def severity(self) -> RuleSeverity:
        return RuleSeverity.WARNING

    def evaluate(self, profile: ProfileResult) -> list[RuleFinding]:
        findings = []
        for col_name, col_profile in profile.column_profiles.items():
            numeric_stats = col_profile.numeric_stats
            if numeric_stats is not None and numeric_stats.std == 0.0:
                findings.append(
                    self.create_finding(
                        column_name=col_name,
                        title="Zero Variance Detected",
                        description=f"Column '{col_name}' has standard deviation of 0.0 (no variance).",
                        evidence={"std": 0.0}
                    )
                )
        return findings`} language="python" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="rule-registration">
          <h3 id="rule-registration" className="mb-3 text-lg font-semibold text-foreground">Evaluating Custom Rules</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            You can instantiate your rule and run it directly in Python:
          </p>
          <CodeBlock code={`import featuresmith as fs

dataset = fs.load("data.csv")
rule = ZeroVarianceRule()

# Run rule directly against computed statistical profiles
profile = fs.profile(dataset)
findings = rule.evaluate(profile)

for finding in findings:
    print(f"[{finding.severity}] {finding.title} in {finding.column_name}")`} language="python" showCopy />
        </section>
      </>
    )
  }
}

// Generate metadata for each dynamic documentation path
export async function generateMetadata({ params }: { params: { slug: string[] } }) {
  const slugPath = params.slug.join("/")
  const doc = DOCS_MAP[slugPath]

  if (!doc) {
    return {
      title: "Under Construction | Featuresmith",
      description: "Documentation page planned on the roadmap."
    }
  }

  return {
    title: `${doc.seoTitle} | Featuresmith Docs`,
    description: doc.seoDescription,
  }
}

export default function DynamicDocPage({ params }: { params: { slug: string[] } }) {
  const slugPath = params.slug.join("/")
  const doc = DOCS_MAP[slugPath]

  // If page does not exist in DOCS_MAP, render a high-quality "Under Construction" page
  if (!doc) {
    const isPlannedGuide = slugPath.startsWith("guides/") || slugPath.endsWith("plugins")
    const sectionTitle = slugPath.split("/")[0].toUpperCase()

    return (
      <article className="prose-custom max-w-none">
        <nav aria-label="Breadcrumb" className="mb-6 flex items-center gap-1 text-sm text-muted-foreground">
          <Link href="/" className="hover:text-foreground">Home</Link>
          <ChevronRight className="h-3.5 w-3.5" aria-hidden />
          <Link href="/docs" className="hover:text-foreground">Docs</Link>
          <ChevronRight className="h-3.5 w-3.5" aria-hidden />
          <span className="text-foreground capitalize">{slugPath.split("/").pop()}</span>
        </nav>

        <header className="mb-10 border-b border-border pb-8">
          <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-primary">
            {sectionTitle}
          </p>
          <h1 className="mb-3 text-3xl font-semibold tracking-tight text-foreground sm:text-4xl capitalize">
            {slugPath.split("/").pop()?.replace("-", " ")}
          </h1>
          <p className="text-base leading-relaxed text-muted-foreground">
            This capability or guide is scheduled in our project roadmap.
          </p>
        </header>

        <div className="rounded-xl border border-border bg-card p-6 md:p-8">
          <div className="flex items-start gap-4">
            <div className="inline-flex h-10 w-10 items-center justify-center rounded-lg bg-primary/8 text-primary ring-1 ring-primary/15">
              <Info className="h-5 w-5" aria-hidden />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-foreground">Roadmap Feature</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                {isPlannedGuide
                  ? "Writing plugins and advanced custom rule guidelines are scheduled for Phase 6 (Plugin Ecosystem). See docs/Phases.md for more details."
                  : "This API implementation is currently planned. Featuresmith is in active development, and features are rolled out systematically to keep the API surface stable."}
              </p>
              <div className="mt-6 flex flex-wrap gap-3">
                <Link
                  href="/#roadmap"
                  className="inline-flex items-center gap-1.5 rounded-md bg-primary px-4 py-2 text-xs font-medium text-primary-foreground hover:opacity-90 transition-all"
                >
                  View Roadmap Phases
                </Link>
                <Link
                  href="https://github.com/adityagangwani30/FeatureSmith"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 rounded-md border border-border bg-transparent px-4 py-2 text-xs font-medium text-foreground hover:bg-accent transition-all"
                >
                  Follow on GitHub
                </Link>
              </div>
            </div>
          </div>
        </div>
      </article>
    )
  }

  return (
    <article className="prose-custom max-w-none">
      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb" className="mb-6 flex items-center gap-1 text-sm text-muted-foreground">
        <Link href="/" className="hover:text-foreground">
          Home
        </Link>
        <ChevronRight className="h-3.5 w-3.5" aria-hidden />
        <Link href="/docs" className="hover:text-foreground">
          Docs
        </Link>
        <ChevronRight className="h-3.5 w-3.5" aria-hidden />
        <span className="text-foreground">{doc.title}</span>
      </nav>

      {/* Page header */}
      <header className="mb-10 border-b border-border pb-8">
        <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-primary">
          {doc.category}
        </p>
        <h1 className="mb-3 text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
          {doc.title}
        </h1>
        <p className="text-base leading-relaxed text-muted-foreground">
          {doc.subtitle}
        </p>
      </header>

      {/* Render the document contents */}
      <div className="prose-custom">
        {doc.render()}
      </div>
    </article>
  )
}
