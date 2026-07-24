import React, { useEffect, useRef } from "react"
import { motion } from "framer-motion"
import { Loader2 } from "lucide-react"
import { MessageBubble } from "./MessageBubble"
import { EmptyState } from "./EmptyState"
import { cursorVariants } from "@/lib/motion"

interface Message {
  id: string
  role: "user" | "assistant" | "system"
  content: string
  timestamp: string
}

interface MessageAreaProps {
  messages: Message[]
  isThinking: boolean
  isStreaming: boolean
  streamingText: string
  onSelectPrompt: (prompt: string) => void
  onNewChat: () => void
  onRegenerate: () => void
}

export const MessageArea: React.FC<MessageAreaProps> = ({
  messages,
  isThinking,
  isStreaming,
  streamingText,
  onSelectPrompt,
  onNewChat,
  onRegenerate
}) => {
  const containerRef = useRef<HTMLDivElement>(null)

  // Scroll to bottom when messages list size updates or streaming updates
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight
    }
  }, [messages, isThinking, isStreaming, streamingText])

  if (messages.length === 0) {
    return <EmptyState onSelectPrompt={onSelectPrompt} onNewChat={onNewChat} />
  }

  return (
    <div
      ref={containerRef}
      className="flex-1 overflow-y-auto px-4 py-6 space-y-6 scrollbar-thin select-text"
    >
      {/* Messages Stack */}
      {messages.map((msg) => (
        <MessageBubble key={msg.id} message={msg} onRegenerate={onRegenerate} />
      ))}

      {/* Thinking state bubble */}
      {isThinking && (
        <div className="flex gap-3 max-w-3xl mr-auto select-none">
          <div className="h-8 w-8 rounded-lg border font-mono text-xs flex items-center justify-center shrink-0 shadow-sm bg-primary text-primary-foreground border-primary/20">
            A
          </div>
          <div className="space-y-1.5 font-mono text-xs text-muted-foreground bg-secondary/15 border border-border/50 rounded-xl p-3.5 flex items-center gap-3">
            <Loader2 className="h-4 w-4 text-primary animate-spin" />
            <div className="space-y-0.5">
              <span className="font-bold text-foreground block">Thinking...</span>
              <span className="text-[10px] text-muted-foreground block">Resolving nodes: evaluate_context_vectors</span>
            </div>
          </div>
        </div>
      )}

      {/* Streaming state bubble */}
      {isStreaming && streamingText && (
        <div className="flex gap-3 max-w-3xl mr-auto">
          <div className="h-8 w-8 rounded-lg border font-mono text-xs flex items-center justify-center shrink-0 shadow-sm bg-primary text-primary-foreground border-primary/20">
            A
          </div>
          <div className="space-y-1 min-w-0">
            <div className="relative px-4 py-3 text-sm leading-relaxed text-foreground bg-transparent border border-transparent">
              {/* Split lines to mock paragraphs during streaming */}
              {streamingText.split("\n").map((line, idx) => (
                <p key={idx} className="my-1 whitespace-pre-wrap">
                  {line}
                  {idx === streamingText.split("\n").length - 1 && (
                    <motion.span
                      variants={cursorVariants}
                      animate="blink"
                      className="inline-block w-2 h-4 ml-0.5 bg-primary rounded-xs align-middle"
                    />
                  )}
                </p>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
