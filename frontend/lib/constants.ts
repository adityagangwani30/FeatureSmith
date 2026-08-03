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
    title: "Foundations",
    status: "done",
    items: [
      "Monorepo workspace setup (core, cli, dashboard)",
      "Ruff linting, MyPy strict type checking, Pytest, and import-linter CI/CD",
      "Core Dataset and ProfileResult Pydantic schemas",
      "Base interface stubs for connectors, rules, exporters, and AIProvider",
    ],
  },
  {
    phase: "Phase 1",
    title: "Foundation — EDA & Rule Engine (v0.1)",
    status: "done",
    items: [
      "Polars-based deterministic Profiling Engine computing statistical profiles",
      "CsvConnector and DataFrameConnector implementations",
      "Deterministic Rule Engine with 8 seed quality & leakage rules",
      "Python SDK: load(), profile(), and analyze() public APIs",
      "CLI: featuresmith analyze command with Rich table and JSON formats",
    ],
  },
  {
    phase: "Phase 2",
    title: "Data Quality — Review Engine, Score, Diff & Leakage (v0.2)",
    status: "done",
    items: [
      "Review Engine with 8 built-in reviewers (schema, quality, leakage)",
      "ML Readiness Score with 8 deterministic dimensions",
      "Dataset Diff via fs.diff() and featuresmith diff command",
      "Intelligent Leakage Detection with 6 pattern detectors",
      "CLI: featuresmith review and featuresmith diff commands",
    ],
  },
  {
    phase: "Phase 3",
    title: "Developer Experience (v0.3)",
    status: "planned",
    items: [
      "Streamlit dashboard browser interface to connect data and browse findings",
      "Connectors for Excel, Parquet, and SQL databases",
      "GitHub Action (featuresmith-action) for CI pipeline gating",
      "Pluggable extension registry via entry points for custom rules & connectors",
    ],
  },
  {
    phase: "Phase 4",
    title: "Feature Intelligence & Export Layer (v0.4)",
    status: "planned",
    items: [
      "Feature engineering transformation recommendations",
      "Recommendation engine with deterministic severity and confidence ranking",
      "Code-generator exporters for sklearn Pipelines and Jupyter Notebooks",
      "Declarative HTML static report generation",
    ],
  },
  {
    phase: "Phase 5",
    title: "Data Observability & History (v0.5)",
    status: "planned",
    items: [
      "Cron-based scheduled re-profiling of data sources",
      "Pluggable Quality History storage backend",
      "Slack, email, and webhook notifications on regressions or schema shifts",
      "Team dashboard view showing dataset health trends over time",
    ],
  },
  {
    phase: "Phase 6",
    title: "AI Assistant Layer (v1.0)",
    status: "planned",
    items: [
      "AIProvider protocol supporting Ollama (local default), OpenAI, and Anthropic",
      "Plain-language dataset narrative summaries and recommendation explanations",
      "Interactive AI Chat Session grounded in ProfileResult findings",
    ],
  },
  {
    phase: "Phase 7",
    title: "AI Data Engineer (v2.0)",
    status: "planned",
    items: [
      "VS Code extension for inline data profiling and chat panel",
      "Jupyter magic commands for quick profiling and explanations",
      "Natural-language featuresmith explain CLI command",
    ],
  },
  {
    phase: "Phase 8",
    title: "Scale & Hosted Tier (v3.0+)",
    status: "planned",
    items: [
      "Snowflake and BigQuery connectors with pushdown profiling",
      "Optional Spark/Ray execution backend for large-scale compute",
      "Hosted dashboard tier with team collaboration and shared chat threads",
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
    label: "Dataset",
    sublabel: "fs.load() normalized schema and connectors",
  },
  {
    id: "profile",
    label: "ProfileResult",
    sublabel: "fs.profile() deterministic statistical profiling",
  },
  {
    id: "rule",
    label: "RuleResult",
    sublabel: "fs.analyze() running 8 deterministic rules",
  },
  {
    id: "cli_sdk",
    label: "CLI & SDK interfaces",
    sublabel: "Zero business logic thin clients calling public SDK APIs",
  },
  {
    id: "recommendation",
    label: "Recommendation Engine (Phase 4+)",
    sublabel: "Grounded feature engineering rankings and rationales",
    future: true,
  },
  {
    id: "ai",
    label: "AI Layer & Chat (Phase 6+)",
    sublabel: "Narrative summaries & interactive context-grounded Q&A",
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
      { title: "Data Models", href: "/docs/sdk/models" },
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
