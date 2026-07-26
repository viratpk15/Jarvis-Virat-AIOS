/**
 * Jarvis AIOS — Tool Console Type Definitions
 */

export type PermissionLevel = "PUBLIC" | "USER" | "ADMIN" | "SYSTEM" | "INTERNAL"

export interface ToolMetadata {
  name: string
  display_name: string
  description: string
  category: string
  tags: string[]
  version: string
  author: string
  permission_level: PermissionLevel
  requires_approval: boolean
  enabled: boolean
  timeout_seconds: number
  supports_streaming: boolean
  supports_async: boolean
  supports_parallel: boolean
  supports_cancellation: boolean
  parameter_schema: Record<string, any>
  output_schema: Record<string, any>
  examples: Array<Record<string, any>>
  icon: string
  documentation_url: string
}

export interface ToolDetailsResponse {
  metadata: ToolMetadata
  schema: Record<string, any>
}
