// frontend/src/features/Agents/components/AgentLibrary.tsx
import { useState } from "react"
import { Bot, Cpu, Wrench, Play, Plus, Search, CheckCircle } from "lucide-react"

export default function AgentLibrary() {
  const [search, setSearch] = useState("")

  const agents = [
    {
      id: "agent_react_01",
      name: "Autonomous Technical Researcher",
      description: "ReAct agent with Python code execution and web browsing search tools.",
      pattern: "ReAct Loop",
      model: "gemini-2.5-flash",
      tools_count: 4,
      status: "active",
      last_run: "10 mins ago",
    },
    {
      id: "agent_plan_exec_02",
      name: "Multi-Step Planner Agent",
      description: "Plan-Execute orchestrator that breaks complex user goals into atomic tasks.",
      pattern: "Plan-Execute",
      model: "gpt-4o",
      tools_count: 6,
      status: "active",
      last_run: "1 hour ago",
    },
    {
      id: "agent_rag_summarizer",
      name: "RAG Synthesis Specialist",
      description: "Memory-aware agent integrated with BM25 vector knowledge retrieval.",
      pattern: "Reflection",
      model: "claude-3-5-sonnet",
      tools_count: 2,
      status: "idle",
      last_run: "Yesterday",
    },
  ]

  const filtered = agents.filter(
    (a) => a.name.toLowerCase().includes(search.toLowerCase()) || a.description.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="space-y-4 font-mono text-xs">
      {/* Top Action Bar */}
      <div className="flex items-center justify-between gap-3 bg-secondary/15 border border-border/40 p-4 rounded-xl">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-2.5 h-3.5 w-3.5 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search agents by name or capability..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 bg-secondary/30 border border-border/40 rounded-lg text-foreground text-xs font-mono"
          />
        </div>
        <button className="flex items-center gap-1.5 px-3 py-1.5 font-bold rounded-lg bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 hover:bg-cyan-500/30 cursor-pointer transition-all">
          <Plus className="h-3.5 w-3.5" />
          Create New Agent
        </button>
      </div>

      {/* Agent Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {filtered.map((agent) => (
          <div key={agent.id} className="p-4 bg-secondary/20 border border-border/30 rounded-xl space-y-3 hover:border-cyan-500/40 transition-all">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-2">
                <Bot className="h-4 w-4 text-cyan-400" />
                <span className="text-foreground font-bold text-xs">{agent.name}</span>
              </div>
              <span className="text-[10px] bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-full flex items-center gap-1">
                <CheckCircle className="h-2.5 w-2.5 text-emerald-400" />
                {agent.status}
              </span>
            </div>

            <p className="text-muted-foreground text-[11px] leading-relaxed">{agent.description}</p>

            <div className="pt-2 border-t border-border/30 grid grid-cols-2 gap-2 text-[10px] text-muted-foreground">
              <div>
                Pattern: <span className="text-cyan-300 font-bold">{agent.pattern}</span>
              </div>
              <div>
                Model: <span className="text-amber-300 font-bold">{agent.model}</span>
              </div>
              <div className="flex items-center gap-1">
                <Wrench className="h-3 w-3 text-cyan-400" />
                <span>{agent.tools_count} Tools Bound</span>
              </div>
              <div className="flex items-center gap-1">
                <Cpu className="h-3 w-3 text-emerald-400" />
                <span>{agent.last_run}</span>
              </div>
            </div>

            <button className="w-full py-1.5 mt-1 font-bold rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 hover:bg-cyan-500/30 transition-all cursor-pointer flex items-center justify-center gap-1">
              <Play className="h-3 w-3" />
              Launch Execution
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}