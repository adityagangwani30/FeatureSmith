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
            Featuresmith is split into two packages depending on your surface requirements:
          </p>
          <ul className="list-disc pl-5 mb-4 space-y-1 text-sm text-muted-foreground">
            <li><strong>Python SDK</strong> only: Install <code>featuresmith-core</code></li>
            <li><strong>CLI & SDK</strong>: Install <code>featuresmith-cli</code></li>
          </ul>
          <CodeBlock code={`# Install Python SDK only
pip install featuresmith-core

# Install CLI & Python SDK
pip install featuresmith-cli`} language="bash" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="install-uv">
          <h3 id="install-uv" className="mb-3 text-lg font-semibold text-foreground">Using uv (Recommended)</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Add Featuresmith to your workspace dependencies:
          </p>
          <CodeBlock code={`# Add Python SDK only
uv add featuresmith-core

# Add CLI & Python SDK
uv add featuresmith-cli`} language="bash" showCopy />
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
          Featuresmith is designed to serve identical, deterministic results whether you are running
          scripted pipelines in Python, exploring interactive Jupyter notebooks, or triggering quality gates in the terminal.
        </p>

        <section className="mb-8" aria-labelledby="qs-notebooks">
          <h3 id="qs-notebooks" className="mb-3 text-lg font-semibold text-foreground">Interactive Tutorial Notebooks (Recommended)</h3>
          <p className="mb-4 text-sm text-muted-foreground">
            The fastest way to master Featuresmith v0.2.0 is through our official hands-on Jupyter notebook series in <code>examples/notebooks/</code>:
          </p>
          <div className="space-y-2.5 mb-6">
            {[
              { file: "01_getting_started.ipynb", title: "01. Getting Started", desc: "Dataset loading (fs.load), statistical profiling (fs.profile), automated review (fs.review), and readiness scoring (fs.score)." },
              { file: "02_dataset_review.ipynb", title: "02. Complete Dataset Review", desc: "Deep dive into the 8 automated reviewers, finding severities, and section categories." },
              { file: "03_ml_readiness_score.ipynb", title: "03. ML Readiness Score", desc: "Understanding 0–100 scorecards, mathematical dimension weights, and actionable remediation suggestions." },
              { file: "04_leakage_detection.ipynb", title: "04. Intelligent Leakage Detection", desc: "Catching target correlations, future timestamps, identifier shapes, and duplicate target copies." },
              { file: "05_dataset_diff.ipynb", title: "05. Dataset Diff Engine", desc: "Comparing dataset versions (fs.diff) to detect schema drift, missingness spikes, and quality regressions." },
              { file: "06_end_to_end_workflow.ipynb", title: "06. End-to-End Validation Gate", desc: "Building a production Python pre-training quality gate function to protect model training jobs." }
            ].map((nb) => (
              <div key={nb.file} className="flex flex-col sm:flex-row sm:items-center justify-between p-3 rounded-lg border border-border bg-card/60 gap-2">
                <div>
                  <span className="font-semibold text-xs text-foreground">{nb.title}</span>
                  <p className="text-[11px] text-muted-foreground">{nb.desc}</p>
                </div>
                <code className="font-mono text-[10px] text-primary bg-primary/10 px-2 py-0.5 rounded w-fit">{nb.file}</code>
              </div>
            ))}
          </div>
          <p className="text-xs text-muted-foreground">
            Explore all interactive tutorials on the <a href="/examples" className="text-primary hover:underline">Examples & Tutorials Page</a> or on <a href="https://github.com/adityagangwani30/FeatureSmith/tree/main/examples/notebooks" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">GitHub</a>.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="qs-sdk">
          <h3 id="qs-sdk" className="mb-3 text-lg font-semibold text-foreground">Python SDK Quick Start</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Run a dataset review using the pre-packaged <code>titanic.csv</code> dataset:
          </p>
          <CodeBlock code={`import featuresmith as fs

# 1. Load the dataset (CSV, Parquet, Excel, pandas/Polars DataFrame)
dataset = fs.load("examples/data/processed/titanic.csv")
print(f"Loaded {dataset.row_count} rows across {dataset.column_count} columns.")

# 2. Extract deterministic statistical profile
profile = fs.profile(dataset)
print(f"Missingness: {profile.dataset_summary.missing_percentage:.2f}%")

# 3. Perform automated dataset code review with 8 reviewers
review_result = fs.review(dataset, target_column="survived")
print(review_result.overall_summary)

# 4. Extract explainable 0–100 ML Readiness Scorecard
scorecard = fs.score(review_result)
if scorecard:
    print(f"ML Readiness Score: {scorecard.overall:.1f}/100")`} language="python" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="qs-cli">
          <h3 id="qs-cli" className="mb-3 text-lg font-semibold text-foreground">CLI Quick Start</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Verify dataset issues inside your shell:
          </p>
          <CodeBlock code={`# Run a complete review report with scorecard
featuresmith review examples/data/processed/titanic.csv --target survived

# Run target leakage and quality rule analysis
featuresmith analyze examples/data/processed/titanic.csv --target survived

# Compare two snapshot profiles (Dataset Diff Engine)
featuresmith diff examples/data/processed/titanic.csv examples/data/processed/titanic.csv --target survived`} language="bash" showCopy />
          <p className="mt-3 text-xs text-muted-foreground">
            The diff example compares the bundled <code>titanic.csv</code> against itself, returning an
            <code> unchanged</code> verdict. Point <code>featuresmith diff</code> at two different snapshots to detect schema and quality drift.
          </p>
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
                <strong>Compute and reasoning separation:</strong> Numerical algorithms and database scans run deterministically using vectorized backends. AI integrations (planned for Phase 6+) are only ever used for natural-language narration or chat - they never perform computation.
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

        <section className="mb-8" aria-labelledby="load-when-use">
          <h3 id="load-when-use" className="mb-3 text-lg font-semibold text-foreground">When to Use It</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Use at the start of any data validation script or pipeline step to parse files or wrap DataFrames into a standard <code>Dataset</code> object containing inferred schemas, column data types, row counts, and source metadata.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="load-args">
          <h3 id="load-args" className="mb-3 text-lg font-semibold text-foreground">Arguments</h3>
          <ul className="space-y-2 text-sm text-muted-foreground" role="list">
            <li><strong>source</strong>: <code>str</code> | <code>pandas.DataFrame</code> | <code>polars.DataFrame</code>. Local file path (<code>.csv</code>, <code>.xlsx</code>, <code>.xls</code>, <code>.parquet</code>) or loaded DataFrame object.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="load-returns">
          <h3 id="load-returns" className="mb-3 text-lg font-semibold text-foreground">Return Value</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Returns a normalized, shallowly immutable <code>Dataset</code> dataclass containing <code>dataframe</code>, <code>backend</code> (<code>"polars"</code> or <code>"pandas"</code>), <code>schema</code> (<code>DatasetSchema</code>), <code>row_count</code>, <code>column_count</code>, <code>dtypes</code>, <code>source</code>, and <code>file_size</code>.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="load-exceptions">
          <h3 id="load-exceptions" className="mb-3 text-lg font-semibold text-foreground">Exceptions</h3>
          <ul className="list-disc pl-5 space-y-1 text-sm text-muted-foreground">
            <li><code>ConnectorError</code>: Base exception raised when a data source cannot be validated or loaded.</li>
            <li><code>SourceNotFoundError</code>: Raised when the target local file path does not exist.</li>
            <li><code>UnsupportedFormatError</code>: Raised when the file extension or object type is unsupported.</li>
            <li><code>SourceParseError</code>: Raised when parsing or reading the file content fails.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="load-example">
          <h3 id="load-example" className="mb-3 text-lg font-semibold text-foreground">Example</h3>
          <CodeBlock code={`import featuresmith as fs
import polars as pl

# Load from local file path (CSV, Parquet, Excel)
ds = fs.load("train.parquet")
print(f"Loaded {ds.row_count} rows across {ds.column_count} columns via {ds.backend}.")

# Load from in-memory Polars or pandas DataFrame
df = pl.DataFrame({"x": [1, 2, 3], "y": [4.0, 5.0, 6.0]})
ds_mem = fs.load(df)
print(ds_mem.preview(2))`} language="python" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="load-notes">
          <h3 id="load-notes" className="mb-3 text-lg font-semibold text-foreground">Notes and Limitations</h3>
          <ul className="list-disc pl-5 space-y-2 text-sm text-muted-foreground border-l-2 border-amber-500 bg-amber-500/5 p-4 rounded-r-lg">
            <li><strong>Zero Data Copying</strong>: In-memory pandas or Polars DataFrames are wrapped directly without copying memory buffers.</li>
            <li><strong>Backend Engines</strong>: Polars is used for CSV and Parquet files; pandas is used for Excel files.</li>
          </ul>
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

        <section className="mb-8" aria-labelledby="profile-when-use">
          <h3 id="profile-when-use" className="mb-3 text-lg font-semibold text-foreground">When to Use It</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Use when you need detailed statistical profiles of dataset columns (min, max, mean, quantiles, missingness, cardinality, frequency tables, correlations) without running rule evaluations or review scoring.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="profile-args">
          <h3 id="profile-args" className="mb-3 text-lg font-semibold text-foreground">Arguments</h3>
          <ul className="space-y-3 text-sm text-muted-foreground" role="list">
            <li><strong>source</strong>: <code>Dataset</code> | <code>str</code> | <code>DataFrame</code>. Pre-loaded Dataset or file/data source.</li>
            <li><strong>max_correlation_columns</strong>: <code>int</code> (default 100). Column cap for Pearson correlation computations to prevent combinatorial blowup.</li>
            <li><strong>max_frequency_table_size</strong>: <code>int</code> (default 1000). Maximum unique categories to track in frequency table summaries.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="profile-returns">
          <h3 id="profile-returns" className="mb-3 text-lg font-semibold text-foreground">Return Value</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Returns a frozen <code>ProfileResult</code> dataclass containing <code>dataset_summary</code>, <code>column_profiles</code>, typed profiles (<code>numeric_profiles</code>, <code>categorical_profiles</code>, <code>datetime_profiles</code>, <code>text_profiles</code>), missingness & duplicate summaries, correlation matrices, and execution metadata.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="profile-exceptions">
          <h3 id="profile-exceptions" className="mb-3 text-lg font-semibold text-foreground">Exceptions</h3>
          <ul className="list-disc pl-5 space-y-1 text-sm text-muted-foreground">
            <li><code>ConnectorError</code>: Raised if an unresolved file path or invalid DataFrame source fails to load before profiling.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="profile-example">
          <h3 id="profile-example" className="mb-3 text-lg font-semibold text-foreground">Example</h3>
          <CodeBlock code={`import featuresmith as fs

profile = fs.profile("customers.csv", max_correlation_columns=50)

# Inspect column summaries
print(profile.column_profiles["age"].missing_count)
print(profile.dataset_summary.row_count)
print(profile.numeric_profiles["income"].mean)`} language="python" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="profile-notes">
          <h3 id="profile-notes" className="mb-3 text-lg font-semibold text-foreground">Notes and Limitations</h3>
          <ul className="list-disc pl-5 space-y-2 text-sm text-muted-foreground border-l-2 border-amber-500 bg-amber-500/5 p-4 rounded-r-lg">
            <li><strong>Deterministic Engine</strong>: Computations run on Polars or pandas backend using vectorized primitives.</li>
            <li><strong>Frozen Output</strong>: The returned <code>ProfileResult</code> is fully frozen, slotted, and serializable via <code>profile.to_dict()</code>.</li>
          </ul>
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

        <section className="mb-8" aria-labelledby="analyze-when-use">
          <h3 id="analyze-when-use" className="mb-3 text-lg font-semibold text-foreground">When to Use It</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Use when you want to compute statistical profiles and evaluate quality rules simultaneously to obtain a list of flagged <code>RuleFinding</code> objects.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="analyze-args">
          <h3 id="analyze-args" className="mb-3 text-lg font-semibold text-foreground">Arguments</h3>
          <ul className="space-y-3 text-sm text-muted-foreground" role="list">
            <li><strong>source</strong>: <code>Dataset</code> | <code>str</code> | <code>DataFrame</code>. Input data or path.</li>
            <li><strong>target_column</strong>: <code>str | None</code> (default None). Target column name. Required for target leakage checks.</li>
            <li><strong>enabled_rules</strong>: <code>list[str] | None</code> (default None). Explicit rule IDs to evaluate. If omitted, runs all defaults.</li>
            <li><strong>rule_config</strong>: <code>dict[str, Any] | None</code>. Keyword argument config overrides for specific rules.</li>
            <li><strong>max_correlation_columns</strong>: <code>int</code> (default 100). Cap limit for correlation matrix computation.</li>
            <li><strong>max_frequency_table_size</strong>: <code>int</code> (default 1000). Frequency table storage cap.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="analyze-returns">
          <h3 id="analyze-returns" className="mb-3 text-lg font-semibold text-foreground">Return Value</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Returns a frozen <code>RuleResult</code> dataclass containing <code>profile</code> (<code>ProfileResult</code>), <code>findings</code> (sequence of <code>RuleFinding</code>), <code>executed_rules</code>, <code>execution_time_ms</code>, and <code>failed_rules</code> (mapping of rule ID to error traceback).
          </p>
        </section>

        <section className="mb-8" aria-labelledby="analyze-exceptions">
          <h3 id="analyze-exceptions" className="mb-3 text-lg font-semibold text-foreground">Exceptions</h3>
          <ul className="list-disc pl-5 space-y-1 text-sm text-muted-foreground">
            <li><code>ConnectorError</code>: Raised if the source dataset fails to load before profiling.</li>
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

