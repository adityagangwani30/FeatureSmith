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
      "Automate code reviews for your datasets before model training. 10 automated reviewers inspect schema, data types, missingness, duplicates, distributions, feature quality, and snapshot deltas.",
  },
  {
    icon: "Sparkles",
    title: "ML Readiness Score",
    description:
      "Know whether your dataset is actually ready for machine learning with an explainable 0–100 quality scorecard across 7 effective health dimensions.",
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
    phase: "Shipped",
    title: "Foundation & Core Review Capabilities (v0.1 → v0.4)",
    status: "done",
    items: [
      "Monorepo core library, SDK (load, review, diff, score, plan), and CLI (featuresmith)",
      "10 built-in automated reviewers (schema, missingness, duplicates, constants, cardinality, stats, leakage, diff, feature quality)",
      "ML Readiness Score with 7 effective health dimensions (0–100 composite scorecard)",
      "Intelligent Leakage Detection with 6 pattern detectors (correlation, timestamp, duplicate target, etc.)",
      "Centralized Recommendation Engine & inspectable Plan primitive (fs.plan() / featuresmith plan)",
    ],
  },
  {
    phase: "Next",
    title: "Dataset Contracts, Apply Layer & Validation (v0.5)",
    status: "in-progress",
    items: [
      "featuresmith.apply — generating clean scikit-learn / Polars transformation code from accepted Plans (never a custom runtime)",
      "Automatic post-export re-review and fs.diff() validation",
      "featuresmith.contract module — DatasetContract schema, featuresmith.lock, and featuresmith lock --check",
    ],
  },
  {
    phase: "Medium-Term",
    title: "Continuous Certification, Observability & Stability (v0.6 → v1.0)",
    status: "planned",
    items: [
      "Portable 'Featuresmith-verified' badge linked to featuresmith verify <hash>",
      "Quality History storage abstraction & time-series quality tracking",
      "Scheduled local re-reviews & regression alerts (Slack, email, webhook)",
      "CI/CD contract drift gating (featuresmith-action GitHub Action)",
      "v1.0.0 Stable Dataset Contract & public API freeze milestone",
    ],
  },
  {
    phase: "Long-Term",
    title: "AI Assistance, Ecosystem Exporters & Scale (v1.1 → v2.0+)",
    status: "future",
    items: [
      "AIProvider protocol (Ollama local default, OpenAI/Anthropic BYO-key), narrative summaries, and NL Plan authoring",
      "dbt model-stub and Feast feature-definition code exporters",
      "MLflow and Weights & Biases run-metadata attachments with Contract fingerprints",
      "Pushdown profiling connectors (DuckDB, Snowflake, BigQuery) & optional Spark/Ray profiler backend",
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
    label: "Dataset Review Engine",
    sublabel: "10 automated reviewers · 0–100 ML Readiness Score · 6 Leakage detectors · Diff-aware review",
  },
  {
    id: "cli_sdk",
    label: "CLI & SDK Interfaces",
    sublabel: "Zero business logic thin clients calling public SDK APIs",
  },
  {
    id: "plan",
    label: "Recommendation & Plan Primitive",
    sublabel: "Ranked recommendations compiled into inspectable transformation steps",
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
      { title: "Dataset Review Engine", href: "/docs/concepts/review" },
      { title: "ML Readiness Score", href: "/docs/concepts/score" },
      { title: "Target Leakage Detection", href: "/docs/concepts/leakage" },
      { title: "Dataset Diff Engine", href: "/docs/concepts/diff" },
      { title: "Target Column Concept", href: "/docs/concepts/target-column" },
      { title: "Mental Model & Workflow", href: "/docs/concepts/workflow" },
      { title: "Interpreting Findings", href: "/docs/concepts/interpretation" },
      { title: "Workflow Cheat Sheet", href: "/docs/concepts/cheatsheet" },
      { title: "Beginner Glossary", href: "/docs/concepts/glossary" },
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
      { title: "plan()", href: "/docs/sdk/plan" },
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
      { title: "plan", href: "/docs/cli/plan" },
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

# 2. Run automated dataset code review with 10 reviewers
review_res = fs.review(dataset, target_column="survived")

# 3. Extract 0-100 ML Readiness Scorecard
scorecard = fs.score(review_res)
if scorecard:
    print(f"ML Readiness Score: {scorecard.overall}/100")
    for dim in scorecard.dimensions:
        print(f"  - {dim.label}: {dim.score}/100 ({len(dim.contributing_findings)} findings)")

# 4. Compare dataset snapshots (Dataset Diff)
diff_res = fs.diff("v1.csv", "v2.csv", target_column="survived")
print(f"Health Verdict: {diff_res.summary.overall_health}")

# 5. Compile an inspectable remediation Plan from accepted recommendations
plan = fs.plan(review_res, accept=["rec.quality.missingness.cabin"])
for item in plan.items:
    print(f"  - {item.title} (confidence {item.confidence})")`

export const CLI_EXAMPLE_CODE = `# Install Featuresmith CLI
pip install featuresmith-cli

# Run complete dataset review report with scorecard
featuresmith review examples/data/processed/titanic.csv --target survived

# Run target leakage and quality rule analysis
featuresmith analyze examples/data/processed/titanic.csv --target survived

# Compare two snapshot profiles (Dataset Diff Engine)
featuresmith diff train_v1.csv train_v2.csv --target survived

# Generate an inspectable remediation Plan from accepted recommendations
featuresmith plan train.csv --target survived --accept rec.quality.missingness.cabin

# Export report to JSON for CI/CD gating (0 = clean, 1 = findings)
featuresmith review train.csv --target survived --format json --output report.json`
