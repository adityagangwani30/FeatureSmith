"use client"

import { motion } from "framer-motion"
import { Cpu, FlaskConical, GitPullRequest, ShieldCheck, GraduationCap } from "lucide-react"
import { Section, SectionHeader, SectionLabel } from "@/components/ui/section"
import { Container } from "@/components/ui/container"

const PERSONAS = [
  {
    icon: Cpu,
    role: "ML Engineers",
    benefit: "Stop target leakage and silent schema breaks before spending GPU hours on model training.",
  },
  {
    icon: FlaskConical,
    role: "Data Scientists",
    benefit: "Audit raw data instantly and receive an explainable 0–100 ML readiness scorecard with actionable tips.",
  },
  {
    icon: GitPullRequest,
    role: "Data Engineers",
    benefit: "Prevent corrupted data drops from silently reaching feature stores and training pipelines.",
  },
  {
    icon: ShieldCheck,
    role: "MLOps Engineers",
    benefit: "Gate CI/CD pipelines with deterministic CLI exit codes and machine-readable JSON reports.",
  },
  {
    icon: GraduationCap,
    role: "Students & Learners",
    benefit: "Learn production data quality best practices with transparent rationale and remediation guidance.",
  },
]

export function PersonasSection() {
  return (
    <Section id="personas" className="border-t border-border bg-muted/20">
      <Container size="md">
        <SectionHeader centered>
          <SectionLabel>Who it's for</SectionLabel>
          <h2 className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            Built for the entire ML team
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-balance text-base leading-relaxed text-muted-foreground">
            Whether you are building pipelines, training models, or managing MLOps, Featuresmith streamlines dataset quality checks.
          </p>
        </SectionHeader>

        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {PERSONAS.map((p, i) => (
            <motion.div
              key={p.role}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: i * 0.06 }}
              className="rounded-xl border border-border bg-card p-6 transition-all hover:border-primary/20"
            >
              <div className="mb-4 inline-flex h-9 w-9 items-center justify-center rounded-lg bg-primary/8 text-primary ring-1 ring-primary/15">
                <p.icon className="h-4 w-4" />
              </div>
              <h3 className="mb-2 text-sm font-semibold text-foreground">{p.role}</h3>
              <p className="text-xs leading-relaxed text-muted-foreground">{p.benefit}</p>
            </motion.div>
          ))}
        </div>
      </Container>
    </Section>
  )
}
