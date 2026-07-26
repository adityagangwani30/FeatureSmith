import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { Hero } from "@/features/home/hero"
import { FeaturesSection } from "@/features/home/features-section"
import { ArchitectureSection } from "@/features/home/architecture-section"
import { CodeExamples } from "@/features/home/code-examples"
import { PhilosophySection } from "@/features/home/philosophy-section"
import { RoadmapSection } from "@/features/home/roadmap-section"
import { OpenSourceSection } from "@/features/home/open-source-section"

export default function HomePage() {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <FeaturesSection />
        <ArchitectureSection />
        <CodeExamples />
        <PhilosophySection />
        <RoadmapSection />
        <OpenSourceSection />
      </main>
      <Footer />
    </>
  )
}
