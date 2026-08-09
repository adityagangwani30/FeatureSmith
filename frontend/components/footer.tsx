import Link from "next/link"
import { Container } from "@/components/ui/container"
import { FeaturesmithLogo } from "./brand"
function GithubIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M12 2C6.477 2 2 6.484 2 12.021c0 4.428 2.865 8.184 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0 1 12 6.844a9.59 9.59 0 0 1 2.504.337c1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482C19.138 20.2 22 16.447 22 12.021 22 6.484 17.522 2 12 2z" />
    </svg>
  )
}

const FOOTER_LINKS = {
  Documentation: [
    { label: "Introduction", href: "/docs" },
    { label: "Quick Start", href: "/docs/quickstart" },
    { label: "Python SDK", href: "/docs/sdk/load" },
    { label: "CLI Reference", href: "/docs/cli/analyze" },
  ],
  Community: [
    { label: "GitHub", href: "https://github.com/adityagangwani30/FeatureSmith", external: true },
    { label: "Discussions", href: "https://github.com/adityagangwani30/FeatureSmith/discussions", external: true },
    { label: "Issues", href: "https://github.com/adityagangwani30/FeatureSmith/issues", external: true },
    { label: "Contributing", href: "https://github.com/adityagangwani30/FeatureSmith/blob/main/CONTRIBUTING.md", external: true },
  ],
  Project: [
    { label: "Roadmap", href: "/roadmap" },
    { label: "Release status", href: "/release" },
    { label: "Benchmarks", href: "/docs/benchmarks" },
    { label: "Changelog", href: "https://github.com/adityagangwani30/FeatureSmith/blob/main/CHANGELOG.md", external: true },
    { label: "Examples", href: "/examples" },
  ],
  Legal: [
    { label: "Apache 2.0 License", href: "https://github.com/adityagangwani30/FeatureSmith/blob/main/LICENSE", external: true },
    { label: "Code of Conduct", href: "https://github.com/adityagangwani30/FeatureSmith/blob/main/CODE_OF_CONDUCT.md", external: true },
    { label: "Security", href: "https://github.com/adityagangwani30/FeatureSmith/blob/main/SECURITY.md", external: true },
  ],
}


export function Footer() {
  return (
    <footer className="border-t border-border bg-muted/30" aria-label="Site footer">
      <Container>
        <div className="py-12 md:py-16">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4 lg:grid-cols-5">
            {/* Brand column */}
            <div className="col-span-2 md:col-span-4 lg:col-span-1">
              <Link href="/" className="transition-opacity hover:opacity-80">
                <FeaturesmithLogo size={20} />
              </Link>
              <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
                Open-source data profiling and validation for Python engineers.
              </p>
              <div className="mt-4 flex items-center gap-3">
                <Link
                  href="https://github.com/adityagangwani30/FeatureSmith"
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="GitHub"
                  className="text-muted-foreground transition-colors hover:text-foreground"
                >
                  <GithubIcon className="h-4 w-4" />
                </Link>
              </div>
            </div>

            {/* Link columns */}
            {Object.entries(FOOTER_LINKS).map(([group, links]) => (
              <div key={group}>
                <h3 className="mb-3 text-xs font-semibold uppercase tracking-wide text-foreground">
                  {group}
                </h3>
                <ul className="space-y-2" role="list">
                  {links.map((link) => (
                    <li key={link.href}>
                      <Link
                        href={link.href}
                        target={"external" in link && link.external ? "_blank" : undefined}
                        rel={"external" in link && link.external ? "noopener noreferrer" : undefined}
                        className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          {/* Bottom bar */}
          <div className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-border pt-6 sm:flex-row">
            <p className="text-xs text-muted-foreground">
              &copy; {new Date().getFullYear()} Featuresmith Contributors. Released under the{" "}
              <Link
                href="https://github.com/adityagangwani30/FeatureSmith/blob/main/LICENSE"
                target="_blank"
                rel="noopener noreferrer"
                className="underline underline-offset-4 hover:text-foreground"
              >
                Apache 2.0 License
              </Link>
              .
            </p>
            <p className="text-xs text-muted-foreground">
              Built by{" "}
              <Link
                href="https://adityagangwani.me"
                target="_blank"
                rel="noopener noreferrer"
                className="underline underline-offset-4 hover:text-foreground font-medium"
              >
                Aditya Gangwani
              </Link>{" "}
              in the open.
            </p>
          </div>
        </div>
      </Container>
    </footer>
  )
}
