import React, { useState, useRef, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Send, Paperclip, Mic, FileText, Image, Archive, Code, X, Sparkles, Square } from "lucide-react"
import { attachmentVariants } from "@/lib/motion"

interface Attachment {
  id: string
  name: string
  type: "pdf" | "image" | "zip" | "markdown" | "code"
}

interface ComposerProps {
  onSend: (text: string, attachments: Attachment[]) => void
  inputText: string
  setInputText: (text: string) => void
  disabled: boolean
  isStreaming?: boolean
  onStopGeneration?: () => void
}

export const Composer: React.FC<ComposerProps> = ({
  onSend,
  inputText,
  setInputText,
  disabled,
  isStreaming = false,
  onStopGeneration
}) => {
  const [attachments, setAttachments] = useState<Attachment[]>([])
  const [isDragOver, setIsDragOver] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const quickPrompts = [
    { label: "Explain this code", prompt: "Please explain this code block and detail its complexity." },
    { label: "Generate tests", prompt: "Can you generate a comprehensive unit test suite for this module?" },
    { label: "Review architecture", prompt: "Perform an architectural and design patterns review of this structure." },
    { label: "Debug error", prompt: "Explain this stack trace error and suggest robust mitigation fixes." }
  ]

  // Auto resize height of textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 180)}px`
    }
  }, [inputText])

  const handleSend = () => {
    if (inputText.trim() || attachments.length > 0) {
      onSend(inputText.trim(), attachments)
      setInputText("")
      setAttachments([])
      if (textareaRef.current) {
        textareaRef.current.focus()
      }
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      if (!disabled && !isStreaming) {
        handleSend()
      }
    }
  }

  // Simulate file upload placeholder attachments
  const handleAttachMockFile = () => {
    const mockFiles: Attachment[] = [
      { id: `f-${Date.now()}`, name: "document.pdf", type: "pdf" },
      { id: `f-${Date.now() + 1}`, name: "screenshot.png", type: "image" },
      { id: `f-${Date.now() + 2}`, name: "app-backup.zip", type: "zip" },
      { id: `f-${Date.now() + 3}`, name: "AppShell.tsx", type: "code" }
    ]
    // Add random mock file
    const randomFile = mockFiles[Math.floor(Math.random() * mockFiles.length)]
    setAttachments((prev) => [...prev, randomFile])
  }

  const removeAttachment = (id: string) => {
    setAttachments((prev) => prev.filter((item) => item.id !== id))
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = () => {
    setIsDragOver(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
    // Simulate drop attachment
    const mockFiles: Attachment[] = [
      { id: `f-${Date.now()}`, name: "dragged-file.zip", type: "zip" },
      { id: `f-${Date.now() + 1}`, name: "index.md", type: "markdown" }
    ]
    const randomFile = mockFiles[Math.floor(Math.random() * mockFiles.length)]
    setAttachments((prev) => [...prev, randomFile])
  }

  const getAttachmentIcon = (type: Attachment["type"]) => {
    const classStr = "h-3.5 w-3.5"
    switch (type) {
      case "pdf":
      case "markdown":
        return <FileText className={`${classStr} text-red-400`} />
      case "image":
        return <Image className={`${classStr} text-emerald-400`} />
      case "zip":
        return <Archive className={`${classStr} text-amber-400`} />
      case "code":
        return <Code className={`${classStr} text-blue-400`} />
    }
  }

  const getAttachmentBadgeBg = (type: Attachment["type"]) => {
    switch (type) {
      case "pdf":
      case "markdown":
        return "bg-red-500/5 border-red-500/15"
      case "image":
        return "bg-emerald-500/5 border-emerald-500/15"
      case "zip":
        return "bg-amber-500/5 border-amber-500/15"
      case "code":
        return "bg-blue-500/5 border-blue-500/15"
    }
  }

  return (
    <div className="p-4 border-t border-border/80 bg-background/50 backdrop-blur-md shrink-0 space-y-3.5">
      {/* Suggestions Row */}
      {inputText.trim() === "" && attachments.length === 0 && !isStreaming && (
        <div className="flex items-center gap-2 overflow-x-auto py-1 scrollbar-none select-none">
          {quickPrompts.map((item, idx) => (
            <button
              key={idx}
              onClick={() => setInputText(item.prompt)}
              className="px-2.5 py-1 text-[10px] font-mono font-semibold bg-secondary/30 hover:bg-secondary/70 border border-border/60 hover:border-primary/30 rounded-lg text-muted-foreground hover:text-foreground cursor-pointer transition-all flex items-center gap-1 shrink-0"
            >
              <Sparkles className="h-3 w-3 text-primary/70" />
              {item.label}
            </button>
          ))}
        </div>
      )}

      {/* Composer Input Area */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`relative border rounded-xl bg-card/35 transition-all duration-300 ${isDragOver ? "border-primary/80 ring-1 ring-primary/40 bg-primary/2" : "border-border/80 hover:border-border"}`}
      >
        {/* Upload overlay */}
        {isDragOver && (
          <div className="absolute inset-0 bg-primary/2 flex items-center justify-center pointer-events-none rounded-xl">
            <span className="text-xs font-mono font-bold text-primary animate-pulse">
              DROP TO ATTACH FILE
            </span>
          </div>
        )}

        {/* Text Area */}
        <textarea
          ref={textareaRef}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Message Jarvis or instruct agent..."
          rows={1}
          disabled={disabled || isStreaming}
          className="w-full resize-none bg-transparent px-4 pt-4 pb-2 border-none outline-none text-sm text-foreground placeholder:text-muted-foreground/60 max-h-45 overflow-y-auto"
        />

        {/* Attachment chips viewport */}
        <AnimatePresence>
          {attachments.length > 0 && (
            <div className="px-4 py-2 border-t border-border/40 flex flex-wrap gap-2 select-none">
              {attachments.map((item) => (
                <motion.div
                  key={item.id}
                  variants={attachmentVariants}
                  initial="initial"
                  animate="animate"
                  exit="exit"
                >
                  <div className={`flex items-center gap-1.5 px-2 py-0.5 border rounded-lg text-[10px] font-mono font-semibold ${getAttachmentBadgeBg(item.type)}`}>
                    {getAttachmentIcon(item.type)}
                    <span className="text-foreground max-w-30 truncate">{item.name}</span>
                    <button
                      onClick={() => removeAttachment(item.id)}
                      className="p-0.5 rounded-full hover:bg-secondary/80 text-muted-foreground hover:text-foreground cursor-pointer focus:outline-none"
                    >
                      <X className="h-2.5 w-2.5" />
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </AnimatePresence>

        {/* Actions bar at bottom */}
        <div className="px-4 pb-3 pt-1 flex items-center justify-between border-t border-transparent select-none text-[10px] font-mono text-muted-foreground/60">
          <div className="flex items-center gap-1.5">
            {/* Attach button */}
            <button
              onClick={handleAttachMockFile}
              disabled={disabled || isStreaming}
              className="p-1.5 rounded-lg hover:bg-secondary/60 text-muted-foreground hover:text-foreground cursor-pointer focus:outline-none transition-colors disabled:opacity-40"
              title="Attach File Mock"
            >
              <Paperclip className="h-4 w-4" />
            </button>

            {/* Voice Notes */}
            <button
              disabled={disabled || isStreaming}
              className="p-1.5 rounded-lg hover:bg-secondary/60 text-muted-foreground hover:text-foreground cursor-pointer focus:outline-none transition-colors disabled:opacity-40"
              title="Voice Prompt Placeholder"
            >
              <Mic className="h-4 w-4" />
            </button>
          </div>

          <div className="flex items-center gap-3">
            {/* Characters Counter */}
            <span className="hidden sm:inline">
              {inputText.length} chars
            </span>

            {/* Stop Generation or Send Button */}
            {isStreaming ? (
              <button
                onClick={onStopGeneration}
                className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-destructive/15 hover:bg-destructive/25 text-destructive border border-destructive/30 transition-all cursor-pointer focus:outline-none focus:ring-1 focus:ring-destructive font-semibold text-xs"
                title="Stop Generating"
              >
                <Square className="h-3 w-3 fill-current" />
                <span>Stop</span>
              </button>
            ) : (
              <button
                onClick={handleSend}
                disabled={disabled || (!inputText.trim() && attachments.length === 0)}
                className="p-1.5 rounded-lg bg-primary hover:bg-primary-foreground text-primary-foreground hover:text-primary transition-all disabled:opacity-40 disabled:hover:bg-primary disabled:hover:text-primary-foreground disabled:cursor-not-allowed cursor-pointer focus:outline-none focus:ring-1 focus:ring-primary shadow shadow-primary/10"
                title="Send Command"
              >
                <Send className="h-3.5 w-3.5" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