print(f"Executed {len(result.executed_rules)} rules with {len(result.findings)} findings.")
for finding in result.findings:
    print(f"[{finding.severity}] {finding.title} in {finding.column_name}")`} language="python" showCopy />
        </section>
      </>
    )
  },
  "sdk/models": {
    title: "Data Models",
    subtitle: "SDK Reference: the complete typed output schema",
    category: "Python SDK",
    seoTitle: "SDK Data Models",
    seoDescription: "Explore Featuresmith's typed output objects across the Profiling, Rule, Review, Scoring, Leakage, and Dataset Diff engines.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Every Featuresmith result is a Python dataclass with <code>frozen=True</code> and <code>slots=True</code>, so instances are read-only, fast, and safely serializable. Each top-level result object exposes a <code>to_dict()</code> method that produces a plain, JSON-ready dictionary.
        </p>

        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          The models are grouped by the engine that produces them. Use the pages below for the full field-by-field reference:
        </p>

        <div className="grid gap-3 sm:grid-cols-2 mb-8">
          {[
            { href: "/docs/sdk/models/profile", title: "Profile Models", desc: "DatasetSummary, ColumnProfile, the four typed column profiles, the three aggregates, and both metadata records returned by fs.profile()." },
            { href: "/docs/sdk/models/rules", title: "Rule & Finding Models", desc: "RuleResult, RuleFinding, finding severities, and the eight built-in validation rules with their default thresholds." },
            { href: "/docs/sdk/models/review", title: "Review Models", desc: "ReviewResult, ReviewSection, the six ReviewCategory values, the four Severity levels, and the eight built-in reviewers." },
            { href: "/docs/sdk/models/score", title: "Score Models", desc: "MLReadinessScore, DimensionScore, the eight scoring dimensions, and the deduction formula behind the 0-100 scorecard." },
            { href: "/docs/sdk/models/leakage", title: "Leakage Models", desc: "LeakageFinding and the six pattern detectors that flag target leakage." },
            { href: "/docs/sdk/models/diff", title: "Diff Models", desc: "DatasetDiffResult and every nested delta model produced by fs.diff()." },
          ].map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="group flex flex-col rounded-lg border border-border bg-card p-4 transition-all duration-150 hover:border-primary/30 hover:bg-accent"
            >
              <span className="mb-1 text-sm font-medium text-foreground">{link.title}</span>
              <span className="text-xs leading-relaxed text-muted-foreground">{link.desc}</span>
            </a>
          ))}
        </div>

        <section className="mb-8" aria-labelledby="models-common">
          <h3 id="models-common" className="mb-3 text-lg font-semibold text-foreground">Related References</h3>
          <ul className="list-disc pl-5 space-y-1 text-sm text-muted-foreground">
            <li>The normalized input model is documented on the <a href="/docs/sdk/dataset" className="text-primary hover:underline">Dataset page</a>.</li>
            <li>Error classes raised during ingestion are documented on the <a href="/docs/sdk/exceptions" className="text-primary hover:underline">Exceptions page</a>.</li>
          </ul>
        </section>
      </>
    )
  },
  "sdk/models/profile": {
    title: "Profile Models",
    subtitle: "SDK Reference: profiling result objects",
    category: "Python SDK",
    seoTitle: "SDK Profile Models",
    seoDescription: "Full field reference for ProfileResult and every nested profiling model returned by fs.profile().",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          <code>fs.profile()</code> returns a single frozen <code>ProfileResult</code>. All nested models below live in <code>featuresmith.core.profile_result</code> and are re-exported as values on the result, so they are reached via attribute access rather than imports.
        </p>

        <section className="mb-8" aria-labelledby="prof-result">
          <h3 id="prof-result" className="mb-3 text-lg font-semibold text-foreground">ProfileResult</h3>
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

    def to_dict(self) -> dict[str, Any]: ...`} language="python" showCopy={false} />
          <p className="mt-3 text-sm text-muted-foreground">
            The typed profile mappings are keyed by column name and only contain columns of the matching <code>logical_type</code>.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="prof-summary">
          <h3 id="prof-summary" className="mb-3 text-lg font-semibold text-foreground">DatasetSummary</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            High-level dataset statistics.
          </p>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class DatasetSummary:
    row_count: int
    column_count: int
    size_in_bytes: int | None
    missing_percentage: float
    duplicate_percentage: float
    num_numeric_columns: int
    num_categorical_columns: int
    num_datetime_columns: int
    num_text_columns: int
    num_constant_columns: int
    num_fully_empty_columns: int`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="prof-column">
          <h3 id="prof-column" className="mb-3 text-lg font-semibold text-foreground">ColumnProfile</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            General profile summary present for every column in the dataset.
          </p>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class ColumnProfile:
    name: str
    dtype: str
    logical_type: str  # "numeric" | "categorical" | "datetime" | "text"
    missing_count: int
    missing_percentage: float
    is_constant: bool
    is_fully_empty: bool`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="prof-numeric">
          <h3 id="prof-numeric" className="mb-3 text-lg font-semibold text-foreground">NumericProfile</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Detailed statistics for a numeric column.
          </p>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class NumericProfile:
    column_name: str
    count: int
    missing_count: int
    missing_percentage: float
    unique_count: int
    mean: float | None
    median: float | None
    mode: float | None
    minimum: float | None
    maximum: float | None
    range: float | None
    variance: float | None
    std_dev: float | None
    q1: float | None
    q2: float | None
    q3: float | None
    iqr: float | None
    sum: float | None
    zero_count: int
    negative_count: int
    positive_count: int
    skewness: float | None
    kurtosis: float | None`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="prof-categorical">
          <h3 id="prof-categorical" className="mb-3 text-lg font-semibold text-foreground">CategoricalProfile</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Detailed statistics for a categorical column. The <code>frequency_table</code> is capped by the <code>max_frequency_table_size</code> profiling option (default 1000).
          </p>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class CategoricalProfile:
    column_name: str
    cardinality: int
    unique_count: int
    missing_count: int
    frequency_table: Mapping[str, int]
    top_values: Sequence[tuple[str, int]]
    least_frequent_values: Sequence[tuple[str, int]]
    most_common_category: str | None
    entropy: float | None  # Shannon entropy, base 2`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="prof-datetime">
          <h3 id="prof-datetime" className="mb-3 text-lg font-semibold text-foreground">DatetimeProfile</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class DatetimeProfile:
    column_name: str
    minimum: str | None        # ISO 8601
    maximum: str | None        # ISO 8601
    range_days: float | None
    missing_count: int
    earliest_record: str | None
    latest_record: str | None`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="prof-text">
          <h3 id="prof-text" className="mb-3 text-lg font-semibold text-foreground">TextProfile</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class TextProfile:
    column_name: str
    avg_length: float | None
    min_length: int | None
    max_length: int | None
    empty_strings: int
    whitespace_only: int
    char_count: int
    word_count: int`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="prof-aggregates">
          <h3 id="prof-aggregates" className="mb-3 text-lg font-semibold text-foreground">Aggregate Summaries</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class MissingValueSummary:
    column_missing_counts: Mapping[str, int]
    column_missing_percentages: Mapping[str, float]
    total_missing: int
    dataset_missing_percentage: float


@dataclass(frozen=True, slots=True)
class DuplicateSummary:
    duplicate_rows_count: int
    duplicate_percentage: float
    constant_columns: Sequence[str]
    fully_empty_columns: Sequence[str]


@dataclass(frozen=True, slots=True)
class CorrelationSummary:
    pearson: Mapping[str, Mapping[str, float | None]]
    spearman: Mapping[str, Mapping[str, float | None]]  # reserved
    kendall: Mapping[str, Mapping[str, float | None]]  # reserved`} language="python" showCopy={false} />
          <p className="mt-3 text-sm text-muted-foreground">
            <code>pearson</code> maps column A to column B to the correlation coefficient (or <code>None</code> when undefined). <code>spearman</code> and <code>kendall</code> are reserved and currently empty.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="prof-metadata">
          <h3 id="prof-metadata" className="mb-3 text-lg font-semibold text-foreground">Metadata Records</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class DatasetMetadata:
    source: str | None
    file_size: int | None
    backend: str  # "pandas" | "polars"
    custom_metadata: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class ExecutionMetadata:
    start_time: str  # ISO 8601
    duration_seconds: float
    featuresmith_version: str`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="prof-example">
          <h3 id="prof-example" className="mb-3 text-lg font-semibold text-foreground">Example</h3>
          <CodeBlock code={`import featuresmith as fs

profile = fs.profile("customers.csv")

