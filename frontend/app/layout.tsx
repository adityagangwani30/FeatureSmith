import { Analytics } from "@vercel/analytics/next"
import type { Metadata, Viewport } from "next"
import { ThemeProvider } from "@/components/theme-provider"
import "./globals.css"

export const metadata: Metadata = {
  title: {
    default: "Featuresmith — Data Profiling & Validation",
    template: "%s · Featuresmith",
  },
  description:
    "An open-source Python library for dataset profiling, rule-based validation, and intelligent feature analysis. Built for engineers who believe data quality is a first-class concern.",
  keywords: ["data profiling", "data validation", "python", "feature engineering", "data quality", "open source"],
  authors: [{ name: "Featuresmith Contributors" }],
  creator: "Featuresmith",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://featuresmith.adityagangwani.me",
    siteName: "Featuresmith",
    title: "Featuresmith — Data Profiling & Validation",
    description:
      "Profile, validate, and understand your data — in one command. Open-source Python library for data quality.",
  },
  twitter: {
    card: "summary_large_image",
    title: "Featuresmith — Data Profiling & Validation",
    description: "Profile, validate, and understand your data — in one command.",
  },
  robots: {
    index: true,
    follow: true,
  },
}

export const viewport: Viewport = {
  colorScheme: "light dark",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#1a1a1a" },
  ],
  width: "device-width",
  initialScale: 1,
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className="bg-background"
    >
      <body className="font-sans antialiased">
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          {children}
        </ThemeProvider>
        {process.env.NODE_ENV === "production" && <Analytics />}
      </body>
    </html>
  )
}
