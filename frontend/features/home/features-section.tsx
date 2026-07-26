"use client"

import { motion } from "framer-motion"
import { Database, BarChart2, ShieldCheck, Terminal, Sparkles, Puzzle } from "lucide-react"
import { Section, SectionHeader, SectionLabel } from "@/components/ui/section"
import { Container } from "@/components/ui/container"
import { FEATURES } from "@/lib/constants"
import type { Feature } from "@/types"

const ICON_MAP: Record<string, React.ElementType> = {
  Database,
  BarChart2,
  ShieldCheck,
  Terminal,
  Sparkles,
  Puzzle,
}

function FeatureCard({ feature, index }: { feature: Feature; index: number }) {
  const Icon = ICON_MAP[feature.icon] ?? Database

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.4, delay: index * 0.05 }}
      className="group rounded-xl border border-border bg-card p-6 transition-all duration-200 hover:border-primary/30 hover:shadow-sm"
    >
      <div className="mb-4 inline-flex h-9 w-9 items-center justify-center rounded-lg bg-primary/8 text-primary ring-1 ring-primary/15">
        <Icon className="h-4 w-4" aria-hidden />
      </div>
      <h3 className="mb-2 text-sm font-semibold text-foreground">{feature.title}</h3>
      <p className="text-sm leading-relaxed text-muted-foreground">{feature.description}</p>
    </motion.div>
  )
}

export function FeaturesSection() {
  return (
    <Section id="features" className="border-t border-border bg-muted/20">
      <Container>
        <SectionHeader centered>
          <SectionLabel>Features</SectionLabel>
          <h2 className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            Everything you need to trust your data
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-balance text-base leading-relaxed text-muted-foreground">
            From raw files to validated feature sets, Featuresmith gives you the
            primitives to build reliable data pipelines.
          </p>
        </SectionHeader>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((feature, i) => (
            <FeatureCard key={feature.title} feature={feature} index={i} />
          ))}
        </div>
      </Container>
    </Section>
  )
}