print(profile.dataset_summary.row_count)
print(profile.numeric_profiles["age"].mean)
print(profile.categorical_profiles["city"].most_common_category)
print(profile.missing_value_summary.dataset_missing_percentage)`} language="python" showCopy />
        </section>
      </>
    )
  },
  "sdk/models/rules": {
    title: "Rule & Finding Models",
    subtitle: "SDK Reference: rule engine output objects",
    category: "Python SDK",
    seoTitle: "SDK Rule & Finding Models",
    seoDescription: "Full field reference for RuleResult, RuleFinding, finding severities, and the eight built-in validation rules.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          <code>fs.analyze()</code> runs the Profiling Engine and then the Rule Engine, returning a single frozen <code>RuleResult</code>. Rules are deterministic, isolated, and never fail the whole run: a rule that crashes is recorded in <code>failed_rules</code> instead.
        </p>

        <section className="mb-8" aria-labelledby="rule-result">
          <h3 id="rule-result" className="mb-3 text-lg font-semibold text-foreground">RuleResult</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class RuleResult:
    profile: ProfileResult
    findings: Sequence[RuleFinding]
    executed_rules: Sequence[str]
    execution_time_ms: float
    failed_rules: Mapping[str, str]  # rule ID -> error traceback

    def to_dict(self) -> dict[str, Any]: ...`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="rule-finding">
          <h3 id="rule-finding" className="mb-3 text-lg font-semibold text-foreground">RuleFinding</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            A single issue identified by one rule. <code>column_name</code> is <code>None</code> for dataset-wide findings (for example duplicate rows).
          </p>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class RuleFinding:
    rule_id: str
    rule_name: str
    category: str  # "quality" | "statistical" | "leakage" | "diff"
    severity: str  # "info" | "warning" | "critical"
    column_name: str | None
    title: str
    description: str
    evidence: Mapping[str, Any]
    confidence: float = 1.0
    id: str = ...          # auto-generated UUID
    metadata: Mapping[str, Any] = ...`} language="python" showCopy={false} />
          <p className="mt-3 text-sm text-muted-foreground">
            <code>category</code> uses lowercase strings. The <code>"diff"</code> category is used by findings derived from a <code>DatasetDiffResult</code> via <code>findings_from_diff()</code>.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="rule-builtins">
          <h3 id="rule-builtins" className="mb-3 text-lg font-semibold text-foreground">Built-in Rules</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            All eight rules are enabled by default. Their defaults can be overridden per rule through the <code>rule_config</code> argument of <code>fs.analyze()</code>:
          </p>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="min-w-full divide-y divide-border text-left text-sm">
              <thead className="bg-muted/50 text-xs font-semibold uppercase tracking-wider text-foreground">
                <tr>
                  <th className="px-4 py-3">Rule ID</th>
                  <th className="px-4 py-3">Name</th>
                  <th className="px-4 py-3">Severity</th>
                  <th className="px-4 py-3">Config Keys (defaults)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-muted-foreground">
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">quality.missing_value_threshold</td>
                  <td className="px-4 py-3">Missing Value Threshold</td>
                  <td className="px-4 py-3">warning (escalates to critical above 50%)</td>
                  <td className="px-4 py-3 font-mono text-xs">threshold=20.0</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">quality.duplicate_rows</td>
                  <td className="px-4 py-3">Duplicate Rows</td>
                  <td className="px-4 py-3">warning</td>
                  <td className="px-4 py-3 font-mono text-xs">threshold=10.0</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">quality.constant_columns</td>
                  <td className="px-4 py-3">Constant Columns</td>
                  <td className="px-4 py-3">warning</td>
                  <td className="px-4 py-3 font-mono text-xs">—</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">quality.fully_empty_columns</td>
                  <td className="px-4 py-3">Fully Empty Columns</td>
                  <td className="px-4 py-3">critical</td>
                  <td className="px-4 py-3 font-mono text-xs">—</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">statistical.high_cardinality</td>
                  <td className="px-4 py-3">High Cardinality</td>
                  <td className="px-4 py-3">warning</td>
                  <td className="px-4 py-3 font-mono text-xs">threshold=0.50, min_cardinality=20</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">statistical.outliers</td>
                  <td className="px-4 py-3">Outlier Detection</td>
                  <td className="px-4 py-3">warning</td>
                  <td className="px-4 py-3 font-mono text-xs">factor=1.5 (IQR multiplier)</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">statistical.high_correlation</td>
                  <td className="px-4 py-3">High Correlation</td>
                  <td className="px-4 py-3">warning</td>
                  <td className="px-4 py-3 font-mono text-xs">threshold=0.90</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">leakage.potential_leakage</td>
                  <td className="px-4 py-3">Potential Target Leakage</td>
                  <td className="px-4 py-3">critical</td>
                  <td className="px-4 py-3 font-mono text-xs">target_column=None, threshold=0.99</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p className="mt-3 text-sm text-muted-foreground">
            The missing-value rule flags every column whose <code>missing_percentage</code> exceeds <code>threshold</code>. The high-cardinality rule flags categorical columns whose unique-ratio <code>cardinality / non-missing</code> exceeds <code>threshold</code> while cardinality is at least <code>min_cardinality</code>. The outlier rule flags numeric columns with values beyond <code>[Q1 - factor*IQR, Q3 + factor*IQR]</code>.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="rule-config">
          <h3 id="rule-config" className="mb-3 text-lg font-semibold text-foreground">Configuring Rules</h3>
          <CodeBlock code={`import featuresmith as fs

result = fs.analyze(
    "train.csv",
    target_column="churn",
    enabled_rules=[
        "quality.missing_value_threshold",
        "statistical.high_correlation",
    ],
    rule_config={
        "quality.missing_value_threshold": {"threshold": 15.0},
        "statistical.high_correlation": {"threshold": 0.85},
    },
)

for finding in result.findings:
    print(f"[{finding.severity}] {finding.title}")`} language="python" showCopy />
        </section>
      </>
    )
  },
  "sdk/models/review": {
    title: "Review Models",
    subtitle: "SDK Reference: review engine output objects",
    category: "Python SDK",
    seoTitle: "SDK Review Models",
    seoDescription: "Full field reference for ReviewResult, ReviewSection, categories, severities, and the eight built-in reviewers.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          <code>fs.review()</code> composes the Profiling and Rule Engines into one structured review. It profiles once, computes rule findings once, then dispatches every enabled reviewer against that frozen context. The result is a single frozen <code>ReviewResult</code>.
        </p>

        <section className="mb-8" aria-labelledby="review-result-model">
          <h3 id="review-result-model" className="mb-3 text-lg font-semibold text-foreground">ReviewResult</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class ReviewResult:
    engine_version: str                       # "0.2.0"
    dataset_summary: DatasetSummary
    generated_at: datetime                    # UTC
    sections: Sequence[ReviewSection]
    overall_summary: str
    score: MLReadinessScore | None
    diff: Any = None                          # reserved for diff-aware reviews

    def to_dict(self) -> dict[str, Any]: ...`} language="python" showCopy={false} />
          <p className="mt-3 text-sm text-muted-foreground">
            Sections are ordered from most severe (<code>critical</code>) to least (<code>passed</code>). <code>score</code> is populated by the review when at least one scoring dimension is applicable; otherwise it is <code>None</code>.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="review-section-model">
          <h3 id="review-section-model" className="mb-3 text-lg font-semibold text-foreground">ReviewSection</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class ReviewSection:
    id: str
    title: str
    category: ReviewCategory
    severity: Severity
    findings: Sequence[RuleFinding]
    narrative: str | None = None
    recommendations: Sequence[Any] = ()

    def to_dict(self) -> dict[str, Any]: ...`} language="python" showCopy={false} />
          <p className="mt-3 text-sm text-muted-foreground">
            The section <code>severity</code> is the highest severity among its findings, or <code>PASSED</code> when the section is clean.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="review-enums">
          <h3 id="review-enums" className="mb-3 text-lg font-semibold text-foreground">ReviewCategory and Severity</h3>
          <CodeBlock code={`class ReviewCategory(Enum):
    SCHEMA = "schema"
    QUALITY = "quality"
    LEAKAGE = "leakage"
    DIFF = "diff"
    FEATURE_QUALITY = "feature_quality"
    CUSTOM = "custom"


class Severity(Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    PASSED = "passed"`} language="python" showCopy={false} />
          <p className="mt-3 text-sm text-muted-foreground">
            <code>DIFF</code>, <code>FEATURE_QUALITY</code>, and <code>CUSTOM</code> are reserved categories. The built-in reviewers currently emit <code>schema</code>, <code>quality</code>, and <code>leakage</code> sections.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="review-builtins">
          <h3 id="review-builtins" className="mb-3 text-lg font-semibold text-foreground">Built-in Reviewers</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Eight reviewers ship out of the box. They are configurable via the <code>reviewer_config</code> argument of <code>fs.review()</code>, keyed by reviewer ID:
          </p>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="min-w-full divide-y divide-border text-left text-sm">
              <thead className="bg-muted/50 text-xs font-semibold uppercase tracking-wider text-foreground">
                <tr>
                  <th className="px-4 py-3">Reviewer ID</th>
                  <th className="px-4 py-3">Section</th>
                  <th className="px-4 py-3">Category</th>
                  <th className="px-4 py-3">Config Keys (defaults)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-muted-foreground">
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">review.schema.health</td>
                  <td className="px-4 py-3">Schema Health</td>
                  <td className="px-4 py-3">schema</td>
                  <td className="px-4 py-3 font-mono text-xs">—</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">review.schema.types</td>
                  <td className="px-4 py-3">Data Types</td>
                  <td className="px-4 py-3">schema</td>
                  <td className="px-4 py-3 font-mono text-xs">identifier_min_count=10</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">review.quality.missingness</td>
                  <td className="px-4 py-3">Missing Values</td>
                  <td className="px-4 py-3">quality</td>
                  <td className="px-4 py-3 font-mono text-xs">threshold=20.0</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">review.quality.duplicates</td>
                  <td className="px-4 py-3">Duplicate Rows</td>
                  <td className="px-4 py-3">quality</td>
                  <td className="px-4 py-3 font-mono text-xs">threshold=10.0</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">review.quality.constants</td>
                  <td className="px-4 py-3">Constant Columns</td>
                  <td className="px-4 py-3">quality</td>
                  <td className="px-4 py-3 font-mono text-xs">—</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">review.quality.cardinality</td>
                  <td className="px-4 py-3">High Cardinality</td>
                  <td className="px-4 py-3">quality</td>
                  <td className="px-4 py-3 font-mono text-xs">threshold=0.50, min_cardinality=20</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">review.quality.basic_statistics</td>
                  <td className="px-4 py-3">Basic Statistics</td>
                  <td className="px-4 py-3">quality</td>
                  <td className="px-4 py-3 font-mono text-xs">skew_threshold=2.0, kurtosis_threshold=10.0</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">review.leakage</td>
                  <td className="px-4 py-3">Leakage Detection</td>
                  <td className="px-4 py-3">leakage</td>
                  <td className="px-4 py-3 font-mono text-xs">detectors=None (built-in set)</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p className="mt-3 text-sm text-muted-foreground">
            The schema health reviewer surfaces fully empty columns (via <code>FullyEmptyColumnsRule</code>) plus structural warnings for empty datasets. The missingness reviewer intentionally excludes fully empty columns so each issue is reported exactly once. The data types reviewer flags numeric columns where every non-null value is distinct (identifier-like) and columns classified as free text. The leakage reviewer dispatches the pattern detectors documented on the <a href="/docs/sdk/models/leakage" className="text-primary hover:underline">Leakage Models</a> page.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="review-config-example">
          <h3 id="review-config-example" className="mb-3 text-lg font-semibold text-foreground">Configuring Reviewers</h3>
          <CodeBlock code={`import featuresmith as fs

result = fs.review(
    "train.csv",
    target_column="churn",
    reviewer_config={
        "review.quality.missingness": {"threshold": 25.0},
        "review.quality.cardinality": {"threshold": 0.40},
    },
)

for section in result.sections:
    print(f"{section.severity.value.upper()} - {section.title}: {len(section.findings)} finding(s)")`} language="python" showCopy />
        </section>
      </>
    )
  },
  "sdk/models/score": {
    title: "Score Models",
    subtitle: "SDK Reference: ML Readiness Score objects",
    category: "Python SDK",
    seoTitle: "SDK Score Models",
    seoDescription: "Full field reference for MLReadinessScore, DimensionScore, the eight scoring dimensions, and the deduction formula.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          The ML Readiness Score is a deterministic 0-100 score computed entirely from an existing <code>ReviewResult</code>. It never reads raw data: every dimension derives from the findings a reviewer already produced, so a given review always yields the same versioned score.
        </p>

        <section className="mb-8" aria-labelledby="score-ml-result">
          <h3 id="score-ml-result" className="mb-3 text-lg font-semibold text-foreground">MLReadinessScore</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class MLReadinessScore:
    scoring_version: str                 # "0.2.0"
    overall: float                       # 0.0 to 100.0
    dimensions: tuple[DimensionScore, ...]
    summary: str
    positive_findings: tuple[str, ...]
    negative_findings: tuple[RuleFinding, ...]

    def to_dict(self) -> dict[str, Any]: ...`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="score-dimension">
          <h3 id="score-dimension" className="mb-3 text-lg font-semibold text-foreground">DimensionScore</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class DimensionScore:
    id: str
    label: str
    score: float
    weight: float
    rationale: str
    contributing_findings: tuple[RuleFinding, ...]
    suggested_actions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]: ...`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="score-dimensions">
          <h3 id="score-dimensions" className="mb-3 text-lg font-semibold text-foreground">The Eight Dimensions</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Each dimension maps one-to-one onto a built-in reviewer section and carries a uniform default weight of <code>1.0</code>:
          </p>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="min-w-full divide-y divide-border text-left text-sm">
              <thead className="bg-muted/50 text-xs font-semibold uppercase tracking-wider text-foreground">
                <tr>
                  <th className="px-4 py-3">Dimension ID</th>
                  <th className="px-4 py-3">Dimension</th>
                  <th className="px-4 py-3">Backing Section</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-muted-foreground">
                {[
                  ["score.schema_health", "Schema Health", "review.schema.health"],
                  ["score.missing_values", "Missing Values", "review.quality.missingness"],
                  ["score.duplicate_records", "Duplicate Records", "review.quality.duplicates"],
                  ["score.data_types", "Data Types", "review.schema.types"],
                  ["score.constant_columns", "Constant Columns", "review.quality.constants"],
                  ["score.high_cardinality", "High Cardinality", "review.quality.cardinality"],
                  ["score.dataset_structure", "Dataset Structure", "review.quality.basic_statistics"],
                  ["score.leakage_risk", "Leakage Risk", "review.leakage"],
                ].map(([id, label, section]) => (
                  <tr key={id}>
                    <td className="px-4 py-3 font-mono text-xs">{id}</td>
                    <td className="px-4 py-3">{label}</td>
                    <td className="px-4 py-3 font-mono text-xs">{section}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="mb-8" aria-labelledby="score-formula">
          <h3 id="score-formula" className="mb-3 text-lg font-semibold text-foreground">Scoring Formula</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Each dimension starts at a perfect <code>100.0</code> and deducts a fixed, versioned amount per finding based on severity:
          </p>
          <ul className="list-disc pl-5 mb-4 space-y-1 text-sm text-muted-foreground">
            <li><strong>Critical finding</strong>: -30.0 points</li>
            <li><strong>Warning finding</strong>: -15.0 points</li>
            <li><strong>Info finding</strong>: -5.0 points</li>
          </ul>
          <p className="mb-3 text-sm text-muted-foreground">
            Scores are clamped to <code>[0, 100]</code> and rounded to one decimal place. The overall score is the weighted average:
          </p>
          <div className="my-4 bg-muted p-3 rounded font-mono text-xs text-center border border-border">
            overall = sum(dim.score * dim.weight) / sum(dim.weight)
          </div>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Inapplicable dimensions (whose backing section is absent) are omitted and their weights renormalized automatically, so a regression-only dataset is not penalized for classification-specific metrics.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="score-example-model">
          <h3 id="score-example-model" className="mb-3 text-lg font-semibold text-foreground">Example</h3>
          <CodeBlock code={`import featuresmith as fs

