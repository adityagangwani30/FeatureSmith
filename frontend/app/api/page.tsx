import type { Metadata } from "next"
import Link from "next/link"
import { Code2 } from "lucide-react"
import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"
import { Container } from "@/components/ui/container"
import { CodeBlock } from "@/components/ui/code-block"

export const metadata: Metadata = { title: "API Reference", description: "Featuresmith public Python API reference." }

export default function ApiPage() {
  return <><Navbar /><main className="min-h-screen bg-background pb-24 pt-28"><Container size="md"><header className="border-b border-border pb-8"><div className="flex items-center gap-3"><Code2 className="h-5 w-5 text-primary" /><p className="text-sm font-semibold text-primary">Python API</p></div><h1 className="mt-3 text-3xl font-semibold text-foreground sm:text-4xl">A small, explicit public surface</h1><p className="mt-3 max-w-2xl text-sm leading-relaxed text-muted-foreground">v0.1.0 exposes three stable entry points for loading tabular data, computing profiles, and running deterministic rules.</p></header><section className="mt-10 space-y-7"><div><h2 className="text-xl font-semibold text-foreground">load(source)</h2><p className="mt-2 text-sm text-muted-foreground">Normalizes CSV, Parquet, Excel, pandas, or Polars input into a Dataset.</p></div><div><h2 className="text-xl font-semibold text-foreground">profile(source, ...)</h2><p className="mt-2 text-sm text-muted-foreground">Returns typed descriptive statistics, missingness, duplicates, and correlations.</p></div><div><h2 className="text-xl font-semibold text-foreground">analyze(source, ...)</h2><p className="mt-2 text-sm text-muted-foreground">Profiles data and runs the built-in quality and leakage rules in one call.</p></div></section><CodeBlock code={'import featuresmith as fs\n\nresult = fs.analyze("customers.csv", target_column="churn")\nfor finding in result.findings:\n    print(finding.title)'} language="python" filename="audit.py" showCopy /><div className="mt-8 flex gap-5 text-sm font-semibold text-primary"><Link href="/docs/sdk/load">SDK reference</Link><Link href="/docs/quickstart">Quick start</Link></div></Container></main><Footer /></>
}
