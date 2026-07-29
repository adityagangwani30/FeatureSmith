"use client"

import { motion } from "framer-motion"
import { Target, Compass } from "lucide-react"
import { Section, SectionHeader, SectionLabel } from "@/components/ui/section"
import { Container } from "@/components/ui/container"

const HIGHLIGHTS = [
  {
    icon: Target,
    title: "Developer-First Alignment",
    description: "Built for engineers who treat data quality as an automated test gate, not a post-hoc analysis task.",
  },
  {
    icon: Compass,
    title: "One Unified Core",
    description: "The SDK, CLI, and dashboard all invoke the exact same engine. No duplication, no fragmented tools.",
  },
]

export function MissionSection() {
  return (
    <Section id="mission" className="relative overflow-hidden border-t border-border bg-gradient-to-b from-background via-muted/5 to-background">
      <Container size="md">
        <div className="flex flex-col items-center text-center">
          <SectionHeader centered>
            <SectionLabel>Mission</SectionLabel>
            <motion.h2
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4 }}
              className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl md:text-5xl"
            >
              Make data quality as routine as code quality.
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: 0.08 }}
              className="mx-auto mt-6 max-w-2xl text-balance text-base leading-relaxed text-muted-foreground sm:text-lg"
            >
              Every serious codebase today has Git, pull requests, tests, CI/CD, and static analysis. Datasets, which are just as load-bearing for ML systems as the surrounding code, get almost none of it. We are building the tools to change that.
            </motion.p>
          </SectionHeader>

          <div className="mt-12 grid gap-6 sm:grid-cols-2 w-full">
            {HIGHLIGHTS.map((item, i) => (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: i * 0.1 }}
                className="group rounded-xl border border-border bg-card p-6 text-left transition-all duration-200 hover:border-primary/20"
              >
                <div className="mb-4 inline-flex h-9 w-9 items-center justify-center rounded-lg bg-primary/8 text-primary ring-1 ring-primary/15">
                  <item.icon className="h-4 w-4" aria-hidden />
                </div>
                <h3 className="mb-2 text-sm font-semibold text-foreground">{item.title}</h3>
                <p className="text-sm leading-relaxed text-muted-foreground">{item.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </Container>
    </Section>
  )
}
