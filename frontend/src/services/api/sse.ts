/**
 * Server-Sent Events (SSE) Interface Foundation
 * Establishes standard structures for token-by-token streaming connections.
 * Note: Implementations will plug directly into Sprint 5.4.
 */

/**
 * Event Types emitted during chat/agent inference runs
 */
export type StreamEventType = 
  | "token"        // Word tokens emitted from LLM
  | "agent_state"  // Transition of graph nodes
  | "tool_output"  // Log lines from execution agents
  | "error"        // Failure alerts
  | "done"         // Execution completed cleanly

/**
 * Normalized event payload
 */
export interface StreamEvent {
  type: StreamEventType
  data: string
  timestamp: string
}

/**
 * Strategy for connection retry delays
 */
export interface ReconnectPolicy {
  maxRetries: number
  initialDelayMs: number
  maxDelayMs: number
  calculateNextDelay: (retryCount: number) => number
}

/**
 * Handler interface to abort streaming requests safely
 */
export interface CancellationToken {
  isCancelled: boolean
  abort: () => void
}

/**
 * Callback listeners registry for stream connections
 */
export interface StreamListeners {
  onToken?: (token: string) => void
  onAgentState?: (nodeName: string) => void
  onToolOutput?: (logLine: string) => void
  onError?: (error: Error) => void
  onDone?: () => void
}

/**
 * Parser transforming raw buffer chunks into structured StreamEvents
 */
export interface EventParser {
  parseChunk: (rawChunk: string) => StreamEvent[]
}

/**
 * Core Connection Manager Interface for Server-Sent Events (SSE)
 */
export interface ISSEClient {
  /**
   * Initializes a connection to the target streaming URL
   * 
   * @param path API route path (e.g. /chat/stream)
   * @param params Query/Body parameters
   * @param listeners Active listeners registry
   * @returns Cancel token handle
   */
  connect: (
    path: string,
    params: Record<string, unknown>,
    listeners: StreamListeners
  ) => CancellationToken

  /**
   * Terminate active streams immediately
   */
  disconnect: () => void
}
