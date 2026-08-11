import type { NavItem, Feature, RoadmapItem, ArchitectureNode, DocSection } from "@/types"

export const NAV_ITEMS: NavItem[] = [
  { label: "Docs", href: "/docs" },
  { label: "SDK", href: "/docs/sdk/load" },
  { label: "CLI", href: "/docs/cli/analyze" },
  { label: "Examples", href: "/examples" },
  { label: "Roadmap", href: "/#roadmap" },
  { label: "GitHub", href: "https://github.com/adityagangwani30/FeatureSmith", external: true },
]

export const FEATURES: Feature[] = [
  {
    icon: "ShieldCheck",
    title: "Dataset Code Review",
    description:
      "Automate code reviews for your datasets before model training. 8 automated reviewers inspect schema, data types, missingness, duplicates, and distributions.",
  },
  {
    icon: "Sparkles",
    title: "ML Readiness Score",
    description:
      "Know whether your dataset is actually ready for machine learning with an explainable 0–100 quality scorecard across 8 health dimensions.",
  },
  {
    icon: "BarChart2",
    title: "Intelligent Leakage Detection",
    description:
      "Prevent target leakage, future timestamps, and ID correlation from silently corrupting model validation scores before training.",
  },
  {
    icon: "Database",
    title: "Dataset Diff Engine",
    description:
      "Understand exactly what changed between two dataset snapshot versions (schema, missingness, distribution shifts, quality deltas).",
  },
  {
    icon: "Terminal",
    title: "CI/CD Gate Integration",
    description:
      "Stop bad datasets in CI pipelines with deterministic exit-code gating (0 = clean, 1 = findings) and machine-readable JSON exports.",
  },
  {
    icon: "Puzzle",
    title: "Extensible Architecture",
    description:
      "Deterministic computation powered by Polars with extensible plugin points for custom reviewers, rules, connectors, and exporters.",
  },
]

export const ROADMAP: RoadmapItem[] = [
  {
    phase: "Phase 0",
    title: "Foundations — Core Library First",
    status: "done",
    items: [
      "Monorepo workspace setup (featuresmith-core, featuresmith-cli, dashboard stub)",
      "Ruff linting, MyPy strict type checking, Pytest, and import-linter CI/CD",
      "Core Dataset and ProfileResult Pydantic schemas",
      "Base interface stubs for connectors, rules, exporters, and AIProvider",
    ],
  },
  {
    phase: "Phase 1",
    title: "Foundation — SDK + CLI MVP, Profiling + Rule Engine (v0.1)",
    status: "done",
    items: [
      "Polars-based deterministic Profiling Engine computing statistical profiles",
      "CsvConnector, ExcelConnector, ParquetConnector, and DataFrameConnector",
      "Deterministic Rule Engine with 8 seed quality & leakage rules",
      "Python SDK: load(), profile(), and analyze() public APIs",
      "CLI: featuresmith analyze command with Rich table and JSON output",
    ],
  },
  {
    phase: "Phase 2",
    title: "Dataset Review Platform — Review Engine, Score, Leakage & Diff (v0.2)",
    status: "done",
    items: [
      "Review Engine with 8 built-in reviewers (schema, quality, leakage)",
      "ML Readiness Score with 8 deterministic dimensions (0–100 quality scorecard)",
      "Intelligent Leakage Detection with 6 pattern detectors (correlation, timestamp, duplicate target, etc.)",
      "Dataset Diff via fs.diff() and featuresmith diff command for snapshot comparisons",
      "CLI: featuresmith review and featuresmith diff commands with exit-code CI gating",
    ],
  },
  {
    phase: "Phase 3",
    title: "Developer Experience — Dashboard, Connectors, CI/CD, Plugins (v0.3)",
    status: "planned",
    items: [
      "featuresmith dashboard (Streamlit) browser interface for browsing findings",
      "SQL database connector (SQLAlchemy) & connector completion",
      "featuresmith-action GitHub Action wrapping review gating",
      "Pluggable extension registry via entry points for custom rules & connectors",
    ],
  },
  {
    phase: "Phase 4",
    title: "Recommendation & Planning — Recommendation Engine & Plan primitive (v0.4)",
    status: "planned",
    items: [
      "Centralized Recommendation Engine merging findings into a ranked, explainable list",
      "FeatureQualityReviewer completing coverage for low-signal & redundant features",
      "featuresmith.plan module — fs.plan() and featuresmith plan producing inspectable Plan objects",
      "Deterministic Plan step rendering and confidence ranking",
    ],
  },
  {
    phase: "Phase 5",
    title: "Dataset Contracts — Apply, Validation, featuresmith.lock (v0.5)",
    status: "planned",
    items: [
      "featuresmith.apply — generating sklearn/Polars code from accepted Plans (never a custom runtime)",
      "Automatic post-apply re-review and fs.diff() validation",
      "featuresmith.contract module — DatasetContract schema, fs.lock(), and featuresmith lock --check",
    ],
  },
  {
    phase: "Phase 6",
    title: "Certification & Observability — Badge, Scheduled Re-review, Quality History (v0.6-v1.0)",
    status: "planned",
    items: [
      "Portable 'Featuresmith-verified' badge linked to featuresmith verify <hash>",
      "Scheduled re-profiling against configured data sources",
      "Pluggable Quality History storage backend",
      "Threshold-based notifications (Slack, email, webhook) on regressions",
    ],
  },
  {
    phase: "Phase 7",
    title: "AI-Assisted Planning — Provider Layer, Narration, Natural-Language Plan Authoring (v1.x)",
    status: "planned",
    items: [
      "AIProvider protocol (Ollama local default, OpenAI/Anthropic opt-in)",
      "Plain-language dataset & Contract-diff narrative summaries",
      "Natural-language Plan authoring (fs.plan(result, instruct='...'))",
      "Interactive AI Chat grounded in deterministic findings",
    ],
  },
  {
    phase: "Phase 8",
    title: "Ecosystem Integrations & Scale — Exporters, VS Code, Distributed Compute, Hosted Tier (v2.0+)",
    status: "planned",
    items: [
      "dbt model-stub and Feast feature-definition code exporters",
      "MLflow and Weights & Biases run-metadata attachment with Contract fingerprint",
      "VS Code extension and Jupyter magic commands",
      "Snowflake/BigQuery connectors & optional Spark/Ray profiler backend",
      "Hosted dashboard tier for team collaboration and shared history",
    ],
  },
]

