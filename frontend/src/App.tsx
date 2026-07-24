import { Suspense, lazy } from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router"
import { RootProvider } from "@/providers"
import AppShell from "@/components/layout/AppShell"
import { LoadingIndicator } from "@/components/common/LoadingIndicator"

// Lazy load page features to optimize performance
const DashboardPage = lazy(() => import("@/features/Dashboard/DashboardPage"))
const WorkspacePage = lazy(() => import("@/features/Workspace/WorkspacePage"))
const AgentsPage = lazy(() => import("@/features/Agents/AgentsPage"))
const MemoryPage = lazy(() => import("@/features/Memory/MemoryPage"))
const FilesPage = lazy(() => import("@/features/Files/FilesPage"))
const ToolsPage = lazy(() => import("@/features/Tools/ToolsPage"))
const ModelsPage = lazy(() => import("@/features/Models/ModelsPage"))
const SettingsPage = lazy(() => import("@/features/Settings/SettingsPage"))

function App() {
  return (
    <RootProvider>
      <BrowserRouter>
        <Suspense fallback={<LoadingIndicator fullScreen message="Loading system components..." />}>
          <Routes>
            <Route path="/" element={<AppShell />}>
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<DashboardPage />} />
              <Route path="workspace" element={<WorkspacePage />} />
              <Route path="agents" element={<AgentsPage />} />
              <Route path="memory" element={<MemoryPage />} />
              <Route path="files" element={<FilesPage />} />
              <Route path="tools" element={<ToolsPage />} />
              <Route path="models" element={<ModelsPage />} />
              <Route path="settings" element={<SettingsPage />} />
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Route>
          </Routes>
        </Suspense>
      </BrowserRouter>
    </RootProvider>
  )
}

export default App
