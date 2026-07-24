import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Folder, Plus, ArrowRight, Calendar, GitBranch, Search } from "lucide-react"
import { EmptyState } from "@/components/common/EmptyState"

export default function WorkspacePage() {
  const [searchTerm, setSearchTerm] = useState("")

  const workspaces = [
    { id: "1", name: "Personal Cloud AI", desc: "Main assistant configuration and plugins for virtual private cloud sync.", updated: "2 hours ago", branch: "main", status: "active" },
    { id: "2", name: "Document Analysis", desc: "Custom workspace optimized for heavy semantic research and PDF parsing.", updated: "3 days ago", branch: "dev", status: "standby" },
    { id: "3", name: "Web Autopilot", desc: "Automated browser navigation pipelines and script executor environment.", updated: "1 week ago", branch: "main", status: "inactive" }
  ]

  const filtered = workspaces.filter((ws) =>
    ws.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    ws.desc.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight bg-linear-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">Workspaces</h1>
          <p className="text-muted-foreground mt-1">Manage isolated environments, configuration profiles, and files.</p>
        </div>
        <Button size="sm" className="gap-2 cursor-pointer font-medium">
          <Plus className="h-4 w-4" />
          New Workspace
        </Button>
      </div>

      {/* Search Input Bar */}
      <div className="relative max-w-sm">
        <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground/75" />
        <input
          type="text"
          placeholder="Filter workspaces by name or keywords..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="pl-9 pr-4 py-2 w-full rounded-lg bg-secondary/30 border border-border/60 text-sm text-foreground outline-none focus-visible:ring-1 focus-visible:ring-primary placeholder:text-muted-foreground/60"
        />
      </div>

      {filtered.length > 0 ? (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filtered.map((ws) => (
            <Card key={ws.id} className="border-border/60 bg-card/30 backdrop-blur-sm hover:border-primary/30 transition-all duration-300 flex flex-col justify-between group">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between mb-2">
                  <div className="p-2 bg-secondary/50 rounded-lg text-primary">
                    <Folder className="h-5 w-5" />
                  </div>
                  <Badge variant={ws.status === "active" ? "default" : "secondary"} className="text-[10px] font-mono">
                    {ws.status}
                  </Badge>
                </div>
                <CardTitle className="text-lg font-bold tracking-tight text-foreground group-hover:text-primary transition-colors">{ws.name}</CardTitle>
                <CardDescription className="text-xs leading-relaxed line-clamp-2 mt-1">{ws.desc}</CardDescription>
              </CardHeader>
              <CardContent className="pb-3">
                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  <div className="flex items-center gap-1.5 font-mono">
                    <GitBranch className="h-3 w-3" />
                    {ws.branch}
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Calendar className="h-3 w-3" />
                    {ws.updated}
                  </div>
                </div>
              </CardContent>
              <CardFooter className="pt-3 border-t border-border/40 flex justify-end">
                <Button variant="ghost" size="sm" className="text-xs gap-1 hover:text-primary cursor-pointer">
                  Enter Workspace
                  <ArrowRight className="h-3 w-3" />
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      ) : (
        <EmptyState
          title="No workspaces found"
          description={`No workspaces match your query "${searchTerm}". Try refinement or configure another profile.`}
          icon={Folder}
          actionText="Clear Filter"
          onAction={() => setSearchTerm("")}
        />
      )}
    </div>
  )
}
