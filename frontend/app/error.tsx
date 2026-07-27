"use client"

import Link from "next/link"
import { useEffect } from "react"

export default function Error({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  useEffect(() => { console.error(error) }, [error])
  return (
    <main className="grid min-h-screen place-items-center bg-background px-6 py-20 text-center">
      <div className="max-w-md"><p className="text-sm font-semibold text-primary">Something went wrong</p><h1 className="mt-3 text-3xl font-semibold text-foreground">We could not load this page</h1><p className="mt-4 text-sm leading-relaxed text-muted-foreground">Try loading the page again. If the problem continues, use the documentation index to continue exploring Featuresmith.</p><div className="mt-7 flex justify-center gap-3"><button onClick={reset} className="rounded-md bg-primary px-3 py-2 text-sm font-medium text-primary-foreground hover:opacity-90">Try again</button><Link href="/docs" className="rounded-md border border-border px-3 py-2 text-sm font-medium text-foreground hover:bg-accent">Browse docs</Link></div></div>
    </main>
  )
}
