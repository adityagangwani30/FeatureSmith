import type { Metadata } from "next"
import Link from "next/link"
import { ArrowRight, CheckCircle2, Clock } from "lucide-react"
import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"
import { Container } from "@/components/ui/container"
import { ROADMAP } from "@/lib/constants"
import { Badge } from "@/components/ui/badge"

export const metadata: Metadata = {
  title: "Roadmap",
  description: "Featuresmith release roadmap and planned capabilities.",
}

export default function RoadmapPage() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-background pb-24 pt-28">
        <Container size="md">
          <header className="border-b border-border pb-8">
            <p className="text-sm font-semibold text-primary">Product Direction</p>
            <h1 className="mt-2 text-3xl font-semibold text-foreground sm:text-4xl">
              Featuresmith Roadmap
            </h1>
            <p className="mt-3 max-w-2xl text-sm leading-relaxed text-muted-foreground">
              Phases 0–3 are shipped in <strong>v0.3.0 (current)</strong>. Everything from Phase 4 onward represents our planned long-term vision toward Dataset Contracts and state management.
            </p>
          </header>

          <div className="mt-10 space-y-10">
            {ROADMAP.map((phase) => {
              const isShipped = phase.status === "done"
              return (
                <section
                  key={phase.phase}
                  className={`border-l-2 pl-5 transition-colors ${
                    isShipped ? "border-emerald-500" : "border-border"
                  }`}
                >
                  <div className="flex flex-wrap items-center gap-3">
                    <p className="text-xs font-semibold uppercase tracking-widest text-primary">
                      {phase.phase}
                    </p>
                    <Badge
                      variant="outline"
                      className={`text-[10px] uppercase font-mono ${
                        isShipped
                          ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-400"
                          : "border-border bg-muted text-muted-foreground"
                      }`}
                    >
                      {isShipped ? (
                        <span className="flex items-center gap-1">
                          <CheckCircle2 className="h-3 w-3" /> Shipped
                        </span>
                      ) : (
                        <span className="flex items-center gap-1">
                          <Clock className="h-3 w-3" /> Planned
                        </span>
                      )}
                    </Badge>
                  </div>
                  <h2 className="mt-2 text-xl font-semibold text-foreground">
                    {phase.title}
                  </h2>
                  <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
                    {phase.items.map((item) => (
                      <li key={item} className="flex items-start gap-2">
                        <span
                          className={`mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full ${
                            isShipped ? "bg-emerald-500" : "bg-muted-foreground/40"
                          }`}
                        />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </section>
              )
            })}
          </div>

          <div className="mt-12 border-t border-border pt-7">
            <Link
              href="/release"
              className="inline-flex items-center gap-2 text-sm font-semibold text-primary hover:underline"
            >
              View v0.3.0 shipped release details
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </Container>
      </main>
      <Footer />
    </>
  )
}
