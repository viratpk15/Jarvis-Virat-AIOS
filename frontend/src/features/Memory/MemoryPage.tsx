import { WorkspaceShell } from "../Tools/components/shell/WorkspaceShell"
import { useMemoryStudioStore } from "./store/useMemoryStudioStore"
import { MemoryTimelinePanel } from "./components/timeline/MemoryTimelinePanel"
import { EntityGraphCanvas } from "./components/graph/EntityGraphCanvas"
import { VectorProjectionMap } from "./components/embeddings/VectorProjectionMap"
import { RecallPlaygroundPanel } from "./components/recall/RecallPlaygroundPanel"
import { ContextWindowPanel } from "./components/context/ContextWindowPanel"
import { MemoryDebuggerPanel } from "./components/debugger/MemoryDebuggerPanel"
import type { MemoryTabType } from "./types/memory.types"

export function MemoryPage() {
  const activeTab = useMemoryStudioStore((s) => s.activeTab)
  const setActiveTab = useMemoryStudioStore((s) => s.setActiveTab)

  const tabs: { id: MemoryTabType; label: string }[] = [
    { id: "timeline", label: "1. Timeline & Inspector" },
    { id: "graph", label: "2. Entity Memory Graph" },
    { id: "embeddings", label: "3. Embedding Explorer" },
    { id: "recall", label: "4. Recall Bench" },
    { id: "context", label: "5. Context Window" },
    { id: "debugger", label: "6. Debugger & Data Ops" },
  ]

  const renderActiveView = () => {
    switch (activeTab) {
      case "timeline":
        return <MemoryTimelinePanel />
      case "graph":
        return <EntityGraphCanvas />
      case "embeddings":
        return <VectorProjectionMap />
      case "recall":
        return <RecallPlaygroundPanel />
      case "context":
        return <ContextWindowPanel />
      case "debugger":
        return <MemoryDebuggerPanel />
      default:
        return <MemoryTimelinePanel />
    }
  }

  return (
    <WorkspaceShell
      title="Memory Studio"
      subtitle="Inspect, recall, compress, and debug cognitive memory across 5 unified tiers"
    >
      <div className="flex flex-col h-full space-y-4">
        {/* Memory Tab Navigation Bar */}
        <nav className="flex border-b border-border/40 font-mono text-xs overflow-x-auto">
          {tabs.map((tab) => {
            const isActive = activeTab === tab.id
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 font-medium focus:outline-none cursor-pointer transition-all whitespace-nowrap ${
                  isActive
                    ? "border-b-2 border-cyan-400 text-cyan-300 font-bold"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                {tab.label}
              </button>
            )
          })}
        </nav>

        {/* Viewport Content */}
        <div className="flex-1 overflow-y-auto">{renderActiveView()}</div>
      </div>
    </WorkspaceShell>
  )
}

export default MemoryPage
