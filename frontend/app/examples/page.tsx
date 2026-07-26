import type { Metadata } from "next"
import Link from "next/link"
import { ChevronRight, ArrowRight, Code, Terminal, Settings } from "lucide-react"
import { Container } from "@/components/ui/container"
import { CodeBlock } from "@/components/ui/code-block"
import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"

export const metadata: Metadata = {
  title: "Examples | Featuresmith",
  description: "Explore real-world Python SDK pipelines, CI/CD integrations, and custom rules written for Featuresmith.",
}

const SDK_EXAMPLE_CODE = `import json
import featuresmith as fs

def run_featuresmith_pipeline(data_path: str, target: str):
    # 1. Load data safely into Dataset layer
    print(f"Loading data from {data_path}...")
    dataset = fs.load(data_path)

    # 2. Run data audit checks (load → profile → rules evaluation)
    print("Running rule audit...")
    result = fs.analyze(
        dataset,
        target_column=target,
        rule_config={
            "quality.missing_value_threshold": {"threshold": 10.0},
            "statistical.high_correlation": {"threshold": 0.85}
        }
    )

    # 3. Handle rules results
    print(f"Audit completed. Findings: {len(result.findings)}")
    for finding in result.findings:
        print(f"[{finding.severity.upper()}] Column: {finding.column_name}")
        print(f"  Issue  : {finding.title}")
        print(f"  Detail : {finding.description}")

    # 4. Serialize result to dictionary/JSON
    report_dict = result.to_dict()
    with open("report.json", "w") as f:
        json.dump(report_dict, f, indent=2, default=str)

if __name__ == "__main__":
    run_featuresmith_pipeline("customers.csv", target="churn")`

const CICD_EXAMPLE_CODE = `# .github/workflows/data-quality-gate.yml
name: Data Quality Gate

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *' # Run daily audits

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install featuresmith-core featuresmith-cli

      - name: Audit dataset quality
        run: |
          # Gate CI build: if critical rule violations exist, exit code 1 fails step
          featuresmith analyze data/incoming_leads.csv --target converted --severity critical --output audit_report.txt

      - name: Upload audit report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: data-audit-report
          path: audit_report.txt`

const CUSTOM_RULE_CODE = `from typing import Any
from featuresmith.rules.base import BaseRule
from featuresmith.core.rule_finding import RuleFinding, RuleSeverity
from featuresmith.core.profile_result import ProfileResult

class ZeroVarianceRule(BaseRule):
    """Custom rule to detect columns with zero variance (no statistical variance)."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__()
        # Allow passing config overrides
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
        
        # Access numerical columns only
        for col_name, col_profile in profile.column_profiles.items():
            numeric_stats = col_profile.numeric_stats
            if numeric_stats is not None:
                # If standard deviation is 0.0, the column has zero variance
                if numeric_stats.std == 0.0:
                    findings.append(
                        self.create_finding(
                            column_name=col_name,
                            title="Zero Variance Detected",
                            description=f"Column '{col_name}' has standard deviation of 0.0 (no variance).",
                            evidence={"std": 0.0}
                        )
                    )
        return findings`

