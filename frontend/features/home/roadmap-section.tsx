"use client"

import { motion } from "framer-motion"
import { CheckCircle2, Circle, Clock, Sparkles } from "lucide-react"
import { Section, SectionHeader, SectionLabel } from "@/components/ui/section"
import { Container } from "@/components/ui/container"
import { ROADMAP } from "@/lib/constants"
import type { RoadmapItem } from "@/types"
import { cn } from "@/lib/utils"

const STATUS_CONFIG = {
  done: {
    icon: CheckCircle2,
    label: "Complete",
    dot: "bg-emerald-500",
    line: "bg-emerald-500/30",
    badge: "border-emerald-500/20 bg-emerald-500/8 text-emerald-600 dark:text-emerald-400",
  },
  "in-progress": {
    icon: Clock,
    label: "In Progress",
    dot: "bg-primary animate-pulse",
    line: "bg-primary/30",
    badge: "border-primary/20 bg-primary/8 text-primary",
  },
  planned: {
    icon: Circle,
    label: "Planned",
    dot: "bg-zinc-400 dark:bg-zinc-600",
    line: "bg-border",
    badge: "border-border bg-muted text-muted-foreground",
  },
  future: {
    icon: Sparkles,
    label: "Future",
    dot: "bg-zinc-300 dark:bg-zinc-700",
    line: "bg-border/50",
    badge: "border-border/50 bg-muted/50 text-muted-foreground/70",
  },
}

function RoadmapCard({ item, index, isLast }: { item: RoadmapItem; index: number; isLast: boolean }) {
  const config = STATUS_CONFIG[item.status]
  const Icon = config.icon

  return (
    <motion.div
      initial={{ opacity: 0, x: -12 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.4, delay: index * 0.08 }}
      className="relative flex gap-6 pb-8"
    >
      {/* Timeline track */}
      <div className="flex flex-col items-center">
        <div
          className={cn(
            "relative z-10 mt-1 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full border bg-background",
            item.status === "done"
              ? "border-emerald-500/30"
              : item.status === "in-progress"
              ? "border-primary/30"
              : "border-border"
          )}
        >
          <Icon
            className={cn(
              "h-3.5 w-3.5",
              item.status === "done"
                ? "text-emerald-500"
                : item.status === "in-progress"
                ? "text-primary"
                : "text-muted-foreground"
            )}
            aria-hidden
          />
        </div>
        {!isLast && (
          <div className={cn("mt-1 w-px flex-1", config.line)} />
        )}
      </div>

      {/* Content */}
      <div className="min-w-0 flex-1 pt-0.5 pb-2">
        <div className="mb-3 flex flex-wrap items-center gap-2">
          <span className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            {item.phase}
          </span>
          <span
            className={cn(
              "rounded-full border px-2 py-0.5 text-[10px] font-medium",
              config.badge
            )}
          >
            {config.label}
          </span>
        </div>
        <h3 className="mb-3 text-base font-semibold text-foreground">{item.title}</h3>
        <ul className="space-y-1.5" role="list">
          {item.items.map((feat) => (
            <li key={feat} className="flex items-start gap-2 text-sm text-muted-foreground">
              <span
                className={cn(
                  "mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full",
                  item.status === "done"
                    ? "bg-emerald-500"
                    : item.status === "in-progress"
                    ? "bg-primary"
                    : "bg-muted-foreground/40"
                )}
                aria-hidden
              />
              {feat}
            </li>
          ))}
        </ul>
      </div>
    </motion.div>
  )
}

export function RoadmapSection() {
  return (
    <Section id="roadmap" className="border-t border-border bg-muted/20">
      <Container size="md">
        <SectionHeader>
          <SectionLabel>Roadmap</SectionLabel>
          <h2 className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            Where we are. Where we{"'"}re going.
          </h2>
          <p className="mt-4 max-w-xl text-balance text-base leading-relaxed text-muted-foreground">
            Featuresmith is actively developed. The roadmap is public and
            contributions are welcome at every phase.
          </p>
        </SectionHeader>

        <div className="md:ml-8">
          {ROADMAP.map((item, i) => (
            <RoadmapCard
              key={item.phase}
              item={item}
              index={i}
              isLast={i === ROADMAP.length - 1}
            />
          ))}
        </div>
      </Container>
    </Section>
  )
}