result = fs.review("data.csv", target_column="label")
score = fs.score(result)

if score:
    print(f"Overall: {score.overall}/100")
    for dim in score.dimensions:
        if dim.score < 100.0:
            print(f"  {dim.label}: {dim.score}/100 - {dim.rationale}")
            print(f"    Actions: {dim.suggested_actions}")`} language="python" showCopy />
        </section>
      </>
    )
  },
  "sdk/models/leakage": {
    title: "Leakage Models",
    subtitle: "SDK Reference: leakage detection objects",
    category: "Python SDK",
    seoTitle: "SDK Leakage Models",
    seoDescription: "Full field reference for LeakageFinding and the six built-in leakage pattern detectors.",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          Target leakage occurs when a feature carries information from the future or from the target itself, giving a model an unfair advantage at training time. The <code>review.leakage</code> reviewer runs named pattern detectors against the frozen profile; each detector emits <code>LeakageFinding</code> objects.
        </p>

        <section className="mb-8" aria-labelledby="leakage-finding">
          <h3 id="leakage-finding" className="mb-3 text-lg font-semibold text-foreground">LeakageFinding</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class LeakageFinding:
    pattern: str                 # detector ID that produced this finding
    column_name: str
    title: str
    rationale: str
    evidence: Mapping[str, Any]
    confidence: float            # 0.0 to 1.0
    severity: str                # "info" | "warning" | "critical"
    suggested_action: str`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="leakage-detectors">
          <h3 id="leakage-detectors" className="mb-3 text-lg font-semibold text-foreground">The Six Built-in Detectors</h3>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="min-w-full divide-y divide-border text-left text-sm">
              <thead className="bg-muted/50 text-xs font-semibold uppercase tracking-wider text-foreground">
                <tr>
                  <th className="px-4 py-3">Pattern ID</th>
                  <th className="px-4 py-3">Detector</th>
                  <th className="px-4 py-3">What It Flags</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-muted-foreground">
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">target_correlation</td>
                  <td className="px-4 py-3">Target Correlation</td>
                  <td className="px-4 py-3">Columns with extreme correlation to the declared target.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">identifier</td>
                  <td className="px-4 py-3">Identifier Shape</td>
                  <td className="px-4 py-3">ID-like columns that also correlate with the target.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">timestamp</td>
                  <td className="px-4 py-3">Timestamp Leakage</td>
                  <td className="px-4 py-3">Datetime columns that extend past a declared prediction cutoff.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">future_info</td>
                  <td className="px-4 py-3">Future Information</td>
                  <td className="px-4 py-3">Columns named like the outcome, or datetime columns extending past a declared event timestamp.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">duplicate_target</td>
                  <td className="px-4 py-3">Duplicate Target Information</td>
                  <td className="px-4 py-3">Columns that are a near-deterministic copy or transform of the target.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono text-xs">suspicious_correlation</td>
                  <td className="px-4 py-3">Suspicious Correlation</td>
                  <td className="px-4 py-3">Suspicious correlations with a secondary signal, never magnitude alone.</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p className="mt-3 text-sm text-muted-foreground">
            Detectors run through <code>builtin_detectors()</code> and are supplied to the <code>review.leakage</code> reviewer. Detector findings carry a confidence label: <code>High</code> at or above 0.7, <code>Medium</code> at or above 0.4, and <code>Low</code> below that.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="leakage-merge">
          <h3 id="leakage-merge" className="mb-3 text-lg font-semibold text-foreground">From Detectors to Review Findings</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            The leakage reviewer merges detector findings into the shared <code>RuleFinding</code> schema so every section speaks the same language:
          </p>
          <ul className="list-disc pl-5 space-y-1 text-sm text-muted-foreground">
            <li>One pattern on a column becomes a finding with <code>rule_id = "leakage.&lt;pattern&gt;"</code>.</li>
            <li>Several patterns on the same column are merged into a single finding with <code>rule_id = "leakage.multiple_patterns"</code>, keeping the worst severity and the highest confidence.</li>
            <li>The original pattern, confidence level, rationale, and suggested action are preserved in the finding's <code>evidence</code> and <code>metadata</code>.</li>
          </ul>
        </section>
      </>
    )
  },
  "sdk/models/diff": {
    title: "Diff Models",
    subtitle: "SDK Reference: dataset diff result objects",
    category: "Python SDK",
    seoTitle: "SDK Diff Models",
    seoDescription: "Full field reference for DatasetDiffResult and every nested delta model returned by fs.diff().",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          <code>fs.diff()</code> profiles two snapshots and compares them, returning one frozen, serializable <code>DatasetDiffResult</code> — the equivalent of a git diff for structured datasets. All models below live in <code>featuresmith.diff.schema</code>.
        </p>

        <section className="mb-8" aria-labelledby="diff-result">
          <h3 id="diff-result" className="mb-3 text-lg font-semibold text-foreground">DatasetDiffResult</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class DatasetDiffResult:
    version: str                       # "0.2.0"
    schema: SchemaDiff
    structure: StructureDiff
    missing_values: tuple[MissingValueDiff, ...]
    duplicates: DuplicateDiff
    constant_columns: ConstantColumnDiff
    cardinality: tuple[CardinalityDiff, ...]
    statistics: tuple[StatisticDiff, ...]
    distributions: tuple[DistributionDiff, ...]
    leakage: LeakageDiff | None        # None when no target column is given
    summary: DatasetDiffSummary
    overall_summary: str

    def to_dict(self) -> dict[str, Any]: ...`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="diff-config">
          <h3 id="diff-config" className="mb-3 text-lg font-semibold text-foreground">DiffConfig</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Tunable thresholds for the diff engine:
          </p>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class DiffConfig:
    distribution_shift_threshold: float = 0.10
    missing_change_threshold: float = 1.0
    duplicate_change_threshold: float = 1.0
    numeric_tolerance: float = 1e-9`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="diff-schema">
          <h3 id="diff-schema" className="mb-3 text-lg font-semibold text-foreground">Schema-Level Deltas</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class ColumnRename:
    previous_name: str
    name: str


@dataclass(frozen=True, slots=True)
class ColumnTypeChange:
    column: str
    previous_dtype: str
    dtype: str
    previous_logical_type: str
    logical_type: str


@dataclass(frozen=True, slots=True)
class SchemaDiff:
    added_columns: tuple[str, ...] = ()
    removed_columns: tuple[str, ...] = ()
    renamed_columns: tuple[ColumnRename, ...] = ()
    type_changes: tuple[ColumnTypeChange, ...] = ()

    @property
    def changed(self) -> bool: ...`} language="python" showCopy={false} />
          <p className="mt-3 text-sm text-muted-foreground">
            <code>added_columns</code> and <code>removed_columns</code> are plain column names.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="diff-structure">
          <h3 id="diff-structure" className="mb-3 text-lg font-semibold text-foreground">StructureDiff</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class StructureDiff:
    previous_row_count: int
    row_count: int
    previous_column_count: int
    column_count: int

    @property
    def rows_added(self) -> int: ...      # never negative

    @property
    def rows_removed(self) -> int: ...

    @property
    def columns_added(self) -> int: ...

    @property
    def columns_removed(self) -> int: ...`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="diff-quality">
          <h3 id="diff-quality" className="mb-3 text-lg font-semibold text-foreground">Quality Deltas</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class MissingValueDiff:
    column: str
    previous_missing_count: int
    missing_count: int
    previous_missing_percentage: float
    missing_percentage: float

    @property
    def delta_count(self) -> int: ...
    @property
    def delta_percentage(self) -> float: ...
    # status: "new" | "resolved" | "regressed" | "improved" | "unchanged"
    @property
    def status(self) -> str: ...


@dataclass(frozen=True, slots=True)
class DuplicateDiff:
    previous_duplicate_count: int
    duplicate_count: int
    previous_duplicate_percentage: float
    duplicate_percentage: float

    @property
    def delta_percentage(self) -> float: ...
    # status: "regressed" | "improved" | "unchanged"
    @property
    def status(self) -> str: ...


@dataclass(frozen=True, slots=True)
class ConstantColumnDiff:
    newly_constant: tuple[str, ...] = ()
    no_longer_constant: tuple[str, ...] = ()

    @property
    def changed(self) -> bool: ...`} language="python" showCopy={false} />
          <p className="mt-3 text-sm text-muted-foreground">
            <code>MissingValueDiff.status</code> reports <code>"new"</code> when missingness was introduced, <code>"resolved"</code> when it disappeared, <code>"regressed"</code>/<code>"improved"</code> when it increased/decreased, and <code>"unchanged"</code> otherwise.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="diff-numeric">
          <h3 id="diff-numeric" className="mb-3 text-lg font-semibold text-foreground">Numeric Deltas</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class CardinalityDiff:
    column: str
    previous_cardinality: int
    cardinality: int

    @property
    def delta(self) -> int: ...


@dataclass(frozen=True, slots=True)
class StatisticDiff:
    column: str
    statistic: str   # "mean" | "median" | "std_dev" | "minimum" | "maximum"
    previous: float | None
    current: float | None
    delta: float | None
    relative_delta: float | None


@dataclass(frozen=True, slots=True)
class DistributionDiff:
    column: str
    previous_mean: float | None
    mean: float | None
    mean_relative_shift: float | None
    significant: bool`} language="python" showCopy={false} />
          <p className="mt-3 text-sm text-muted-foreground">
            Only statistics that actually changed are emitted, and only distribution shifts that exceed the configured threshold are flagged.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="diff-leakage">
          <h3 id="diff-leakage" className="mb-3 text-lg font-semibold text-foreground">Leakage Deltas</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class LeakageColumnDiff:
    column: str
    previous_severity: str | None
    severity: str | None
    status: str   # "new" | "removed" | "escalated" | "de_escalated" | "unchanged"

    @property
    def changed(self) -> bool: ...


