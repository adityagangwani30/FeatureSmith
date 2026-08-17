"use client"

import { motion } from "framer-motion"
import { ArrowRight, CheckCircle2, Database, FileDiff, ShieldAlert, Sparkles, ListChecks, ClipboardList } from "lucide-react"
import { Section, SectionHeader, SectionLabel } from "@/components/ui/section"
import { Container } from "@/components/ui/container"

const WORKFLOW_STEPS = [
  {
    step: "01",
    icon: Database,
    title: "Raw Dataset",
    subtitle: "CSV, Parquet, Excel, pandas/Polars",
    description: "Load tabular data into a normalized contract with zero data transformations.",
  },
  {
    step: "02",
    icon: CheckCircle2,
    title: "Dataset Review",
    subtitle: "fs.review() / featuresmith review",
    description: "10 automated reviewers evaluate schema, data types, missingness, duplicates, cardinality, feature quality, and snapshot deltas.",
  },
  {
    step: "03",
    icon: Sparkles,
    title: "ML Readiness Score",
    subtitle: "Explainable 0–100 Scorecard",
    description: "Get a clear 0-100 score across 7 effective health dimensions with actionable fix suggestions.",
  },
  {
    step: "04",
    icon: ShieldAlert,
    title: "Leakage Detection",
    subtitle: "6 Named Pattern Detectors",
    description: "Catch target correlations, timestamp anomalies, and identifier shapes before training.",
  },
  {
    step: "05",
    icon: FileDiff,
    title: "Dataset Diff",
    subtitle: "fs.diff() Snapshot Comparison",
    description: "Compare dataset versions to ensure schema, missingness, and health didn't regress.",
  },
  {
    step: "06",
    icon: ListChecks,
    title: "Recommendations",
    subtitle: "Ranked, Explainable Fixes",
    description: "The Recommendation Engine merges findings into a ranked list with confidence and traceability.",
  },
  {
    step: "07",
    icon: ClipboardList,
    title: "Plan",
    subtitle: "fs.plan() / featuresmith plan",
    description: "Compile accepted recommendations into an inspectable, deterministic Plan of transformation steps.",
  },
]

export function WorkflowSection() {
  return (
    <Section id="workflow" className="border-t border-border bg-muted/10 relative">
      <Container size="md">
        <SectionHeader centered>
          <SectionLabel>Product Workflow</SectionLabel>
          <h2 className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            From Raw Data to Confident Training
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-balance text-base leading-relaxed text-muted-foreground">
            Understand how Featuresmith's flagship capabilities work together in a single continuous developer loop.
          </p>
        </SectionHeader>

        {/* Horizontal / Grid workflow steps */}
        <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {WORKFLOW_STEPS.map((s, i) => (
            <motion.div
              key={s.step}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: i * 0.08 }}
              className="relative flex flex-col justify-between rounded-xl border border-border bg-background p-5 shadow-sm transition-all hover:border-primary/30"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="font-mono text-xs font-semibold text-primary">{s.step}</span>
                  <s.icon className="h-4 w-4 text-muted-foreground" />
                </div>
                <h3 className="font-semibold text-foreground text-sm mb-0.5">{s.title}</h3>
                <p className="text-[11px] font-mono text-primary/80 mb-2">{s.subtitle}</p>
                <p className="text-xs text-muted-foreground leading-relaxed">{s.description}</p>
              </div>

              {i < WORKFLOW_STEPS.length - 1 && (
                <div className="hidden lg:block absolute -right-3 top-1/2 -translate-y-1/2 z-10 text-muted-foreground/40">
                  <ArrowRight className="h-4 w-4" />
                </div>
              )}
            </motion.div>
          ))}
        </div>
      </Container>
    </Section>
  )
}
