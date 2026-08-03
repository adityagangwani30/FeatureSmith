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
    icon: "Database",
    title: "Dataset Layer",
    description:
      "Unified interface for loading tabular data from CSV, Parquet, Excel, pandas, and Polars DataFrames into a normalized contract.",
  },
  {
    icon: "BarChart2",
    title: "Profiling Engine",
    description:
      "Deterministic computation of 23 numeric metrics, categorical frequency, text profiles, datetime ranges, and Pearson correlations.",
  },
  {
    icon: "ShieldCheck",
    title: "Rule Engine",
    description:
      "8 built-in deterministic validation and leakage rules covering duplicate rows, missingness ratios, empty columns, and target leakage.",
  },
  {
    icon: "Terminal",
    title: "CLI Wrapper",
    description:
      "Thin Typer command-line client enabling styled Rich tables, JSON export, and exit-code gating (0 = clean, 1 = findings) for CI pipelines.",
  },
  {
    icon: "Sparkles",
    title: "AI-Ready Architecture",
    description:
      "Core structure prepared for pluggable AI Providers (Ollama, OpenAI, Anthropic) to narrate results, rank recommendations, and run interactive Q&A.",
  },
  {
    icon: "Puzzle",
    title: "Extensible design",
    description:
      "Built-in extension points for registering custom connectors, rules, exporters, and AI providers using standard setuptools entry points.",
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

# ── Load ───────────────────────────────────────────────────
# Load dataset from CSV, Excel, Parquet, or in-memory DataFrame
dataset = fs.load("customers.csv")
print(dataset.row_count)        # 50000
print(dataset.schema.names)     # ['id', 'age', 'churn', ...]

# ── Profile ────────────────────────────────────────────────
# Run deterministic profiling engine
profile = fs.profile("customers.csv")
for name, col in profile.column_profiles.items():
    print(f"{name}: {col.missing_count} missing values")

# ── Analyze ────────────────────────────────────────────────
# Run rule engine: loader → profiler → rules evaluation
result = fs.analyze("customers.csv", target_column="churn")

for finding in result.findings:
    print(f"[{finding.severity.upper()}] {finding.title}")
    print(f"  Column : {finding.column_name}")
    print(f"  Rule   : {finding.rule_id}")
    print(f"  Detail : {finding.description}")

print(f"Executed: {len(result.executed_rules)} rules in {result.execution_time_ms:.1f}ms")`

export const CLI_EXAMPLE_CODE = `# Install featuresmith-core and featuresmith-cli packages
pip install featuresmith-core featuresmith-cli

# Run basic analysis (styled Rich terminal tables)
featuresmith analyze customers.csv

# Run leakage detection targeting churn with exit-code gating for CI/CD
featuresmith analyze customers.csv --target churn --severity warning

# Output findings as machine-readable JSON to a report file
featuresmith analyze customers.csv --format json --output report.json

# Run analysis in quiet mode (useful for script integrations)
featuresmith analyze customers.csv --output report.txt --quiet`
