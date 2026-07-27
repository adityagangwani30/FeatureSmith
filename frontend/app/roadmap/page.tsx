import type { Metadata } from "next"
import Link from "next/link"
import { ArrowRight } from "lucide-react"
import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"
import { Container } from "@/components/ui/container"
import { ROADMAP } from "@/lib/constants"

export const metadata: Metadata = { title: "Roadmap", description: "Featuresmith release roadmap and planned capabilities." }

export default function RoadmapPage() {
  return <><Navbar /><main className="min-h-screen bg-background pb-24 pt-28"><Container size="md"><header className="border-b border-border pb-8"><p className="text-sm font-semibold text-primary">Product direction</p><h1 className="mt-2 text-3xl font-semibold text-foreground sm:text-4xl">Featuresmith roadmap</h1><p className="mt-3 max-w-2xl text-sm leading-relaxed text-muted-foreground">The core profiling, validation, CLI, and Python SDK are ready for v0.1.0. Later phases are intentionally marked as planned rather than presented as current capability.</p></header><div className="mt-10 space-y-10">{ROADMAP.map((phase) => <section key={phase.phase} className="border-l-2 border-border pl-5"><div className="flex flex-wrap items-baseline gap-3"><p className="text-xs font-semibold uppercase tracking-widest text-primary">{phase.phase}</p><p className="text-xs text-muted-foreground">{phase.status.replace("-", " ")}</p></div><h2 className="mt-2 text-xl font-semibold text-foreground">{phase.title}</h2><ul className="mt-4 space-y-2 text-sm text-muted-foreground">{phase.items.map((item) => <li key={item}>- {item}</li>)}</ul></section>)}</div><div className="mt-12 border-t border-border pt-7"><Link href="/release" className="inline-flex items-center gap-2 text-sm font-semibold text-primary">View v0.1.0 release status<ArrowRight className="h-4 w-4" /></Link></div></Container></main><Footer /></>
}
