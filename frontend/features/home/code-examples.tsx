"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { Section, SectionHeader, SectionLabel } from "@/components/ui/section"
import { Container } from "@/components/ui/container"
import { CodeBlock } from "@/components/ui/code-block"
import { PYTHON_EXAMPLE_CODE, CLI_EXAMPLE_CODE } from "@/lib/constants"
import { cn } from "@/lib/utils"

const TABS = [
  { id: "python", label: "Python SDK", filename: "example.py" },
  { id: "cli", label: "CLI", filename: "terminal" },
] as const

type TabId = (typeof TABS)[number]["id"]

export function CodeExamples() {
  const [active, setActive] = useState<TabId>("python")

  return (
    <Section id="code-examples" className="border-t border-border bg-muted/20">
      <Container size="md">
        <SectionHeader centered>
          <SectionLabel>Code Examples</SectionLabel>
          <h2 className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            Intuitive by design
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-balance text-base leading-relaxed text-muted-foreground">
            Featuresmith{"'"}s API is designed to feel natural whether you{"'"}re
            scripting from the terminal or integrating into a Python codebase.
          </p>
        </SectionHeader>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-50px" }}
          transition={{ duration: 0.4 }}
        >
          {/* Tab switcher */}
          <div className="mb-4 flex items-center gap-1 rounded-lg border border-border bg-muted/50 p-1 w-fit">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActive(tab.id)}
                className={cn(
                  "rounded-md px-4 py-1.5 text-sm font-medium transition-all duration-150",
                  active === tab.id
                    ? "bg-background text-foreground shadow-sm"
                    : "text-muted-foreground hover:text-foreground"
                )}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Code block */}
          {active === "python" ? (
            <CodeBlock
              code={PYTHON_EXAMPLE_CODE}
              language="python"
              filename="example.py"
            />
          ) : (
            <CodeBlock
              code={CLI_EXAMPLE_CODE}
              language="bash"
              filename="terminal"
            />
          )}
        </motion.div>

        {/* Install hint */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="mt-6 flex items-center gap-3 rounded-lg border border-border bg-card px-4 py-3"
        >
          <span className="text-xs text-muted-foreground">Install via pip:</span>
          <code className="font-mono text-sm text-foreground">pip install featuresmith-core</code>
          <span className="ml-auto rounded bg-muted px-2 py-0.5 font-mono text-[10px] text-muted-foreground">
            latest: 0.1.0
          </span>
        </motion.div>
      </Container>
    </Section>
  )
}
