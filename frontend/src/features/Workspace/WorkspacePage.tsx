import React, { useState, useEffect } from "react"
import { useNavigate } from "react-router"
import { motion, AnimatePresence } from "framer-motion"
import { Menu, ChevronLeft, ChevronRight, AlertCircle, RefreshCw } from "lucide-react"
import { useQueryClient } from "@tanstack/react-query"

import { Button } from "@/components/ui/button"
import { Sidebar } from "./components/Sidebar"
import { Header } from "./components/Header"
import { MessageArea } from "./components/MessageArea"
import { Composer } from "./components/Composer"
import { dashboardGridVariants } from "@/lib/motion"
import { streamChatMessage, type CancellationToken } from "@/services/api/sse"

import { queryKeys } from "@/services/queries/queryKeys"
import { UnauthorizedError } from "@/services/api/errors"
import {
  useConversationsQuery,
  useCreateConversationMutation,
  useDeleteConversationMutation,
  useRenameConversationMutation,
  useTogglePinMutation
} from "@/services/queries/chat"
import type { Conversation, Attachment, Message } from "@/types/api"

export default function WorkspacePage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [windowWidth, setWindowWidth] = useState(typeof window !== "undefined" ? window.innerWidth : 1200)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [inputText, setInputText] = useState("")

  // Real-time SSE streaming state
  const [isThinking, setIsThinking] = useState(false)
  const [isStreaming, setIsStreaming] = useState(false)
  const [streamingText, setStreamingText] = useState("")
  const [streamError, setStreamError] = useState<string | null>(null)
  const [cancelToken, setCancelToken] = useState<CancellationToken | null>(null)
  const [optimisticUserMsg, setOptimisticUserMsg] = useState<Message | null>(null)

  // Real backend queries & mutations
  const { data: conversations = [], isLoading: isLoadingConvs, isError: isConvError, error: convError, refetch } = useConversationsQuery()
  const createConvMutation = useCreateConversationMutation()
  const deleteConvMutation = useDeleteConversationMutation()
  const renameConvMutation = useRenameConversationMutation()
  const togglePinMutation = useTogglePinMutation()

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
    handleResize()
    return () => window.removeEventListener("resize", handleResize)
  }, [])

  // Auto-select initial conversation on load
  useEffect(() => {
    if (conversations.length > 0 && (!selectedId || !conversations.some((c) => c.id === selectedId))) {
      setSelectedId(conversations[0].id)
    }
  }, [conversations, selectedId])

  const selectedChat: Conversation | null = conversations.find((c) => c.id === selectedId) || (conversations[0] ?? null)

  const handleSelectChat = (id: string) => {
    if (isStreaming && cancelToken) {
      cancelToken.abort()
    }
    setIsThinking(false)
    setIsStreaming(false)
    setStreamingText("")
    setOptimisticUserMsg(null)
    setSelectedId(id)
  }

  const handleNewChat = () => {
    if (isStreaming && cancelToken) {
      cancelToken.abort()
    }
    setIsThinking(false)
    setIsStreaming(false)
    setStreamingText("")
    setOptimisticUserMsg(null)

    createConvMutation.mutate(undefined, {
      onSuccess: (newConv) => {
        setSelectedId(newConv.id)
      }
    })
  }

  const handleTogglePin = (id: string, e?: React.MouseEvent) => {
    if (e) e.stopPropagation()
    togglePinMutation.mutate(id)
  }

  const handleDeleteChat = (id: string, e?: React.MouseEvent) => {
    if (e) e.stopPropagation()
    deleteConvMutation.mutate(id, {
      onSuccess: () => {
        if (selectedId === id) {
          const remaining = conversations.filter((c) => c.id !== id)
          setSelectedId(remaining.length > 0 ? remaining[0].id : null)
        }
      }
    })
  }

  const handleRenameChat = (newTitle: string) => {
    if (!selectedId) return
    renameConvMutation.mutate({ sessionId: selectedId, title: newTitle })
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

  // Submit prompt using real-time SSE streaming
  const handleSend = (text: string, _attachedFiles: Attachment[]) => {
    const activeSessionId = selectedId || selectedChat?.id
    if (!activeSessionId || !text.trim()) return

    // Clear previous errors & reset stream buffers
    setStreamError(null)
    setIsThinking(true)
    setIsStreaming(false)
    setStreamingText("")

    const userTime = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    const optMsg: Message = {
      id: `user-opt-${Date.now()}`,
      role: "user",
      content: text,
      timestamp: userTime
    }
    setOptimisticUserMsg(optMsg)

    const tokenHandle = streamChatMessage(activeSessionId, text, {
      onThinking: () => {
        setIsThinking(true)
        setIsStreaming(false)
      },
      onToken: (tokenStr: string) => {
        setIsThinking(false)
        setIsStreaming(true)
        setStreamingText((prev) => prev + tokenStr)
      },
      onDone: () => {
        setIsThinking(false)
        setIsStreaming(false)
        setStreamingText("")
        setCancelToken(null)
        setOptimisticUserMsg(null)

        // Invalidate queries so final persisted messages are synced clean
        queryClient.invalidateQueries({ queryKey: queryKeys.conversations.list() })
        queryClient.invalidateQueries({ queryKey: queryKeys.conversations.detail(activeSessionId) })
      },
      onError: (err: Error) => {
        setIsThinking(false)
        setIsStreaming(false)
        setStreamingText("")
        setCancelToken(null)
        setStreamError(err.message || "Failed to stream response from server.")

        if (err instanceof UnauthorizedError) {
          localStorage.removeItem("jarvis_access_token")
          navigate("/auth")
        }
      }
    })

    setCancelToken(tokenHandle)
  }

  const handleStopGeneration = () => {
    if (cancelToken) {
      cancelToken.abort()
    }
    setIsThinking(false)
    setIsStreaming(false)
    setStreamingText("")
    setCancelToken(null)
    setOptimisticUserMsg(null)
  }

  const handleSelectPrompt = (prompt: string) => {
    setInputText(prompt)
  }

  const isMobile = windowWidth < 768

  // Active message list combining loaded history + optimistic user message
  const activeMessages: Message[] = selectedChat ? [
    ...selectedChat.messages,
    ...(optimisticUserMsg ? [optimisticUserMsg] : [])
  ] : []

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
              selectedId={selectedId || (selectedChat?.id ?? null)}
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
            className="absolute left-0 top-50 z-50 h-10 w-4 rounded-r-md border border-l-0 border-border/80 bg-sidebar hover:bg-secondary text-muted-foreground flex items-center justify-center cursor-pointer transition-colors shadow-sm focus:outline-none"
            title={sidebarOpen ? "Hide sidebar" : "Show sidebar"}
          >
            {sidebarOpen ? <ChevronLeft className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
          </button>
        )}

        {/* Global Error Banner if API connection fails */}
        {(streamError || isConvError) && (
          <div className="bg-destructive/15 border-b border-destructive/30 px-4 py-2 text-xs flex items-center justify-between text-destructive shrink-0">
            <div className="flex items-center gap-2">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <span>
                {streamError || convError?.message || "Backend communications error. Check server availability."}
              </span>
            </div>
            <Button
              variant="outline"
              size="xs"
              onClick={() => {
                setStreamError(null)
                refetch()
              }}
              className="gap-1 border-destructive/40 text-destructive hover:bg-destructive/10"
            >
              <RefreshCw className="h-3 w-3" />
              Retry
            </Button>
          </div>
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
              messages={activeMessages}
              isThinking={isThinking}
              isStreaming={isStreaming}
              streamingText={streamingText}
              onSelectPrompt={handleSelectPrompt}
              onNewChat={handleNewChat}
              onRegenerate={() => {
                if (selectedChat.messages.length > 0) {
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
              disabled={isLoadingConvs || isThinking || isStreaming}
              isStreaming={isThinking || isStreaming}
              onStopGeneration={handleStopGeneration}
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


