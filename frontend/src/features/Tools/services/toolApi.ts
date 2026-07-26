import { useQuery } from "@tanstack/react-query"
import { apiClient } from "@/services/api/apiClient"
import type { ToolMetadata, ToolDetailsResponse } from "../types/tools.types"

/**
 * Fetch all registered tools from GET /api/v1/tools
 */
export async function fetchTools(category?: string | null, tag?: string | null, query?: string): Promise<ToolMetadata[]> {
  const params = new URLSearchParams()
  if (category) params.append("category", category)
  if (tag) params.append("tag", tag)
  if (query) params.append("query", query)

  const queryString = params.toString()
  const endpoint = `/api/v1/tools${queryString ? `?${queryString}` : ""}`
  return apiClient.get<ToolMetadata[]>(endpoint)
}

/**
 * Fetch unique tool categories from GET /api/v1/tools/categories
 */
export async function fetchCategories(): Promise<string[]> {
  return apiClient.get<string[]>("/api/v1/tools/categories")
}

/**
 * Fetch specific tool metadata and OpenAPI schema from GET /api/v1/tools/{name}
 */
export async function fetchToolDetails(toolName: string): Promise<ToolDetailsResponse> {
  return apiClient.get<ToolDetailsResponse>(`/api/v1/tools/${toolName}`)
}

/**
 * React Query Hook for discovery tool list
 */
export function useToolsQuery(category?: string | null, tag?: string | null, query?: string) {
  return useQuery({
    queryKey: ["tools", category, tag, query],
    queryFn: () => fetchTools(category, tag, query),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

/**
 * React Query Hook for categories list
 */
export function useCategoriesQuery() {
  return useQuery({
    queryKey: ["tool-categories"],
    queryFn: fetchCategories,
    staleTime: 10 * 60 * 1000, // 10 minutes
  })
}

/**
 * React Query Hook for tool details schema
 */
export function useToolDetailsQuery(toolName: string | null) {
  return useQuery({
    queryKey: ["tool-details", toolName],
    queryFn: () => fetchToolDetails(toolName!),
    enabled: Boolean(toolName),
    staleTime: 5 * 60 * 1000,
  })
}
