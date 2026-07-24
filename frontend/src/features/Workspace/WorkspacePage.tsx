import React, { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Menu, ChevronLeft, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Sidebar } from "./components/Sidebar"
import { Header } from "./components/Header"
import { MessageArea } from "./components/MessageArea"
import { Composer } from "./components/Composer"
import { dashboardGridVariants } from "@/lib/motion"

interface Message {
  id: string
  role: "user" | "assistant" | "system"
  content: string
  timestamp: string
}

interface Attachment {
  id: string
  name: string
  type: "pdf" | "image" | "zip" | "markdown" | "code"
}

interface Conversation {
  id: string
  title: string
  preview: string
  time: string
  pinned: boolean
  model: string
  unread: boolean
  group: "Today" | "Yesterday" | "Last Week" | "Older"
  messages: Message[]
}

export default function WorkspacePage() {
  const [windowWidth, setWindowWidth] = useState(typeof window !== "undefined" ? window.innerWidth : 1200)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [selectedId, setSelectedId] = useState<string | null>("c1")
  const [inputText, setInputText] = useState("")

  // Simulation states
  const [isThinking, setIsThinking] = useState(false)
  const [isStreaming, setIsStreaming] = useState(false)
  const [streamingText, setStreamingText] = useState("")

  const [conversations, setConversations] = useState<Conversation[]>([
    {
      id: "c1",
      title: "Debug FastAPI memory leak in vector index cache",
      preview: "I analyzed the memory dump files. The issue stems from the cache registry indexer holding strong references...",
      time: "10m ago",
      pinned: true,
      model: "Gemini 2.5 Pro",
      unread: false,
      group: "Today",
      messages: [
        {
          id: "m1",
          role: "user",
          content: "Can you analyze why our FastAPI kernel memory builds up after index cache sync loops?",
          timestamp: "10:20 AM"
        },
        {
          id: "m2",
          role: "assistant",
          content: "I analyzed the memory dump files. The issue stems from the cache registry indexer holding strong references to old context vectors rather than utilizing weak reference caches.\n\nHere is the offending code block inside `MemoryManager`:\n```python\nclass MemoryManager:\n    def __init__(self):\n        self._registry = {} # Holds strong references\n\n    def sync_vectors(self, vectors):\n        for vec in vectors:\n            self._registry[vec.id] = vec # Prevents garbage collection\n```\n\nTo resolve this memory leak, we should refactor it using Python's `weakref` dict:\n```python\nimport weakref\n\nclass MemoryManager:\n    def __init__(self):\n        self._registry = weakref.WeakValueDictionary() # Resolves memory leak\n```\nThis enables Python's garbage collector to release vectors once they are dereferenced elsewhere.",
          timestamp: "10:22 AM"
        }
      ]
    },
    {
      id: "c2",
      title: "Integrate framer-motion page variants in app shell",
      preview: "We should declare a centralized dashboardGridVariants inside src/lib/motion.ts that cascades...",
      time: "2h ago",
      pinned: true,
      model: "Gemini 2.5 Flash",
      unread: true,
      group: "Today",
      messages: [
        {
          id: "m3",
          role: "user",
          content: "How do we define standardized staggered transitions for our home dashboard widgets?",
          timestamp: "8:10 AM"
        },
        {
          id: "m4",
          role: "assistant",
          content: "We should declare a centralized `dashboardGridVariants` inside `src/lib/motion.ts` that cascades entry offsets to all children elements. We can then apply staggered transitions like this:\n```typescript\nexport const dashboardGridVariants: Variants = {\n  initial: { opacity: 0 },\n  animate: {\n    opacity: 1,\n    transition: {\n      staggerChildren: 0.03\n    }\n  }\n}\n```\nThis is fully configured and ready for reuse across all widgets.",
          timestamp: "8:12 AM"
        }
      ]
    },
    {
      id: "c3",
      title: "Draft system prompt instructions for agents",
      preview: "Initialize the OS guide using AGENTS.md rules. Specify LangGraph composition...",
      time: "Yesterday",
      pinned: false,
      model: "Gemini 2.5 Pro",
      unread: false,
      group: "Yesterday",
      messages: []
    }
  ])

  // Track window size resize events for panels layout responsive boundaries
  useEffect(() => {
    const handleResize = () => {
      setWindowWidth(window.innerWidth)
      if (window.innerWidth < 1024) {
        setSidebarOpen(false)
      } else {
        setSidebarOpen(true)
      }
    }
    window.addEventListener("resize", handleResize)
    // Run once on mount
    handleResize()
    return () => window.removeEventListener("resize", handleResize)
  }, [])

  const selectedChat = conversations.find((c) => c.id === selectedId) || null

  const handleSelectChat = (id: string) => {
    setSelectedId(id)
    // Clear unread mark
    setConversations((prev) =>
      prev.map((c) => (c.id === id ? { ...c, unread: false } : c))
    )
  }

  const handleNewChat = () => {
    const newChat: Conversation = {
      id: `c-${Date.now()}`,
      title: "New Conversation",
      preview: "Session initialized. Cognitive engine standby.",
      time: "Just now",
      pinned: false,
      model: "Gemini 2.5 Pro",
      unread: false,
      group: "Today",
      messages: []
    }
    setConversations((prev) => [newChat, ...prev])
    setSelectedId(newChat.id)
  }

  const handleTogglePin = (id: string, e?: React.MouseEvent) => {
    if (e) e.stopPropagation()
    setConversations((prev) =>
      prev.map((c) => (c.id === id ? { ...c, pinned: !c.pinned } : c))
    )
  }

  const handleDeleteChat = (id: string, e?: React.MouseEvent) => {
    if (e) e.stopPropagation()
    setConversations((prev) => prev.filter((c) => c.id !== id))
    if (selectedId === id) {
      setSelectedId(null)
    }
  }

  const handleRenameChat = (newTitle: string) => {
    if (!selectedId) return
    setConversations((prev) =>
      prev.map((c) => (c.id === selectedId ? { ...c, title: newTitle } : c))
    )
  }

  const handleExport = (format: "markdown" | "json") => {
    if (!selectedChat) return
    let blob: Blob
    let filename: string
    
    if (format === "json") {
      blob = new Blob([JSON.stringify(selectedChat, null, 2)], { type: "application/json" })
      filename = `${selectedChat.title.toLowerCase().replace(/\s+/g, "-")}.json`
    } else {
      const mdContent = selectedChat.messages
        .map((m) => `### ${m.role.toUpperCase()} (${m.timestamp})\n\n${m.content}`)
        .join("\n\n---\n\n")
      blob = new Blob([mdContent], { type: "text/markdown" })
      filename = `${selectedChat.title.toLowerCase().replace(/\s+/g, "-")}.md`
    }

    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  }

  // Submit new prompt and simulate reply stream
  const handleSend = (text: string, attachedFiles: Attachment[]) => {
    if (!selectedId || (!text.trim() && attachedFiles.length === 0)) return

    const timeString = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    
    // Construct attachments string if any exist
    let fullContent = text
    if (attachedFiles.length > 0) {
      const filesStr = attachedFiles.map((f) => `\`${f.name}\` (${f.type})`).join(", ")
      fullContent = `[Attached: ${filesStr}]\n\n${text}`
    }

    const userMsg: Message = {
      id: `m-${Date.now()}`,
      role: "user",
      content: fullContent,
      timestamp: timeString
    }

    // Update messages list
    setConversations((prev) =>
      prev.map((c) => {
        if (c.id === selectedId) {
          const updatedMsgs = [...c.messages, userMsg]
          return {
            ...c,
            preview: text || `Uploaded ${attachedFiles.length} file(s)`,
            time: "Just now",
            messages: updatedMsgs
          }
        }
        return c
      })
    )

    // Trigger simulated thinking phase
    setIsThinking(true)

    // Simulate logs in Inspector
    const logsEvent = new CustomEvent("inspector-log", {
      detail: { text: `[LLM_ENGINE] Inference request received. Prompt length: ${text.length} chars.` }
    })
    window.dispatchEvent(logsEvent)

    setTimeout(() => {
      setIsThinking(false)
      setIsStreaming(true)

      const replyTemplate = `I received your workspace instruction regarding: "${text}".

Let me scan the active context registry files...
All virtual subroutines are fully nominal. Here is the recommended execution path:
1. **Load dependency tree**: Scans import mappings inside \`src/App.tsx\`.
2. **Compile type verification suites**: Performs type assertions checking.
3. **Execute lint suites**: Runs local \`oxlint\` checks.

Let me know if you would like me to compile this code or start a test suite run.`

      let currentText = ""
      const words = replyTemplate.split(" ")
      let wordIndex = 0

      const timer = setInterval(() => {
        if (wordIndex < words.length) {
          currentText += (wordIndex === 0 ? "" : " ") + words[wordIndex]
          setStreamingText(currentText)
          wordIndex++
        } else {
          clearInterval(timer)
          setIsStreaming(false)
          setStreamingText("")

          // Push the final assistant reply
          const assistantMsg: Message = {
            id: `m-${Date.now() + 1}`,
            role: "assistant",
            content: replyTemplate,
            timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
          }

          setConversations((prev) =>
            prev.map((c) => {
              if (c.id === selectedId) {
                return {
                  ...c,
                  preview: replyTemplate.substring(0, 80) + "...",
                  time: "Just now",
                  messages: [...c.messages, assistantMsg]
                }
              }
              return c
            })
          )
        }
      }, 70) // Fast word stream animation
    }, 2000)
  }

  const handleSelectPrompt = (prompt: string) => {
    setInputText(prompt)
  }

  const isMobile = windowWidth < 768

  return (
    <motion.div
      variants={dashboardGridVariants}
      initial="initial"
      animate="animate"
      className="flex h-full w-full bg-background overflow-hidden relative"
    >
      {/* 1. Sidebar - Left Side */}
      <AnimatePresence mode="wait">
        {sidebarOpen && (
          <motion.div
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: isMobile ? "100%" : 280, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className={`h-full shrink-0 z-40 ${isMobile ? "absolute inset-0 bg-background" : "relative"}`}
          >
            <Sidebar
              conversations={conversations}
              selectedId={selectedId}
              onSelect={(id) => {
                handleSelectChat(id)
                if (isMobile) setSidebarOpen(false)
              }}
              onNewChat={handleNewChat}
              onTogglePin={handleTogglePin}
              onDelete={handleDeleteChat}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* 2. Main Workspace Split Panel */}
      <div className="flex-1 flex flex-col h-full overflow-hidden relative bg-background">
        
        {/* Toggle Sidebar handle for Desktop/Tablet */}
        {!isMobile && (
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="absolute left-0 top-[200px] z-50 h-10 w-4 rounded-r-md border border-l-0 border-border/80 bg-sidebar hover:bg-secondary text-muted-foreground flex items-center justify-center cursor-pointer transition-colors shadow-sm focus:outline-none"
            title={sidebarOpen ? "Hide sidebar" : "Show sidebar"}
          >
            {sidebarOpen ? <ChevronLeft className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
          </button>
        )}

        {selectedChat ? (
          <>
            {/* Header */}
            <div className="flex items-center bg-background shrink-0">
              {isMobile && (
                <Button
                  onClick={() => setSidebarOpen(true)}
                  variant="ghost"
                  size="icon"
                  className="h-9 w-9 ml-2 text-muted-foreground cursor-pointer"
                >
                  <Menu className="h-4.5 w-4.5" />
                </Button>
              )}
              <div className="flex-1 min-w-0">
                <Header
                  title={selectedChat.title}
                  model={selectedChat.model}
                  scope="Personal Cloud AI"
                  pinned={selectedChat.pinned}
                  onTogglePin={() => handleTogglePin(selectedChat.id)}
                  onRename={handleRenameChat}
                  onDelete={() => handleDeleteChat(selectedChat.id)}
                  onExport={handleExport}
                />
              </div>
            </div>

            {/* Conversation Messages List viewport */}
            <MessageArea
              messages={selectedChat.messages}
              isThinking={isThinking}
              isStreaming={isStreaming}
              streamingText={streamingText}
              onSelectPrompt={handleSelectPrompt}
              onNewChat={handleNewChat}
              onRegenerate={() => {
                if (selectedChat.messages.length > 0) {
                  // Simulate regeneration
                  const lastUserMsg = [...selectedChat.messages].reverse().find((m) => m.role === "user")
                  if (lastUserMsg) {
                    handleSend(lastUserMsg.content, [])
                  }
                }
              }}
            />

            {/* Prompt Composer input panel */}
            <Composer
              onSend={handleSend}
              inputText={inputText}
              setInputText={setInputText}
              disabled={isThinking || isStreaming}
            />
          </>
        ) : (
          <div className="flex-1 flex flex-col h-full bg-background justify-between">
            {isMobile && (
              <div className="p-3 border-b border-border/60 flex items-center shrink-0">
                <Button
                  onClick={() => setSidebarOpen(true)}
                  variant="ghost"
                  size="icon"
                  className="h-9 w-9 text-muted-foreground cursor-pointer"
                >
                  <Menu className="h-4.5 w-4.5" />
                </Button>
                <span className="font-bold text-xs uppercase tracking-wider text-muted-foreground font-mono ml-2">Jarvis OS</span>
              </div>
            )}
            <MessageArea
              messages={[]}
              isThinking={false}
              isStreaming={false}
              streamingText=""
              onSelectPrompt={handleSelectPrompt}
              onNewChat={handleNewChat}
              onRegenerate={() => {}}
            />
            <Composer
              onSend={handleSend}
              inputText={inputText}
              setInputText={setInputText}
              disabled={false}
            />
          </div>
        )}
      </div>
    </motion.div>
  )
}
