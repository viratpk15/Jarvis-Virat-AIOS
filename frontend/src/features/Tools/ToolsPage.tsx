import { WorkspaceShell } from "./components/shell/WorkspaceShell"
import { ToolExplorer } from "./components/explorer/ToolExplorer"
import { ToolInspector } from "./components/inspector/ToolInspector"

export default function ToolsPage() {
  return (
    <WorkspaceShell
      title="Tool Console"
      subtitle="Native AI Engine Tool Discovery, Schema Inspection & Metadata"
    >
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-full items-start">
        {/* Left / Center Column: Tool Explorer */}
        <div className="lg:col-span-7 xl:col-span-8">
          <ToolExplorer />
        </div>

        {/* Right Column: Tool Inspector */}
        <div className="lg:col-span-5 xl:col-span-4 sticky top-0">
          <ToolInspector />
        </div>
      </div>
    </WorkspaceShell>
  )
}
