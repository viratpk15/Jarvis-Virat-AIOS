import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { queryKeys } from "./queryKeys"
import {
  listConversations,
  getConversationDetails,
  createConversationApi,
  renameConversationApi,
  deleteConversationApi,
  pinConversationApi,
  sendMessageApi,
} from "../api/chat"
import type { Conversation, Message } from "@/types/api"
import { normalizeError, APIError } from "../api/errors"

/** Fetch all active conversation sessions. */
export const useConversationsQuery = () => {
  return useQuery<Conversation[], APIError>({
    queryKey: queryKeys.conversations.list(),
    queryFn: listConversations,
    staleTime: 1000 * 60 * 5,
  })
}

/** Fetch a single conversation session by ID. */
export const useConversationDetailQuery = (sessionId: string | null) => {
  return useQuery<Conversation | null, APIError>({
    queryKey: queryKeys.conversations.detail(sessionId || ""),
    queryFn: async () => {
      if (!sessionId) return null
      return await getConversationDetails(sessionId)
    },
    staleTime: 1000 * 60 * 5,
  })
}

/** Send a message to the backend /chat endpoint. */
export const useSendMessageMutation = () => {
  const queryClient = useQueryClient()

  return useMutation<
    { response: string; userMessage: Message; assistantMessage: Message },
    APIError,
    { session_id: string; message: string; attachedFiles?: Array<{ name: string; type: string }> }
  >({
    mutationFn: async ({ session_id, message, attachedFiles }) => {
      if (attachedFiles) {
        void attachedFiles
      }
      const userTime = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
      const userMessage: Message = { id: `user-${Date.now()}`, role: "user", content: message, timestamp: userTime }
      try {
        const apiResponse = await sendMessageApi(session_id, message)
        const assistantTime = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
        const assistantMessage: Message = { id: `assistant-${Date.now()}`, role: "assistant", content: apiResponse.response, timestamp: assistantTime }
        return { response: apiResponse.response, userMessage, assistantMessage }
      } catch (rawError) {
        throw normalizeError(rawError)
      }
    },
    onSettled: (_data, _error, variables) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.conversations.list() })
      if (variables?.session_id) {
        queryClient.invalidateQueries({ queryKey: queryKeys.conversations.detail(variables.session_id) })
      }
    },
  })
}

/** Create a new conversation thread. */
export const useCreateConversationMutation = () => {
  const queryClient = useQueryClient()
  return useMutation<Conversation, APIError, void>({
    mutationFn: async () => {
      return await createConversationApi()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.conversations.list() })
    },
  })
}

/** Delete a conversation thread. */
export const useDeleteConversationMutation = () => {
  const queryClient = useQueryClient()
  return useMutation<void, APIError, string>({
    mutationFn: async (sessionId) => {
      await deleteConversationApi(sessionId)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.conversations.list() })
    },
  })
}

/** Rename a conversation thread title. */
export const useRenameConversationMutation = () => {
  const queryClient = useQueryClient()
  return useMutation<void, APIError, { sessionId: string; title: string }>({
    mutationFn: async ({ sessionId, title }) => {
      await renameConversationApi(sessionId, title)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.conversations.list() })
    },
  })
}

/** Toggle pinned status for a conversation thread. */
export const useTogglePinMutation = () => {
  const queryClient = useQueryClient()
  return useMutation<void, APIError, string>({
    mutationFn: async (sessionId) => {
      const conv = await getConversationDetails(sessionId)
      await pinConversationApi(sessionId, !conv.pinned)
    },
    onSuccess: (_, sessionId) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.conversations.list() })
      queryClient.invalidateQueries({ queryKey: queryKeys.conversations.detail(sessionId) })
    },
  })
}
