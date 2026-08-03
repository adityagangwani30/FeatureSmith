import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { Hero } from "@/features/home/hero"
import { WhyExistsSection } from "@/features/home/why-exists-section"
import { WorkflowSection } from "@/features/home/workflow-section"
import { FeaturesSection } from "@/features/home/features-section"
import { PositioningSection } from "@/features/home/positioning-section"
import { PersonasSection } from "@/features/home/personas-section"
import { CodeExamples } from "@/features/home/code-examples"
import { ArchitectureSection } from "@/features/home/architecture-section"
import { FlagshipVisionSection } from "@/features/home/flagship-vision-section"
import { RoadmapSection } from "@/features/home/roadmap-section"
import { OpenSourceSection } from "@/features/home/open-source-section"

export default function HomePage() {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <WhyExistsSection />
        <WorkflowSection />
        <FeaturesSection />
        <PositioningSection />
        <PersonasSection />
        <CodeExamples />
        <ArchitectureSection />
        <FlagshipVisionSection />
        <RoadmapSection />
        <OpenSourceSection />
      </main>
      <Footer />
    </>
  )
}
