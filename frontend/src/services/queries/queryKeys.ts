/**
 * Query Key Factory Registry
 * Centralizes query keys used by TanStack Query, eliminating magic strings.
 */
export const queryKeys = {
  auth: {
    all: () => ["auth"] as const,
    profile: () => ["auth", "profile"] as const
  },
  
  health: {
    all: () => ["health"] as const,
    status: () => ["health", "status"] as const
  },
  
  dashboard: {
    all: () => ["dashboard"] as const,
    telemetry: () => ["dashboard", "telemetry"] as const
  },
  
  projects: {
    all: () => ["projects"] as const,
    list: () => ["projects", "list"] as const,
    detail: (id: string) => ["projects", "detail", id] as const
  },
  
  conversations: {
    all: () => ["conversations"] as const,
    list: () => ["conversations", "list"] as const,
    detail: (id: string) => ["conversations", "detail", id] as const
  },
  
  agents: {
    all: () => ["agents"] as const,
    list: () => ["agents", "list"] as const,
    state: (id: string) => ["agents", "state", id] as const
  },
  
  memory: {
    all: () => ["memory"] as const,
    cache: (sessionId: string) => ["memory", "cache", sessionId] as const
  },
  
  files: {
    all: () => ["files"] as const,
    list: () => ["files", "list"] as const
  },
  
  settings: {
    all: () => ["settings"] as const,
    system: () => ["settings", "system"] as const
  }
} as const
