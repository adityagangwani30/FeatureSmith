import { Analytics } from "@vercel/analytics/next"
import type { Metadata, Viewport } from "next"
import { ThemeProvider } from "@/components/theme-provider"
import "./globals.css"

export const metadata: Metadata = {
  title: {
    default: "Featuresmith — Make data quality as routine as code quality",
    template: "%s · Featuresmith",
  },
  description:
    "An open-source, developer-first toolkit for understanding, validating, and improving structured data. Every dataset deserves a code review.",
  keywords: ["data profiling", "data validation", "python", "feature engineering", "data quality", "open source", "developer tools", "structured data"],
  authors: [{ name: "Featuresmith Contributors" }],
  creator: "Featuresmith",
  metadataBase: new URL("https://featuresmith.adityagangwani.me"),
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://featuresmith.adityagangwani.me",
    siteName: "Featuresmith",
    title: "Featuresmith — Make data quality as routine as code quality",
    description:
      "An open-source, developer-first toolkit for understanding, validating, and improving structured data. Every dataset deserves a code review.",
    images: [
      {
        url: "https://featuresmith.adityagangwani.me/og-image.png",
        width: 1774,
        height: 887,
        alt: "Featuresmith Banner",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Featuresmith — Make data quality as routine as code quality",
    description: "An open-source, developer-first toolkit for understanding, validating, and improving structured data. Every dataset deserves a code review.",
    images: ["https://featuresmith.adityagangwani.me/og-image.png"],
  },
  robots: {
    index: true,
    follow: true,
  },
  icons: {
    icon: [
      { url: "/favicon-32x32.png", sizes: "32x32", type: "image/png" },
      { url: "/favicon-16x16.png", sizes: "16x16", type: "image/png" },
    ],
    shortcut: "/favicon.ico",
    apple: [
      { url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" },
    ],
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
