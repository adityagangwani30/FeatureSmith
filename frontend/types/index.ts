export interface NavItem {
  label: string
  href: string
  external?: boolean
}

export interface Feature {
  icon: string
  title: string
  description: string
}

export interface RoadmapItem {
  phase: string
  title: string
  status: "done" | "in-progress" | "planned" | "future"
  items: string[]
}

export interface CodeExample {
  language: "python" | "bash"
  title: string
  filename?: string
  code: string
}

export interface ArchitectureNode {
  id: string
  label: string
  sublabel: string
  future?: boolean
}

export interface DocSection {
  title: string
  href: string
  items?: { title: string; href: string }[]
}
