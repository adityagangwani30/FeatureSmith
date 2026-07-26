"use client"

import { motion } from "framer-motion"
import { Section, SectionHeader, SectionLabel } from "@/components/ui/section"
import { Container } from "@/components/ui/container"
import { ARCHITECTURE_NODES } from "@/lib/constants"
import type { ArchitectureNode } from "@/types"
import { cn } from "@/lib/utils"

function ArchNode({ node, index }: { node: ArchitectureNode; index: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.35, delay: index * 0.07 }}
      className="flex flex-col items-center"
    >
      {/* Node box */}
      <div
        className={cn(
          "relative w-full max-w-sm rounded-lg border px-6 py-4 text-center transition-all duration-200",
          node.future
            ? "border-dashed border-border/60 bg-muted/30 opacity-70"
            : "border-border bg-card shadow-sm hover:border-primary/30 hover:shadow-md"
        )}
      >
        {node.future && (
          <span className="absolute -top-2.5 left-1/2 -translate-x-1/2 rounded-full border border-border bg-background px-2 py-0.5 text-[10px] font-medium uppercase tracking-widest text-muted-foreground">
            Planned
          </span>
        )}
        <p
          className={cn(
            "text-sm font-semibold",
            node.future ? "text-muted-foreground" : "text-foreground"
          )}
        >
          {node.label}
        </p>
        <p className="mt-1 text-xs leading-relaxed text-muted-foreground">{node.sublabel}</p>
      </div>

      {/* Connector arrow (not shown for last node) */}
      {index < ARCHITECTURE_NODES.length - 1 && (
        <div className="flex flex-col items-center">
          <div
            className={cn(
              "h-6 w-px",
              ARCHITECTURE_NODES[index + 1].future ? "border-l border-dashed border-border/50" : "bg-border"
            )}
          />
          <svg
            className={cn(
              "h-3 w-3",
              ARCHITECTURE_NODES[index + 1].future ? "text-border/50" : "text-border"
            )}
            viewBox="0 0 12 12"
            fill="currentColor"
            aria-hidden
          >
            <path d="M6 12L0 0h12L6 12z" />
          </svg>
        </div>
      )}
    </motion.div>
  )
}

export function ArchitectureSection() {
  return (
    <Section id="architecture">
      <Container size="md">
        <SectionHeader centered>
          <SectionLabel>Architecture</SectionLabel>
          <h2 className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            A clean, composable pipeline
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-balance text-base leading-relaxed text-muted-foreground">
            Featuresmith is designed as a layered pipeline. Each stage builds on
            the last, giving you clear extension points as your needs grow.
          </p>
        </SectionHeader>

        <div className="mx-auto flex max-w-sm flex-col items-center">
          {ARCHITECTURE_NODES.map((node, i) => (
            <ArchNode key={node.id} node={node} index={i} />
          ))}
        </div>

        {/* Legend */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.5 }}
          className="mt-10 flex items-center justify-center gap-6 text-xs text-muted-foreground"
        >
          <span className="flex items-center gap-1.5">
            <span className="h-px w-6 bg-border" />
            Available
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-px w-6 border-t border-dashed border-border/60" />
            Planned
          </span>
        </motion.div>
      </Container>
    </Section>
  )
}
