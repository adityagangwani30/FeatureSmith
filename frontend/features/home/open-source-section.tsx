"use client"

import Link from "next/link"
import { motion } from "framer-motion"
import { GitFork, Heart, Scale, BookOpen, Terminal } from "lucide-react"
import { Section } from "@/components/ui/section"
import { Container } from "@/components/ui/container"

function GithubIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M12 2C6.477 2 2 6.484 2 12.021c0 4.428 2.865 8.184 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0 1 12 6.844a9.59 9.59 0 0 1 2.504.337c1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482C19.138 20.2 22 16.447 22 12.021 22 6.484 17.522 2 12 2z" />
    </svg>
  )
}

const STATS = [
  { Icon: Scale, label: "License", value: "Apache 2.0" },
  { Icon: GitFork, label: "Development", value: "Active" },
  { Icon: Heart, label: "Contribution", value: "Open Source" },
]

export function OpenSourceSection() {
  return (
    <Section id="open-source">
      <Container size="md">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-50px" }}
          transition={{ duration: 0.45 }}
          className="relative overflow-hidden rounded-2xl border border-border bg-card px-8 py-12 text-center md:px-16"
        >
          {/* Decorative corner dots */}
          <span className="absolute left-4 top-4 h-1.5 w-1.5 rounded-full bg-border" aria-hidden />
          <span className="absolute right-4 top-4 h-1.5 w-1.5 rounded-full bg-border" aria-hidden />
          <span className="absolute bottom-4 left-4 h-1.5 w-1.5 rounded-full bg-border" aria-hidden />
          <span className="absolute bottom-4 right-4 h-1.5 w-1.5 rounded-full bg-border" aria-hidden />

          <p className="mb-3 text-xs font-semibold uppercase tracking-widest text-primary">
            Open Source
          </p>
          <h2 className="mb-4 text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            Built in the open.
            <br className="hidden sm:block" />
            For everyone.
          </h2>
          <p className="mx-auto mb-8 max-w-lg text-balance text-base leading-relaxed text-muted-foreground">
            Featuresmith is Apache 2.0-licensed and developed entirely in public. Every
            design decision, API change, and roadmap item is visible on GitHub.
            We believe the best tools are built with the community, not for it.
          </p>

          {/* Stats */}
          <div className="mb-10 flex flex-wrap items-center justify-center gap-8 border-b border-border/60 pb-8">
            {STATS.map(({ Icon, label, value }) => (
              <div key={label} className="flex flex-col items-center gap-1">
                <div className="flex items-center gap-1.5 text-muted-foreground">
                  <Icon className="h-3.5 w-3.5" />
                  <span className="text-xs">{label}</span>
                </div>
                <span className="text-xl font-semibold text-foreground">{value}</span>
              </div>
            ))}
          </div>

          {/* 3 Call-To-Action Cards */}
          <div className="grid gap-4 sm:grid-cols-3 text-left">
            <div className="rounded-lg border border-border bg-background p-4 flex flex-col justify-between">
              <div>
                <div className="mb-2 inline-flex h-7 w-7 items-center justify-center rounded bg-primary/8 text-primary">
                  <Terminal className="h-4 w-4" />
                </div>
                <h3 className="text-xs font-bold text-foreground uppercase tracking-wider mb-1">1. Install</h3>
                <p className="text-xs text-muted-foreground mb-3 leading-relaxed">Add Featuresmith SDK and CLI to your environment.</p>
              </div>
              <code className="block bg-muted px-2 py-1 rounded text-[10px] font-mono text-foreground select-all text-center">
                pip install featuresmith-core
              </code>
            </div>

            <div className="rounded-lg border border-border bg-background p-4 flex flex-col justify-between">
              <div>
                <div className="mb-2 inline-flex h-7 w-7 items-center justify-center rounded bg-primary/8 text-primary">
                  <BookOpen className="h-4 w-4" />
                </div>
                <h3 className="text-xs font-bold text-foreground uppercase tracking-wider mb-1">2. Read Docs</h3>
                <p className="text-xs text-muted-foreground mb-3 leading-relaxed">Dive into installation guides, CLI details, and SDK references.</p>
              </div>
              <Link
                href="/docs"
                className="block text-center text-xs font-medium bg-primary text-primary-foreground py-1 rounded transition-opacity hover:opacity-90"
              >
                Go to Documentation
              </Link>
            </div>

            <div className="rounded-lg border border-border bg-background p-4 flex flex-col justify-between">
              <div>
                <div className="mb-2 inline-flex h-7 w-7 items-center justify-center rounded bg-primary/8 text-primary">
                  <Heart className="h-4 w-4" />
                </div>
                <h3 className="text-xs font-bold text-foreground uppercase tracking-wider mb-1">3. Contribute</h3>
                <p className="text-xs text-muted-foreground mb-3 leading-relaxed">Add custom rules or connectors. View guidelines on GitHub.</p>
              </div>
              <Link
                href="https://github.com/adityagangwani30/FeatureSmith/blob/main/CONTRIBUTING.md"
                target="_blank"
                rel="noopener noreferrer"
                className="block text-center text-xs font-medium border border-border text-foreground py-1 rounded hover:bg-accent transition-colors"
              >
                View Contributor Guide
              </Link>
            </div>
          </div>
        </motion.div>
      </Container>
    </Section>
  )
}
