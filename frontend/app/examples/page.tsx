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

const SDK_EXAMPLE_CODE = `import featuresmith as fs

def run_featuresmith_pipeline(data_path: str, target: str):
    # 1. Load data into normalized Dataset wrapper
    print(f"Loading dataset from {data_path}...")
    dataset = fs.load(data_path)
    print(f"Loaded {dataset.row_count} rows across {dataset.column_count} columns.")

    # 2. Perform automated dataset code review with 8 reviewers
    print("Running automated dataset review...")
    review_result = fs.review(dataset, target_column=target)

    # 3. Extract explainable 0–100 ML Readiness Scorecard
    scorecard = fs.score(review_result)
    if scorecard:
        print(f"ML Readiness Score: {scorecard.overall:.1f} / 100")
        print("Dimension Breakdown:")
        for dim in scorecard.dimensions:
            print(f"  - {dim.label:<20}: {dim.score:5.1f}/100 ({len(dim.contributing_findings)} findings)")

    # 4. Compare with baseline dataset snapshot (Dataset Diff)
    diff_res = fs.diff(data_path, "baseline.csv", target_column=target)
    print(f"Dataset Health Verdict: {diff_res.summary.overall_health.upper()}")

if __name__ == "__main__":
    run_featuresmith_pipeline("customer_churn.csv", target="churn_label")`

const CICD_EXAMPLE_CODE = `# .github/workflows/data-quality-gate.yml
name: Data Quality Gate

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *' # Daily pipeline audits

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
          pip install featuresmith-cli

      - name: Audit dataset quality & leakage
        run: |
          # Gate CI build on review findings
          featuresmith review data/train.csv --target churn_label --format json --output report.json

      - name: Upload audit report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: data-audit-report
          path: report.json`

