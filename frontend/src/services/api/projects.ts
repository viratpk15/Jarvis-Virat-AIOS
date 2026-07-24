import { apiClient } from "./apiClient"
import type { Project } from "@/types/api"

/**
 * Projects & Workspaces Service Module
 * Handles workspace projects settings, completion telemetry, and tasks.
 */

/**
 * Retrieves the full list of active workspace projects.
 * Note: Backed by GET /projects contract.
 * 
 * @returns Array of project items.
 */
export const listProjects = async (): Promise<Project[]> => {
  return apiClient.get<Project[]>("/projects")
}

/**
 * Retrieves target configurations and tasks metadata for a single project.
 * Note: Backed by GET /projects/{id} contract.
 * 
 * @param id Unique project ID.
 * @returns Project details.
 */
export const getProject = async (id: string): Promise<Project> => {
  return apiClient.get<Project>(`/projects/${id}`)
}

/**
 * Creates a new project environment.
 * Note: Backed by POST /projects contract.
 * 
 * @param project Partial project options.
 * @returns Created project details.
 */
export const createProject = async (project: Omit<Project, "id">): Promise<Project> => {
  return apiClient.post<Project>("/projects", project)
}

/**
 * Destroys a project resource.
 * Note: Backed by DELETE /projects/{id} contract.
 * 
 * @param id Target ID to delete.
 */
export const deleteProject = async (id: string): Promise<void> => {
  return apiClient.del<void>(`/projects/${id}`)
}
