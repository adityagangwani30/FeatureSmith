"use client"

import Link from "next/link"
import { motion } from "framer-motion"
import { ArrowRight, Star, Package, Scale, Code2 } from "lucide-react"

function GithubIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M12 2C6.477 2 2 6.484 2 12.021c0 4.428 2.865 8.184 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0 1 12 6.844a9.59 9.59 0 0 1 2.504.337c1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482C19.138 20.2 22 16.447 22 12.021 22 6.484 17.522 2 12 2z" />
    </svg>
  )
}
import { Badge } from "@/components/ui/badge"
import { Container } from "@/components/ui/container"
import { AnimatedLogo } from "@/components/brand"

const TERMINAL_LINES = [
  { text: "$ featuresmith review examples/data/processed/titanic.csv --target survived", type: "command" },
  { text: "", type: "blank" },
  { text: "  Featuresmith Dataset Review (v0.3.0)", type: "output" },
  { text: "  Rows: 891 | Columns: 12 | Engine: v0.3.0", type: "dim" },
  { text: "", type: "blank" },
  { text: "  [CRITICAL] Missing Values in column 'cabin' (77.1% missing)", type: "output" },
  { text: "  [WARNING] High Skewness in column 'fare' (skewness 4.78)", type: "output" },
  { text: "  [INFO] Identifier column 'passengerid' detected", type: "output" },
  { text: "  [PASSED] Leakage Detection: No target leakage found", type: "success" },
  { text: "", type: "blank" },
  { text: "  ML Readiness Score: 86.9 / 100", type: "success" },
  { text: "  Summary: 5 of 8 dimensions healthy; 3 with findings", type: "dim" },
  { text: "  ────────────────────────────────────────", type: "dim" },
]

const typeColors: Record<string, string> = {
  command: "text-zinc-200 font-semibold",
  output: "text-amber-400",
  success: "text-emerald-400 font-medium",
  dim: "text-zinc-500",
  blank: "text-transparent",
}

const STATS = [
  { icon: Scale, label: "License", value: "Apache 2.0" },
  { icon: Star, label: "Unit Tests", value: "311 Passing" },
  { icon: Code2, label: "Type Safety", value: "Strict MyPy" },
  { icon: Package, label: "Linter", value: "Ruff & Import Linter" },
]

const fadeUp = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
}

export function Hero() {
  return (
    <section
      className="relative flex min-h-screen flex-col items-center justify-center pb-16 pt-24"
      aria-label="Hero"
    >
      {/* Subtle grid background */}
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage:
            "linear-gradient(to right, currentColor 1px, transparent 1px), linear-gradient(to bottom, currentColor 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        }}
        aria-hidden
      />

      <Container size="md">
        <div className="flex flex-col items-center text-center">
          {/* Hero Brand Icon */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, ease: "easeOut" }}
            className="mb-8 text-primary"
          >
            <AnimatedLogo size={80} showWordmark={false} />
          </motion.div>

          {/* Top badge */}
          <motion.div
            {...fadeUp}
            transition={{ duration: 0.4 }}
            className="mb-6"
          >
            <Badge variant="outline" className="gap-1.5 px-3 py-1 text-xs">
              <span className="inline-block h-1.5 w-1.5 rounded-full bg-primary" aria-hidden />
              v0.3.0 &mdash; Diff-Aware Dataset Review
            </Badge>
          </motion.div>

          {/* Headline */}
          <motion.h1
            {...fadeUp}
            transition={{ duration: 0.4, delay: 0.06 }}
            className="text-balance text-4xl font-semibold tracking-tight text-foreground sm:text-5xl md:text-6xl lg:text-[64px]"
          >
            Every dataset deserves
            <br className="hidden sm:block" />
            a code review.
          </motion.h1>

          {/* Subheading */}
          <motion.p
            {...fadeUp}
            transition={{ duration: 0.4, delay: 0.12 }}
            className="mt-5 max-w-2xl text-balance text-base leading-relaxed text-muted-foreground sm:text-lg"
          >
            Most ML failures originate from dataset quality, not model architecture.
            Featuresmith is an open-source Dataset Review Platform that brings automated code reviews, ML readiness scores, target leakage detection, and version diffing to tabular data.
          </motion.p>

          {/* CTAs */}
          <motion.div
            {...fadeUp}
            transition={{ duration: 0.4, delay: 0.18 }}
            className="mt-8 flex flex-wrap items-center justify-center gap-3"
          >
            <Link
              href="/docs"
              className="inline-flex items-center gap-2 rounded-md bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground transition-all hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              Get Started
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
            <Link
              href="https://github.com/adityagangwani30/FeatureSmith"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-md border border-border bg-transparent px-5 py-2.5 text-sm font-medium text-foreground transition-all hover:bg-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <GithubIcon className="h-4 w-4" />
              View on GitHub
              <span className="rounded bg-muted px-1.5 py-0.5 text-xs text-muted-foreground">
                v0.3.0
              </span>
            </Link>
          </motion.div>

          {/* Stats row */}
          <motion.div
            {...fadeUp}
            transition={{ duration: 0.4, delay: 0.24 }}
            className="mt-10 flex flex-wrap items-center justify-center gap-6"
          >
            {STATS.map(({ icon: Icon, label, value }) => (
              <div key={label} className="flex items-center gap-1.5 text-sm text-muted-foreground">
                <Icon className="h-3.5 w-3.5" aria-hidden />
                <span className="font-medium text-foreground">{value}</span>
                <span>{label}</span>
              </div>
            ))}
          </motion.div>

          {/* Terminal window */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.32 }}
            className="mt-14 w-full max-w-2xl overflow-hidden rounded-xl border border-zinc-800 bg-zinc-950 shadow-2xl shadow-black/30"
          >
            {/* Terminal header */}
            <div className="flex items-center gap-2 border-b border-zinc-800 bg-zinc-900 px-4 py-3">
              <span className="h-3 w-3 rounded-full bg-red-500/70" aria-hidden />
              <span className="h-3 w-3 rounded-full bg-yellow-500/70" aria-hidden />
              <span className="h-3 w-3 rounded-full bg-green-500/70" aria-hidden />
              <span className="ml-3 font-mono text-xs text-zinc-500">featuresmith review</span>
            </div>

            {/* Terminal body */}
            <div className="p-5 text-left">
              <div className="font-mono text-[13px] leading-6">
                {TERMINAL_LINES.map((line, i) => (
                  <div key={i} className={typeColors[line.type]}>
                    {line.text || "\u00A0"}
                  </div>
                ))}
                <div className="flex items-center gap-1 text-zinc-400">
                  <span>$</span>
                  <span className="inline-block h-4 w-2 animate-pulse bg-zinc-400" />
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </Container>
    </section>
  )
}
