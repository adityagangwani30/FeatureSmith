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
    cmd: "featuresmith review  ✅ v0.3.0",
    description: "Automate code reviews for your datasets before model training. 9 automated reviewers inspect schema, missingness, duplicates, data types, constants, cardinality, basic statistics, target leakage, and snapshot deltas.",
  },
  {
    icon: Sparkles,
    title: "ML Readiness Score",
    cmd: "8 Health Dimensions  ✅ v0.3.0",
    description: "Know whether your dataset is actually ready for machine learning. Deterministic 0–100 score computed across 8 health dimensions with per-dimension breakdowns and fix suggestions.",
  },
  {
    icon: ShieldAlert,
    title: "Intelligent Leakage Detection",
    cmd: "6 Pattern Detectors  ✅ v0.3.0",
    description: "Prevent target leakage and future information from corrupting validation scores. 6 pattern detectors merge column findings across correlation, identifier, timestamp, and duplicate targets.",
  },
  {
    icon: FileDiff,
    title: "Dataset Diff Engine",
    cmd: "featuresmith diff  ✅ v0.3.0",
    description: "Understand exactly what changed between two dataset snapshot versions. Compare via fs.diff() or inline in a review with fs.review(source, previous=...) and featuresmith review --previous.",
  },
]

export function FlagshipVisionSection() {
  return (
    <Section id="flagship-vision" className="border-t border-border bg-muted/20 relative">
      <Container size="md">
        <SectionHeader centered>
          <div className="flex justify-center mb-3">
            <Badge variant="outline" className="border-dashed border-primary/40 text-primary font-medium text-xs">
              v0.3.0 &mdash; Flagship Capabilities
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
              <div className="absolute right-4 top-4 text-[10px] font-mono text-emerald-400 bg-emerald-950/40 border border-emerald-800/60 rounded px-1.5 py-0.5">
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

        {/* Long-Term Vision & Progression */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="mt-16 rounded-xl border border-border bg-card p-6 md:p-8"
        >
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-border pb-4 mb-6">
            <div>
              <span className="text-xs font-semibold uppercase tracking-widest text-primary">Long-Term Vision</span>
              <h3 className="text-lg font-semibold text-foreground mt-1">The Dataset Contract Lifecycle</h3>
            </div>
            <Badge variant="outline" className="text-xs text-muted-foreground border-border">
              Planned Progression (Phases 5–6)
            </Badge>
          </div>

          <p className="text-sm text-muted-foreground mb-6 leading-relaxed">
            Featuresmith is evolving toward complete Dataset State Management. While v0.3.0 ships the deterministic <strong>Review Engine</strong>, <strong>Dataset Diff</strong>, and <strong>Diff-Aware Review</strong>, the long-term architecture completes a continuous engineering loop:
          </p>

          <div className="grid gap-3 sm:grid-cols-2 md:grid-cols-4 font-mono text-xs">
            {[
              { step: "1. Review", desc: "Audit quality & leakage", status: "v0.3.0 Shipped" },
              { step: "2. Recommend", desc: "Ranked fix suggestions", status: "Phase 5 Planned" },
              { step: "3. Plan", desc: "Inspectable change set", status: "Phase 5 Planned" },
              { step: "4. Apply", desc: "Generate sklearn/Polars code", status: "Phase 6 Planned" },
              { step: "5. Review Again", desc: "Verify fix outcome", status: "Phase 6 Planned" },
              { step: "6. Diff", desc: "Compare snapshot deltas", status: "v0.3.0 Shipped" },
              { step: "7. Document", desc: "Record transformation log", status: "Phase 6 Planned" },
              { step: "8. Lock / Contract", desc: "Write featuresmith.lock", status: "Phase 6 Planned" },
            ].map((s) => (
              <div key={s.step} className="rounded-md border border-border/80 bg-background/60 p-3 flex flex-col justify-between">
                <div>
                  <span className="font-semibold text-foreground text-xs">{s.step}</span>
                  <p className="text-[11px] font-sans text-muted-foreground mt-1">{s.desc}</p>
                </div>
                <span className={`mt-3 text-[10px] px-1.5 py-0.5 rounded w-fit ${s.status.includes("Shipped") ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" : "bg-muted text-muted-foreground"}`}>
                  {s.status}
                </span>
              </div>
            ))}
          </div>

          <p className="mt-6 text-xs text-muted-foreground italic border-t border-border/50 pt-4">
            Note: Featuresmith generates code for existing libraries (Polars, pandas, scikit-learn, dbt) and will never introduce a proprietary execution engine or custom transformation runtime.
          </p>
        </motion.div>
      </Container>
    </Section>
  )
}
