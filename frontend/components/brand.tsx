"use client"

import React from "react"
import { motion } from "framer-motion"
import { cn } from "@/lib/utils"

export interface BrandProps {
  size?: number | string
  animated?: boolean
  className?: string
}

export interface LogoProps extends BrandProps {
  showWordmark?: boolean
}

/**
 * FeaturesmithIcon renders the official Featuresmith icon.
 * It strictly preserves the three left-aligned stacked horizontal capsule geometry,
 * relative bar widths (20 : 15 : 8), equal heights and spacing, and gradients.
 */
export function FeaturesmithIcon({
  size = 24,
  animated = true,
  className,
}: BrandProps) {
  const pixelSize = typeof size === "number" ? `${size}px` : size

  // Sequential entrance animation: Left-to-right (each bar translates x: -6 -> 0 and fades in)
  const barVariants = {
    hidden: { x: -6, opacity: 0 },
    visible: (custom: number) => ({
      x: 0,
      opacity: 1,
      transition: {
        x: { type: "tween" as const, duration: 0.45, ease: "easeOut" as const, delay: custom * 0.15 },
        opacity: { duration: 0.45, ease: "easeOut" as const, delay: custom * 0.15 },
      },
    }),
  }

  return (
    <div
      className={cn("inline-flex items-center justify-center select-none", className)}
      style={{ width: pixelSize, height: pixelSize }}
    >
      <svg
        viewBox="0 0 32 32"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full"
        aria-hidden="true"
      >
        <title>Featuresmith Icon</title>
        
        {/* Official brand gradients */}
        <defs>
          <linearGradient id="topBarGradient" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#2563EB" />
            <stop offset="100%" stopColor="#06B5D4" />
          </linearGradient>
          <linearGradient id="middleBarGradient" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#7C3AED" />
            <stop offset="100%" stopColor="#6366F1" />
          </linearGradient>
          <linearGradient id="bottomBarGradient" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#2B3142" />
            <stop offset="100%" stopColor="#4B5563" />
          </linearGradient>
        </defs>

        {/* Top Bar: capsule width 20, height 4, x=6, y=6, r=2 */}
        <motion.rect
          x="6"
          y="6"
          width="20"
          height="4"
          rx="2"
          ry="2"
          fill="url(#topBarGradient)"
          initial={animated ? "hidden" : "visible"}
          animate="visible"
          custom={0}
          variants={barVariants}
        />

        {/* Middle Bar: capsule width 15, height 4, x=6, y=14, r=2 */}
        <motion.rect
          x="6"
          y="14"
          width="15"
          height="4"
          rx="2"
          ry="2"
          fill="url(#middleBarGradient)"
          initial={animated ? "hidden" : "visible"}
          animate="visible"
          custom={1}
          variants={barVariants}
        />

        {/* Bottom Bar: capsule width 8, height 4, x=6, y=22, r=2 */}
        <motion.rect
          x="6"
          y="22"
          width="8"
          height="4"
          rx="2"
          ry="2"
          fill="url(#bottomBarGradient)"
          initial={animated ? "hidden" : "visible"}
          animate="visible"
          custom={2}
          variants={barVariants}
        />
      </svg>
    </div>
  )
}

/**
 * FeaturesmithLogo renders the icon alongside the stylized brand name wordmark "Featuresmith".
 * It includes keyboard accessibility and theme support.
 */
export function FeaturesmithLogo({
  size = 24,
  animated = true,
  showWordmark = true,
  className,
}: LogoProps) {
  // Fade-in wordmark after the icon is complete (delayed by 0.45s)
  const wordmarkVariants = {
    hidden: { opacity: 0, x: -4 },
    visible: {
      opacity: 1,
      x: 0,
      transition: { duration: 0.4, ease: "easeOut" as const, delay: 0.45 },
    },
  }

  // Restrained hover: scale 1.02 + translate y: -1.5px + slight brightness shimmer
  const hoverVariants = {
    hover: animated ? {
      scale: 1.02,
      y: -1.5,
      filter: "brightness(1.08)",
      transition: { duration: 0.2, ease: "easeOut" as const }
    } : {}
  }

  // Sizing mapping for typography
  const textClass = typeof size === "number" && size <= 20 ? "text-sm" : "text-base"

  return (
    <motion.div
      className={cn(
        "inline-flex items-center gap-3 font-semibold select-none cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 rounded-md",
        className
      )}
      whileHover={animated ? "hover" : undefined}
      variants={hoverVariants}
      role="img"
      aria-label="Featuresmith Logo"
      tabIndex={0}
    >
      <FeaturesmithIcon size={size} animated={animated} />
      
      {showWordmark && (
        <motion.span
          className={cn(
            "tracking-tight font-sans font-semibold text-foreground transition-colors duration-300",
            textClass
          )}
          initial={animated ? "hidden" : "visible"}
          animate="visible"
          variants={wordmarkVariants}
        >
          Featuresmith
        </motion.span>
      )}
    </motion.div>
  )
}

/**
 * AnimatedLogo is a fully animated instance of the logo designed for high visibility sections.
 */
export function AnimatedLogo({
  size = 48,
  ...props
}: Omit<LogoProps, "animated">) {
  return (
    <FeaturesmithLogo
      size={size}
      animated={true}
      {...props}
    />
  )
}
