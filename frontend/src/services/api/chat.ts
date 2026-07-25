import { apiClient } from "./apiClient"
import type { ConversationResponse, Conversation } from "@/types/api"

// API functions for conversation management
export const listConversations = async (): Promise<Conversation[]> => {
  return apiClient.get<Conversation[]>("/conversations")
}

export const getConversationDetails = async (session_id: string): Promise<Conversation> => {
  return apiClient.get<Conversation>(`/conversations/${session_id}`)
}

export const createConversationApi = async (): Promise<Conversation> => {
  return apiClient.post<Conversation>("/conversations")
}

export const renameConversationApi = async (session_id: string, title: string): Promise<Conversation> => {
  return apiClient.patch<Conversation>(`/conversations/${session_id}/rename`, { title })
}

export const deleteConversationApi = async (session_id: string): Promise<void> => {
  return apiClient.del<void>(`/conversations/${session_id}`)
}

export const pinConversationApi = async (session_id: string, pinned: boolean): Promise<Conversation> => {
  return apiClient.post<Conversation>(`/conversations/${session_id}/pin`, { pinned })
}

/**
 * Dispatches a chat message prompt to the real backend /chat endpoint.
 *
 * @param session_id Unique session identifier bound to user token.
 * @param message User prompt content.
 * @returns Generated backend response payload.
 */
export const sendMessageApi = async (session_id: string, message: string): Promise<ConversationResponse> => {
  return apiClient.post<ConversationResponse>("/chat", {
    session_id,
    message,
  })
}

export const sendMessage = sendMessageApi
