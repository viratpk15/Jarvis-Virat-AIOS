import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ToyBrick, Settings, CheckCircle2, AlertCircle, ShieldAlert } from "lucide-react"

export default function ToolsPage() {
  const tools = [
    { id: "t1", name: "Web Search API", category: "Connectivity", desc: "Queries Google search engine, parses HTML results, and returns summarized links.", status: "ready", auth: "verified" },
    { id: "t2", name: "Filesystem Access", category: "OS System", desc: "Reads, writes, and lists directory files inside verified workspace contexts.", status: "ready", auth: "elevated" },
    { id: "t3", name: "Git Operations", category: "Dev Tools", desc: "Allows staging, committing, branch switching, and diff comparisons.", status: "warning", auth: "elevated" }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight bg-linear-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">Tool Registry</h1>
          <p className="text-muted-foreground mt-1">Expose native system capabilities, shells, and APIs as actionable tools for agents.</p>
        </div>
        <Button size="sm" className="gap-2 cursor-pointer font-medium">
          <ToyBrick className="h-4 w-4" />
          Register Tool
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {tools.map((tool) => (
          <Card key={tool.id} className="border-border/60 bg-card/30 backdrop-blur-sm hover:border-primary/30 transition-all duration-300 flex flex-col justify-between">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="p-2.5 bg-secondary/50 rounded-lg text-primary border border-border/40">
                  <ToyBrick className="h-5 w-5" />
                </div>
                <div className="flex items-center gap-1.5">
                  <Badge variant="outline" className="text-[10px] font-mono border-border/50 bg-secondary/20">
                    {tool.category}
                  </Badge>
                </div>
              </div>
              <CardTitle className="text-base font-bold text-foreground mt-4">{tool.name}</CardTitle>
              <CardDescription className="text-xs leading-relaxed mt-1 line-clamp-3">{tool.desc}</CardDescription>
            </CardHeader>
            <CardContent className="pt-0">
              <div className="flex items-center gap-4 text-xs font-mono text-muted-foreground mt-2">
                <div className="flex items-center gap-1">
                  {tool.status === "ready" ? (
                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" />
                  ) : (
                    <AlertCircle className="h-3.5 w-3.5 text-amber-500" />
                  )}
                  {tool.status}
                </div>
                <div className="flex items-center gap-1">
                  <ShieldAlert className="h-3.5 w-3.5 text-violet-500" />
                  {tool.auth}
                </div>
              </div>
            </CardContent>
            <CardFooter className="pt-3 border-t border-border/40 flex justify-end">
              <Button variant="ghost" size="sm" className="text-xs gap-1 hover:text-primary cursor-pointer">
                <Settings className="h-3.5 w-3.5" />
                Configure
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  )
}
