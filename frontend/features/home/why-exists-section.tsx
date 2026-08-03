"use client"

import { motion } from "framer-motion"
import { ShieldCheck, BarChart3, Wrench, AlertTriangle, Eye, Sparkles } from "lucide-react"
import { Section, SectionHeader, SectionLabel } from "@/components/ui/section"
import { Container } from "@/components/ui/container"

const FAILURE_MODES = [
  {
    icon: AlertTriangle,
    title: "Hidden Target Leakage",
    description: "Future timestamps, target correlations, or duplicate ID columns silently artificially inflate validation scores but crash in production.",
  },
  {
    icon: Eye,
    title: "Silent Schema Drift",
    description: "Unannounced column type changes, null spikes, or unexpected categorical distributions breaking downstream feature pipelines.",
  },
  {
    icon: ShieldCheck,
    title: "Missing Values & Outliers",
    description: "Unchecked null ratios and extreme anomalous values degrading model weights and inference accuracy without throwing runtime errors.",
  },
  {
    icon: BarChart3,
    title: "Dataset Regressions",
    description: "Quality drops between snapshot versions (v1 vs v2) going completely unnoticed before expensive model re-training runs.",
  },
  {
    icon: Wrench,
    title: "Bad Pre-training Assumptions",
    description: "Training complex neural nets or tree models on datasets plagued by constant zero-variance columns or high-cardinality noise.",
  },
]

export function WhyExistsSection() {
  return (
    <Section id="why-exists" className="border-t border-border bg-card">
      <Container size="md">
        <SectionHeader centered>
          <SectionLabel>The Problem</SectionLabel>
          <h2 className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            Engineering discipline stops at the dataset's edge.
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-balance text-base leading-relaxed text-muted-foreground">
            Every serious codebase has linters, formatters, static analyzers, and CI/CD tests. But machine learning datasets—which are just as load-bearing as software code—get almost none of it.
          </p>
        </SectionHeader>

        {/* 5 Failure modes grid */}
        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {FAILURE_MODES.map((mode, i) => (
            <motion.div
              key={mode.title}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: i * 0.06 }}
              className="rounded-xl border border-border bg-background p-6 transition-all duration-200 hover:border-primary/20"
            >
              <div className="mb-4 inline-flex h-9 w-9 items-center justify-center rounded-lg bg-red-500/10 text-red-500 ring-1 ring-red-500/20">
                <mode.icon className="h-4 w-4" />
              </div>
              <h3 className="mb-2 font-semibold text-foreground text-sm">{mode.title}</h3>
              <p className="text-xs leading-relaxed text-muted-foreground">{mode.description}</p>
            </motion.div>
          ))}

          {/* Solution card */}
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4, delay: 0.3 }}
            className="rounded-xl border border-primary/30 bg-primary/5 p-6 transition-all duration-200"
          >
            <div className="mb-4 inline-flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary ring-1 ring-primary/20">
              <Sparkles className="h-4 w-4" />
            </div>
            <h3 className="mb-2 font-semibold text-foreground text-sm">Featuresmith Solution</h3>
            <p className="text-xs leading-relaxed text-muted-foreground">
              Automated pre-training dataset code reviews, 0–100 ML readiness scorecards, and CI/CD gate checks to catch failures before they cost compute.
            </p>
          </motion.div>
        </div>
      </Container>
    </Section>
  )
}
