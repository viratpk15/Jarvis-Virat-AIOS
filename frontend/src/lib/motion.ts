import type { Variants } from "framer-motion"

export const springTransition = {
  type: "spring" as const,
  stiffness: 300,
  damping: 30
}

export const easeTransition = {
  type: "tween" as const,
  ease: [0.16, 1, 0.3, 1] as const, // easeOutExpo
  duration: 0.4
}

export const pageVariants: Variants = {
  initial: { opacity: 0, y: 10 },
  animate: { opacity: 1, y: 0, transition: easeTransition },
  exit: { opacity: 0, y: -10, transition: { duration: 0.15 } }
}

export const sidebarVariants: Variants = {
  expanded: { width: 260, transition: springTransition },
  collapsed: { width: 68, transition: springTransition }
}

export const sidebarItemVariants: Variants = {
  initial: { opacity: 0, x: -10 },
  animate: { opacity: 1, x: 0, transition: { duration: 0.2 } },
  exit: { opacity: 0, x: -10, transition: { duration: 0.1 } }
}

export const panelVariants: Variants = {
  open: { 
    width: 320, 
    opacity: 1,
    x: 0,
    display: "flex",
    transition: springTransition 
  },
  closed: { 
    width: 0, 
    opacity: 0,
    x: 20,
    transitionEnd: { display: "none" },
    transition: springTransition 
  }
}

export const dialogVariants: Variants = {
  initial: { opacity: 0, scale: 0.95, y: -20 },
  animate: { opacity: 1, scale: 1, y: 0, transition: easeTransition },
  exit: { opacity: 0, scale: 0.95, y: -10, transition: { duration: 0.15 } }
}

export const fadeVariants: Variants = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 0.2 } },
  exit: { opacity: 0, transition: { duration: 0.15 } }
}

export const commandPaletteItemVariants: Variants = {
  hover: { backgroundColor: "rgba(255, 255, 255, 0.08)", scale: 1.01 },
  tap: { scale: 0.99 }
}

export const dashboardGridVariants: Variants = {
  initial: { opacity: 0 },
  animate: {
    opacity: 1,
    transition: {
      staggerChildren: 0.03
    }
  }
}

export const dashboardCardVariants: Variants = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0, transition: easeTransition },
  hover: {
    y: -3,
    transition: { duration: 0.2, ease: "easeOut" }
  },
  tap: { scale: 0.985 }
}

export const dashboardItemVariants: Variants = {
  initial: { opacity: 0, x: -8 },
  animate: { opacity: 1, x: 0, transition: easeTransition }
}

