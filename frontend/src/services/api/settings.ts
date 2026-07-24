import { apiClient } from "./apiClient"

/**
 * System Settings Service Module
 * Coordinates customizable workspace features and API tokens.
 */

export interface SystemSettings {
  theme: "dark" | "light" | "system"
  llmModel: string
  temperature: number
  maxTokens: number
  debugMode: boolean
}

/**
 * Retrieves client/server synchronization parameters.
 * Note: Backed by GET /settings contract.
 * 
 * @returns Settings values.
 */
export const getSystemSettings = async (): Promise<SystemSettings> => {
  return apiClient.get<SystemSettings>("/settings")
}

/**
 * Updates configurations.
 * Note: Backed by PATCH /settings contract.
 * 
 * @param settings Updated configuration settings.
 * @returns Updated settings.
 */
export const updateSystemSettings = async (settings: Partial<SystemSettings>): Promise<SystemSettings> => {
  return apiClient.patch<SystemSettings>("/settings", settings)
}