const CUSTOM_RULE_CODE = `from featuresmith.core.profile_result import ProfileResult
from featuresmith.rules.base import BaseRule
from featuresmith.core.rule_finding import RuleFinding

class ZeroVarianceRule(BaseRule):
    """Detect numeric columns with zero standard deviation."""

    @property
    def id(self) -> str:
        return "statistical.zero_variance"

    @property
    def name(self) -> str:
        return "Zero Variance Columns"

    @property
    def description(self) -> str:
        return "Flags numeric columns with no observed variance."

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
        for col_name, numeric_profile in profile.numeric_profiles.items():
            if numeric_profile.std_dev == 0.0:
                findings.append(
                    RuleFinding(
                        rule_id=self.id,
                        rule_name=self.name,
                        category=self.category,
                        severity=self.severity,
                        column_name=col_name,
                        title="Zero Variance Detected",
                        description=f"Column '{col_name}' has standard deviation of 0.0.",
                        evidence={"std_dev": numeric_profile.std_dev}
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
              Examples & Tutorials
            </h1>
            <p className="mt-3 text-base leading-relaxed text-muted-foreground">
              Production-grade implementations demonstrating Featuresmith SDK pipelines,
              interactive Jupyter tutorials, automated CI/CD quality gates, and custom rule design.
            </p>
          </header>

          {/* Educational Notebooks Section */}
          <section className="mb-14" aria-labelledby="tutorial-notebooks">
            <div className="mb-6">
              <div className="flex items-center gap-2.5 mb-2">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/8 text-primary ring-1 ring-primary/15">
                  <Code className="h-4.5 w-4.5" aria-hidden />
                </div>
                <h2 id="tutorial-notebooks" className="text-xl font-semibold text-foreground">
                  Official Jupyter Tutorial Notebooks
                </h2>
              </div>
              <p className="text-sm leading-relaxed text-muted-foreground">
                Follow our step-by-step interactive learning path located in <code>examples/notebooks/</code>. Every notebook includes real code, problem statements, output interpretations, and best practices.
              </p>
            </div>

            <div className="space-y-3">
              {[
                {
                  filename: "01_getting_started.ipynb",
                  title: "01. Getting Started with Featuresmith",
                  topic: "Getting Started & Dataset Profiling",
                  description: "Learn how to load datasets (fs.load), run deterministic profiling (fs.profile), conduct automated reviews (fs.review), and extract ML readiness scores (fs.score)."
                },
                {
                  filename: "02_dataset_review.ipynb",
                  title: "02. Complete Dataset Review Walkthrough",
                  topic: "Dataset Review Engine & 8 Reviewers",
                  description: "Explore the 8 automated reviewers evaluating schema health, data types, missingness spikes, duplicate records, constant columns, high cardinality, distributions, and leakage risk."
                },
                {
                  filename: "03_ml_readiness_score.ipynb",
                  title: "03. Understanding the ML Readiness Score",
                  topic: "ML Readiness Score & Health Dimensions",
                  description: "Deep dive into the 0–100 quality scorecard, mathematical dimension weights, category breakdowns, and actionable remediation suggestions."
                },
                {
                  filename: "04_leakage_detection.ipynb",
                  title: "04. Detecting Data Leakage before Training",
                  topic: "Intelligent Leakage Detection",
                  description: "Master target correlation detectors, timestamp anomalies, identifier shapes, post-outcome names, and duplicate target copies using 6 specialized pattern detectors."
                },
                {
                  filename: "05_dataset_diff.ipynb",
                  title: "05. Comparing Dataset Versions with Dataset Diff",
                  topic: "Dataset Diff Engine (fs.diff)",
                  description: "Compare dataset snapshot versions (v1 vs v2) to detect schema drift, missingness spikes, distribution shifts, and receive an overall health verdict."
                },
                {
                  filename: "06_end_to_end_workflow.ipynb",
                  title: "06. End-to-End ML Dataset Validation Workflow",
                  topic: "End-to-End Validation Pipeline Gate",
                  description: "Build an automated Python pre-training quality gate function that validates datasets, enforces score thresholds, and halts pipelines on critical findings."
                }
              ].map((nb) => (
                <div key={nb.filename} className="rounded-lg border border-border bg-card p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 transition-all hover:border-primary/30">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="rounded bg-primary/10 px-2 py-0.5 text-[10px] font-semibold text-primary">{nb.topic}</span>
                    </div>
                    <h3 className="text-sm font-semibold text-foreground">{nb.title}</h3>
                    <p className="mt-1 text-xs leading-relaxed text-muted-foreground">{nb.description}</p>
                    <code className="mt-2 block w-fit font-mono text-[10px] text-muted-foreground bg-muted/60 px-1.5 py-0.5 rounded">{nb.filename}</code>
                  </div>
                  <Link
                    href={`https://github.com/adityagangwani30/FeatureSmith/blob/main/examples/notebooks/${nb.filename}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-shrink-0 inline-flex items-center gap-1.5 rounded-md border border-border bg-transparent px-3.5 py-1.5 text-xs font-medium text-foreground hover:bg-accent transition-all"
                  >
                    View Source
                    <ArrowRight className="h-3 w-3" />
                  </Link>
                </div>
              ))}
            </div>
          </section>

          {/* Python SDK Pipeline Example */}
          <section className="mb-14" aria-labelledby="sdk-pipeline">
            <div className="mb-4 flex items-center gap-2.5">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/8 text-primary ring-1 ring-primary/15">
                <Code className="h-4.5 w-4.5" aria-hidden />
              </div>
              <h2 id="sdk-pipeline" className="text-xl font-semibold text-foreground">Python SDK Pipeline</h2>
            </div>
            <p className="mb-4 text-sm leading-relaxed text-muted-foreground">
              This pipeline script demonstrates loading data, executing automated dataset code reviews, extracting scorecards, and running snapshot comparisons via <code>fs.diff()</code>.
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
              Integrate the Featuresmith CLI into your GitHub Actions workflow. Deterministic exit code gating ensures broken or leaked datasets never reach training.
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
              Extend the <code>BaseRule</code> abstraction to create custom deterministic check rules. This example detects numeric columns with zero standard deviation.
            </p>
            <CodeBlock code={CUSTOM_RULE_CODE} language="python" filename="zero_variance.py" showCopy />
          </section>

          {/* Example Datasets Grid */}
          <section className="mb-14" aria-labelledby="example-datasets">
            <div className="mb-6 border-t border-border pt-10">
              <h2 id="example-datasets" className="text-xl font-semibold text-foreground">Included Real-World Example Datasets</h2>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                The Titanic dataset is bundled in the repository (no setup needed). The other datasets are
                generated or downloaded with the example preparation scripts in the project root:
              </p>
              <div className="mt-2 font-mono text-xs text-muted-foreground bg-muted/50 p-3 rounded border border-border">
                python examples/download_datasets.py   # optional: network fetch for raw datasets
                python examples/prepare_datasets.py
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {[
                {
                  title: "Iris Classification",
                  source: "scikit-learn (load_iris)",
                  rows: "150",
                  cols: "5",
                  description: "Canonical clean benchmark dataset containing 0 missing values and clean feature ranges. Serves as a 100/100 baseline.",
                  score: "100.0/100 (PASSED)",
                  target: "species"
                },
                {
                  title: "Titanic Classification",
                  source: "OpenML (titanic)",
                  rows: "891",
                  cols: "12",
                  description: "Historical survival dataset containing cabin null spikes, free text columns, and age missingness. Triggers missing value and data type findings.",
                  score: "86.9/100 (WARNINGS)",
                  target: "survived"
                },
                {
                  title: "California Housing",
                  source: "scikit-learn (fetch_california_housing)",
                  rows: "20,640",
                  cols: "9",
                  description: "Continuous spatial housing metrics for regression. Triggers distribution skewness and kurtosis structural findings.",
                  score: "90.0/100 (WARNINGS)",
                  target: "median_house_value"
                },
                {
                  title: "Customer Churn & Leakage",
                  source: "Telco Churn Dataset",
                  rows: "7,043",
                  cols: "24",
                  description: "Telecom subscriber records containing synthetic target leakage columns. Triggers 4 intelligent leakage pattern detectors.",
                  score: "94.4/100 (CRITICAL LEAKAGE)",
                  target: "churn_label"
                },
                {
                  title: "Retail Sales Snapshot",
                  source: "Superstore Transactions",
                  rows: "1,000",
                  cols: "10",
                  description: "Transactional sales dataset used to demonstrate Dataset Diff (fs.diff) snapshot version comparisons (v1 vs v2).",
                  score: "Verdict: REGRESSED",
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
                    <div className="w-full mt-1 text-primary">Score: {ds.score}</div>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* CTA Box */}
          <div className="mt-16 rounded-xl border border-border bg-muted/20 p-6 md:p-8 text-center">
            <h3 className="text-base font-semibold text-foreground">Ready to inspect performance?</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Review Featuresmith's loading, profiling, review, and score benchmarks.
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