export const ARCHITECTURE_NODES: ArchitectureNode[] = [
  {
    id: "raw",
    label: "Raw Data Source",
    sublabel: "CSV · Excel · Parquet · DataFrame",
  },
  {
    id: "dataset",
    label: "Dataset Layer",
    sublabel: "fs.load() normalized schema and connectors",
  },
  {
    id: "review",
    label: "Dataset Review Engine (v0.2.0)",
    sublabel: "8 automated reviewers · 0–100 ML Readiness Score · 6 Leakage detectors · Diff",
  },
  {
    id: "cli_sdk",
    label: "CLI & SDK Interfaces",
    sublabel: "Zero business logic thin clients calling public SDK APIs",
  },
  {
    id: "plan",
    label: "Recommendation & Plan Primitive (Phase 4+)",
    sublabel: "Inspectable transformation steps and rationales before execution",
    future: true,
  },
  {
    id: "contract",
    label: "Dataset Contracts & featuresmith.lock (Phase 5+)",
    sublabel: "Versioned lockfiles, post-apply validation, CI drift-gating",
    future: true,
  },
  {
    id: "ai",
    label: "AI-Assisted Planning & Chat (Phase 7+)",
    sublabel: "Natural-language plan authoring & narrative summaries over deterministic facts",
    future: true,
  },
]

