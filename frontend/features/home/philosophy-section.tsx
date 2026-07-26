"use client"

import { motion } from "framer-motion"
import { Layers, Wrench, Blocks } from "lucide-react"
import { Section, SectionHeader, SectionLabel } from "@/components/ui/section"
import { Container } from "@/components/ui/container"

const PRINCIPLES = [
  {
    icon: Layers,
    title: "Correctness over convenience",
    body: "Data quality decisions should be explicit, not implicit. Featuresmith never silently coerces values or swallows errors. Every operation returns a result you can inspect, log, and act on.",
  },
  {
    icon: Wrench,
    title: "The right defaults, the right escape hatches",
    body: "Sensible defaults get you to insights in seconds. But every default is overridable. Validators, loaders, reporters, and thresholds are all configurable — nothing is locked behind an abstraction you can't reach.",
  },
  {
    icon: Blocks,
    title: "Core-first architecture",
    body: "All business logic resides in Featuresmith Core. The Python SDK, CLI, Dashboard, and any future extensions are thin wrappers over this unified engine. Zero duplicated logic, identical findings across every surface.",
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

        <div className="grid gap-8 md:grid-cols-3">
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
      </Container>
    </Section>
  )
}
