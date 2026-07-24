import { apiClient } from "./apiClient"
import type { ConversationResponse, Conversation } from "@/types/api"

/**
 * Chat & Conversation Service Module
 * Coordinates message delivery and session history queries.
 */

/**
 * Dispatches a chat message prompt inside a specific session workspace.
 * 
 * @param session_id Unique identifier for the conversation thread.
 * @param message The user's query text content.
 * @returns Server response containing the generated answer.
 */
export const sendMessage = async (session_id: string, message: string): Promise<ConversationResponse> => {
  return apiClient.post<ConversationResponse>("/chat", {
    session_id,
    message
  })
}

/**
 * Retrieves the full list of active conversation sessions for the authenticated user.
 * Note: Backed by GET /sessions contract once enabled.
 * 
 * @returns Array of active conversation threads.
 */
export const listConversations = async (): Promise<Conversation[]> => {
  return apiClient.get<Conversation[]>("/sessions")
}

/**
 * Retrieves detailed conversation logs and histories for a specific session.
 * Note: Backed by GET /sessions/{session_id} contract.
 * 
 * @param session_id Unique session identifier.
 * @returns Target conversation log metadata and message lists.
 */
export const getConversationDetails = async (session_id: string): Promise<Conversation> => {
  return apiClient.get<Conversation>(`/sessions/${session_id}`)
}

/**
 * Deletes a session history trace.
 * Note: Backed by DELETE /sessions/{session_id} contract.
 * 
 * @param session_id Target session identifier to destroy.
 */
export const deleteConversation = async (session_id: string): Promise<void> => {
  return apiClient.del<void>(`/sessions/${session_id}`)
}
