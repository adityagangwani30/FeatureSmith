import type { Metadata } from "next"
import Link from "next/link"
import { CheckCircle2 } from "lucide-react"
import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"
import { Container } from "@/components/ui/container"

export const metadata: Metadata = { title: "v0.1.0 Release", description: "Featuresmith v0.1.0 release scope and supported surfaces." }

const READY = ["CSV, Parquet, Excel, pandas, and Polars inputs", "Deterministic profiling with numeric, categorical, text, datetime, and correlation summaries", "Eight built-in data quality and target leakage rules", "Python SDK: load(), profile(), and analyze()", "CLI analysis with table and JSON output plus CI exit codes"]
const LATER = ["AI narration and interactive chat", "Plugin entry points and external provider integrations", "Dashboard, report generation, and database connectors"]

export default function ReleasePage() {
  return <><Navbar /><main className="min-h-screen bg-background pb-24 pt-28"><Container size="md"><header className="border-b border-border pb-8"><p className="text-sm font-semibold text-primary">Release</p><h1 className="mt-2 text-3xl font-semibold text-foreground sm:text-4xl">Featuresmith v0.1.0</h1><p className="mt-3 max-w-2xl text-sm leading-relaxed text-muted-foreground">A focused initial release for deterministic tabular-data profiling and validation in Python.</p></header><section className="mt-10"><h2 className="text-xl font-semibold text-foreground">Included in this release</h2><ul className="mt-5 space-y-3 text-sm text-muted-foreground">{READY.map((item) => <li key={item} className="flex gap-2"><CheckCircle2 className="mt-0.5 h-4 w-4 flex-none text-primary" />{item}</li>)}</ul></section><section className="mt-10 border-t border-border pt-8"><h2 className="text-xl font-semibold text-foreground">Planned for future releases</h2><ul className="mt-4 space-y-2 text-sm text-muted-foreground">{LATER.map((item) => <li key={item}>- {item}</li>)}</ul></section><div className="mt-10"><Link href="/docs/quickstart" className="text-sm font-semibold text-primary hover:underline">Start with the quick start guide</Link></div></Container></main><Footer /></>
}
