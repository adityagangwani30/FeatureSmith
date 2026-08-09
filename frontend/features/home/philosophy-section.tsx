"use client"

import { motion } from "framer-motion"
import { Terminal, ShieldAlert, Sparkles, Home, Puzzle, Eye, CheckCircle } from "lucide-react"
import { Section, SectionHeader, SectionLabel } from "@/components/ui/section"
import { Container } from "@/components/ui/container"

const PRINCIPLES = [
  {
    icon: Terminal,
    title: "Developer-first",
    body: "Every capability ships as something a developer can call, script, or pipe — first as a Python import, then a CLI command — before it becomes a UI.",
  },
  {
    icon: ShieldAlert,
    title: "Engineering over dashboards",
    body: "Featuresmith is shaped like a check that runs automatically in CI next to your other gates, not a dashboard report you open once and forget.",
  },
  {
    icon: Sparkles,
    title: "AI assists, never replaces",
    body: "The deterministic engine works fully with the AI layer switched off. AI narrates and ranks computed facts, but never computes a number itself.",
  },
  {
    icon: Home,
    title: "Local-first, cloud-optional",
    body: "Full value with zero network calls using local files and models. Cloud LLMs and connectors are strictly opt-in via configuration.",
  },
  {
    icon: Puzzle,
    title: "Composable by default",
    body: "Connectors, rules, exporters, and AI providers are simple plugins behind small, stable interfaces. Core code remains untouched.",
  },
  {
    icon: Eye,
    title: "Evidence before recommendations",
    body: "Every recommendation shows the underlying calculated statistic before any narrative or suggested action. Nothing is auto-applied without approval.",
  },
  {
    icon: CheckCircle,
    title: "Trust over hype",
    body: "We ship what exists and label what doesn't. Every roadmap phase is clearly marked, and documentation is written to check against actual code.",
  },
]

export function PhilosophySection() {
  return (
    <Section id="philosophy">
      <Container>
        <SectionHeader>
          <SectionLabel>Philosophy</SectionLabel>
          <h2 className="max-w-xl text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            Principles that guide every decision
          </h2>
        </SectionHeader>

        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {PRINCIPLES.map(({ icon: Icon, title, body }, i) => (
            <motion.div
              key={title}
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.4, delay: i * 0.08 }}
            >
              <div className="mb-4 inline-flex h-8 w-8 items-center justify-center rounded-md border border-border bg-muted text-muted-foreground">
                <Icon className="h-4 w-4" aria-hidden />
              </div>
              <h3 className="mb-2 text-sm font-semibold text-foreground">{title}</h3>
              <p className="text-sm leading-relaxed text-muted-foreground">{body}</p>
            </motion.div>
          ))}
        </div>

        {/* Permanent Boundaries */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.3 }}
          className="mt-14 rounded-xl border border-border bg-muted/30 p-6 md:p-8"
        >
          <span className="text-xs font-semibold uppercase tracking-widest text-primary">Permanent Boundaries</span>
          <h3 className="text-lg font-semibold text-foreground mt-1 mb-3">What Featuresmith Will Intentionally NOT Become</h3>
          <p className="text-sm text-muted-foreground mb-6 leading-relaxed">
            Featuresmith owns the loop of understanding, planning, validating, and proving dataset state — and deliberately stops at the edge of executing transformations or orchestrating jobs.
          </p>
          <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3 text-xs text-muted-foreground">
            <div className="rounded-lg border border-border bg-background p-4">
              <span className="font-semibold text-foreground block mb-1">Not an Orchestrator</span>
              We leave DAG scheduling and retries to Airflow, Dagster, and Prefect.
            </div>
            <div className="rounded-lg border border-border bg-background p-4">
              <span className="font-semibold text-foreground block mb-1">Not an Execution Engine</span>
              No proprietary runtime. Recommendations compile to real Polars, pandas, and scikit-learn code.
            </div>
            <div className="rounded-lg border border-border bg-background p-4">
              <span className="font-semibold text-foreground block mb-1">Not a Feature Store</span>
              Featuresmith certifies data state, exporting to existing feature stores for online serving.
            </div>
            <div className="rounded-lg border border-border bg-background p-4">
              <span className="font-semibold text-foreground block mb-1">Not an AutoML / Training System</span>
              Recommendations focus purely on dataset health and readiness, never hyperparameter tuning.
            </div>
            <div className="rounded-lg border border-border bg-background p-4">
              <span className="font-semibold text-foreground block mb-1">Not a No-Code Platform</span>
              Developer-first design: importable, scriptable, and pipeable before any UI surface.
            </div>
            <div className="rounded-lg border border-border bg-background p-4">
              <span className="font-semibold text-foreground block mb-1">Not a Replacement for Judgment</span>
              All plans and recommendations are advisory — reviewable and editable before human approval.
            </div>
          </div>
        </motion.div>
      </Container>
    </Section>
  )
}
