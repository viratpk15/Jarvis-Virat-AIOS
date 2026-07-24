import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Database, ToyBrick, Users, Activity, Terminal } from "lucide-react"

export default function DashboardPage() {
  const stats = [
    { title: "System Status", value: "Online", desc: "Core kernel running", icon: Activity, color: "text-emerald-500", badge: "v1.0.0-alpha" },
    { title: "Active Agents", value: "4 / 12", desc: "8 agents in standby mode", icon: Users, color: "text-violet-500", badge: "Active" },
    { title: "Memory Usage", value: "1.2 GB", desc: "Of 8 GB allocated", icon: Database, color: "text-blue-500", badge: "15% Load" },
    { title: "Loaded Tools", value: "28 Tools", desc: "All modules verified", icon: ToyBrick, color: "text-amber-500", badge: "Ready" }
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight bg-linear-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">Jarvis AIOS Dashboard</h1>
        <p className="text-muted-foreground mt-1">Real-time telemetry and overview of the active AI operating system.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, idx) => {
          const Icon = stat.icon
          return (
            <Card key={idx} className="border-border/60 bg-card/30 backdrop-blur-sm overflow-hidden relative group hover:border-primary/30 transition-all duration-300">
              <div className="absolute top-0 left-0 w-full h-0.5 bg-linear-to-r from-transparent via-primary/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">{stat.title}</CardTitle>
                <div className={`p-2 rounded-lg bg-secondary/40 ${stat.color}`}>
                  <Icon className="h-4 w-4" />
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex items-baseline justify-between">
                  <div className="text-2xl font-bold tracking-tight">{stat.value}</div>
                  <Badge variant="secondary" className="text-[10px] bg-secondary/80 border-border/50 font-mono">{stat.badge}</Badge>
                </div>
                <p className="text-xs text-muted-foreground mt-1">{stat.desc}</p>
              </CardContent>
            </Card>
          )
        })}
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card className="col-span-2 border-border/60 bg-card/30 backdrop-blur-sm">
          <CardHeader className="flex flex-row items-center gap-3">
            <Terminal className="h-5 w-5 text-primary" />
            <div>
              <CardTitle className="text-base font-semibold">Active Process Log</CardTitle>
              <CardDescription>Real-time OS task executions and model calls.</CardDescription>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-3 font-mono text-xs text-muted-foreground bg-secondary/20 p-4 rounded-xl border border-border/50 min-h-55">
              <div className="flex justify-between items-center text-emerald-400">
                <span>[SYSTEM] Kernel initialization successful.</span>
                <span>Just now</span>
              </div>
              <div className="flex justify-between items-center">
                <span>[AGENT_MGR] Loaded agent 'CodeOrchestrator' from manifest.</span>
                <span>2m ago</span>
              </div>
              <div className="flex justify-between items-center text-violet-400">
                <span>[LLM_ENGINE] Completed inference (Prompt Tokens: 1.4k, Completion: 242)</span>
                <span>5m ago</span>
              </div>
              <div className="flex justify-between items-center text-blue-400">
                <span>[MEMORY] Vector index synchronization complete.</span>
                <span>12m ago</span>
              </div>
              <div className="flex justify-between items-center">
                <span>[TOOL_ENG] Executing 'fetch_github_repository_structure' tool.</span>
                <span>15m ago</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/60 bg-card/30 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="text-base font-semibold">Resource Monitor</CardTitle>
            <CardDescription>System resource distributions.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-1">
              <div className="flex justify-between text-xs font-medium">
                <span>CPU Allocations</span>
                <span className="text-muted-foreground">34%</span>
              </div>
              <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
                <div className="h-full bg-primary rounded-full" style={{ width: "34%" }} />
              </div>
            </div>
            <div className="space-y-1">
              <div className="flex justify-between text-xs font-medium">
                <span>Memory Footprint</span>
                <span className="text-muted-foreground">15%</span>
              </div>
              <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
                <div className="h-full bg-blue-500 rounded-full" style={{ width: "15%" }} />
              </div>
            </div>
            <div className="space-y-1">
              <div className="flex justify-between text-xs font-medium">
                <span>Thread Queue</span>
                <span className="text-muted-foreground">88% Capacity</span>
              </div>
              <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
                <div className="h-full bg-amber-500 rounded-full" style={{ width: "88%" }} />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