@dataclass(frozen=True, slots=True)
class LeakageDiff:
    columns: tuple[LeakageColumnDiff, ...] = ()

    @property
    def new_findings(self) -> tuple[LeakageColumnDiff, ...]: ...
    @property
    def removed_findings(self) -> tuple[LeakageColumnDiff, ...]: ...
    @property
    def escalated(self) -> tuple[LeakageColumnDiff, ...]: ...
    @property
    def de_escalated(self) -> tuple[LeakageColumnDiff, ...]: ...
    @property
    def changed(self) -> bool: ...`} language="python" showCopy={false} />
          <p className="mt-3 text-sm text-muted-foreground">
            The leakage comparison is only produced when a target column is provided to <code>fs.diff()</code>.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="diff-summary">
          <h3 id="diff-summary" className="mb-3 text-lg font-semibold text-foreground">DatasetDiffSummary</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class DatasetDiffSummary:
    rows_added: int
    rows_removed: int
    columns_added: int
    columns_removed: int
    columns_renamed: int
    type_changes: int
    schema_changed: bool
    missing_values_increased: int
    missing_values_decreased: int
    duplicate_rows_increased: bool
    duplicate_rows_decreased: bool
    newly_constant_columns: int
    no_longer_constant_columns: int
    leakage_new: int
    leakage_removed: int
    leakage_escalated: int
    leakage_de_escalated: int
    overall_health: str   # "regressed" | "improved" | "unchanged"
    recommendation: str`} language="python" showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="diff-example-model">
          <h3 id="diff-example-model" className="mb-3 text-lg font-semibold text-foreground">Example</h3>
          <CodeBlock code={`import featuresmith as fs

result = fs.diff("v1.csv", "v2.csv", target_column="churn")

print(result.overall_summary)
print(f"Health: {result.summary.overall_health}")
for diff in result.missing_values:
    print(f"  {diff.column}: {diff.status} ({diff.delta_percentage:+.2f}pp)")`} language="python" showCopy />
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
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--quiet</td>
                  <td className="px-4 py-3 text-sm">Suppress all standard console report output.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--verbose</td>
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
          Featuresmith v0.2.0 supports programmatic rule configurations in the Python SDK and command-line flags in the CLI. File-based configuration is not yet active.
        </p>

        <div className="mb-6 rounded-lg border border-primary/20 bg-primary/5 p-4 text-sm text-muted-foreground flex gap-3">
          <div className="mt-0.5 inline-flex h-6 w-6 items-center justify-center rounded bg-primary/10 text-primary">
            <Info className="h-4 w-4" aria-hidden />
          </div>
          <div>
            <p className="font-semibold text-foreground mb-1 text-xs">Roadmap Notice: File-Based Config (.featuresmith.yml)</p>
            <p className="text-xs">
              Layered file-based configuration (via a <code>.featuresmith.yml</code> file at the project root) is a planned enhancement scheduled for Phase 3+. In the current release, configure rules directly in code or use CLI flags.
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
          Featuresmith is fully extensible. You can add your own deterministic rules by extending the <code>BaseRule</code> interface and registering them with the Rule Engine.
        </p>

        <section className="mb-8" aria-labelledby="rule-abstract">
          <h3 id="rule-abstract" className="mb-3 text-lg font-semibold text-foreground">The BaseRule Interface</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            All rules must extend <code>BaseRule</code> and implement the following properties and method:
          </p>
          <ul className="list-disc pl-5 space-y-2 text-sm text-muted-foreground" role="list">
            <li><code>id</code>: A unique dotted identifier (e.g., <code>statistical.zero_variance</code>).</li>
            <li><code>name</code>: A short human-readable rule title.</li>
            <li><code>description</code>: What the rule flags.</li>
            <li><code>category</code>: The group category (<code>quality</code>, <code>statistical</code>, or <code>leakage</code>).</li>
            <li><code>severity</code>: The default finding severity as a string (<code>"info"</code>, <code>"warning"</code>, or <code>"critical"</code>).</li>
            <li><code>enabled_by_default</code>: Whether the rule runs by default in the engine.</li>
            <li><code>evaluate(profile: ProfileResult) -&gt; list[RuleFinding]</code>: The core audit logic.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="rule-example">
          <h3 id="rule-example" className="mb-3 text-lg font-semibold text-foreground">Custom Rule Implementation</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Here is a complete rule that flags numeric columns with zero standard deviation (constant-value columns), using the real <code>BaseRule</code> API and the <code>NumericProfile</code> output of the profiling engine:
          </p>
          <CodeBlock code={`from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.rules.base import BaseRule


class ZeroVarianceRule(BaseRule):
    """Custom rule to detect numeric columns with zero variance."""

    @property
    def id(self) -> str:
        return "statistical.zero_variance"

    @property
    def name(self) -> str:
        return "Zero Variance Columns"

    @property
    def description(self) -> str:
        return "Flags numeric columns whose standard deviation is zero."

    @property
    def category(self) -> str:
        return "statistical"

    @property
    def severity(self) -> str:
        return "warning"

    @property
    def enabled_by_default(self) -> bool:
        return True

    def evaluate(self, profile: ProfileResult) -> list[RuleFinding]:
        findings: list[RuleFinding] = []
        for col_name, num_prof in profile.numeric_profiles.items():
            if num_prof.std_dev == 0.0:
                findings.append(
                    RuleFinding(
                        rule_id=self.id,
                        rule_name=self.name,
                        category=self.category,
                        severity=self.severity,
                        column_name=col_name,
                        title=f"Zero variance in column '{col_name}'",
                        description=(
                            f"Column '{col_name}' has a standard deviation "
                            f"of 0.0 (no variance)."
                        ),
                        evidence={
                            "std_dev": num_prof.std_dev,
                            "unique_count": num_prof.unique_count,
                        },
                        confidence=1.0,
                    )
                )
        return findings`} language="python" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="rule-evaluation">
          <h3 id="rule-evaluation" className="mb-3 text-lg font-semibold text-foreground">Evaluating Custom Rules</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            You can run the rule directly against a computed profile:
          </p>
          <CodeBlock code={`import featuresmith as fs

dataset = fs.load("data.csv")
profile = fs.profile(dataset)

rule = ZeroVarianceRule()
findings = rule.evaluate(profile)

for finding in findings:
    print(f"[{finding.severity}] {finding.title} in {finding.column_name}")`} language="python" showCopy />
          <p className="mt-3 text-sm text-muted-foreground">
            To run your custom rule inside the Rule Engine (for example alongside the built-ins through <code>fs.analyze()</code>), register it in a <code>RuleRegistry</code> and pass the registry to a <code>RuleEngine</code>:
          </p>
          <CodeBlock code={`from featuresmith.rules.engine import RuleEngine
from featuresmith.rules.registry import RuleRegistry, default_registry

# Start from the built-in rules and add your custom rule
registry = RuleRegistry([*default_registry().list_rules(), ZeroVarianceRule()])
engine = RuleEngine(registry=registry)

result = engine.run(
    profile,
    target_column="churn",
    enabled_rules=["statistical.zero_variance"],
)

print(f"Executed {len(result.executed_rules)} rule(s): {result.executed_rules}")
print(f"Failed: {result.failed_rules}")`} language="python" showCopy />
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
            In v0.2.0, file-based configuration via a local <code>.featuresmith.yml</code> file is not yet available (it is a planned enhancement for a future release). Customize the strictness of your CI gate by passing the <code>--severity</code> flag to the CLI.
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

        <section className="mb-8" aria-labelledby="rel-v020">
          <h3 id="rel-v020" className="mb-3 text-lg font-semibold text-foreground">Featuresmith v0.2.0</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Featuresmith v0.2.0 introduces the Review Engine, Dataset Diff comparison framework, ML Readiness Scorecard, and Intelligent Leakage Detection.
          </p>
          <h4 className="mt-4 mb-2 text-sm font-semibold text-foreground">Highlights:</h4>
          <ul className="list-disc pl-5 mb-4 space-y-1 text-sm text-muted-foreground">
            <li><strong>Review Engine</strong>: Orchestrates multiple parallel dataset reviewers in a 5-stage pipeline, outputting structured reports.</li>
            <li><strong>ML Readiness Score</strong>: Calculates a deterministic 0–100 score across 8 dimensions (Missing Values, Duplicates, Leakage, etc.) with actionable feedback.</li>
            <li><strong>Dataset Diff Engine</strong>: Compares two snapshot profiles to identify schema changes, distribution shifts, and quality regressions.</li>
            <li><strong>Intelligent Leakage Detection</strong>: Features 6 pattern-matching detectors to catch target leakage, duplicate targets, and future information leaks.</li>
            <li><strong>CLI Expansion</strong>: Introduces <code>featuresmith review</code> and <code>featuresmith diff</code> subcommands for terminal validation and CI/CD gating.</li>
          </ul>
        </section>

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
            The following packages are officially published on PyPI for <code>v0.2.0</code>:
          </p>
          <ul className="list-disc pl-5 mb-4 space-y-1 text-sm text-muted-foreground">
            <li><code>featuresmith-core</code>: Core engine library.</li>
            <li><code>featuresmith-cli</code>: CLI thin wrapper client.</li>
          </ul>
          <p className="text-sm text-muted-foreground">
            Note: <code>featuresmith-dashboard</code> is deferred to a future roadmap phase (Phase 3) and is not published in <code>v0.2.0</code>.
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
            <strong>No.</strong> Featuresmith v0.2.0 does not contain active LLM integrations or run cloud requests. In future AI phases (Phase 6+), provider integration is strictly opt-in and configured entirely via API keys. Furthermore, the AI layer only receives computed, aggregated statistical summaries (never raw data table rows), ensuring high privacy constraints.
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
            Yes! Custom connectors can be registered in <code>featuresmith.connectors.registry</code> and custom rules can be registered in the rule engine directly. Dynamic plugin autoloading via packaging entry points is scheduled for Phase 3.
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
  },
  "sdk/review": {
    title: "fs.review()",
    subtitle: "SDK Reference: run a complete engineering review",
    category: "Python SDK",
    seoTitle: "fs.review() API Reference",
    seoDescription: "API documentation and parameter reference for featuresmith.review().",
    render: () => (
      <>
        <CodeBlock code={`def review(
    source: object,
    *,
    previous: object | None = None,
    target_column: str | None = None,
    enabled_reviewers: Sequence[str] | None = None,
    enabled_categories: Sequence[ReviewCategory] | None = None,
    reviewer_config: Mapping[str, Mapping[str, Any]] | None = None,
    max_correlation_columns: int = 100,
    max_frequency_table_size: int = 1000,
) -> ReviewResult:`} language="python" showCopy={false} />

        <section className="mb-8 mt-6" aria-labelledby="review-overview">
          <h3 id="review-overview" className="mb-3 text-lg font-semibold text-foreground">Overview</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Performs a comprehensive engineering review of a dataset. It orchestrates a multi-stage pipeline: resolving inputs, constructing context, executing registered built-in reviewers in isolation, and computing the deterministic ML Readiness Score. The review reuses computed rule findings and profiles under the hood so no raw data is re-read or re-profiled during reviewer dispatch.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="review-when-use">
          <h3 id="review-when-use" className="mb-3 text-lg font-semibold text-foreground">When to Use It</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Use in Python scripts, data ingestion pipelines, or notebooks to evaluate a dataset's readiness for ML modeling in a single call. It consolidates schema checks, data quality audits, and target leakage diagnostics into a single structured result.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="review-params">
          <h3 id="review-params" className="mb-3 text-lg font-semibold text-foreground">Parameters</h3>
          <ul className="space-y-3 text-sm text-muted-foreground" role="list">
            <li><strong>source</strong>: <code>Dataset</code> | <code>str</code> | <code>DataFrame</code>. The input dataset path (CSV, Parquet, Excel) or in-memory DataFrame (pandas, Polars).</li>
            <li><strong>previous</strong>: <code>object | None</code> (default None). Prior snapshot for diff-aware reviews. <em>Note: Providing a value raises a <code>NotImplementedError</code>; use the standalone <code>fs.diff()</code> instead.</em></li>
            <li><strong>target_column</strong>: <code>str | None</code> (default None). Name of the target column. Highly recommended to enable target leakage checks.</li>
            <li><strong>enabled_reviewers</strong>: <code>Sequence[str] | None</code> (default None). Optional list of specific reviewer IDs to execute.</li>
            <li><strong>enabled_categories</strong>: <code>Sequence[ReviewCategory] | None</code> (default None). Optional list of reviewer categories to execute (schema, quality, leakage, diff, feature_quality, custom).</li>
            <li><strong>reviewer_config</strong>: <code>Mapping[str, Mapping[str, Any]] | None</code> (default None). Parameter overrides for specific reviewers (e.g. customized thresholds).</li>
            <li><strong>max_correlation_columns</strong>: <code>int</code> (default 100). Cap limit for correlation matrix computation during profiling.</li>
            <li><strong>max_frequency_table_size</strong>: <code>int</code> (default 1000). Frequency table storage cap.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="review-returns">
          <h3 id="review-returns" className="mb-3 text-lg font-semibold text-foreground">Return Value</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Returns a frozen <code>ReviewResult</code> dataclass containing:
          </p>
          <ul className="list-disc pl-5 space-y-1 text-sm text-muted-foreground">
            <li><code>engine_version</code>: <code>str</code> representing the Review Engine result schema version (currently <code>"0.2.0"</code>).</li>
            <li><code>dataset_summary</code>: <code>DatasetSummary</code> with row and column count descriptors.</li>
            <li><code>generated_at</code>: UTC timestamp.</li>
            <li><code>sections</code>: Sorted sequence of <code>ReviewSection</code> objects representing the active reviewers' sections (sorted from critical to passed).</li>
            <li><code>overall_summary</code>: Concise plain-text roll-up.</li>
            <li><code>score</code>: An optional <code>MLReadinessScore</code> containing overall rating and per-dimension breakdown.</li>
            <li><code>diff</code>: Reserved for future diff-aware reviews (currently always <code>None</code>).</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="review-example">
          <h3 id="review-example" className="mb-3 text-lg font-semibold text-foreground">SDK Example</h3>
          <CodeBlock code={`import featuresmith as fs

result = fs.review(
    "train.csv",
    target_column="churn",
    reviewer_config={
        "review.quality.missingness": {"threshold": 25.0},
        "review.quality.cardinality": {"threshold": 0.40}
    }
)

# Output summary and score
print(result.overall_summary)
if result.score:
    print(f"ML Readiness: {result.score.overall}/100")
    for dim in result.score.dimensions:
        print(f"  {dim.label}: {dim.score}/100")`} language="python" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="review-render">
          <h3 id="review-render" className="mb-3 text-lg font-semibold text-foreground">Rendering Review Output</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            The top-level <code>featuresmith</code> package re-exports <code>fs.render()</code> to generate formatted text reports:
          </p>
          <CodeBlock code={`import featuresmith as fs

result = fs.review("train.csv", target_column="churn")
report_text = fs.render(result, target="console")
print(report_text)`} language="python" showCopy />
          <p className="mt-3 text-sm text-muted-foreground">
            <code>fs.render(result: ReviewResult, target: str = "console") -&gt; str</code> formats the review sections, severity badges, and score scorecard into plain text suitable for terminal output or logging.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="review-output-ex">
          <h3 id="review-output-ex" className="mb-3 text-lg font-semibold text-foreground">Output Example</h3>
          <CodeBlock code={`# result.overall_summary
'8 of 8 sections passed with 0 finding(s) identified across the review.'

# result.score.overall
100.0`} showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="review-workflows">
          <h3 id="review-workflows" className="mb-3 text-lg font-semibold text-foreground">Common Workflows</h3>
          <ul className="list-disc pl-5 space-y-2 text-sm text-muted-foreground">
            <li>
              <strong>Continuous Integration Gates</strong>: Validate loaded files in pipeline tests and inspect findings programmatically to block merges when critical errors are uncovered.
            </li>
            <li>
              <strong>Dataset Triage</strong>: Run a quick review over multiple candidate datasets to determine which has the highest data quality and lowest target leakage before selecting a source.
            </li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="review-limitations">
          <h3 id="review-limitations" className="mb-3 text-lg font-semibold text-foreground">Notes and Limitations</h3>
          <ul className="list-disc pl-5 space-y-2 text-sm text-muted-foreground border-l-2 border-amber-500 bg-amber-500/5 p-4 rounded-r-lg">
            <li><strong>No Diff-Aware Review</strong>: Passing a prior snapshot to <code>previous</code> raises a <code>NotImplementedError</code>. Comparing snapshots requires the standalone <code>fs.diff()</code> engine.</li>
            <li><strong>Deferred Features</strong>: Centralized recommendation generation is not implemented. Reviewers output findings only. Observability trend logs and HTML static reports are planned for future releases.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="review-cross-links">
          <h3 id="review-cross-links" className="mb-3 text-lg font-semibold text-foreground">Related Documentation</h3>
          <p className="text-sm text-muted-foreground">
            See the CLI counterpart <a href="/docs/cli/review" className="text-primary hover:underline">featuresmith review</a> and the ML score reference <a href="/docs/sdk/score" className="text-primary hover:underline">fs.score()</a>.
          </p>
        </section>
      </>
    )
  },
  "sdk/diff": {
    title: "fs.diff()",
    subtitle: "SDK Reference: compare two dataset snapshots",
    category: "Python SDK",
    seoTitle: "fs.diff() API Reference",
    seoDescription: "API documentation and parameter reference for featuresmith.diff().",
    render: () => (
      <>
        <CodeBlock code={`def diff(
    old: object,
    new: object,
    *,
    target_column: str | None = None,
    max_correlation_columns: int = 100,
    max_frequency_table_size: int = 1000,
) -> DatasetDiffResult:`} language="python" showCopy={false} />

        <section className="mb-8 mt-6" aria-labelledby="diff-overview">
          <h3 id="diff-overview" className="mb-3 text-lg font-semibold text-foreground">Overview</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Compares two versions (older vs. newer) of a dataset. It profiles both versions and computes statistical deltas, schema additions/deletions, missingness drifts, cardinality deltas, constant column status changes, basic distribution shifts, and target leakage status changes (when a target column is specified).
          </p>
        </section>

        <section className="mb-8" aria-labelledby="diff-when-use">
          <h3 id="diff-when-use" className="mb-3 text-lg font-semibold text-foreground">When to Use It</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Use before retraining a machine learning model. If a new version of the training dataset contains removed columns or severe missing value regressions, this function catches them before a model training run is initiated.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="diff-params">
          <h3 id="diff-params" className="mb-3 text-lg font-semibold text-foreground">Parameters</h3>
          <ul className="space-y-3 text-sm text-muted-foreground" role="list">
            <li><strong>old</strong>: <code>Dataset</code> | <code>str</code> | <code>DataFrame</code>. The older snapshot path or object.</li>
            <li><strong>new</strong>: <code>Dataset</code> | <code>str</code> | <code>DataFrame</code>. The newer snapshot path or object.</li>
            <li><strong>target_column</strong>: <code>str | None</code> (default None). The target column for target-aware leakage comparisons.</li>
            <li><strong>max_correlation_columns</strong>: <code>int</code> (default 100). Cap limit for correlation computations during snapshot profiling.</li>
            <li><strong>max_frequency_table_size</strong>: <code>int</code> (default 1000). Frequency table size limit.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="diff-returns">
          <h3 id="diff-returns" className="mb-3 text-lg font-semibold text-foreground">Return Value</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Returns a frozen <code>DatasetDiffResult</code> dataclass containing:
          </p>
          <ul className="list-disc pl-5 space-y-1 text-sm text-muted-foreground">
            <li><code>version</code>: <code>str</code> (currently <code>"0.2.0"</code>).</li>
            <li><code>schema</code>: <code>SchemaDiff</code> containing columns added, removed, renamed, and data type changes.</li>
            <li><code>structure</code>: <code>StructureDiff</code> showing row/column deltas.</li>
            <li><code>missing_values</code>: Per-column missingness deltas (<code>MissingValueDiff</code>), each classified as new, resolved, regressed, improved, or unchanged.</li>
            <li><code>duplicates</code>: Duplicate rows count and percentage shifts.</li>
            <li><code>constant_columns</code>: Newly constant and no longer constant columns.</li>
            <li><code>cardinality</code>: Per-column cardinality changes.</li>
            <li><code>statistics</code>: Deltas for basic numeric metrics (mean, median, std_dev, minimum, maximum).</li>
            <li><code>distributions</code>: Significant mean shifts.</li>
            <li><code>leakage</code>: Target leakage deltas (new, removed, escalated, or de-escalated patterns).</li>
            <li><code>summary</code>: <code>DatasetDiffSummary</code> showing counts and overall health (<code>regressed</code>, <code>improved</code>, or <code>unchanged</code>).</li>
            <li><code>overall_summary</code>: One-line templated summary.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="diff-example">
          <h3 id="diff-example" className="mb-3 text-lg font-semibold text-foreground">SDK Example</h3>
          <CodeBlock code={`import featuresmith as fs

result = fs.diff("v1.csv", "v2.csv", target_column="churn")

print(result.overall_summary)
print(f"Status: {result.summary.overall_health}")
print(f"Recommendation: {result.summary.recommendation}")`} language="python" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="diff-output-ex">
          <h3 id="diff-output-ex" className="mb-3 text-lg font-semibold text-foreground">Output Example</h3>
          <CodeBlock code={`# result.overall_summary
'Rows 0 removed, 100 added; columns 0 removed, 1 added; overall health: improved.'

# result.summary.recommendation
'Dataset improved: missingness reduced in 2 column(s). No blocking regressions detected.'`} showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="diff-workflows">
          <h3 id="diff-workflows" className="mb-3 text-lg font-semibold text-foreground">Common Workflows</h3>
          <ul className="list-disc pl-5 space-y-2 text-sm text-muted-foreground">
            <li>
              <strong>Retraining Pipeline Gates</strong>: Programmatically diff input versions before initiating a training loop, rejecting the job if the overall health returns <code>"regressed"</code>.
            </li>
            <li>
              <strong>Schema Drift Detection</strong>: Verify that no data types were silently modified or key features dropped during upstream extraction updates.
            </li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="diff-helpers">
          <h3 id="diff-helpers" className="mb-3 text-lg font-semibold text-foreground">Diff Helper Functions</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            The <code>featuresmith</code> package re-exports two public helper functions for working with <code>DatasetDiffResult</code>:
          </p>
          <CodeBlock code={`import featuresmith as fs

# 1. Extract RuleFinding objects from a DatasetDiffResult
findings = fs.diff_findings(result)

# 2. Render console text report for a DatasetDiffResult
report_text = fs.render_diff(result, target="console")`} language="python" showCopy />
          <ul className="list-disc pl-5 mt-3 space-y-1 text-sm text-muted-foreground">
            <li><code>fs.diff_findings(result: DatasetDiffResult) -&gt; list[RuleFinding]</code>: Converts diff status changes (such as dropped columns, missingness regressions, and leakage status changes) into standard <code>RuleFinding</code> objects for severity-based filtering and CI gating.</li>
            <li><code>fs.render_diff(result: DatasetDiffResult, target: str = "console") -&gt; str</code>: Renders a formatted string report for terminal display or text export.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="diff-limitations">
          <h3 id="diff-limitations" className="mb-3 text-lg font-semibold text-foreground">Notes and Limitations</h3>
          <ul className="list-disc pl-5 space-y-2 text-sm text-muted-foreground border-l-2 border-amber-500 bg-amber-500/5 p-4 rounded-r-lg">
            <li><strong>Standalone Operation</strong>: Dataset Diff is implemented as a standalone engine. It is not integrated as a reviewer inside the Review Engine pipeline. Calling <code>fs.review(previous=...)</code> raises a <code>NotImplementedError</code>.</li>
            <li><strong>Advisory Recommendations</strong>: Findings and overall health recommendations are purely advisory and do not automatically mutate data or abort processes unless coded into your caller logic.</li>
            <li><strong>Diff Findings Accessor</strong>: Use <code>fs.diff_findings(result)</code> to derive standard <code>RuleFinding</code> objects from a diff result. The CLI's diff command consumes these findings for severity-based exit-code gating.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="diff-cross-links">
          <h3 id="diff-cross-links" className="mb-3 text-lg font-semibold text-foreground">Related Documentation</h3>
          <p className="text-sm text-muted-foreground">
            See the CLI counterpart <a href="/docs/cli/diff" className="text-primary hover:underline">featuresmith diff</a> and the review reference <a href="/docs/sdk/review" className="text-primary hover:underline">fs.review()</a>.
          </p>
        </section>
      </>
    )
  },
  "sdk/score": {
    title: "fs.score()",
    subtitle: "SDK Reference: extract or calculate ML Readiness Score",
    category: "Python SDK",
    seoTitle: "fs.score() API Reference",
    seoDescription: "API documentation and parameter reference for featuresmith.score().",
    render: () => (
      <>
        <CodeBlock code={`def score(result: ReviewResult) -> MLReadinessScore | None:`} language="python" showCopy={false} />

        <section className="mb-8 mt-6" aria-labelledby="score-overview">
          <h3 id="score-overview" className="mb-3 text-lg font-semibold text-foreground">Overview</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Extracts or computes the ML Readiness Score of a dataset. When the provided <code>ReviewResult</code> already carries a score, it is returned directly; otherwise, the score is calculated deterministically from the findings in the result's review sections. This function is a lightweight read-only accessor and never re-runs the data profiling or rule execution stages.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="score-when-use">
          <h3 id="score-when-use" className="mb-3 text-lg font-semibold text-foreground">When to Use It</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Use when you need to inspect the quality breakdown of a dataset across named dimensions after a review has run. It allows you to check specific dimension ratings, review why points were deducted, and gather suggestions on how to improve the overall score.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="score-params">
          <h3 id="score-params" className="mb-3 text-lg font-semibold text-foreground">Parameters</h3>
          <ul className="space-y-3 text-sm text-muted-foreground" role="list">
            <li><strong>result</strong>: <code>ReviewResult</code>. An existing result object produced by <code>fs.review()</code>.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="score-returns">
          <h3 id="score-returns" className="mb-3 text-lg font-semibold text-foreground">Return Value</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            Returns an <code>MLReadinessScore</code> dataclass (or <code>None</code> if no dimensions are applicable) containing:
          </p>
          <ul className="list-disc pl-5 space-y-1 text-sm text-muted-foreground">
            <li><code>scoring_version</code>: <code>str</code> (currently <code>"0.2.0"</code>).</li>
            <li><code>overall</code>: <code>float</code> score scaled from 0.0 to 100.0, representing the weighted average of all applicable dimensions.</li>
            <li><code>dimensions</code>: Sequence of <code>DimensionScore</code> objects carrying metrics for Schema Health, Missing Values, Duplicate Records, Data Types, Constant Columns, High Cardinality, Dataset Structure, and Leakage Risk.</li>
          </ul>
          <p className="mt-3 text-sm text-muted-foreground">
            Each <code>DimensionScore</code> includes a <code>score</code>, <code>weight</code>, <code>rationale</code>, <code>contributing_findings</code>, and <code>suggested_actions</code>.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="score-example">
          <h3 id="score-example" className="mb-3 text-lg font-semibold text-foreground">SDK Example</h3>
          <CodeBlock code={`import featuresmith as fs

result = fs.review("data.csv", target_column="label")
score = fs.score(result)

if score:
    print(f"Overall Score: {score.overall}/100")
    for dim in score.dimensions:
        if dim.score < 100.0:
            print(f"[{dim.label}] Rationale: {dim.rationale}")
            print(f"  Actions to improve: {dim.suggested_actions}")`} language="python" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="score-math">
          <h3 id="score-math" className="mb-3 text-lg font-semibold text-foreground">Scoring Formula</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Each dimension starts at a perfect score of 100.0. Deductions are subtracted based on the severity of the findings in the corresponding section:
          </p>
          <ul className="list-disc pl-5 mt-2 space-y-1 text-sm text-muted-foreground">
            <li><strong>Critical Finding</strong>: -30.0 points</li>
            <li><strong>Warning Finding</strong>: -15.0 points</li>
            <li><strong>Info Finding</strong>: -5.0 points</li>
          </ul>
          <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
            The overall score is calculated as the weighted average:
          </p>
          <div className="my-4 bg-muted p-3 rounded font-mono text-xs text-center border border-border">
            overall = sum(dim.score * dim.weight) / sum(dim.weight)
          </div>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Inapplicable dimensions are omitted and their weights are renormalized automatically, ensuring that regression-only datasets are not unfairly penalized for missing classification-specific metrics.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="score-limitations">
          <h3 id="score-limitations" className="mb-3 text-lg font-semibold text-foreground">Notes and Limitations</h3>
          <ul className="list-disc pl-5 space-y-2 text-sm text-muted-foreground border-l-2 border-amber-500 bg-amber-500/5 p-4 rounded-r-lg">
            <li><strong>Read-Only Accessor</strong>: <code>fs.score()</code> does not trigger any profiling or rule-evaluation runs. It is completely derived from pre-existing findings.</li>
            <li><strong>Configuration Status</strong>: Configuration of custom weights in a <code>.featuresmith.yml</code> file is deferred. The score currently uses uniform default weights (1.0).</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="score-cross-links">
          <h3 id="score-cross-links" className="mb-3 text-lg font-semibold text-foreground">Related Documentation</h3>
          <p className="text-sm text-muted-foreground">
            See the review SDK reference <a href="/docs/sdk/review" className="text-primary hover:underline">fs.review()</a> and the CLI scorecard overview <a href="/docs/cli/score" className="text-primary hover:underline">featuresmith score</a>.
          </p>
        </section>
      </>
    )
  },
  "sdk/dataset": {
    title: "Dataset",
    subtitle: "SDK Reference: the normalized dataset model",
    category: "Python SDK",
    seoTitle: "Dataset Model",
    seoDescription: "Reference for the featuresmith Dataset model, including its nine dataclass fields, from_dataframe(), and preview().",
    render: () => (
      <>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          A normalized, immutable view of a loaded tabular dataset. <code>fs.load()</code> returns a
          <code> Dataset</code>, and it is also what <code>fs.profile()</code>, <code>fs.analyze()</code>,
          and <code>fs.review()</code> accept as their primary input. The class is a frozen,
          slotted dataclass so every instance is read-only and safely serializable.
        </p>
        <p className="mb-6 text-sm leading-relaxed text-muted-foreground">
          The <code>Dataset</code> type lives in <code>featuresmith.core.dataset</code>. It is not
          re-exported from the top-level <code>featuresmith</code> package, so import it explicitly:
        </p>
        <CodeBlock code={`from featuresmith.core.dataset import Dataset`} language="python" showCopy />

        <section className="mb-8" aria-labelledby="ds-fields">
          <h3 id="ds-fields" className="mb-3 text-lg font-semibold text-foreground">Dataclass Fields</h3>
          <CodeBlock code={`@dataclass(frozen=True, slots=True)
class Dataset:
    dataframe: Any                # pandas or Polars dataframe (memory is not copied)
    backend: str                  # "pandas" or "polars"
    schema: DatasetSchema         # columns: tuple[ColumnSchema(name, dtype), ...]
    metadata: Mapping[str, object]
    row_count: int                # default 0
    column_count: int             # default 0
    dtypes: Mapping[str, str]     # column name -> backend dtype string
    source: str | None            # original local file path, if any (default None)
    file_size: int | None         # source file size in bytes, if known (default None)`} language="python" showCopy={false} />
          <p className="mt-3 text-sm text-muted-foreground">
            In practice every field except <code>dataframe</code>, <code>backend</code>, and <code>schema</code> is
            computed for you during loading, so you normally construct a <code>Dataset</code> via
            <code> fs.load()</code> or <code>Dataset.from_dataframe()</code> rather than directly.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="ds-from-dataframe">
          <h3 id="ds-from-dataframe" className="mb-3 text-lg font-semibold text-foreground">from_dataframe()</h3>
          <CodeBlock code={`@classmethod
def from_dataframe(
    cls,
    dataframe: Any,
    *,
    backend: str,
    source: str | None = None,
    file_size: int | None = None,
    metadata: Mapping[str, object] | None = None,
) -> Dataset:`} language="python" showCopy={false} />
          <p className="mt-3 text-sm text-muted-foreground">
            Creates a normalized dataset from a pandas or Polars dataframe, inferring the schema and dtype
            mapping. Used internally by the connectors; the public way to obtain a <code>Dataset</code> is
            <code> fs.load()</code>.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="ds-preview">
          <h3 id="ds-preview" className="mb-3 text-lg font-semibold text-foreground">preview(rows=5)</h3>
          <CodeBlock code={`def preview(self, rows: int = 5) -> Any:`} language="python" showCopy={false} />
          <p className="mt-3 text-sm text-muted-foreground">
            Returns the first <code>rows</code> rows of the underlying dataframe (same backend as the source).
            Raises <code>ValueError</code> when <code>rows</code> is negative.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="ds-example">
          <h3 id="ds-example" className="mb-3 text-lg font-semibold text-foreground">Example</h3>
          <CodeBlock code={`import featuresmith as fs

dataset = fs.load("train.parquet")

print(dataset.row_count)        # number of rows
print(dataset.column_count)     # number of columns
print(dataset.backend)          # "pandas" or "polars"
print(dataset.source)           # original file path, if loaded from disk

# Inspect the normalized schema and preview rows
for column in dataset.schema.columns:
    print(column.name, column.dtype)

print(dataset.preview(5))       # first 5 rows as a dataframe`} language="python" showCopy />
        </section>
      </>
    )
  },
  "cli/review": {
    title: "featuresmith review",
    subtitle: "CLI command reference for comprehensive reviews",
    category: "CLI Reference",
    seoTitle: "CLI Review Command Reference",
    seoDescription: "Examine flags and options of the featuresmith review command.",
    render: () => (
      <>
        <CodeBlock code={`featuresmith review <source> [options]`} language="bash" showCopy={false} />
        <p className="mt-4 mb-6 text-sm leading-relaxed text-muted-foreground">
          Runs a dataset review and prints a structured, severity-sorted findings tree alongside the ML Readiness Score.
        </p>

        <section className="mb-8" aria-labelledby="review-flags">
          <h3 id="review-flags" className="mb-4 text-lg font-semibold text-foreground">Flags and Options</h3>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="min-w-full divide-y divide-border text-left text-sm">
              <tbody className="divide-y divide-border text-muted-foreground">
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--target TEXT</td>
                  <td className="px-4 py-3 text-sm">Name of the target column in the dataset to validate and enable leakage reviewers.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--previous PATH</td>
                  <td className="px-4 py-3 text-sm">Path to a prior snapshot for diff-aware reviews. <em>Note: Not yet available; triggers an error.</em></td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--format [table|json]</td>
                  <td className="px-4 py-3 text-sm">Output format to display (default: <code>table</code>).</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--output PATH</td>
                  <td className="px-4 py-3 text-sm">Path to save the plain report or JSON structure.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--fail-on [info|warning|critical]</td>
                  <td className="px-4 py-3 text-sm">Severity threshold for CI-gating exit codes (default: <code>critical</code>).</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--only TEXT</td>
                  <td className="px-4 py-3 text-sm">Comma-separated reviewer categories to run (schema, quality, leakage, diff, feature_quality, custom).</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--no-score</td>
                  <td className="px-4 py-3 text-sm">Omit the ML Readiness Score scorecard from the report.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--quiet</td>
                  <td className="px-4 py-3 text-sm">Suppress all standard console report output.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--verbose</td>
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

        <section className="mb-8" aria-labelledby="review-exit-codes">
          <h3 id="review-exit-codes" className="mb-3 text-lg font-semibold text-foreground">Exit Codes</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            The command returns standardized exit codes matching the analyze conventions:
          </p>
          <ul className="list-disc pl-5 space-y-1 text-sm text-muted-foreground">
            <li><code>0</code>: Clean — no findings meet or exceed the severity threshold specified in <code>--fail-on</code>.</li>
            <li><code>1</code>: Findings meeting or exceeding the threshold were detected (gating CI/CD pipelines).</li>
            <li><code>2</code>: Invalid usage, bad configuration, unknown target column, or unsupported format.</li>
            <li><code>3</code>: File not found or failed to parse.</li>
            <li><code>4</code>: Unexpected internal error.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="review-cli-example">
          <h3 id="review-cli-example" className="mb-3 text-lg font-semibold text-foreground">CLI Syntax Examples</h3>
          <CodeBlock code={`# 1. Standard review with leakage target
featuresmith review train.csv --target churn

# 2. Category filtering with CI gating
featuresmith review train.csv --only schema,leakage --fail-on warning --no-score

# 3. JSON format save
featuresmith review train.csv --format json --output review_report.json`} language="bash" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="review-cli-limitations">
          <h3 id="review-cli-limitations" className="mb-3 text-lg font-semibold text-foreground">Notes and Limitations</h3>
          <ul className="list-disc pl-5 space-y-2 text-sm text-muted-foreground border-l-2 border-amber-500 bg-amber-500/5 p-4 rounded-r-lg">
            <li><strong>--previous Unavailable</strong>: The review CLI does not support diff-aware audits yet. Providing the flag displays an error message and exits with code 2. Use <code>featuresmith diff</code> instead.</li>
            <li><strong>Target column validation</strong>: When <code>--target</code> is specified, the CLI actively checks for column presence in the schema and fails early with code 2 if not found.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="review-cli-cross">
          <h3 id="review-cli-cross" className="mb-3 text-lg font-semibold text-foreground">Related Documentation</h3>
          <p className="text-sm text-muted-foreground">
            See the SDK equivalent <a href="/docs/sdk/review" className="text-primary hover:underline">fs.review()</a> and the diff CLI reference <a href="/docs/cli/diff" className="text-primary hover:underline">featuresmith diff</a>.
          </p>
        </section>
      </>
    )
  },
  "cli/diff": {
    title: "featuresmith diff",
    subtitle: "CLI command reference for snapshot diffs",
    category: "CLI Reference",
    seoTitle: "CLI Diff Command Reference",
    seoDescription: "Examine flags and options of the featuresmith diff command.",
    render: () => (
      <>
        <CodeBlock code={`featuresmith diff <old> <new> [options]`} language="bash" showCopy={false} />
        <p className="mt-4 mb-6 text-sm leading-relaxed text-muted-foreground">
          Compares two dataset snapshots and outputs structural, schema, missingness, duplicate, cardinality, and distribution shifts.
        </p>

        <section className="mb-8" aria-labelledby="diff-flags">
          <h3 id="diff-flags" className="mb-4 text-lg font-semibold text-foreground">Flags and Options</h3>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="min-w-full divide-y divide-border text-left text-sm">
              <tbody className="divide-y divide-border text-muted-foreground">
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">&lt;old&gt;</td>
                  <td className="px-4 py-3 text-sm">Required argument: path to the older dataset version (CSV, Excel, Parquet).</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">&lt;new&gt;</td>
                  <td className="px-4 py-3 text-sm">Required argument: path to the newer dataset version.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--target TEXT</td>
                  <td className="px-4 py-3 text-sm">Name of the target column in both datasets to compare target leakage changes.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--format [table|json]</td>
                  <td className="px-4 py-3 text-sm">Output format to display (default: <code>table</code>).</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--output PATH</td>
                  <td className="px-4 py-3 text-sm">Path to save the plain report or JSON output.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--fail-on [info|warning|critical]</td>
                  <td className="px-4 py-3 text-sm">Severity threshold for CI-gating exit codes (default: <code>critical</code>).</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--quiet</td>
                  <td className="px-4 py-3 text-sm">Suppress all standard console report output.</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-mono font-medium text-foreground text-xs">--verbose</td>
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

        <section className="mb-8" aria-labelledby="diff-exit-codes">
          <h3 id="diff-exit-codes" className="mb-3 text-lg font-semibold text-foreground">Exit Codes</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            The command returns exit codes based on structural regressions and quality drops:
          </p>
          <ul className="list-disc pl-5 space-y-1 text-sm text-muted-foreground">
            <li><code>0</code>: Clean — no regression or quality drop meets or exceeds the severity threshold specified in <code>--fail-on</code>.</li>
            <li><code>1</code>: Regressions (e.g. dropped columns, dtype mismatches, increased missingness, or target leakage escalation) meeting or exceeding the threshold were detected.</li>
            <li><code>2</code>: Invalid usage, bad configuration, or target column missing.</li>
            <li><code>3</code>: Source files missing or failed to parse.</li>
            <li><code>4</code>: Internal error.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="diff-cli-example">
          <h3 id="diff-cli-example" className="mb-3 text-lg font-semibold text-foreground">CLI Syntax Examples</h3>
          <CodeBlock code={`# Compare two dataset snapshots
featuresmith diff train_v1.csv train_v2.csv

# Diff target leakage status changes
featuresmith diff train_v1.csv train_v2.csv --target churn --fail-on warning

# Output JSON report
featuresmith diff train_v1.csv train_v2.csv --format json --output diff_report.json`} language="bash" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="diff-cli-limitations">
          <h3 id="diff-cli-limitations" className="mb-3 text-lg font-semibold text-foreground">Notes and Limitations</h3>
          <ul className="list-disc pl-5 space-y-2 text-sm text-muted-foreground border-l-2 border-amber-500 bg-amber-500/5 p-4 rounded-r-lg">
            <li><strong>Target validation</strong>: The target column is validated against the schema of both snapshot versions. Missing columns in either version result in an exit code 2.</li>
            <li><strong>Deterministic summary</strong>: Deliberately uses the deterministic statistical profiling engine to generate snapshots, avoiding raw-data re-reads during comparisons.</li>
          </ul>
        </section>

        <section className="mb-8" aria-labelledby="diff-cli-cross">
          <h3 id="diff-cli-cross" className="mb-3 text-lg font-semibold text-foreground">Related Documentation</h3>
          <p className="text-sm text-muted-foreground">
            See the SDK equivalent <a href="/docs/sdk/diff" className="text-primary hover:underline">fs.diff()</a> and the review CLI reference <a href="/docs/cli/review" className="text-primary hover:underline">featuresmith review</a>.
          </p>
        </section>
      </>
    )
  },
  "cli/score": {
    title: "featuresmith score",
    subtitle: "Understanding ML Readiness Score CLI integration",
    category: "CLI Reference",
    seoTitle: "CLI Score Reference",
    seoDescription: "Learn how the ML Readiness Score is rendered in the CLI report.",
    render: () => (
      <>
        <section className="mb-8" aria-labelledby="score-cli-overview">
          <h3 id="score-cli-overview" className="mb-3 text-lg font-semibold text-foreground">Overview</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            There is no standalone <code>featuresmith score</code> CLI subcommand. Instead, the versioned, explainable ML Readiness Score is computed automatically and displayed inline as a section at the end of the standard <code>featuresmith review</code> report.
          </p>
        </section>

        <section className="mb-8" aria-labelledby="score-cli-use">
          <h3 id="score-cli-use" className="mb-3 text-lg font-semibold text-foreground">How it is Used</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            By default, running a review includes the scorecard output. To prevent calculating or rendering the score scorecard (useful for clean log outputs or minimal JSON size), call the review command with the <code>--no-score</code> flag.
          </p>
          <CodeBlock code={`featuresmith review train.csv --no-score`} language="bash" showCopy />
        </section>

        <section className="mb-8" aria-labelledby="score-cli-output">
          <h3 id="score-cli-output" className="mb-3 text-lg font-semibold text-foreground">Console Scorecard Example</h3>
          <p className="mb-3 text-sm text-muted-foreground">
            When computed, the CLI console renderer formats the score and displays contributing issues dynamically:
          </p>
          <CodeBlock code={`ML Readiness Score (scoring v0.2.0)
Overall: 98.1/100

  Schema Health: 100/100
  Missing Values: 85/100 (1 finding(s))
  Duplicate Records: 100/100
  Data Types: 100/100
  Constant Columns: 100/100
  High Cardinality: 100/100
  Dataset Structure: 100/100
  Leakage Risk: 100/100

Summary: Overall ML Readiness is 98.1/100 across 8 dimension(s); 7 fully healthy, 1 with findings lowering the score.

What would improve this score:
  - Address the flagged issue: High missing values in column 'age' (in column 'age').`} showCopy={false} />
        </section>

        <section className="mb-8" aria-labelledby="score-cli-json">
          <h3 id="score-cli-json" className="mb-3 text-lg font-semibold text-foreground">JSON Integration</h3>
          <p className="text-sm leading-relaxed text-muted-foreground">
            If the review is output with <code>--format json</code>, the score object is nested as the <code>score</code> field in the output payload. If <code>--no-score</code> is requested, the field yields <code>null</code> rather than <code>0</code>, keeping "not scored" distinct from "scored poorly".
          </p>
        </section>

        <section className="mb-8" aria-labelledby="score-cli-cross">
          <h3 id="score-cli-cross" className="mb-3 text-lg font-semibold text-foreground">Related Documentation</h3>
          <p className="text-sm text-muted-foreground">
            See the SDK equivalent <a href="/docs/sdk/score" className="text-primary hover:underline">fs.score()</a> and the review CLI reference <a href="/docs/cli/review" className="text-primary hover:underline">featuresmith review</a>.
          </p>
        </section>
      </>
    )
  }
}
