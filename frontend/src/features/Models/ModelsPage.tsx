import { Sparkles, Cpu, Sliders } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export default function ModelsPage() {
  const models = [
    { id: "m1", name: "Gemini 2.5 Flash", provider: "Google AI", desc: "Default fast model optimized for quick reasoning, code editing, and low-latency agent pipelines.", status: "default", context: "1.0M tokens", speed: "Ultra High" },
    { id: "m2", name: "Gemini 2.5 Pro", provider: "Google AI", desc: "Advanced reasoning model optimized for complex multi-step coding problems and semantic searches.", status: "available", context: "2.0M tokens", speed: "High" },
    { id: "m3", name: "Gemini 1.5 Flash", provider: "Google AI", desc: "Legacy fast inference engine, maintained as a local fallback model.", status: "standby", context: "1.0M tokens", speed: "High" }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight bg-linear-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent">Model Registry</h1>
          <p className="text-muted-foreground mt-1">Configure language model endpoints, routing variables, and token margins.</p>
        </div>
        <Button size="sm" variant="outline" className="gap-2 cursor-pointer border-border hover:bg-secondary">
          <Cpu className="h-4 w-4 text-primary" />
          Manage Providers
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {models.map((model) => (
          <Card key={model.id} className="border-border/60 bg-card/30 backdrop-blur-sm hover:border-primary/30 transition-all duration-300 flex flex-col justify-between group">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between mb-2">
                <div className="p-2 bg-secondary/50 rounded-lg text-primary">
                  <Sparkles className="h-5 w-5" />
                </div>
                <Badge variant={model.status === "default" ? "default" : "secondary"} className="text-[10px] uppercase font-mono">
                  {model.status}
                </Badge>
              </div>
              <CardTitle className="text-lg font-bold tracking-tight text-foreground group-hover:text-primary transition-colors">{model.name}</CardTitle>
              <CardDescription className="text-xs leading-relaxed mt-1">{model.desc}</CardDescription>
            </CardHeader>
            <CardContent className="pb-4 pt-2 border-t border-border/20">
              <div className="space-y-1.5 text-xs font-mono text-muted-foreground mt-2">
                <div className="flex justify-between"><span>Provider:</span> <span className="text-foreground">{model.provider}</span></div>
                <div className="flex justify-between"><span>Context Limit:</span> <span className="text-foreground">{model.context}</span></div>
                <div className="flex justify-between"><span>Latency:</span> <span className="text-primary font-medium">{model.speed}</span></div>
              </div>
            </CardContent>
            <CardFooter className="pt-3 border-t border-border/40 flex justify-end">
              <Button variant="ghost" size="sm" className="text-xs gap-1 hover:text-primary cursor-pointer">
                <Sliders className="h-3.5 w-3.5" />
                Configure Parameters
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  )
}
