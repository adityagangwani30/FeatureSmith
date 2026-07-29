import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { Hero } from "@/features/home/hero"
import { MissionSection } from "@/features/home/mission-section"
import { WhyExistsSection } from "@/features/home/why-exists-section"
import { FeaturesSection } from "@/features/home/features-section"
import { CodeExamples } from "@/features/home/code-examples"
import { ArchitectureSection } from "@/features/home/architecture-section"
import { FlagshipVisionSection } from "@/features/home/flagship-vision-section"
import { PhilosophySection } from "@/features/home/philosophy-section"
import { RoadmapSection } from "@/features/home/roadmap-section"
import { OpenSourceSection } from "@/features/home/open-source-section"

export default function HomePage() {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <MissionSection />
        <WhyExistsSection />
        <FeaturesSection />
        <CodeExamples />
        <ArchitectureSection />
        <FlagshipVisionSection />
        <PhilosophySection />
        <RoadmapSection />
        <OpenSourceSection />
      </main>
      <Footer />
    </>
  )
}
