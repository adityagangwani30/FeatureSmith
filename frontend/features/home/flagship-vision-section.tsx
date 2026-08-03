"use client"

import { motion } from "framer-motion"
import { Sparkles, FileDiff, ShieldAlert, CheckSquare } from "lucide-react"
import { Section, SectionHeader, SectionLabel } from "@/components/ui/section"
import { Container } from "@/components/ui/container"
import { Badge } from "@/components/ui/badge"

const VISION_CARDS = [
  {
    icon: CheckSquare,
    title: "Dataset Review",
    cmd: "featuresmith review  ✅ v0.2.0",
    description: "Automate code reviews for your datasets before model training. 8 automated reviewers inspect schema, missingness, duplicates, data types, constants, cardinality, basic statistics, and target leakage.",
  },
  {
    icon: Sparkles,
    title: "ML Readiness Score",
    cmd: "8 Health Dimensions  ✅ v0.2.0",
    description: "Know whether your dataset is actually ready for machine learning. Deterministic 0–100 score computed across 8 health dimensions with per-dimension breakdowns and fix suggestions.",
  },
  {
    icon: ShieldAlert,
    title: "Intelligent Leakage Detection",
    cmd: "6 Pattern Detectors  ✅ v0.2.0",
    description: "Prevent target leakage and future information from corrupting validation scores. 6 pattern detectors merge column findings across correlation, identifier, timestamp, and duplicate targets.",
  },
  {
    icon: FileDiff,
    title: "Dataset Diff Engine",
    cmd: "featuresmith diff  ✅ v0.2.0",
    description: "Understand exactly what changed between two dataset snapshot versions. Standalone engine compares schema, missingness, distribution shifts, and overall dataset health verdicts.",
  },
]

export function FlagshipVisionSection() {
  return (
    <Section id="flagship-vision" className="border-t border-border bg-muted/20 relative">
      <Container size="md">
        <SectionHeader centered>
          <div className="flex justify-center mb-3">
            <Badge variant="outline" className="border-dashed border-primary/40 text-primary font-medium text-xs">
              v0.2.0 &mdash; Flagship Capabilities
            </Badge>
          </div>
          <h2 className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            Flagship Capabilities
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-balance text-base leading-relaxed text-muted-foreground">
            Built for production ML engineering workflows. Featuresmith brings dataset review, readiness scoring, leakage detection, and snapshot diffing to your terminal and Python code.
          </p>
        </SectionHeader>

        <div className="mt-12 grid gap-6 sm:grid-cols-2">
          {VISION_CARDS.map((card, i) => (
            <motion.div
              key={card.title}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: i * 0.08 }}
              className="group relative rounded-xl border border-dashed border-border bg-background p-6 transition-all duration-200 hover:border-primary/30"
            >
              <div className="absolute right-4 top-4 text-[10px] font-mono text-zinc-500 bg-zinc-900 border border-zinc-800 rounded px-1.5 py-0.5">
                {card.cmd}
              </div>
              <div className="mb-4 inline-flex h-9 w-9 items-center justify-center rounded-lg bg-primary/8 text-primary ring-1 ring-primary/15">
                <card.icon className="h-4 w-4" aria-hidden />
              </div>
              <h3 className="mb-2 text-sm font-semibold text-foreground flex items-center gap-1.5">
                {card.title}
              </h3>
              <p className="text-sm leading-relaxed text-muted-foreground">{card.description}</p>
            </motion.div>
          ))}
        </div>
      </Container>
    </Section>
  )
}
