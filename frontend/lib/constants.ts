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
    phase: "Phase 0 & 1",
    title: "Foundations & Core MVP",
    status: "done",
    items: [
      "Core Dataset schema abstractions and explicit loading registry",
      "Connectors for CSV, Parquet, Excel, pandas, and Polars DataFrames",
      "Deterministic Profiling Engine with Cap-controlled correlation matrix",
      "Deterministic Rule Engine with 8 seed quality & leakage rules",
      "CLI analyze command with table/json formatting and exit-code gating",
    ],
  },
  {
    phase: "Phase 2 & 3",
    title: "AI Narration & Interactive Chat",
    status: "in-progress",
    items: [
      "AI Provider protocol supporting Ollama (local), OpenAI, and Anthropic",
      "Plain-language dataset narration and recommendation ranking",
      "Interactive AI Chat Session grounded entirely in computed ProfileResult",
      "Zero network-fallback template mode when no LLM provider is active",
    ],
  },
  {
    phase: "Phase 4 & 5",
    title: "Export Layer & Dashboard UI",
    status: "planned",
    items: [
      "Export code-generators for sklearn Pipelines and Jupyter Notebooks",
      "HTML static report generation with declarative chart specs",
      "Streamlit Dashboard for interactive browser-based uploads, charts, and chat",
      "SQL database connectors with profile pushdown capabilities",
    ],
  },
  {
    phase: "Phase 6 & 7",
    title: "Plugin Ecosystem & Editor Extensions",
    status: "future",
    items: [
      "Dataset diffing and distribution drift detection across snapshots",
      "Plugin cookiecutter templates for community rules, connectors, and exporters",
      "VS Code extension for inline data profiling & interactive chat in-editor",
      "Feature store exports (Feast schemas)",
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
    label: "Recommendation Engine (Phase 2+)",
    sublabel: "Grounded feature engineering rankings and rationales",
    future: true,
  },
  {
    id: "ai",
    label: "AI Layer & Chat (Phase 2+)",
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
