# Design System Architecture: Jarvis AIOS

```mermaid
graph TD
    subgraph Client Layer
        A[HTML Document / root] --> B[ThemeProvider]
        B --> C[localStorage Sync]
    end

    subgraph Theme Token Layer
        B --> D{Active Theme Class}
        D -- .dark --> E[Premium Dark Tokens]
        D -- .light --> F[Premium Light Tokens]
        D -- .aurora --> G[Aurora Tokens]
    end

    subgraph Component Engine
        E --> H[globals.css Semantic Variables]
        F --> H
        G --> H
        H --> I[Tailwind CSS v4 Utility Engine]
        I --> J[UI Primitives: Button, Card, Input, Dialog]
        I --> K[AppShell Navigation & Sidebar]
        I --> L[Inspector Panel & Tabs]
        I --> M[Feature Pages: Workspace, Dashboard, Agents]
    end

    subgraph Motion Engine
        N[framer-motion] --> O[motion.ts Physics & Variants]
        O --> J
        O --> K
        O --> L
    end
```

## Layer Descriptions

1. **Client & Persistence Layer**: `ThemeProvider` initializes the saved theme from `localStorage` without FOUC, attaching `.dark`, `.light`, or `.aurora` class to `document.documentElement`.
2. **Semantic Design Token Layer**: HSL CSS variables mapping background, surface, text, border, accent, glass, and shadow specifications.
3. **Component Engine**: Pure component layer utilizing semantic tokens. No hardcoded hex values.
4. **Motion Engine**: Framer Motion standardized springs and eases providing desktop-grade micro-interactions.
