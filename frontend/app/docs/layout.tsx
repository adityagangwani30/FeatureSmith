"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { useState } from "react"
import { ChevronRight, Menu, X, Search } from "lucide-react"
import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { DOC_SECTIONS } from "@/lib/constants"
import { cn } from "@/lib/utils"

// ─── Sidebar ─────────────────────────────────────────────────────────────────

function DocsSidebar({ className }: { className?: string }) {
  const pathname = usePathname()

  return (
    <aside className={cn("w-64 flex-shrink-0", className)} aria-label="Documentation navigation">
      {/* Search */}
      <div className="mb-4">
        <button
          className="flex w-full items-center gap-2 rounded-md border border-border bg-muted/50 px-3 py-2 text-sm text-muted-foreground transition-colors hover:bg-accent"
          aria-label="Search documentation"
        >
          <Search className="h-3.5 w-3.5" aria-hidden />
          <span className="flex-1 text-left">Search docs...</span>
          <kbd className="hidden rounded border border-border bg-background px-1.5 py-0.5 font-mono text-[10px] sm:inline-flex">
            ⌘K
          </kbd>
        </button>
      </div>

      {/* Nav sections */}
      <nav>
        {DOC_SECTIONS.map((section) => (
          <div key={section.href} className="mb-6">
            <p className="mb-1.5 px-2 text-[11px] font-semibold uppercase tracking-widest text-muted-foreground">
              {section.title}
            </p>
            {section.items && (
              <ul role="list" className="space-y-0.5">
                {section.items.map((item) => {
                  const isActive = pathname === item.href
                  return (
                    <li key={item.href}>
                      <Link
                        href={item.href}
                        className={cn(
                          "flex items-center rounded-md px-2 py-1.5 text-sm transition-colors",
                          isActive
                            ? "bg-primary/8 font-medium text-primary"
                            : "text-muted-foreground hover:bg-accent hover:text-foreground"
                        )}
                        aria-current={isActive ? "page" : undefined}
                      >
                        {item.title}
                      </Link>
                    </li>
                  )
                })}
              </ul>
            )}
          </div>
        ))}
      </nav>
    </aside>
  )
}

// ─── Table of Contents ────────────────────────────────────────────────────────

const PLACEHOLDER_TOC = [
  { id: "introduction", label: "Introduction", level: 1 },
  { id: "installation", label: "Installation", level: 1 },
  { id: "quick-start", label: "Quick Start", level: 1 },
  { id: "loading-data", label: "Loading Data", level: 2 },
  { id: "profiling", label: "Profiling", level: 2 },
  { id: "validation", label: "Validation", level: 2 },
  { id: "next-steps", label: "Next Steps", level: 1 },
]

function TableOfContents() {
  return (
    <aside className="hidden w-48 flex-shrink-0 xl:block" aria-label="Table of contents">
      <div className="sticky top-20">
        <p className="mb-3 text-[11px] font-semibold uppercase tracking-widest text-muted-foreground">
          On this page
        </p>
        <nav>
          <ul role="list" className="space-y-1">
            {PLACEHOLDER_TOC.map((item) => (
              <li key={item.id}>
                <a
                  href={`#${item.id}`}
                  className={cn(
                    "block rounded text-xs text-muted-foreground transition-colors hover:text-foreground",
                    item.level === 2 ? "py-1 pl-3" : "py-1"
                  )}
                >
                  {item.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </aside>
  )
}

// ─── Layout ───────────────────────────────────────────────────────────────────

export default function DocsLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <>
      <Navbar />

      <div className="min-h-screen">
        {/* Mobile sidebar overlay */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm md:hidden"
            onClick={() => setSidebarOpen(false)}
            aria-hidden
          />
        )}

        {/* Mobile sidebar drawer */}
        <div
          className={cn(
            "fixed inset-y-0 left-0 z-50 w-72 overflow-y-auto border-r border-border bg-background p-6 transition-transform duration-200 md:hidden",
            sidebarOpen ? "translate-x-0" : "-translate-x-full"
          )}
          role="dialog"
          aria-modal="true"
          aria-label="Documentation navigation"
        >
          <div className="mb-6 flex items-center justify-between">
            <span className="text-sm font-semibold">Documentation</span>
            <button
              onClick={() => setSidebarOpen(false)}
              className="rounded-md p-1.5 text-muted-foreground hover:bg-accent"
              aria-label="Close navigation"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
          <DocsSidebar />
        </div>

        {/* Main content area */}
        <div className="mx-auto max-w-7xl px-4 pt-20 sm:px-6 lg:px-8">
          {/* Mobile header bar */}
          <div className="mb-6 flex items-center gap-3 border-b border-border pb-4 md:hidden">
            <button
              onClick={() => setSidebarOpen(true)}
              className="flex items-center gap-2 rounded-md border border-border px-3 py-1.5 text-sm text-muted-foreground hover:bg-accent"
              aria-label="Open navigation"
            >
              <Menu className="h-4 w-4" />
              Menu
            </button>
            {/* Breadcrumb */}
            <nav aria-label="Breadcrumb" className="flex items-center gap-1 text-sm text-muted-foreground">
              <Link href="/docs" className="hover:text-foreground">
                Docs
              </Link>
              <ChevronRight className="h-3 w-3" aria-hidden />
              <span className="text-foreground">Introduction</span>
            </nav>
          </div>

          <div className="flex gap-8 lg:gap-12">
            {/* Desktop sidebar */}
            <DocsSidebar className="sticky top-20 hidden h-[calc(100vh-5rem)] overflow-y-auto pb-12 md:block" />

            {/* Main content */}
            <main
              className="min-w-0 flex-1 pb-24"
              id="main-content"
              aria-label="Documentation content"
            >
              {children}
            </main>

            {/* Table of Contents */}
            <TableOfContents />
          </div>
        </div>
      </div>

      <Footer />
    </>
  )
}
