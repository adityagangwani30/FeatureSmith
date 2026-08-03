import Link from "next/link"
import type { Metadata } from "next"
import { ArrowRight, ChevronRight } from "lucide-react"
import { CodeBlock } from "@/components/ui/code-block"

export const metadata: Metadata = {
  title: "Introduction",
  description: "Get started with Featuresmith — the open-source Python library for data profiling and validation.",
}

const INSTALL_CODE = `# Python SDK only (import featuresmith)
pip install featuresmith-core

# CLI & Python SDK (featuresmith CLI command)
pip install featuresmith-cli`

const QUICKSTART_CODE = `import featuresmith as fs

# 1. Load the dataset (CSV, Parquet, Excel, pandas/Polars DataFrame)
dataset = fs.load("examples/data/processed/titanic.csv")
print(f"Loaded {dataset.row_count} rows across columns: {dataset.schema.names}")

# 2. Extract profile statistics
profile = fs.profile(dataset)
for col_name, col in profile.column_profiles.items():
    if col.missing_count > 0:
        print(f"Column '{col_name}' has {col.missing_count} missing values")

# 3. Perform a comprehensive review with ML Readiness Scorecard
result = fs.review(dataset, target_column="survived")
print(result.overall_summary)

if result.score:
    print(f"ML Readiness Score: {result.score.overall}/100")`

const QUICK_LINKS = [
  {
    title: "Installation",
    description: "Install Featuresmith via pip or from source.",
    href: "/docs/installation",
  },
  {
    title: "Quick Start",
    description: "Load a dataset, run your first profile, and validate in minutes.",
    href: "/docs/quickstart",
  },
  {
    title: "Python SDK",
    description: "Full API reference for the Dataset, Profile, and Rule classes.",
    href: "/docs/sdk",
  },
  {
    title: "CLI Reference",
    description: "Command-line interface for analyze, profile, and validate.",
    href: "/docs/cli",
  },
]

export default function DocsPage() {
  return (
    <article className="prose-custom max-w-none">
      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb" className="mb-6 flex items-center gap-1 text-sm text-muted-foreground">
        <Link href="/" className="hover:text-foreground">
          Home
        </Link>
        <ChevronRight className="h-3.5 w-3.5" aria-hidden />
        <span className="text-foreground">Documentation</span>
      </nav>

      {/* Page header */}
      <header className="mb-10 border-b border-border pb-8">
        <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-primary">
          Getting Started
        </p>
        <h1 className="mb-3 text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
          Introduction
        </h1>
        <p className="text-base leading-relaxed text-muted-foreground">
          Featuresmith is an open-source Python library for dataset profiling,
          rule-based validation, and intelligent feature analysis. This guide
          will get you up and running in minutes.
        </p>
      </header>

      {/* What is Featuresmith */}
      <section className="mb-10" aria-labelledby="what-is">
        <h2 id="what-is" className="mb-3 text-xl font-semibold text-foreground">
          What is Featuresmith?
        </h2>
        <p className="mb-4 text-sm leading-relaxed text-muted-foreground">
          Modern data pipelines move fast. Schema drift, unexpected nulls, and
          silent type coercions cause downstream failures that are expensive to
          debug. Featuresmith gives you a lightweight, composable toolkit to
          understand and validate your data before it causes problems.
        </p>
        <ul className="space-y-2 text-sm text-muted-foreground" role="list">
          {[
            "Profile datasets to understand distributions, nulls, and cardinality",
            "Define validation rules as code, not configuration",
            "Run analysis from the CLI or integrate into any Python workflow",
            "Designed to scale from a single script to a full CI/CD pipeline",
          ].map((item) => (
            <li key={item} className="flex items-start gap-2">
              <span className="mt-2 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" aria-hidden />
              {item}
            </li>
          ))}
        </ul>
      </section>

      {/* Installation */}
      <section className="mb-10" aria-labelledby="installation">
        <h2 id="installation" className="mb-3 text-xl font-semibold text-foreground">
          Installation
        </h2>
        <p className="mb-4 text-sm leading-relaxed text-muted-foreground">
          Install Featuresmith from PyPI using pip:
        </p>
        <CodeBlock code={INSTALL_CODE} language="bash" showCopy />
        <p className="mt-3 text-xs text-muted-foreground">
          Requires Python 3.11 or higher. Featuresmith uses Polars and Pandas
          under the hood, which are installed automatically.
        </p>
      </section>

      {/* Quick start */}
      <section className="mb-10" aria-labelledby="quick-start">
        <h2 id="quick-start" className="mb-3 text-xl font-semibold text-foreground">
          Quick Start
        </h2>
        <p className="mb-4 text-sm leading-relaxed text-muted-foreground">
          Run your first dataset review using the pre-packaged <code>titanic.csv</code> dataset:
        </p>
        <CodeBlock code={QUICKSTART_CODE} language="python" filename="quickstart.py" showCopy />
      </section>

      {/* Quick links grid */}
      <section aria-labelledby="next-steps">
        <h2 id="next-steps" className="mb-4 text-xl font-semibold text-foreground">
          Explore the docs
        </h2>
        <div className="grid gap-3 sm:grid-cols-2">
          {QUICK_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="group flex flex-col rounded-lg border border-border bg-card p-4 transition-all duration-150 hover:border-primary/30 hover:bg-accent"
            >
              <span className="mb-1 text-sm font-medium text-foreground">{link.title}</span>
              <span className="mb-3 text-xs leading-relaxed text-muted-foreground">
                {link.description}
              </span>
              <span className="mt-auto flex items-center gap-1 text-xs font-medium text-primary transition-all group-hover:gap-2">
                Read more
                <ArrowRight className="h-3 w-3" aria-hidden />
              </span>
            </Link>
          ))}
        </div>
      </section>

      {/* Prev / Next navigation */}
      <nav
        className="mt-16 flex items-center justify-end border-t border-border pt-6"
        aria-label="Document navigation"
      >
        <Link
          href="/docs/installation"
          className="flex items-center gap-2 rounded-md border border-border px-4 py-2 text-sm text-muted-foreground transition-colors hover:border-primary/30 hover:text-foreground"
        >
          Installation
          <ChevronRight className="h-4 w-4" aria-hidden />
        </Link>
      </nav>
    </article>
  )
}
