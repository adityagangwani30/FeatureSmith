import React from "react"
import { CodeBlock } from "@/components/ui/code-block"
import { Info, AlertTriangle, AlertCircle, CheckCircle2 } from "lucide-react"

export interface DocContent {
  title: string
  subtitle: string
  category: string
  seoTitle: string
  seoDescription: string
  render: () => React.JSX.Element
}

export const DOCS_MAP: Record<string, DocContent> = {
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
          as a CLI, or built directly from source for local development. We recommend using <code>uv</code> or <code>pip</code>.
        </p>

        <section className="mb-8" aria-labelledby="install-pip">
          <h3 id="install-pip" className="mb-3 text-lg font-semibold text-foreground">Using pip</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Install the latest version of the core library and the CLI from PyPI:
          </p>
          <CodeBlock code="pip install featuresmith-core featuresmith-cli" language="bash" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="install-uv">
          <h3 id="install-uv" className="mb-3 text-lg font-semibold text-foreground">Using uv (Recommended)</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Add Featuresmith to your workspace dependencies:
          </p>
          <CodeBlock code="uv add featuresmith-core featuresmith-cli" language="bash" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="install-source">
          <h3 id="install-source" className="mb-3 text-lg font-semibold text-foreground">From Source (Development)</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Clone the repository and sync the workspace for local contribution:
          </p>
          <CodeBlock code={`git clone https://github.com/adityagangwani30/FeatureSmith.git
cd FeatureSmith
uv sync
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
            <li><strong>Runtime</strong>: Python 3.13.7 (or higher compatible)</li>
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
                  <td className="px-4 py-3 font-mono">13.21</td>
                  <td className="px-4 py-3 font-mono">78.42</td>
                  <td className="px-4 py-3 font-mono">0.71</td>
                  <td className="px-4 py-3 font-semibold text-primary font-mono">56.78</td>
                  <td className="px-4 py-3 font-mono">1.20 MB</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-semibold text-foreground">100,000</td>
                  <td className="px-4 py-3 font-mono">147.03</td>
                  <td className="px-4 py-3 font-mono">562.74</td>
                  <td className="px-4 py-3 font-mono">0.73</td>
                  <td className="px-4 py-3 font-semibold text-primary font-mono">514.64</td>
                  <td className="px-4 py-3 font-mono">11.82 MB</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-semibold text-foreground">500,000</td>
                  <td className="px-4 py-3 font-mono">499.74</td>
                  <td className="px-4 py-3 font-mono">3,667.91</td>
                  <td className="px-4 py-3 font-mono">12.57</td>
                  <td className="px-4 py-3 font-semibold text-primary font-mono">2,331.68</td>
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
              <span><strong>Linear Complexity:</strong> Execution times and memory footprint scale near-linearly with row count, taking under 4 seconds for half a million rows.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>Memory Gating:</strong> Peak memory remains highly constrained (only 62 MB for 500K rows) thanks to vectorized Polars engine allocations.</span>
            </li>
          </ul>
        </section>
      </>
    )
  },
  "dev-setup": {
    title: "Development Setup",
    subtitle: "Setting up your environment to develop and test Featuresmith",
    category: "Getting Started",
    seoTitle: "Development Setup",
    seoDescription: "Step-by-step developer workspace setup for Featuresmith, using uv, pre-commit, and pytest.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Featuresmith uses a monorepo structure managed by <code>uv workspaces</code>. Follow this guide to set up a clean, isolated local development environment.
        </p>

        <section className="mb-8" aria-labelledby="ds-prereqs">
          <h3 id="ds-prereqs" className="mb-3 text-lg font-semibold text-foreground">Prerequisites</h3>
          <ul className="list-disc pl-5 space-y-1.5 text-sm text-muted-foreground">
            <li>Python 3.11 or higher installed on your system.</li>
            <li>Astral <code>uv</code> installed (see <a href="https://docs.astral.sh/uv/" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">uv docs</a>).</li>
            <li>Git for source control.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="ds-clone">
          <h3 id="ds-clone" className="mb-3 text-lg font-semibold text-foreground">1. Clone and Sync Workspace</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Clone the repository and run <code>uv sync</code> to automatically create a virtual environment and link all local packages:
          </p>
          <CodeBlock code={`git clone https://github.com/adityagangwani30/FeatureSmith.git
cd FeatureSmith
uv sync`} language="bash" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="ds-hooks">
          <h3 id="ds-hooks" className="mb-3 text-lg font-semibold text-foreground">2. Install Pre-commit Hooks</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            We use pre-commit hooks to enforce formatting (Ruff) and static typing (Mypy) before code is committed:
          </p>
          <CodeBlock code="uv run pre-commit install" language="bash" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="ds-verify">
          <h3 id="ds-verify" className="mb-3 text-lg font-semibold text-foreground">3. Running Checks and Tests</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Ensure your configuration is correct by running the test suite and linters:
          </p>
          <CodeBlock code={`# Run formatting checks
uv run ruff format . --check

# Run linter checks
uv run ruff check .

# Run type checks
uv run mypy .

# Run import boundary constraints
uv run lint-imports

# Run test suite
uv run pytest`} language="bash" showCopy />
          <div className="mt-4 rounded-lg bg-amber-500/10 p-4 text-xs text-amber-800 dark:text-amber-300 border border-amber-500/20">
            <div className="flex gap-2.5">
              <AlertTriangle className="h-4 w-4 flex-none" />
              <div>
                <strong>Windows Environment Note:</strong> If pytest encounters permissions or lockout issues with standard system temp directories, point the temp folders directly inside the workspace:
                <code className="mt-2 block bg-muted/80 p-2 rounded text-[10px] text-foreground font-mono">
                  $env:TMP=".pytest_tmp"; $env:TEMP=".pytest_tmp"; uv run pytest
                </code>
              </div>
            </div>
          </div>
        </section>
      </>
    )
  },
  "contributing": {
    title: "Contributing Guidelines",
    subtitle: "Standards and processes for contributing to Featuresmith",
    category: "Getting Started",
    seoTitle: "Contributing Guidelines",
    seoDescription: "How to open pull requests, compile tests, follow commit rules, and respect package boundaries.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Featuresmith welcomes community contributions! To maintain code stability and high quality, please review our requirements below.
        </p>

        <section className="mb-8" aria-labelledby="contrib-packages">
          <h3 id="contrib-packages" className="mb-3 text-lg font-semibold text-foreground">Package Separation Guardrails</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            To enforce our "one core, many thin surfaces" architecture, we use <code>import-linter</code>. The rule is simple:
          </p>
          <div className="mb-3 rounded-lg bg-blue-500/10 p-4 text-xs text-blue-800 dark:text-blue-300 border border-blue-500/20">
            <div className="flex gap-2.5">
              <Info className="h-4 w-4 flex-none" />
              <span>
                Surface wrappers (such as <code>featuresmith-cli</code> and <code>featuresmith-dashboard</code>) <strong>MUST NOT</strong> import internal core logic. They can only interface with the library via the public API endpoints exposed in <code>featuresmith.api</code>.
              </span>
            </div>
          </div>
        </section>

        <section className="mb-8" aria-labelledby="contrib-commits">
          <h3 id="contrib-commits" className="mb-3 text-lg font-semibold text-foreground">Commit Conventions</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            We follow the <a href="https://www.conventionalcommits.org/" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">Conventional Commits</a> standard, scoped by package:
          </p>
          <CodeBlock code={`feat(rules): add zero variance numerical check
fix(cli): correct formatting of json output reports
docs(architecture): expand connectors description
test(profiling): add test for datetime timezone offset handling`} language="bash" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="contrib-testing">
          <h3 id="contrib-testing" className="mb-3 text-lg font-semibold text-foreground">Testing Standards</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            PRs without comprehensive test coverage will not be merged.
          </p>
          <ul className="list-disc pl-5 space-y-1 text-sm text-muted-foreground">
            <li>Every new rule must have at least one positive fixture test (violations triggered) and one negative test (violations not triggered).</li>
            <li>New connectors must include unit tests utilizing physical mockup fixtures.</li>
            <li>Core logic packages require at least 85% statement coverage.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="contrib-pr">
          <h3 id="contrib-pr" className="mb-3 text-lg font-semibold text-foreground">Pull Request Checklist</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Before submitting a pull request, ensure that:
          </p>
          <ul className="list-disc pl-5 space-y-1 text-sm text-muted-foreground">
            <li>Strict type hinting is present on all new inputs/outputs (verified with <code>mypy --strict .</code>).</li>
            <li>Formatting conforms to Ruff (<code>ruff format .</code>).</li>
            <li>No new external library dependencies are introduced without a corresponding Architecture Decision Record (ADR) under <code>docs/adr/</code>.</li>
          </ul>
        </section>
      </>
    )
  },
  "concepts/architecture": {
    title: "Architecture Overview",
    subtitle: "Design principles and framework layout of Featuresmith",
    category: "Core Concepts",
    seoTitle: "Architecture Overview",
    seoDescription: "Examine Featuresmith's core-first architecture, compute and reasoning separation, and modular plugin layout.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Featuresmith is engineered around a core-first layout. All critical logic is centralized, ensuring surfaces remain thin rendering components.
        </p>

        <section className="mb-8" aria-labelledby="arch-principles">
          <h3 id="arch-principles" className="mb-4 text-lg font-semibold text-foreground">Architectural Design Rules</h3>
          <ul className="space-y-4 text-sm text-muted-foreground">
            <li className="flex gap-2">
              <span className="mt-1.5 h-1.5 w-1.5 flex-none rounded-full bg-primary" />
              <div>
                <strong>One core, many thin surfaces:</strong> All business logic — loading, profiling, rule validation, custom rules — resides inside the package <code>featuresmith-core</code>. Interfaces (CLI and Dashboard) only wrap the SDK api surface.
              </div>
            </li>
            <li className="flex gap-2">
              <span className="mt-1.5 h-1.5 w-1.5 flex-none rounded-full bg-primary" />
              <div>
                <strong>Compute and reasoning separation:</strong> Numerical algorithms and database scans run deterministically using vectorized backends. AI integrations (planned for Phase 2+) are only ever used for natural-language narration or chat - they never perform computation.
              </div>
            </li>
            <li className="flex gap-2">
              <span className="mt-1.5 h-1.5 w-1.5 flex-none rounded-full bg-primary" />
              <div>
                <strong>Modular plugin structure:</strong> Connectors, rules, exporters, and AI providers inherit from stable base classes (e.g. <code>BaseRule</code>, <code>BaseConnector</code>), allowing third-party extensions without altering repository core code.
              </div>
            </li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="arch-flow">
          <h3 id="arch-flow" className="mb-3 text-lg font-semibold text-foreground">Data Pipeline Blueprint</h3>
          <p className="mb-4 text-sm text-muted-foreground">
            The flow of execution runs in a linear sequence, transitioning between structured stages:
          </p>
          <CodeBlock code={`[Raw Dataset / DataFrame]
           │
           ▼  (Connectors Load)
    [Dataset Object]
           │
           ▼  (Profiling Engine Summarizes)
  [ProfileResult Dataclass]
           │
           ▼  (Rule Engine Audits)
  [RuleResult (Profile + Findings)]
           │
           ▼  (Exporter / Chat Integration)
[Sklearn Pipelines / Text Reports / FAQ response]`} language="bash" showCopy={false} />
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

        <section className="mb-8" aria-labelledby="dataset-attributes">
          <h3 id="dataset-attributes" className="mb-3 text-lg font-semibold text-foreground">The Dataset Class</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            The <code>Dataset</code> class wraps loaded tabular engines and exposes the following properties:
          </p>
          <ul className="list-disc pl-5 space-y-1.5 text-sm text-muted-foreground">
            <li><code>dataframe</code>: The raw underlying DataFrame (Polars or pandas).</li>
            <li><code>backend</code>: Indication of engine, returning <code>"polars"</code> or <code>"pandas"</code>.</li>
            <li><code>schema</code>: The ordered <code>DatasetSchema</code> list of columns.</li>
            <li><code>row_count</code>: Total row dimension of the table.</li>
            <li><code>column_count</code>: Total column dimension of the table.</li>
            <li><code>dtypes</code>: Mapping of column names to backend dtype strings.</li>
            <li><code>source</code>: Local path of the source file, or <code>None</code> if in-memory.</li>
            <li><code>file_size</code>: Size of the source file in bytes, or <code>None</code> if in-memory.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="dataset-preview">
          <h3 id="dataset-preview" className="mb-3 text-lg font-semibold text-foreground">Previewing Data</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            You can read a clean preview subset of the records using the <code>preview()</code> method:
          </p>
          <CodeBlock code={`import featuresmith as fs

dataset = fs.load("train.parquet")
# Get the first 5 records as a backend-specific dataframe
head_df = dataset.preview(5)`} language="python" showCopy />
        </section>
      </>
    )
  },
  "concepts/connectors": {
    title: "Connectors",
    subtitle: "Normalized ingestion engines for local and memory data formats",
    category: "Core Concepts",
    seoTitle: "Connectors",
    seoDescription: "Examine Featuresmith's support for CSV, Parquet, Excel, pandas, and Polars DataFrames.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Featuresmith implements ingestion using dedicated, deterministic connectors registered in a static registry. This registry decodes inputs and returns a unified <code>Dataset</code> contract.
        </p>

        <section className="mb-8" aria-labelledby="conn-list">
          <h3 id="conn-list" className="mb-3 text-lg font-semibold text-foreground">Supported Source Formats</h3>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="min-w-full divide-y divide-border text-left text-sm">
              <thead className="bg-muted/50 text-xs font-semibold uppercase tracking-wider text-foreground">
                <tr>
                  <th className="px-4 py-3">Format / Extension</th>
                  <th className="px-4 py-3">Internal Connector</th>
                  <th className="px-4 py-3">DataFrame Backend</th>
                  <th className="px-4 py-3">Dependencies</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-muted-foreground">
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">.csv</td>
                  <td className="px-4 py-3">CsvConnector</td>
                  <td className="px-4 py-3">Polars</td>
                  <td className="px-4 py-3">polars</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">.parquet, .pq</td>
                  <td className="px-4 py-3">ParquetConnector</td>
                  <td className="px-4 py-3">Polars</td>
                  <td className="px-4 py-3">polars, pyarrow</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">.xlsx, .xls, .xlsm</td>
                  <td className="px-4 py-3">ExcelConnector</td>
                  <td className="px-4 py-3">pandas</td>
                  <td className="px-4 py-3">pandas, openpyxl</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">pandas.DataFrame</td>
                  <td className="px-4 py-3">DataFrameConnector</td>
                  <td className="px-4 py-3">pandas</td>
                  <td className="px-4 py-3">pandas</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">polars.DataFrame</td>
                  <td className="px-4 py-3">DataFrameConnector</td>
                  <td className="px-4 py-3">Polars</td>
                  <td className="px-4 py-3">polars</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section className="mb-8" aria-labelledby="conn-errors">
          <h3 id="conn-errors" className="mb-3 text-lg font-semibold text-foreground">Ingestion Robustness & Security</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Connectors validate physical path existence, readable access, and extension matching prior to loading. If any validation or parsing step fails, a <code>ConnectorError</code> (such as <code>SourceNotFoundError</code> or <code>SourceParseError</code>) is raised.
          </p>
          <CodeBlock code={`import featuresmith as fs
from featuresmith.core.exceptions import SourceNotFoundError

try:
    dataset = fs.load("missing_data.csv")
except SourceNotFoundError as e:
    print(f"Data file is missing: {e}")`} language="python" showCopy />
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
          Featuresmith does not compute layout charts in core; it computes **deterministic statistical descriptors** returned as a typed, serializable <code>ProfileResult</code>.
        </p>

        <section className="mb-8" aria-labelledby="prof-metrics">
          <h3 id="prof-metrics" className="mb-3 text-lg font-semibold text-foreground">Statistical Coverage</h3>
          <p className="mb-4 text-sm text-muted-foreground">
            The profiling engine executes optimized, batched vectorized computations to compile:
          </p>
          <ul className="space-y-3 text-sm text-muted-foreground" role="list">
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>23 Numeric Metrics:</strong> Mean, median, mode, min, max, standard deviation, variance, skewness, kurtosis, quantiles (IQR, Q1, Q2, Q3), sum, zero count, negative count, positive count, range, and counts.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>Categorical Profiles:</strong> Cardinality, unique count, entropy, top frequency tables (capped), least frequent tables, and missing rates.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>Datetime Profiles:</strong> Minimum (earliest), maximum (latest), range span in days, and missing rates.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              <span><strong>Text Profiles:</strong> Average/min/max string length, empty strings count, whitespace-only count, total character count, and word count.</span>
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
                  <td className="px-4 py-3">Columns with &gt; 20% missing values (configurable).</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-foreground text-xs">quality.duplicate_rows</td>
                  <td className="px-4 py-3">quality</td>
                  <td className="px-4 py-3 text-amber-500 font-semibold">warning</td>
                  <td className="px-4 py-3">Datasets with &gt; 10% duplicate rows (configurable).</td>
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
          <h3 id="rules-isolation" className="mb-3 text-lg font-semibold text-foreground">Rule Exception Isolation</h3>
          <p className="mb-4 text-sm text-muted-foreground">
            A crash in a custom rule or internal rule evaluation must not block the rest of the profiling pipeline. Featuresmith handles exceptions internally per rule, listing rule failure stack traces in the final <code>RuleResult.failed_rules</code> mapping without terminating the run.
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
        <CodeBlock code={`def profile(
    source: object, 
    *, 
    max_correlation_columns: int = 100,
    max_frequency_table_size: int = 1000
) -> ProfileResult:`} language="python" showCopy={false} />
        <p className="mt-4 mb-6 text-sm leading-relaxed text-muted-foreground">
          Profile a Dataset or tabular source directly, executing vectorized summaries and returning a strongly-typed, serializable <code>ProfileResult</code>.
        </p>

        <section className="mb-8" aria-labelledby="profile-args">
          <h3 id="profile-args" className="mb-3 text-lg font-semibold text-foreground">Arguments</h3>
          <ul className="space-y-3 text-sm text-muted-foreground" role="list">
            <li><strong>source</strong>: <code>Dataset</code> | <code>str</code> | <code>DataFrame</code>. Pre-loaded Dataset or file/data source.</li>
            <li><strong>max_correlation_columns</strong>: <code>int</code> (default 100). Column cap for Pearson correlation computations.</li>
            <li><strong>max_frequency_table_size</strong>: <code>int</code> (default 1000). Maximum unique categories to track in frequency table summaries.</li>
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
    max_frequency_table_size: int = 1000,
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
            <li><strong>max_frequency_table_size</strong>: <code>int</code> (default 1000). Frequency table storage cap.</li>
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
  "sdk/models": {
    title: "Data Models",
    subtitle: "SDK Reference: strongly-typed data structures",
    category: "Python SDK",
    seoTitle: "SDK Data Models",
    seoDescription: "Examine Featuresmith's typed output schemas including Dataset, ProfileResult, RuleFinding, and RuleResult.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Featuresmith uses Python dataclasses with <code>frozen=True</code> to represent structures. This ensures they are read-only and safely serializable.
        </p>

        <section className="mb-8" aria-labelledby="models-profile-result">
          <h3 id="models-profile-result" className="mb-3 text-lg font-semibold text-foreground">ProfileResult</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            The output returned from <code>fs.profile()</code>.
          </p>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class ProfileResult:
    dataset_summary: DatasetSummary
    column_profiles: Mapping[str, ColumnProfile]
    numeric_profiles: Mapping[str, NumericProfile]
    categorical_profiles: Mapping[str, CategoricalProfile]
    datetime_profiles: Mapping[str, DatetimeProfile]
    text_profiles: Mapping[str, TextProfile]
    missing_value_summary: MissingValueSummary
    duplicate_summary: DuplicateSummary
    correlation_summary: CorrelationSummary
    dataset_metadata: DatasetMetadata
    execution_metadata: ExecutionMetadata

    def to_dict(self) -> dict[str, Any]:
        """Convert result to a standard serializable dictionary."""`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="models-rule-finding">
          <h3 id="models-rule-finding" className="mb-3 text-lg font-semibold text-foreground">RuleFinding</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            A single issue identified by the rules auditing step.
          </p>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class RuleFinding:
    rule_id: str
    rule_name: str
    category: str  # "quality" | "statistical" | "leakage"
    severity: str  # "info" | "warning" | "critical"
    column_name: str | None
    title: str
    description: str
    evidence: Mapping[str, Any]
    confidence: float = 1.0
    id: str = ...  # Auto-generated UUID string
    metadata: Mapping[str, Any] = ...  # Extra key-value metadata`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="models-rule-result">
          <h3 id="models-rule-result" className="mb-3 text-lg font-semibold text-foreground">RuleResult</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            The aggregate output returned from <code>fs.analyze()</code>.
          </p>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class RuleResult:
    profile: ProfileResult
    findings: Sequence[RuleFinding]
    executed_rules: Sequence[str]
    execution_time_ms: float
    failed_rules: Mapping[str, str]  # Rule ID -> Exception traceback mapping

    def to_dict(self) -> dict[str, Any]:
        """Convert result to a standard serializable dictionary."""`} language="python" showCopy={false} />
        </section>
      </>
    )
  },
  "sdk/exceptions": {
    title: "Exceptions Reference",
    subtitle: "SDK Reference: custom error classes raised during ingestion",
    category: "Python SDK",
    seoTitle: "SDK Exceptions",
    seoDescription: "Examine Featuresmith custom exception hierarchies, including ConnectorError and SourceParseError.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Featuresmith uses a structured class hierarchy for errors raised during loading and ingestion. All custom exceptions inherit from <code>ConnectorError</code>.
        </p>

        <section className="mb-8" aria-labelledby="exc-hierarchy">
          <h3 id="exc-hierarchy" className="mb-3 text-lg font-semibold text-foreground">Exception Hierarchy</h3>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="min-w-full divide-y divide-border text-left text-sm">
              <thead className="bg-muted/50 text-xs font-semibold uppercase tracking-wider text-foreground">
                <tr>
                  <th className="px-4 py-3">Exception Class</th>
                  <th className="px-4 py-3">Parent Class</th>
                  <th className="px-4 py-3">Trigger Condition</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-muted-foreground">
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">ConnectorError</td>
                  <td className="px-4 py-3 font-mono text-xs">Exception</td>
                  <td className="px-4 py-3">Base error for all loading and connector-specific failures.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">SourceNotFoundError</td>
                  <td className="px-4 py-3 font-mono text-xs">ConnectorError</td>
                  <td className="px-4 py-3">Raised when a local file path does not exist.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">UnsupportedFormatError</td>
                  <td className="px-4 py-3 font-mono text-xs">ConnectorError</td>
                  <td className="px-4 py-3">Raised when a file extension or object type is unsupported.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">SourceParseError</td>
                  <td className="px-4 py-3 font-mono text-xs">ConnectorError</td>
                  <td className="px-4 py-3">Raised when pandas or Polars fails to parse a corrupted dataset.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section className="mb-8" aria-labelledby="exc-handling">
          <h3 id="exc-handling" className="mb-3 text-lg font-semibold text-foreground">Robust Ingestion Guardrails</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Exceptions do not expose raw table values or secure system information. Catching specific errors is simple:
          </p>
          <CodeBlock code={`import featuresmith as fs
from featuresmith.core.exceptions import SourceNotFoundError, UnsupportedFormatError

try:
    ds = fs.load("unsupported_extension.txt")
except UnsupportedFormatError as e:
    print(f"Format check failed: {e}")
except SourceNotFoundError:
    print("File path missing.")`} language="python" showCopy />
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
    subtitle: "Configuring the Rule Engine via CLI flags and SDK arguments",
    category: "CLI Reference",
    seoTitle: "CLI and SDK Configuration Reference",
    seoDescription: "Examine options and parameters to configure the Featuresmith Rule Engine in CLI and Python SDK.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Featuresmith v0.1.0 supports programmatic rule configurations in the Python SDK and command-line flags in the CLI. File-based configuration is not yet active.
        </p>

        <div className="mb-6 rounded-lg border border-primary/20 bg-primary/5 p-4 text-sm text-muted-foreground flex gap-3">
          <div className="mt-0.5 inline-flex h-6 w-6 items-center justify-center rounded bg-primary/10 text-primary">
            <Info className="h-4 w-4" aria-hidden />
          </div>
          <div>
            <p className="font-semibold text-foreground mb-1 text-xs">Roadmap Notice: File-Based Config (.featuresmith.yml)</p>
            <p className="text-xs">
              Layered file-based configuration (via a <code>.featuresmith.yml</code> file at the project root) is a planned enhancement scheduled for Phase 2+. In the current release, configure rules directly in code or use CLI flags.
            </p>
          </div>
        </div>

        <section className="mb-8" aria-labelledby="cfg-sdk">
          <h3 id="cfg-sdk" className="mb-3 text-lg font-semibold text-foreground">1. Python SDK Configuration</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Configure rules programmatically by passing the <code>enabled_rules</code> list and the <code>rule_config</code> dictionary to the <code>fs.analyze()</code> function:
          </p>
          <CodeBlock code={`import featuresmith as fs

result = fs.analyze(
    "dataset.csv",
    target_column="churn",
    enabled_rules=[
        "quality.missing_value_threshold",
        "statistical.high_correlation"
    ],
    rule_config={
        "quality.missing_value_threshold": {"threshold": 15.0},
        "statistical.high_correlation": {"threshold": 0.85}
    }
)`} language="python" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="cfg-cli">
          <h3 id="cfg-cli" className="mb-3 text-lg font-semibold text-foreground">2. CLI Options</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Control CLI analyze parameters using flags (such as filtering by severity or limiting correlation analysis sizes):
          </p>
          <CodeBlock code={`# Target column and correlation column limits
featuresmith analyze dataset.csv --target churn --max-correlation-columns 50

# Severity filtering and report generation
featuresmith analyze dataset.csv --severity warning --output report.txt`} language="bash" showCopy />
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
  },
  "guides/cicd": {
    title: "CI/CD Integration",
    subtitle: "Automate data quality and target leakage checks in your deployment pipelines",
    category: "Guides",
    seoTitle: "CI/CD Pipeline Integration Guide",
    seoDescription: "Learn how to integrate Featuresmith into GitHub Actions, GitLab CI, and other automation workflows.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Data quality issues and target leakage often sneak into production because datasets are updated out-of-band or model retraining runs automatically. Featuresmith is designed to run inside CI/CD pipelines to prevent model degradation by gating deployments on strict rule audits.
        </p>

        <section className="mb-8" aria-labelledby="cicd-exit-codes">
          <h3 id="cicd-exit-codes" className="mb-3 text-lg font-semibold text-foreground">Exit-Code Gating</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            The <code>featuresmith analyze</code> command returns deterministic exit codes that shell runners can check to decide whether to block or proceed with the build:
          </p>
          <ul className="list-disc pl-5 space-y-2 text-sm text-muted-foreground" role="list">
            <li><code>0</code>: <strong>Clean run</strong> — no findings detected at or above the requested severity threshold.</li>
            <li><code>1</code>: <strong>Rule violation(s) detected</strong> — one or more audits failed. This will automatically fail standard CI steps unless ignored.</li>
            <li><code>2</code>: <strong>Invalid input</strong> — misspelled arguments, target column not in schema, or incorrect options.</li>
            <li><code>3</code>: <strong>Ingestion/load failure</strong> — database or files could not be read or parsed.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="cicd-github-actions">
          <h3 id="cicd-github-actions" className="mb-3 text-lg font-semibold text-foreground">GitHub Actions Workflow</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Here is a complete, copy-pasteable GitHub Actions workflow file (<code>.github/workflows/data-audit.yml</code>) that runs Featuresmith on every pull request to check for schema drift and target leakage:
          </p>
          <CodeBlock code={`name: Data Quality Audit

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  audit-data:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Install Python & uv
        uses: astral-sh/setup-uv@v3
        with:
          python-version: "3.11"

      - name: Install Featuresmith
        run: |
          uv pip install featuresmith-core featuresmith-cli --system

      - name: Run Data Quality Audit
        run: |
          # Gate pipeline on 'warning' and 'critical' severity levels
          featuresmith analyze data/train.csv --target churn --severity warning`} language="yaml" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="cicd-customization">
          <h3 id="cicd-customization" className="mb-3 text-lg font-semibold text-foreground">Customizing Gates</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            You can customize the strictness of your CI gate by overriding severity settings in your local <code>.featuresmith.yml</code> configuration file, or by passing the <code>--severity</code> flag to the CLI.
          </p>
          <CodeBlock code={`# Only fail builds on critical violations (fully empty columns or target leakage)
featuresmith analyze data/train.csv --target churn --severity critical`} language="bash" showCopy />
        </section>
      </>
    )
  },
  "resources/release": {
    title: "Release Notes",
    subtitle: "Featuresmith version releases and feature scope",
    category: "Resources",
    seoTitle: "Release Notes",
    seoDescription: "Review release scope, packaged components, and migration notes for Featuresmith releases.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Featuresmith release schedules and packaged capabilities are tracked below.
        </p>

        <section className="mb-8" aria-labelledby="rel-v010">
          <h3 id="rel-v010" className="mb-3 text-lg font-semibold text-foreground">Featuresmith v0.1.0 (First Public Release)</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Featuresmith v0.1.0 focuses on deterministic statistical summaries, tabular ingestion connectors, and rule-based validation audits.
          </p>
          <h4 className="mt-4 mb-2 text-sm font-semibold text-foreground">Highlights:</h4>
          <ul className="list-disc pl-5 mb-4 space-y-1 text-sm text-muted-foreground">
            <li>Tabular loaders mapping CSV, Excel, Parquet, and in-memory pandas/Polars DataFrames to normalized Dataset layers.</li>
            <li>Vectorized Profiling Engine computing 23 continuous numerical metrics, categorical frequencies, datetime ranges, text shapes, and correlation caps.</li>
            <li>Rule Engine executing 8 deterministic quality, statistical, and leakage audits.</li>
            <li>Command line tool (<code>featuresmith-cli</code>) for running audits in scripts or CI with structured exit codes.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="rel-distribution">
          <h3 id="rel-distribution" className="mb-3 text-lg font-semibold text-foreground">Distribution Packages Scope</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            The following packages are officially published on PyPI for <code>v0.1.0</code>:
          </p>
          <ul className="list-disc pl-5 mb-4 space-y-1 text-sm text-muted-foreground">
            <li><code>featuresmith-core</code>: Core engine library.</li>
            <li><code>featuresmith-cli</code>: CLI thin wrapper client.</li>
          </ul>
          <p className="text-sm text-muted-foreground">
            Note: <code>featuresmith-dashboard</code> is deferred to a future roadmap phase (Phase 5) and is not published in <code>v0.1.0</code>.
          </p>
        </section>
      </>
    )
  },
  "resources/faq": {
    title: "Frequently Asked Questions",
    subtitle: "Common questions about Featuresmith design, security, and usage",
    category: "Resources",
    seoTitle: "FAQ",
    seoDescription: "Answers to frequently asked questions about Featuresmith.",
    render: () => (
      <>
        <section className="mb-8" aria-labelledby="faq-privacy">
          <h3 id="faq-privacy" className="mb-2 text-base font-semibold text-foreground">Does Featuresmith send my dataset to third-party AI APIs?</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            <strong>No.</strong> Featuresmith v0.1.0 does not contain active LLM integrations or run cloud requests. In future AI phases (Phase 2+), provider integration is strictly opt-in and configured entirely via API keys. Furthermore, the AI layer only receives computed, aggregated statistical summaries (never raw data table rows), ensuring high privacy constraints.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="faq-scale">
          <h3 id="faq-scale" className="mb-2 text-base font-semibold text-foreground">How does Featuresmith scale on very large datasets?</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Featuresmith is built on top of <code>Polars</code>, utilizing lazy query execution and multi-threaded calculations to compute statistics instantly. On a standard machine, half a million rows are audited in under 3 seconds. To prevent combinatorial issues on very wide tables, Pearson correlations are capped at 100 columns by default.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="faq-extend">
          <h3 id="faq-extend" className="mb-2 text-base font-semibold text-foreground">Can I add custom connectors and rules?</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Yes! Custom connectors can be registered in <code>featuresmith.connectors.registry</code> and custom rules can be registered in the rule engine directly. Dynamic plugin autoloading via packaging entry points is scheduled for Phase 6.
          </p>
        </section>
      </>
    )
  },
  "resources/troubleshooting": {
    title: "Troubleshooting",
    subtitle: "Common errors and environmental hurdles with solutions",
    category: "Resources",
    seoTitle: "Troubleshooting",
    seoDescription: "Solve common issues with uv environments, pytest permissions, and package boundary imports.",
    render: () => (
      <>
        <section className="mb-8" aria-labelledby="ts-temp">
          <h3 id="ts-temp" className="mb-3 text-lg font-semibold text-foreground">Pytest permissions and temp lockouts on Windows</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            <strong>Symptom:</strong> Running <code>pytest</code> fails instantly with permission errors when creating temp folders.
          </p>
          <p className="mb-3 text-sm text-muted-foreground">
            <strong>Solution:</strong> The system default temp paths may have access restrictions. Override standard temp paths by pointing environment variables directly to a folder inside the workspace before invoking the test suite:
          </p>
          <CodeBlock code={`$env:TMP=".pytest_tmp"
$env:TEMP=".pytest_tmp"
uv run pytest`} language="bash" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="ts-import">
          <h3 id="ts-import" className="mb-3 text-lg font-semibold text-foreground">Import Linter constraints violation</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            <strong>Symptom:</strong> Running <code>lint-imports</code> triggers a contract failure: <code>Import of internal core module is not allowed from surface wrappers</code>.
          </p>
          <p className="mb-3 text-sm text-muted-foreground">
            <strong>Solution:</strong> Ensure your custom CLI or dashboard modifications only import from <code>featuresmith.api</code>. Importing from internal submodules (like <code>featuresmith.rules.engine</code> or <code>featuresmith.connectors.csv_connector</code>) is forbidden.
          </p>
        </section>
      </>
    )
  }
}
