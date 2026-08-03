"use client"

import { motion } from "framer-motion"
import { Scale, CheckCircle2, ShieldCheck, Zap } from "lucide-react"
import { Section, SectionHeader, SectionLabel } from "@/components/ui/section"
import { Container } from "@/components/ui/container"

const COMPARISONS = [
  {
    tool: "pandas / Polars",
    heading: "Raw manipulation vs. Automated Dataset Reviews",
    description:
      "pandas and Polars provide low-level dataframe operations. Featuresmith builds automated dataset reviews, 0–100 ML readiness scorecards, quality rules, and leakage detection on top of them.",
  },
  {
    tool: "ydata-profiling",
    heading: "Exploratory HTML reports vs. CI/CD Gate Engine",
    description:
      "ydata-profiling generates heavy HTML reports for manual EDA. Featuresmith is a lightweight, ultra-fast CLI & Python SDK built for automated dataset code reviews and exit-code CI/CD gates.",
  },
  {
    tool: "Great Expectations",
    heading: "Pipeline assertions vs. ML Dataset Readiness",
    description:
      "Great Expectations manages complex pipeline assertions. Featuresmith is a zero-config, developer-first toolkit purpose-built for ML dataset readiness, leakage detection, and version diffing.",
  },
]

export function PositioningSection() {
  return (
    <Section id="positioning" className="border-t border-border bg-background">
      <Container size="md">
        <SectionHeader centered>
          <SectionLabel>Positioning</SectionLabel>
          <h2 className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            Why Featuresmith?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-balance text-base leading-relaxed text-muted-foreground">
            Think of Featuresmith as the equivalent of <strong>Ruff</strong> or <strong>ESLint</strong> for tabular datasets.
          </p>
        </SectionHeader>

        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {COMPARISONS.map((c, i) => (
            <motion.div
              key={c.tool}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: i * 0.08 }}
              className="rounded-xl border border-border bg-card p-6 transition-all hover:border-primary/20"
            >
              <div className="mb-3 inline-flex items-center gap-1.5 rounded-md bg-muted px-2.5 py-1 text-xs font-mono font-medium text-foreground">
                <Scale className="h-3.5 w-3.5 text-primary" />
                vs. {c.tool}
              </div>
              <h3 className="mb-2 text-sm font-semibold text-foreground leading-snug">{c.heading}</h3>
              <p className="text-xs leading-relaxed text-muted-foreground">{c.description}</p>
            </motion.div>
          ))}
        </div>
      </Container>
    </Section>
  )
}
