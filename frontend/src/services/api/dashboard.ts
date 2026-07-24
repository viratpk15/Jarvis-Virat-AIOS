import { apiClient } from "./apiClient"
import type { DashboardResponse } from "@/types/api"

/**
 * System Telemetry & Dashboard Service Module
 * Aggregates core system stats, memory allocations, CPU/load parameters, and loaded tools list.
 */

/**
 * Fetches dashboard aggregation statistics from the Jarvis runtime.
 * Note: Backed by GET /system/telemetry contract.
 * 
 * @returns Combined stats for tools, memory, agents, and overall system status.
 */
export const getDashboardStats = async (): Promise<DashboardResponse> => {
  return apiClient.get<DashboardResponse>("/system/telemetry")
}
