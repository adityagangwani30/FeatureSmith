import Link from "next/link"
import { ArrowLeft, BookOpen } from "lucide-react"

export default function NotFound() {
  return (
    <main className="grid min-h-screen place-items-center bg-background px-6 py-20 text-center">
      <div className="max-w-md">
        <p className="text-sm font-semibold text-primary">404</p>
        <h1 className="mt-3 text-3xl font-semibold text-foreground">This page does not exist</h1>
        <p className="mt-4 text-sm leading-relaxed text-muted-foreground">The link may be outdated, or the page has moved. The documentation index is a good place to continue.</p>
        <div className="mt-7 flex flex-wrap justify-center gap-3">
          <Link href="/" className="inline-flex items-center gap-2 rounded-md border border-border px-3 py-2 text-sm font-medium text-foreground hover:bg-accent"><ArrowLeft className="h-4 w-4" />Home</Link>
          <Link href="/docs" className="inline-flex items-center gap-2 rounded-md bg-primary px-3 py-2 text-sm font-medium text-primary-foreground hover:opacity-90"><BookOpen className="h-4 w-4" />Browse docs</Link>
        </div>
      </div>
    </main>
  )
}
