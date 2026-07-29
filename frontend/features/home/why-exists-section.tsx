"use client"

import { motion } from "framer-motion"
import { ShieldCheck, BarChart3, Wrench, AlertTriangle, Eye, Sparkles } from "lucide-react"
import { Section, SectionHeader, SectionLabel } from "@/components/ui/section"
import { Container } from "@/components/ui/container"

const STEPS = [
  {
    icon: BarChart3,
    title: "1. Understand",
    description: "Profile dataset shapes, column distributions, and pairwise relationships deterministically.",
  },
  {
    icon: ShieldCheck,
    title: "2. Validate",
    description: "Catch critical data-quality regressions and target leakage issues with testable rules.",
  },
  {
    icon: Wrench,
    title: "3. Improve",
    description: "Turn accepted findings into clean, reviewable preprocessing pipelines (sklearn / notebooks).",
  },
]

export function WhyExistsSection() {
  return (
    <Section id="why-exists" className="border-t border-border bg-card">
      <Container size="md">
        <SectionHeader centered>
          <SectionLabel>Why Featuresmith?</SectionLabel>
          <h2 className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            One Toolkit, One Loop
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-balance text-base leading-relaxed text-muted-foreground">
            Data understanding, validation, and improvement should not be five disconnected tools.
            Featuresmith integrates them into a single engineering workflow.
          </p>
        </SectionHeader>

        {/* The Loop Diagram/Cards */}
        <div className="mt-12 grid gap-6 sm:grid-cols-3">
          {STEPS.map((step, i) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: i * 0.08 }}
              className="relative rounded-xl border border-border bg-background p-6 text-center transition-all duration-200 hover:border-primary/20"
            >
              <div className="mx-auto mb-4 flex h-10 w-10 items-center justify-center rounded-full bg-primary/8 text-primary">
                <step.icon className="h-5 w-5" />
              </div>
              <h3 className="mb-2 font-semibold text-foreground text-sm">{step.title}</h3>
              <p className="text-xs leading-relaxed text-muted-foreground">{step.description}</p>
            </motion.div>
          ))}
        </div>

        {/* Detailed context sections */}
        <div className="mt-16 grid gap-8 md:grid-cols-2">
          <motion.div
            initial={{ opacity: 0, x: -16 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.45 }}
            className="flex gap-4"
          >
            <div className="mt-1 flex-shrink-0 text-primary">
              <Eye className="h-5 w-5" />
            </div>
            <div>
              <h3 className="font-semibold text-sm text-foreground mb-1">Developer-First CI Integration</h3>
              <p className="text-sm leading-relaxed text-muted-foreground">
                Featuresmith is built to be run automatically. Just like <code>ruff</code> or <code>pytest</code>,
                it runs as a gate in your CI/CD pipeline, failing the build on critical quality issues before they reach models.
              </p>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 16 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.45 }}
            className="flex gap-4"
          >
            <div className="mt-1 flex-shrink-0 text-primary">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <h3 className="font-semibold text-sm text-foreground mb-1">AI as an Assistant, Not Identity</h3>
              <p className="text-sm leading-relaxed text-muted-foreground">
                The deterministic engine works with the AI layer completely switched off.
                When active, AI only receives precomputed statistical profiles (never raw dataset rows) to narrate findings.
              </p>
            </div>
          </motion.div>
        </div>
      </Container>
    </Section>
  )
}
