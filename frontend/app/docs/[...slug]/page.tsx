import Link from "next/link"
import { notFound, redirect } from "next/navigation"
import { ChevronRight, Info } from "lucide-react"
import { DOCS_MAP } from "./docs-content"

const PLANNED_DOCS = new Set(["sdk/plugins", "guides/plugins"])

export async function generateStaticParams() {
  const slugs = [...Object.keys(DOCS_MAP), "sdk/plugins", "guides/plugins"]
  return slugs.map((slug) => ({
    slug: slug.split("/"),
  }))
}

// Generate metadata for each dynamic documentation path
export async function generateMetadata({ params }: { params: Promise<{ slug: string[] }> }) {
  const resolvedParams = await params
  const slugPath = resolvedParams.slug.join("/")
  const doc = DOCS_MAP[slugPath]

  if (!doc && PLANNED_DOCS.has(slugPath)) {
    return {
      title: "Coming Soon | Featuresmith",
      description: "This documentation page is planned for a future Featuresmith release."
    }
  }

  if (!doc) {
    return {
      title: "Not Found | Featuresmith Docs",
      description: "The requested documentation page was not found."
    }
  }

  return {
    title: `${doc.seoTitle} | Featuresmith Docs`,
    description: doc.seoDescription,
  }
}

export default async function DynamicDocPage({ params }: { params: Promise<{ slug: string[] }> }) {
  const resolvedParams = await params
  const slugPath = resolvedParams.slug.join("/")

  if (slugPath === "concepts") {
    redirect("/docs/concepts/dataset")
  }
  if (slugPath === "sdk") {
    redirect("/docs/sdk/load")
  }
  if (slugPath === "cli") {
    redirect("/docs/cli/analyze")
  }
  if (slugPath === "guides") {
    redirect("/docs/guides/cicd")
  }
  if (slugPath === "resources") {
    redirect("/docs/resources/release")
  }

  const doc = DOCS_MAP[slugPath]

  // Planned documentation is represented by a deliberate release-safe page.
  if (!doc && PLANNED_DOCS.has(slugPath)) {
    const isPlannedGuide = slugPath.startsWith("guides/") || slugPath.endsWith("plugins")
    const sectionTitle = slugPath.split("/")[0].toUpperCase()

    return (
      <article className="prose-custom max-w-none">
        <nav aria-label="Breadcrumb" className="mb-6 flex items-center gap-1 text-sm text-muted-foreground">
          <Link href="/" className="hover:text-foreground">Home</Link>
          <ChevronRight className="h-3.5 w-3.5" aria-hidden />
          <Link href="/docs" className="hover:text-foreground">Docs</Link>
          <ChevronRight className="h-3.5 w-3.5" aria-hidden />
          <span className="text-foreground capitalize">{slugPath.split("/").pop()}</span>
        </nav>

        <header className="mb-10 border-b border-border pb-8">
          <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-primary">
            {sectionTitle}
          </p>
          <h1 className="mb-3 text-3xl font-semibold tracking-tight text-foreground sm:text-4xl capitalize">
            {slugPath.split("/").pop()?.replace("-", " ")}
          </h1>
          <p className="text-base leading-relaxed text-muted-foreground">
            Coming Soon: this capability is planned for a future Featuresmith release.
          </p>
        </header>

        <div className="rounded-xl border border-border bg-card p-6 md:p-8">
          <div className="flex items-start gap-4">
            <div className="inline-flex h-10 w-10 items-center justify-center rounded-lg bg-primary/8 text-primary ring-1 ring-primary/15">
              <Info className="h-5 w-5" aria-hidden />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-foreground">Planned for a Future Release</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                {isPlannedGuide
                  ? "Plugin authoring and automatic plugin discovery are scheduled for the Plugin Ecosystem phase. The current release supports explicit in-repository rule registration."
                  : "This API surface is planned and is not part of the supported v0.4.0 release."}
              </p>
              <div className="mt-6 flex flex-wrap gap-3">
                <Link
                  href="/roadmap"
                  className="inline-flex items-center gap-1.5 rounded-md bg-primary px-4 py-2 text-xs font-medium text-primary-foreground hover:opacity-90 transition-all"
                >
                  View Roadmap Phases
                </Link>
                <Link
                  href="https://github.com/adityagangwani30/FeatureSmith"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 rounded-md border border-border bg-transparent px-4 py-2 text-xs font-medium text-foreground hover:bg-accent transition-all"
                >
                  Follow on GitHub
                </Link>
              </div>
            </div>
          </div>
        </div>
      </article>
    )
  }

  if (!doc) notFound()

  return (
    <article className="prose-custom max-w-none">
      {/* Breadcrumb */}
      <nav aria-label="Breadcrumb" className="mb-6 flex items-center gap-1 text-sm text-muted-foreground">
        <Link href="/" className="hover:text-foreground">
          Home
        </Link>
        <ChevronRight className="h-3.5 w-3.5" aria-hidden />
        <Link href="/docs" className="hover:text-foreground">
          Docs
        </Link>
        <ChevronRight className="h-3.5 w-3.5" aria-hidden />
        <span className="text-foreground">{doc.title}</span>
      </nav>

      {/* Page header */}
      <header className="mb-10 border-b border-border pb-8">
        <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-primary">
          {doc.category}
        </p>
        <h1 className="mb-3 text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
          {doc.title}
        </h1>
        <p className="text-base leading-relaxed text-muted-foreground">
          {doc.subtitle}
        </p>
      </header>

      {/* Render the document contents */}
      <div className="prose-custom">
        {doc.render()}
      </div>
    </article>
  )
}