export default function ExamplesPage() {
  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-background pt-20 pb-24">
        <Container size="md">
          {/* Breadcrumb */}
          <nav aria-label="Breadcrumb" className="mb-6 flex items-center gap-1 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-foreground">Home</Link>
            <ChevronRight className="h-3.5 w-3.5" aria-hidden />
            <span className="text-foreground">Examples</span>
          </nav>

          {/* Page header */}
          <header className="mb-12 border-b border-border pb-8">
            <h1 className="text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
              Examples
            </h1>
            <p className="mt-3 text-base leading-relaxed text-muted-foreground">
              Production-grade implementations demonstrating Featuresmith SDK pipelines,
              automated CI/CD quality gates, and custom rule design.
            </p>
          </header>

          {/* Python SDK Pipeline Example */}
          <section className="mb-14" aria-labelledby="sdk-pipeline">
            <div className="mb-4 flex items-center gap-2.5">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/8 text-primary ring-1 ring-primary/15">
                <Code className="h-4.5 w-4.5" aria-hidden />
              </div>
              <h2 id="sdk-pipeline" className="text-xl font-semibold text-foreground">Python SDK Pipeline</h2>
            </div>
            <p className="mb-4 text-sm leading-relaxed text-muted-foreground">
              This script illustrates loading a CSV dataset, executing deterministic audits targeting a leakage column, handling rule findings, and writing serialized reports to disk.
            </p>
            <CodeBlock code={SDK_EXAMPLE_CODE} language="python" filename="pipeline.py" showCopy />
          </section>

          {/* CI/CD Quality Gate Example */}
          <section className="mb-14" aria-labelledby="cicd-gate">
            <div className="mb-4 flex items-center gap-2.5">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/8 text-primary ring-1 ring-primary/15">
                <Terminal className="h-4.5 w-4.5" aria-hidden />
              </div>
              <h2 id="cicd-gate" className="text-xl font-semibold text-foreground">CI/CD Quality Gate</h2>
            </div>
            <p className="mb-4 text-sm leading-relaxed text-muted-foreground">
              Integrate the Featuresmith CLI into your GitHub Actions workflow. Exit code 1 gates the build on critical quality or leakage violations, and uploads the generated text reports.
            </p>
            <CodeBlock code={CICD_EXAMPLE_CODE} language="yaml" filename="data-quality-gate.yml" showCopy />
          </section>

          {/* Custom Rule Design Example */}
          <section className="mb-14" aria-labelledby="custom-rule">
            <div className="mb-4 flex items-center gap-2.5">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/8 text-primary ring-1 ring-primary/15">
                <Settings className="h-4.5 w-4.5" aria-hidden />
              </div>
              <h2 id="custom-rule" className="text-xl font-semibold text-foreground">Designing Custom Rules</h2>
            </div>
            <p className="mb-4 text-sm leading-relaxed text-muted-foreground">
              Extend the <code>BaseRule</code> abstraction to create your own deterministic validation checks. This example detects numeric columns with zero standard deviation.
            </p>
            <CodeBlock code={CUSTOM_RULE_CODE} language="python" filename="zero_variance.py" showCopy />
          </section>

          {/* Example Datasets Grid */}
          <section className="mb-14" aria-labelledby="example-datasets">
            <div className="mb-6 border-t border-border pt-10">
              <h2 id="example-datasets" className="text-xl font-semibold text-foreground">Included Example Datasets</h2>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                Run the downloader utility in the root workspace to fetch and prepare these datasets programmatically:
              </p>
              <div className="mt-2 font-mono text-xs text-muted-foreground bg-muted/50 p-3 rounded border border-border">
                python examples/download_datasets.py && python examples/prepare_datasets.py
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {[
                {
                  title: "Iris",
                  source: "scikit-learn (load_iris)",
                  rows: "150",
                  cols: "5",
                  description: "Canonical clean machine learning dataset containing no missing values or outliers. Serves as a perfect baseline.",
                  findings: "0 findings",
                  target: "N/A"
                },
                {
                  title: "Titanic",
                  source: "OpenML (titanic)",
                  rows: "1,309",
                  cols: "14",
                  description: "Messy historical log containing missing ages and duplicate tickets. Triggers missing value threshold rules.",
                  findings: "Warnings (Missingness, Duplicates)",
                  target: "survived"
                },
                {
                  title: "California Housing",
                  source: "scikit-learn (fetch_california_housing)",
                  rows: "20,640",
                  cols: "9",
                  description: "Continuous spatial housing metrics with extreme values. Triggers numeric outlier detection and correlation rules.",
                  findings: "Warnings (Outliers, Correlation)",
                  target: "median_house_value"
                },
                {
                  title: "Customer Churn",
                  source: "OpenML (Telco-Customer-Churn)",
                  rows: "7,043",
                  cols: "24",
                  description: "IBM subscriber records containing synthetic correlation columns. Triggers critical target leakage validations.",
                  findings: "Critical (Target Leakage)",
                  target: "churn_label"
                },
                {
                  title: "Retail Sales",
                  source: "Synthetic Simulation (Superstore)",
                  rows: "1,000",
                  cols: "10",
                  description: "Transactional orders with datetime strings and empty fields. Triggers constant and fully empty column rules.",
                  findings: "Critical (Empty), Warnings (Constant)",
                  target: "N/A"
                }
              ].map((ds) => (
                <div key={ds.title} className="group rounded-xl border border-border bg-card p-5 transition-all duration-200 hover:border-primary/30 hover:shadow-sm">
                  <h3 className="text-sm font-semibold text-foreground">{ds.title}</h3>
                  <p className="mt-1 text-[11px] text-muted-foreground">Source: {ds.source}</p>
                  <p className="mt-3 text-xs leading-relaxed text-muted-foreground">{ds.description}</p>
                  <div className="mt-4 border-t border-border/60 pt-3 flex flex-wrap gap-2 text-[10px] text-muted-foreground font-mono">
                    <div>Rows: <span className="text-foreground">{ds.rows}</span></div>
                    <div>Cols: <span className="text-foreground">{ds.cols}</span></div>
                    {ds.target !== "N/A" && <div>Target: <span className="text-foreground">{ds.target}</span></div>}
                    <div className="w-full mt-1 text-primary">Audit: {ds.findings}</div>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Educational Notebooks List */}
          <section className="mb-14" aria-labelledby="tutorial-notebooks">
            <div className="mb-6 border-t border-border pt-10">
              <h2 id="tutorial-notebooks" className="text-xl font-semibold text-foreground">Jupyter Tutorial Notebooks</h2>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                Step-by-step interactive notebooks located in <code>examples/notebooks/</code>:
              </p>
            </div>

            <div className="space-y-3">
              {[
                {
                  filename: "01_getting_started.ipynb",
                  title: "Getting Started",
                  description: "Learn how to install Featuresmith, load datasets from CSV or DataFrame, run profiling, and view audit summaries."
                },
                {
                  filename: "02_exploring_datasets.ipynb",
                  title: "Exploring Datasets & Statistical Profiling",
                  description: "Deep dive into continuous numeric summaries, categorical value distributions, datetime spans, and Pearson correlation matrices."
                },
                {
                  filename: "03_understanding_rule_findings.ipynb",
                  title: "Rule Engine Configs & Gating",
                  description: "Inspect validation findings, customize rule parameters (e.g. missingness ratios), gate specific check rules, and isolate exceptions."
                },
                {
                  filename: "04_data_science_workflows.ipynb",
                  title: "Target Leakage & Modeling Pipelines",
                  description: "Set up pre-modeling filters to automatically detect and prune target leakage features before passing variables to estimators."
                }
              ].map((nb) => (
                <div key={nb.filename} className="rounded-lg border border-border bg-card p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div>
                    <h3 className="text-sm font-semibold text-foreground">{nb.title}</h3>
                    <p className="mt-1 text-xs text-muted-foreground">{nb.description}</p>
                    <code className="mt-2 block w-fit font-mono text-[10px] text-zinc-500 bg-muted px-1.5 py-0.5 rounded">{nb.filename}</code>
                  </div>
                  <Link
                    href={`https://github.com/adityagangwani30/FeatureSmith/blob/main/examples/notebooks/${nb.filename}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-shrink-0 inline-flex items-center gap-1.5 rounded-md border border-border bg-transparent px-3 py-1.5 text-xs font-medium text-foreground hover:bg-accent transition-all"
                  >
                    View Source
                    <ArrowRight className="h-3 w-3" />
                  </Link>
                </div>
              ))}
            </div>
          </section>

          {/* CTA Box */}
          <div className="mt-16 rounded-xl border border-border bg-muted/20 p-6 md:p-8 text-center">
            <h3 className="text-base font-semibold text-foreground">Ready to inspect performance?</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Review Featuresmith's loading, profiling, and rule engine benchmarks.
            </p>
            <div className="mt-5 flex justify-center gap-4">
              <Link
                href="/docs/benchmarks"
                className="inline-flex items-center gap-1 text-xs font-semibold text-primary transition-all hover:gap-2"
              >
                View Benchmarks
                <ArrowRight className="h-3 w-3" aria-hidden />
              </Link>
            </div>
          </div>
        </Container>
      </div>
      <Footer />
    </>
  )
}