export const DOC_SECTIONS: DocSection[] = [
  {
    title: "Getting Started",
    href: "/docs",
    items: [
      { title: "Introduction", href: "/docs" },
      { title: "Installation", href: "/docs/installation" },
      { title: "Quick Start", href: "/docs/quickstart" },
      { title: "Tutorial Notebooks", href: "/examples#tutorial-notebooks" },
      { title: "Benchmarks", href: "/docs/benchmarks" },
      { title: "Development Setup", href: "/docs/dev-setup" },
      { title: "Contributing", href: "/docs/contributing" },
    ],
  },
  {
    title: "Core Concepts",
    href: "/docs/concepts",
    items: [
      { title: "Architecture Overview", href: "/docs/concepts/architecture" },
      { title: "Dataset Layer", href: "/docs/concepts/dataset" },
      { title: "Connectors", href: "/docs/concepts/connectors" },
      { title: "Profiling Engine", href: "/docs/concepts/profiling" },
      { title: "Rule Engine", href: "/docs/concepts/rules" },
    ],
  },
  {
    title: "Python SDK",
    href: "/docs/sdk",
    items: [
      { title: "load()", href: "/docs/sdk/load" },
      { title: "profile()", href: "/docs/sdk/profile" },
      { title: "analyze()", href: "/docs/sdk/analyze" },
      { title: "review()", href: "/docs/sdk/review" },
      { title: "diff()", href: "/docs/sdk/diff" },
      { title: "score()", href: "/docs/sdk/score" },
      { title: "Dataset", href: "/docs/sdk/dataset" },
      { title: "Data Models", href: "/docs/sdk/models" },
      { title: "Profile Models", href: "/docs/sdk/models/profile" },
      { title: "Rule & Finding Models", href: "/docs/sdk/models/rules" },
      { title: "Review Models", href: "/docs/sdk/models/review" },
      { title: "Score Models", href: "/docs/sdk/models/score" },
      { title: "Leakage Models", href: "/docs/sdk/models/leakage" },
      { title: "Diff Models", href: "/docs/sdk/models/diff" },
      { title: "Exceptions", href: "/docs/sdk/exceptions" },
      { title: "Plugins", href: "/docs/sdk/plugins" },
    ],
  },
  {
    title: "CLI Reference",
    href: "/docs/cli",
    items: [
      { title: "analyze", href: "/docs/cli/analyze" },
      { title: "review", href: "/docs/cli/review" },
      { title: "diff", href: "/docs/cli/diff" },
      { title: "score", href: "/docs/cli/score" },
      { title: "Configuration", href: "/docs/cli/config" },
    ],
  },
  {
    title: "Guides",
    href: "/docs/guides",
    items: [
      { title: "CI/CD Integration", href: "/docs/guides/cicd" },
      { title: "Custom Rules", href: "/docs/guides/rules" },
      { title: "Writing Plugins", href: "/docs/guides/plugins" },
    ],
  },
  {
    title: "Resources",
    href: "/docs/resources",
    items: [
      { title: "Release Notes", href: "/docs/resources/release" },
      { title: "FAQ", href: "/docs/resources/faq" },
      { title: "Troubleshooting", href: "/docs/resources/troubleshooting" },
    ],
  },
]


export const PYTHON_EXAMPLE_CODE = `import featuresmith as fs

# 1. Load dataset (CSV, Parquet, Excel, pandas/Polars DataFrame)
dataset = fs.load("examples/data/processed/titanic.csv")
print(f"Loaded {dataset.row_count} rows across {len(dataset.schema.names)} columns.")

# 2. Run automated dataset code review with 8 reviewers
review_res = fs.review(dataset, target_column="survived")

# 3. Extract 0-100 ML Readiness Scorecard
scorecard = fs.score(review_res)
if scorecard:
    print(f"ML Readiness Score: {scorecard.overall}/100")
    for dim in scorecard.dimensions:
        print(f"  - {dim.label}: {dim.score}/100 ({len(dim.contributing_findings)} findings)")

# 4. Compare dataset snapshots (Dataset Diff)
diff_res = fs.diff("v1.csv", "v2.csv", target_column="survived")
print(f"Health Verdict: {diff_res.summary.overall_health}")`

export const CLI_EXAMPLE_CODE = `# Install Featuresmith CLI
pip install featuresmith-cli

# Run complete dataset review report with scorecard
featuresmith review examples/data/processed/titanic.csv --target survived

# Run target leakage and quality rule analysis
featuresmith analyze examples/data/processed/titanic.csv --target survived

# Compare two snapshot profiles (Dataset Diff Engine)
featuresmith diff train_v1.csv train_v2.csv --target survived

# Export report to JSON for CI/CD gating (0 = clean, 1 = findings)
featuresmith review train.csv --target survived --format json --output report.json`
