import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Save, Shield, Settings2 } from "lucide-react"

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight bg-linear-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">Settings</h1>
        <p className="text-muted-foreground mt-1">Configure your local Jarvis AIOS runtime parameters and agent preferences.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="border-border/60 bg-card/30 backdrop-blur-sm">
          <CardHeader>
            <div className="flex items-center gap-2 text-primary">
              <Settings2 className="h-5 w-5" />
              <CardTitle className="text-base font-semibold">General AI Engine</CardTitle>
            </div>
            <CardDescription>Setup default API endpoint bindings and model choices.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider font-mono">Primary Model</label>
              <Input placeholder="gemini-2.5-flash" className="bg-secondary/40 border-border/50 text-sm focus-visible:ring-primary" />
            </div>
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider font-mono">Reasoning Temperature</label>
              <Input type="number" step="0.1" defaultValue="0.2" className="bg-secondary/40 border-border/50 text-sm focus-visible:ring-primary" />
            </div>
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider font-mono">Fallback API Key</label>
              <Input type="password" placeholder="••••••••••••••••••••" className="bg-secondary/40 border-border/50 text-sm focus-visible:ring-primary" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/60 bg-card/30 backdrop-blur-sm">
          <CardHeader>
            <div className="flex items-center gap-2 text-primary">
              <Shield className="h-5 w-5" />
              <CardTitle className="text-base font-semibold">Security Settings</CardTitle>
            </div>
            <CardDescription>Configure filesystem and tool authorization thresholds.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider font-mono">Workspace Directory Root</label>
              <Input placeholder="/Users/virat/MyPersonalCloud/Virat/AI-Engineering/Projects/Jarvis" className="bg-secondary/40 border-border/50 text-sm focus-visible:ring-primary" />
            </div>
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider font-mono">Tool Confirmation Scope</label>
              <Input placeholder="Commands, Write Actions, Web Requests" className="bg-secondary/40 border-border/50 text-sm focus-visible:ring-primary" />
            </div>
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider font-mono">System Prompt Override</label>
              <Textarea placeholder="You are Jarvis, a production-grade AI Operating System..." className="bg-secondary/40 border-border/50 text-sm min-h-20.5 focus-visible:ring-primary" />
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="flex justify-end gap-3">
        <Button variant="outline" className="cursor-pointer border-border font-medium">Cancel</Button>
        <Button className="gap-2 cursor-pointer font-medium">
          <Save className="h-4 w-4" />
          Save Configurations
        </Button>
      </div>
    </div>
  )
}
