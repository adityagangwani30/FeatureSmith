import { cn } from "@/lib/utils"

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "outline" | "primary" | "success" | "muted"
}

const variantClasses: Record<NonNullable<BadgeProps["variant"]>, string> = {
  default:
    "border border-border bg-muted text-muted-foreground",
  outline:
    "border border-border bg-transparent text-foreground",
  primary:
    "border border-primary/20 bg-primary/8 text-primary",
  success:
    "border border-emerald-500/20 bg-emerald-500/8 text-emerald-600 dark:text-emerald-400",
  muted:
    "border border-border bg-muted/50 text-muted-foreground",
}

export function Badge({ className, variant = "default", children, ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium",
        variantClasses[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  )
}
