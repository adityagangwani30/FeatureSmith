"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { useState } from "react"
import { ChevronRight, Menu, Search, X } from "lucide-react"
import { Footer } from "@/components/footer"
import { Navbar } from "@/components/navbar"
import { DOC_SECTIONS } from "@/lib/constants"
import { cn } from "@/lib/utils"

function DocsSidebar({ className, onNavigate }: { className?: string; onNavigate?: () => void }) {
  const pathname = usePathname()
  const [query, setQuery] = useState("")
  const normalizedQuery = query.trim().toLowerCase()

  return (
    <aside className={cn("w-64 flex-shrink-0", className)} aria-label="Documentation navigation">
      <div className="mb-4">
        <label className="flex items-center gap-2 rounded-md border border-border bg-muted/50 px-3 py-2 text-sm text-muted-foreground focus-within:ring-2 focus-within:ring-ring">
          <Search className="h-3.5 w-3.5" aria-hidden />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            className="min-w-0 flex-1 bg-transparent text-foreground outline-none placeholder:text-muted-foreground"
            placeholder="Filter documentation"
            aria-label="Filter documentation"
          />
        </label>
      </div>

      <nav>
        {DOC_SECTIONS.map((section) => {
          const items = section.items?.filter((item) =>
            !normalizedQuery || item.title.toLowerCase().includes(normalizedQuery) || section.title.toLowerCase().includes(normalizedQuery)
          )
          if (!items?.length) return null
          return (
            <div key={section.href} className="mb-6">
              <p className="mb-1.5 px-2 text-[11px] font-semibold uppercase tracking-widest text-muted-foreground">{section.title}</p>
              <ul role="list" className="space-y-0.5">
                {items.map((item) => {
                  const isActive = pathname === item.href
                  return (
                    <li key={item.href}>
                      <Link
                        href={item.href}
                        onClick={onNavigate}
                        className={cn(
                          "flex items-center rounded-md px-2 py-1.5 text-sm transition-colors",
                          isActive ? "bg-primary/8 font-medium text-primary" : "text-muted-foreground hover:bg-accent hover:text-foreground"
                        )}
                        aria-current={isActive ? "page" : undefined}
                      >
                        {item.title}
                      </Link>
                    </li>
                  )
                })}
              </ul>
            </div>
          )
        })}
      </nav>
    </aside>
  )
}

function DocsShortcuts() {
  const links = [
    { href: "/docs/quickstart", label: "Quick Start" },
    { href: "/docs/sdk/load", label: "Python SDK" },
    { href: "/docs/cli/analyze", label: "CLI Reference" },
    { href: "/examples", label: "Examples" },
  ]
  return (
    <aside className="hidden w-48 flex-shrink-0 xl:block" aria-label="Documentation shortcuts">
      <div className="sticky top-20">
        <p className="mb-3 text-[11px] font-semibold uppercase tracking-widest text-muted-foreground">Explore</p>
        <nav><ul role="list" className="space-y-1">
          {links.map((link) => <li key={link.href}><Link href={link.href} className="block rounded py-1 text-xs text-muted-foreground transition-colors hover:text-foreground">{link.label}</Link></li>)}
        </ul></nav>
      </div>
    </aside>
  )
}

export default function DocsLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  return (
    <>
      <Navbar />
      <div className="min-h-screen">
        {sidebarOpen && <div className="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm md:hidden" onClick={() => setSidebarOpen(false)} aria-hidden />}
        <div className={cn("fixed inset-y-0 left-0 z-50 w-72 overflow-y-auto border-r border-border bg-background p-6 transition-transform duration-200 md:hidden", sidebarOpen ? "translate-x-0" : "-translate-x-full")} role="dialog" aria-modal="true" aria-label="Documentation navigation">
          <div className="mb-6 flex items-center justify-between"><span className="text-sm font-semibold">Documentation</span><button onClick={() => setSidebarOpen(false)} className="rounded-md p-1.5 text-muted-foreground hover:bg-accent" aria-label="Close navigation"><X className="h-4 w-4" /></button></div>
          <DocsSidebar onNavigate={() => setSidebarOpen(false)} />
        </div>
        <div className="mx-auto max-w-7xl px-4 pt-20 sm:px-6 lg:px-8">
          <div className="mb-6 flex items-center gap-3 border-b border-border pb-4 md:hidden">
            <button onClick={() => setSidebarOpen(true)} className="flex items-center gap-2 rounded-md border border-border px-3 py-1.5 text-sm text-muted-foreground hover:bg-accent" aria-label="Open navigation"><Menu className="h-4 w-4" />Menu</button>
            <nav aria-label="Breadcrumb" className="flex items-center gap-1 text-sm text-muted-foreground"><Link href="/docs" className="hover:text-foreground">Docs</Link><ChevronRight className="h-3 w-3" aria-hidden /><span className="text-foreground">Guide</span></nav>
          </div>
          <div className="flex gap-8 lg:gap-12">
            <DocsSidebar className="sticky top-20 hidden h-[calc(100vh-5rem)] overflow-y-auto pb-12 md:block" />
            <main className="min-w-0 flex-1 pb-24" id="main-content" aria-label="Documentation content">{children}</main>
            <DocsShortcuts />
          </div>
        </div>
      </div>
      <Footer />
    </>
  )
}
