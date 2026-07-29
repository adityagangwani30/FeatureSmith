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
    cmd: "featuresmith review <dataset>",
    description: "A single command for a comprehensive engineering review of a dataset — checking missingness, leakage, balance, and quality in one pass.",
  },
  {
    icon: ShieldAlert,
    title: "Intelligent Leakage Detection",
    cmd: "Pattern-based discovery",
    description: "Going beyond basic thresholds to recognize target leakage shapes like label derivation, time-based leakage, or identifier leakage.",
  },
  {
    icon: FileDiff,
    title: "Dataset Diffing",
    cmd: "featuresmith diff <v1> <v2>",
    description: "Compare two versions of a dataset side-by-side. Spot added/removed columns, schema shifts, and distribution drift before training.",
  },
  {
    icon: Sparkles,
    title: "ML Readiness Score",
    cmd: "Composite quality scorecard",
    description: "A single, multi-dimensional metric (e.g. ML Readiness: 91/100) detailing dataset health across schema, quality, and leakage dimensions.",
  },
]

export function FlagshipVisionSection() {
  return (
    <Section id="flagship-vision" className="border-t border-border bg-muted/20 relative">
      <Container size="md">
        <SectionHeader centered>
          <div className="flex justify-center mb-3">
            <Badge variant="outline" className="border-dashed border-primary/40 text-primary font-medium text-xs">
              Future Roadmap
            </Badge>
          </div>
          <h2 className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            The Flagship Vision
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-balance text-base leading-relaxed text-muted-foreground">
            Featuresmith aims to become the standard engineering toolkit for the structured data lifecycle.
            These define the future destination we are building toward.
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
