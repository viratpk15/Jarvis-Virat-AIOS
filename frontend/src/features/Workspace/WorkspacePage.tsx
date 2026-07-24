import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Folder, Plus, ArrowRight, Calendar, GitBranch } from "lucide-react"

export default function WorkspacePage() {
  const workspaces = [
    { id: "1", name: "Personal Cloud AI", desc: "Main assistant configuration and plugins for virtual private cloud sync.", updated: "2 hours ago", branch: "main", status: "active" },
    { id: "2", name: "Document Analysis", desc: "Custom workspace optimized for heavy semantic research and PDF parsing.", updated: "3 days ago", branch: "dev", status: "standby" },
    { id: "3", name: "Web Autopilot", desc: "Automated browser navigation pipelines and script executor environment.", updated: "1 week ago", branch: "main", status: "inactive" }
  ]

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

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {workspaces.map((ws) => (
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
    </div>
  )
}
