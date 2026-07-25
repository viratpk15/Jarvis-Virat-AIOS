# Developer Walkthrough: Jarvis AIOS Theme System & Interaction Upgrade

## Overview

This guide details how to work with, extend, and maintain the new **Jarvis AIOS Premium Design System**.

---

## 1. How the 3-Theme System Works

### 1.1 CSS Tokens (`src/styles/globals.css`)
Theme variables are declared using standard HSL values attached to root classes:
- `:root, .dark` — **Premium Dark** (AMOLED black, violet accents)
- `.light` — **Premium Light** (Soft white workspace, charcoal typography, royal blue accents)
- `.aurora` — **Aurora** (Cybernetic space black, electric purple/cyan glow)

```css
.dark {
  --background: 240 10% 2%;
  --foreground: 0 0% 98%;
  --card: 240 10% 4.5%;
  --primary: 250 84% 67%;
  /* ... */
}
```

### 1.2 Adding a New Future Theme
To add a 4th theme (e.g. `nord` or `cyberpunk`):
1. Open `src/styles/globals.css`.
2. Add `@custom-variant nord (&:is(.nord *));`
3. Define the CSS variables under `.nord { --background: ...; --foreground: ...; }`.
4. Update `Theme` type in `ThemeProvider.tsx` (`export type Theme = "dark" | "light" | "aurora" | "nord"`).
5. Add a theme card entry in `SettingsPage.tsx`.

*Zero component modification required!*

---

## 2. Using Micro-Interaction Utilities

### 2.1 Buttons & Interactive Elements
All buttons inherit built-in GPU micro-interactions via `buttonVariants` in `src/components/ui/button.tsx`:
- `hover:-translate-y-0.5`
- `active:scale-[0.97]`
- `focus-visible:ring-2 focus-visible:ring-ring/50`

### 2.2 Shared Layout Motion Indicators
To add smooth sliding active indicators (like the left Sidebar or Inspector Tabs):
```tsx
import { motion } from "framer-motion"
import { springTransition } from "@/lib/motion"

{isActive && (
  <motion.div
    layoutId="uniqueActiveKey"
    className="absolute inset-0 bg-primary rounded-lg shadow-md"
    transition={springTransition}
  />
)}
```

---

## 3. Motion System & Reduced Motion Policy

All physics presets live in `src/lib/motion.ts`:
- `springTransition`: Snappy desktop spring (`stiffness: 350, damping: 30, mass: 0.8`)
- `easeTransition`: Smooth cubic-bezier (`ease: [0.16, 1, 0.3, 1], duration: 0.3`)

Accessibility reduced-motion override is globally enforced in `globals.css` via `@media (prefers-reduced-motion: reduce)`.
