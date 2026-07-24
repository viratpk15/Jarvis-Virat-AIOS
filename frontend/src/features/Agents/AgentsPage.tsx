import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Bot, Settings2, Play, Square, Search } from "lucide-react"
import { EmptyState } from "@/components/common/EmptyState"

export default function AgentsPage() {
  const [searchTerm, setSearchTerm] = useState("")

  const agents = [
    { id: "a1", name: "Code Orchestrator", type: "Specialized", desc: "Analyzes codebases, maps dependencies, and writes structured code improvements.", status: "running", model: "Gemini 2.5 Flash" },
    { id: "a2", name: "Web Navigator", type: "Tool-user", desc: "Surfs websites, extracts text content, and completes automated browser-based flows.", status: "idle", model: "Gemini 1.5 Pro" },
    { id: "a3", name: "Personal Assistant", type: "Generalist", desc: "Main communication agent, responds to general queries and maintains semantic history.", status: "running", model: "Gemini 2.5 Pro" }
  ]

  const filtered = agents.filter((agent) =>
    agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    agent.desc.toLowerCase().includes(searchTerm.toLowerCase()) ||
    agent.model.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight bg-linear-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">AI Agents</h1>
          <p className="text-muted-foreground mt-1">Configure and monitor active LangGraph agents running within the OS.</p>
        </div>
        <Button size="sm" className="gap-2 cursor-pointer font-medium">
          <Bot className="h-4 w-4" />
          Deploy Agent
        </Button>
      </div>

      {/* Search Input Bar */}
      <div className="relative max-w-sm">
        <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground/75" />
        <input
          type="text"
          placeholder="Filter agents by name, model, or status..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="pl-9 pr-4 py-2 w-full rounded-lg bg-secondary/30 border border-border/60 text-sm text-foreground outline-none focus-visible:ring-1 focus-visible:ring-primary placeholder:text-muted-foreground/60"
        />
      </div>

      {filtered.length > 0 ? (
        <div className="grid gap-6 md:grid-cols-2">
          {filtered.map((agent) => (
            <Card key={agent.id} className="border-border/60 bg-card/30 backdrop-blur-sm hover:border-primary/30 transition-all duration-300 flex flex-col justify-between">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2.5 bg-secondary/50 rounded-lg text-primary border border-border/40">
                      <Bot className="h-5 w-5" />
                    </div>
                    <div>
                      <CardTitle className="text-base font-bold text-foreground">{agent.name}</CardTitle>
                      <CardDescription className="text-xs font-medium font-mono text-primary/80 mt-0.5">{agent.model}</CardDescription>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="outline" className="text-[10px] font-mono border-border/60 bg-secondary/20">
                      {agent.type}
                    </Badge>
                    <span className={`h-2 w-2 rounded-full ${agent.status === "running" ? "bg-emerald-500 animate-pulse" : "bg-zinc-500"}`} />
                  </div>
                </div>
                <p className="text-sm text-muted-foreground mt-4 leading-relaxed">{agent.desc}</p>
              </CardHeader>
              <CardContent className="pt-0 pb-4">
                {/* Future agent telemetry details */}
              </CardContent>
              <CardFooter className="pt-3 border-t border-border/40 flex justify-between">
                <Button variant="ghost" size="sm" className="text-xs gap-1 hover:text-primary cursor-pointer">
                  <Settings2 className="h-3.5 w-3.5" />
                  Configure
                </Button>
                <Button size="sm" variant={agent.status === "running" ? "destructive" : "secondary"} className="text-xs gap-1.5 cursor-pointer font-semibold">
                  {agent.status === "running" ? (
                    <>
                      <Square className="h-3 w-3 fill-current" />
                      Stop Agent
                    </>
                  ) : (
                    <>
                      <Play className="h-3 w-3 fill-current" />
                      Start Agent
                    </>
                  )}
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      ) : (
        <EmptyState
          title="No agents found"
          description={`No active AI agents match your query "${searchTerm}". Deploy a new specialized agent template.`}
          icon={Bot}
          actionText="Clear Filter"
          onAction={() => setSearchTerm("")}
        />
      )}
    </div>
  )
}
