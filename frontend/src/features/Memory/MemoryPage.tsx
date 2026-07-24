import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Database, Brain, RefreshCw, Key, HardDrive } from "lucide-react"

export default function MemoryPage() {
  const memories = [
    { key: "usr_pref_theme", value: "dark", scope: "global", timestamp: "1 hour ago" },
    { key: "proj_last_compiled_file", value: "src/main.tsx", scope: "session", timestamp: "12 minutes ago" },
    { key: "assistant_role_profile", value: "Senior Frontend Engineer", scope: "system", timestamp: "Just now" }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight bg-linear-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">Memory Manager</h1>
          <p className="text-muted-foreground mt-1">Monitor session variables, model contextual bindings, and vector indexes.</p>
        </div>
        <Button variant="outline" size="sm" className="gap-2 cursor-pointer border-border hover:bg-secondary">
          <RefreshCw className="h-4 w-4" />
          Synchronize Index
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <Card className="border-border/60 bg-card/30 backdrop-blur-sm">
          <CardHeader className="flex flex-row items-center gap-2 pb-2">
            <Brain className="h-4 w-4 text-primary" />
            <CardTitle className="text-sm font-semibold">Active Key Store</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">142 Keys</div>
            <p className="text-xs text-muted-foreground mt-1">Currently cached in RAM.</p>
          </CardContent>
        </Card>
        <Card className="border-border/60 bg-card/30 backdrop-blur-sm">
          <CardHeader className="flex flex-row items-center gap-2 pb-2">
            <Database className="h-4 w-4 text-blue-500" />
            <CardTitle className="text-sm font-semibold">Vector Storage</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1,824 Vectors</div>
            <p className="text-xs text-muted-foreground mt-1">Indexed in local memory.</p>
          </CardContent>
        </Card>
        <Card className="border-border/60 bg-card/30 backdrop-blur-sm">
          <CardHeader className="flex flex-row items-center gap-2 pb-2">
            <HardDrive className="h-4 w-4 text-emerald-500" />
            <CardTitle className="text-sm font-semibold">Persistence Layer</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Ephemera</div>
            <p className="text-xs text-muted-foreground mt-1">Pending disk serialization setup.</p>
          </CardContent>
        </Card>
      </div>

      <Card className="border-border/60 bg-card/30 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-base font-semibold">Cached Key-Value States</CardTitle>
          <CardDescription>Variables bound in current LLM reasoning scope.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="border border-border/50 rounded-xl overflow-hidden">
            <table className="w-full text-sm text-left">
              <thead className="bg-secondary/40 border-b border-border/50 text-xs font-semibold text-muted-foreground uppercase font-mono">
                <tr>
                  <th className="px-6 py-3">Key Binding</th>
                  <th className="px-6 py-3">Value</th>
                  <th className="px-6 py-3">Scope</th>
                  <th className="px-6 py-3 text-right">Modified</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/40 font-mono text-xs">
                {memories.map((mem) => (
                  <tr key={mem.key} className="hover:bg-secondary/20 transition-colors">
                    <td className="px-6 py-4 flex items-center gap-2 font-medium text-foreground">
                      <Key className="h-3.5 w-3.5 text-primary/80" />
                      {mem.key}
                    </td>
                    <td className="px-6 py-4 text-muted-foreground truncate max-w-xs">{mem.value}</td>
                    <td className="px-6 py-4">
                      <Badge variant="secondary" className="text-[10px] uppercase font-semibold">
                        {mem.scope}
                      </Badge>
                    </td>
                    <td className="px-6 py-4 text-right text-muted-foreground">{mem.timestamp}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
