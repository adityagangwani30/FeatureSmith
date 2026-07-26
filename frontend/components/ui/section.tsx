import { cn } from "@/lib/utils"

interface SectionProps extends React.HTMLAttributes<HTMLElement> {
  as?: "section" | "div" | "article"
}

export function Section({ className, as: Tag = "section", children, ...props }: SectionProps) {
  return (
    <Tag className={cn("py-20 md:py-28", className)} {...props}>
      {children}
    </Tag>
  )
}

interface SectionHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  centered?: boolean
}

export function SectionHeader({ className, centered = false, children, ...props }: SectionHeaderProps) {
  return (
    <div className={cn("mb-12 md:mb-16", centered && "text-center", className)} {...props}>
      {children}
    </div>
  )
}

interface SectionLabelProps extends React.HTMLAttributes<HTMLParagraphElement> {}

export function SectionLabel({ className, children, ...props }: SectionLabelProps) {
  return (
    <p
      className={cn(
        "mb-3 text-xs font-semibold uppercase tracking-widest text-primary",
        className
      )}
      {...props}
    >
      {children}
    </p>
  )
}
