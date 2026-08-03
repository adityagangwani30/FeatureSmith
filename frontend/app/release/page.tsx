import type { Metadata } from "next"
import Link from "next/link"
import { CheckCircle2 } from "lucide-react"
import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"
import { Container } from "@/components/ui/container"

export const metadata: Metadata = { title: "v0.2.0 Release", description: "Featuresmith v0.2.0 release scope and supported surfaces." }

const READY = [
  "CSV, Parquet, Excel, pandas, and Polars inputs",
  "Deterministic profiling with numeric, categorical, text, datetime, and correlation summaries",
  "Review Engine with 8 built-in reviewers (schema, quality, and leakage)",
  "ML Readiness Score with 8 deterministic dimensions and scorecard rendering",
  "Dataset Diff via fs.diff() and featuresmith diff command for snapshot comparisons",
  "Intelligent Leakage Detection with 6 pattern detectors (correlation, timestamp, duplicate target, etc.)",
  "Python SDK: load(), profile(), analyze(), review(), diff(), and score()",
  "CLI analysis, review, and diff commands with table/JSON output and CI exit codes"
]
const LATER = [
  "Interactive Dashboard (featuresmith-dashboard) and HTML report exports",
  "Config-driven weight overrides via .featuresmith.yml",
  "AI narration and interactive chat integrations (Phase 6+)",
  "Extensible dynamic plugin discovery (Phase 3)"
]

export default function ReleasePage() {
  return <><Navbar /><main className="min-h-screen bg-background pb-24 pt-28"><Container size="md"><header className="border-b border-border pb-8"><p className="text-sm font-semibold text-primary">Release</p><h1 className="mt-2 text-3xl font-semibold text-foreground sm:text-4xl">Featuresmith v0.2.0</h1><p className="mt-3 max-w-2xl text-sm leading-relaxed text-muted-foreground">A major feature release introducing the Review Engine, Dataset Diff, ML Readiness Score, and Leakage Detection.</p></header><section className="mt-10"><h2 className="text-xl font-semibold text-foreground">Included in this release</h2><ul className="mt-5 space-y-3 text-sm text-muted-foreground">{READY.map((item) => <li key={item} className="flex gap-2"><CheckCircle2 className="mt-0.5 h-4 w-4 flex-none text-primary" />{item}</li>)}</ul></section><section className="mt-10 border-t border-border pt-8"><h2 className="text-xl font-semibold text-foreground">Planned for future releases</h2><ul className="mt-4 space-y-2 text-sm text-muted-foreground">{LATER.map((item) => <li key={item}>- {item}</li>)}</ul></section><div className="mt-10"><Link href="/docs/quickstart" className="text-sm font-semibold text-primary hover:underline">Start with the quick start guide</Link></div></Container></main><Footer /></>
}
