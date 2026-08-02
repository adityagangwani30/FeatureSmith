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
    cmd: "featuresmith review <dataset>  ✅ v0.2.0",
    description: "8/11 review sections implemented (schema, missingness, duplicates, types, constants, cardinality, basic stats, leakage). ML Readiness Score attached. Missing: recommendations, duplicate columns, outliers, distribution, feature quality.",
  },
  {
    icon: ShieldAlert,
    title: "Intelligent Leakage Detection",
    cmd: "6 pattern detectors  ✅ v0.2.0",
    description: "Target correlation, identifier shape, timestamp, future info, duplicate target, suspicious correlation — all implemented with merged per-column findings and scoring integration.",
  },
  {
    icon: FileDiff,
    title: "Dataset Diffing",
    cmd: "featuresmith diff <v1> <v2>  ✅ v0.2.0",
    description: "Standalone engine: schema, structure, quality, distribution, and leakage deltas with overall health verdict (regressed/improved/unchanged). Not integrated as Review Engine reviewer.",
  },
  {
    icon: Sparkles,
    title: "ML Readiness Score",
    cmd: "8 dimensions  ✅ v0.2.0",
    description: "Schema Health, Missing Values, Duplicate Records, Data Types, Constant Columns, High Cardinality, Dataset Structure, Leakage Risk. Per-dimension breakdown. Missing: Class Balance, Feature Quality, Distribution Health.",
  },
]

export function FlagshipVisionSection() {
  return (
    <Section id="flagship-vision" className="border-t border-border bg-muted/20 relative">
      <Container size="md">
        <SectionHeader centered>
          <div className="flex justify-center mb-3">
            <Badge variant="outline" className="border-dashed border-primary/40 text-primary font-medium text-xs">
              v0.2.0 — Partially Delivered
            </Badge>
          </div>
          <h2 className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            The Flagship Vision
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-balance text-base leading-relaxed text-muted-foreground">
            Featuresmith aims to become the standard engineering toolkit for the structured data lifecycle.
            In v0.2.0, Dataset Review, ML Readiness Score, Dataset Diff, and Intelligent Leakage Detection
            are partially delivered — see each card for implementation status.
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
