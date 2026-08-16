import type { Metadata } from "next"
import Link from "next/link"
import { CheckCircle2, ArrowRight } from "lucide-react"
import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"
import { Container } from "@/components/ui/container"

export const metadata: Metadata = {
  title: "v0.3.0 Release",
  description: "Featuresmith v0.3.0 release scope — Diff-Aware Dataset Review, Dataset Review Engine, ML Readiness Score, Intelligent Leakage Detection, and Dataset Diff.",
}

const READY = [
  "Diff-Aware Dataset Review: fs.review(source, previous=...) and featuresmith review --previous compare a dataset against a prior snapshot inside the review itself",
  "Dataset Review Engine: 9 automated reviewers evaluating schema, missingness, duplicates, distributions, target leakage, and snapshot deltas",
  "ML Readiness Score: Explainable 0–100 composite scorecard across 8 health dimensions with fix suggestions",
  "Intelligent Leakage Detection: 6 pattern detectors (target correlation, identifier shape, timestamp anomalies, duplicate targets)",
  "Dataset Diff Engine: Snapshot comparisons via fs.diff() and featuresmith diff command for schema, nulls, and health deltas",
  "Supported Data Sources: CSV, Parquet, Excel, pandas, and Polars DataFrames",
  "Python SDK: Public entry points for load(), profile(), analyze(), review(), diff(), and score()",
  "CLI Interface: featuresmith analyze, review, and diff commands with Rich table, JSON output, and exit-code CI gating",
]

const FUTURE_ROADMAP = [
  "Phase 4 (v0.3+): Interactive Streamlit dashboard, GitHub Action (featuresmith-action), and dynamic plugin discovery",
  "Phase 5 (v0.4): Recommendation Engine and inspectable Plan transformation primitive",
  "Phase 6 (v0.5): Dataset Contracts, code-generator Apply layer (sklearn/Polars), validation re-review, and featuresmith.lock",
  "Phase 7 (v0.6–v1.0): Portable certification badges (featuresmith verify) and scheduled quality observability",
  "Phase 8 (v1.x): AI-Assisted Planning, natural-language Plan authoring, and narrative summaries",
  "Phase 9 (v2.0+): Ecosystem exporters (dbt/Feast/MLflow/W&B), VS Code extension, and distributed compute",
]

export default function ReleasePage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-background pb-24 pt-28">
        <Container size="md">
          <header className="border-b border-border pb-8">
            <p className="text-sm font-semibold text-primary">Release Announcement</p>
            <h1 className="mt-2 text-3xl font-semibold text-foreground sm:text-4xl">
              Featuresmith v0.3.0 &mdash; Diff-Aware Dataset Review
            </h1>
            <p className="mt-3 max-w-2xl text-sm leading-relaxed text-muted-foreground">
              v0.3.0 is officially shipped. This release adds the DiffReviewer, which brings snapshot comparison directly into the review pipeline: pass a previous snapshot to <code>fs.review(source, previous=...)</code> or <code>featuresmith review --previous</code> and the review reports exactly what changed between dataset versions.
            </p>
          </header>

          <section className="mt-10">
            <h2 className="text-xl font-semibold text-foreground">What Featuresmith can do today (v0.3.0)</h2>
            <ul className="mt-5 space-y-3.5 text-sm text-muted-foreground">
              {READY.map((item) => (
                <li key={item} className="flex gap-2.5">
                  <CheckCircle2 className="mt-0.5 h-4 w-4 flex-none text-emerald-400" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </section>

          <section className="mt-12 border-t border-border pt-8">
            <h2 className="text-xl font-semibold text-foreground">Where Featuresmith is going (Future Roadmap)</h2>
            <p className="mt-2 text-sm text-muted-foreground">
              These future capabilities reflect our documented roadmap toward Dataset Contracts and state management:
            </p>
            <ul className="mt-4 space-y-2.5 text-sm text-muted-foreground">
              {FUTURE_ROADMAP.map((item) => (
                <li key={item} className="flex gap-2">
                  <span className="text-primary font-bold">•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </section>

          <div className="mt-10 flex flex-wrap gap-4 border-t border-border pt-8">
            <Link
              href="/docs/quickstart"
              className="inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:opacity-90 transition-opacity"
            >
              Get Started with v0.3.0
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              href="/roadmap"
              className="inline-flex items-center gap-2 rounded-md border border-border bg-transparent px-4 py-2 text-sm font-semibold text-foreground hover:bg-accent transition-colors"
            >
              Explore Full Product Roadmap
            </Link>
          </div>
        </Container>
      </main>
      <Footer />
    </>
  )
}
