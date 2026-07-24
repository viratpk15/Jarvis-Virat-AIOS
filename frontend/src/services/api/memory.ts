import { apiClient } from "./apiClient"
import type { MemoryStore } from "@/types/api"

/**
 * Cognitive Memory Service Module
 * Connects to SQLite and Embedding systems, exposing session context matrices.
 */

/**
 * Retrieves memory statistics, summarizations, and synchronization states for a session.
 * Note: Backed by GET /memory/{session_id} contract.
 * 
 * @param session_id Target session ID.
 * @returns Embeddings count and system summary.
 */
export const getMemoryCache = async (session_id: string): Promise<MemoryStore> => {
  return apiClient.get<MemoryStore>(`/memory/${session_id}`)
}

/**
 * Flushes memory registries and invalidates embedding indices for a session.
 * Note: Backed by DELETE /memory/{session_id} contract.
 * 
 * @param session_id Target session ID to flush.
 */
export const clearMemoryCache = async (session_id: string): Promise<void> => {
  return apiClient.del<void>(`/memory/${session_id}`)
}
