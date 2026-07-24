import { apiClient } from "./apiClient"
import type { Agent } from "@/types/api"

/**
 * AI Agents Service Module
 * Handles monitoring logs, scheduling queues, and active graph nodes metrics.
 */

/**
 * Retrieves the full list of active agent subroutines (Planner, Executor, researchers, etc).
 * Note: Backed by GET /agents contract.
 * 
 * @returns Array of agent configurations.
 */
export const listAgents = async (): Promise<Agent[]> => {
  return apiClient.get<Agent[]>("/agents")
}

/**
 * Retrieves target status information and steps completions for a single agent.
 * Note: Backed by GET /agents/{id}/state contract.
 * 
 * @param id Unique agent ID.
 * @returns Agent execution status and logs.
 */
export const getAgentState = async (id: string): Promise<Agent> => {
  return apiClient.get<Agent>(`/agents/${id}/state`)
}
