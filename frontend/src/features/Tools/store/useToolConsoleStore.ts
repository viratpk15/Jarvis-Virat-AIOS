import { create } from "zustand"

interface ToolConsoleState {
  selectedToolName: string | null
  searchQuery: string
  selectedCategory: string | null
  selectedTag: string | null
  sidebarCollapsed: boolean
  commandPaletteOpen: boolean

  setSelectedToolName: (name: string | null) => void
  setSearchQuery: (query: string) => void
  setSelectedCategory: (category: string | null) => void
  setSelectedTag: (tag: string | null) => void
  toggleSidebar: () => void
  setCommandPaletteOpen: (open: boolean) => void
  resetFilters: () => void
}

export const useToolConsoleStore = create<ToolConsoleState>((set) => ({
  selectedToolName: null,
  searchQuery: "",
  selectedCategory: null,
  selectedTag: null,
  sidebarCollapsed: false,
  commandPaletteOpen: false,

  setSelectedToolName: (name) => set({ selectedToolName: name }),
  setSearchQuery: (query) => set({ searchQuery: query }),
  setSelectedCategory: (category) => set({ selectedCategory: category }),
  setSelectedTag: (tag) => set({ selectedTag: tag }),
  toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
  setCommandPaletteOpen: (open) => set({ commandPaletteOpen: open }),
  resetFilters: () => set({ searchQuery: "", selectedCategory: null, selectedTag: null }),
}))
