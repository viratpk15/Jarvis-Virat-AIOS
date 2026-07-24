import { useState } from "react"
import { Link, useLocation, Outlet } from "react-router"
import { motion, AnimatePresence } from "framer-motion"
import {
  LayoutDashboard,
  FolderOpen,
  Bot,
  Brain,
  ToyBrick,
  Settings,
  ChevronLeft,
  ChevronRight,
  User,
  LogOut,
  Bell,
  Cpu,
  Wifi,
  Database
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { cn } from "@/lib/utils"

export default function AppShell() {
  const [collapsed, setCollapsed] = useState(false)
  const location = useLocation()

  const navItems = [
    { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
    { name: "Workspace", path: "/workspace", icon: FolderOpen },
    { name: "AI Agents", path: "/agents", icon: Bot },
    { name: "Memory", path: "/memory", icon: Brain },
    { name: "Tool Registry", path: "/tools", icon: ToyBrick },
    { name: "Settings", path: "/settings", icon: Settings },
  ]

  // Get active item name for breadcrumbs
  const activeItem = navItems.find((item) => item.path === location.pathname) || navItems[0]

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-background text-foreground font-sans">
      {/* Sidebar */}
      <motion.aside
        animate={{ width: collapsed ? 64 : 260 }}
        transition={{ duration: 0.3, ease: "easeInOut" }}
        className="flex flex-col h-full border-r border-border/80 bg-sidebar select-none relative z-40"
      >
        {/* Toggle Button */}
        <Button
          onClick={() => setCollapsed(!collapsed)}
          variant="outline"
          size="icon"
          className="absolute -right-3.5 top-6 h-7 w-7 rounded-full bg-sidebar border border-border/80 hover:bg-secondary cursor-pointer z-50 hidden md:flex items-center justify-center text-muted-foreground shadow-sm"
        >
          {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </Button>

        {/* Logo Area */}
        <div className="h-16 flex items-center px-4 gap-3 border-b border-border/80 overflow-hidden shrink-0">
          <div className="flex items-center justify-center h-9 w-9 rounded-lg bg-primary text-primary-foreground font-bold text-lg shadow-lg shadow-primary/20 shrink-0">
            J
          </div>
          {!collapsed && (
            <motion.span
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.1 }}
              className="font-bold text-base tracking-tight bg-linear-to-r from-foreground via-foreground/90 to-primary bg-clip-text text-transparent"
            >
              Jarvis AIOS
            </motion.span>
          )}
        </div>

        {/* Nav Links */}
        <div className="flex-1 overflow-y-auto px-3 py-4">
          <nav className="space-y-1.5">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path || (item.path === "/dashboard" && location.pathname === "/")

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group relative cursor-pointer",
                    isActive
                      ? "bg-primary text-primary-foreground shadow-md shadow-primary/10"
                      : "text-muted-foreground hover:bg-secondary hover:text-foreground"
                  )}
                >
                  <Icon className={cn("h-4 w-4 shrink-0", isActive ? "" : "group-hover:text-primary transition-colors")} />
                  {!collapsed && (
                    <motion.span
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.05 }}
                    >
                      {item.name}
                    </motion.span>
                  )}
                  {collapsed && (
                    <div className="absolute left-16 px-2 py-1 bg-popover text-popover-foreground text-xs rounded border border-border opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50 shadow-md">
                      {item.name}
                    </div>
                  )}
                </Link>
              )
            })}
          </nav>
        </div>

        {/* User Footer */}
        <div className="p-3 border-t border-border/80 shrink-0">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <div className={cn(
                "flex items-center gap-3 p-2 rounded-lg hover:bg-secondary/60 cursor-pointer transition-all",
                collapsed ? "justify-center" : ""
              )}>
                <Avatar className="h-8 w-8 border border-primary/20">
                  <AvatarFallback className="bg-primary/10 text-primary font-semibold text-xs">U</AvatarFallback>
                </Avatar>
                {!collapsed && (
                  <div className="flex-1 text-left min-w-0">
                    <p className="text-xs font-semibold truncate text-foreground">Virat</p>
                    <p className="text-[10px] text-muted-foreground truncate">virat@jarvis.ai</p>
                  </div>
                )}
              </div>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-52 border-border/80 bg-popover/90 backdrop-blur-md">
              <DropdownMenuLabel className="font-mono text-xs uppercase tracking-wider text-muted-foreground">User Session</DropdownMenuLabel>
              <DropdownMenuSeparator className="bg-border/60" />
              <DropdownMenuItem className="cursor-pointer gap-2 text-xs">
                <User className="h-3.5 w-3.5" />
                Profile Details
              </DropdownMenuItem>
              <DropdownMenuItem className="cursor-pointer gap-2 text-xs">
                <Settings className="h-3.5 w-3.5" />
                Preference Settings
              </DropdownMenuItem>
              <DropdownMenuSeparator className="bg-border/60" />
              <DropdownMenuItem className="cursor-pointer gap-2 text-xs text-destructive hover:bg-destructive/10">
                <LogOut className="h-3.5 w-3.5" />
                Disconnect Session
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </motion.aside>

      {/* Main View Area */}
      <div className="flex-1 flex flex-col h-full bg-background relative overflow-hidden">
        {/* Top Header */}
        <header className="h-16 flex items-center justify-between px-6 border-b border-border/80 bg-background/50 backdrop-blur-md z-30 select-none">
          {/* Breadcrumbs */}
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span className="font-medium hover:text-foreground transition-colors">Jarvis</span>
            <span>/</span>
            <span className="font-semibold text-foreground">{activeItem.name}</span>
          </div>

          {/* Quick Actions */}
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-secondary cursor-pointer text-muted-foreground hover:text-foreground">
              <Bell className="h-4.5 w-4.5" />
            </Button>
            <Separator orientation="vertical" className="h-4 bg-border" />
            <div className="flex items-center gap-1.5 px-2.5 py-1 bg-secondary/40 border border-border/60 rounded-full text-[10px] font-mono font-medium text-emerald-500">
              <Wifi className="h-3 w-3" />
              CONNECTED
            </div>
          </div>
        </header>

        {/* Content Container */}
        <div className="flex-1 overflow-y-auto px-6 py-6">
          <main className="max-w-6xl mx-auto w-full pb-8">
            <AnimatePresence mode="wait">
              <motion.div
                key={location.pathname}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.15, ease: "easeOut" }}
              >
                <Outlet />
              </motion.div>
            </AnimatePresence>
          </main>
        </div>

        {/* Bottom Status bar */}
        <footer className="h-9 border-t border-border/80 bg-sidebar/85 backdrop-blur px-6 flex items-center justify-between text-[11px] font-mono text-muted-foreground select-none shrink-0">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5">
              <Cpu className="h-3 w-3 text-primary/80" />
              <span>CPU: 34%</span>
            </div>
            <div className="flex items-center gap-1.5">
              <Database className="h-3 w-3 text-primary/80" />
              <span>MEM: 15%</span>
            </div>
          </div>
          <div className="flex items-center gap-1">
            <span>JARVIS SYSTEM RUNTIME</span>
            <span className="h-1.5 w-1.5 bg-emerald-500 rounded-full animate-pulse ml-1" />
          </div>
        </footer>
      </div>
    </div>
  )
}
