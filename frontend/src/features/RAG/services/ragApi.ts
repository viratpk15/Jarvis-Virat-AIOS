import { useQuery } from "@tanstack/react-query"
import { apiClient } from "@/services/api/apiClient"
import { queryKeys } from "@/services/queries/queryKeys"
import type {
  KnowledgeBase,
  Dataset,
  Document,
  Chunk,
  HybridSearchResult,
  RAGEvaluation,
  KnowledgeGraphData,
} from "../types/rag.types"

export async function fetchKnowledgeBases(): Promise<KnowledgeBase[]> {
  return apiClient.get<KnowledgeBase[]>("/api/v1/rag/knowledge-bases")
}

export async function fetchDatasets(kbId?: string | null): Promise<Dataset[]> {
  const url = kbId ? `/api/v1/rag/datasets?kb_id=${kbId}` : "/api/v1/rag/datasets"
  return apiClient.get<Dataset[]>(url)
}

export async function fetchDocuments(datasetId?: string | null): Promise<Document[]> {
  const url = datasetId ? `/api/v1/rag/documents?dataset_id=${datasetId}` : "/api/v1/rag/documents"
  return apiClient.get<Document[]>(url)
}

export async function fetchChunks(documentId?: string | null): Promise<Chunk[]> {
  const url = documentId ? `/api/v1/rag/chunks?document_id=${documentId}` : "/api/v1/rag/chunks"
  return apiClient.get<Chunk[]>(url)
}

export async function previewChunkingApi(payload: {
  text: string
  chunk_size: number
  overlap: number
  strategy: string
}): Promise<any[]> {
  return apiClient.post<any[]>("/api/v1/rag/chunk-preview", payload)
}

export async function runHybridSearchApi(payload: {
  query: string
  kb_id?: string | null
  top_k: number
  alpha: number
  use_reranker: boolean
}): Promise<HybridSearchResult> {
  return apiClient.post<HybridSearchResult>("/api/v1/rag/hybrid-search", payload)
}

export async function fetchRAGAnalytics(): Promise<any> {
  return apiClient.get<any>("/api/v1/rag/analytics")
}

export async function fetchKnowledgeGraph(kbId: string = "kb_enterprise_01"): Promise<KnowledgeGraphData> {
  return apiClient.get<KnowledgeGraphData>(`/api/v1/rag/graph?kb_id=${kbId}`)
}

export async function fetchEvaluations(): Promise<RAGEvaluation[]> {
  return apiClient.get<RAGEvaluation[]>("/api/v1/rag/evaluations")
}

// React Query Hooks — keyed via central queryKeys factory
export function useKnowledgeBasesQuery() {
  return useQuery({
    queryKey: queryKeys.rag.knowledgeBases(),
    queryFn: fetchKnowledgeBases,
  })
}

export function useDatasetsQuery(kbId?: string | null) {
  return useQuery({
    queryKey: queryKeys.rag.datasets(kbId),
    queryFn: () => fetchDatasets(kbId),
  })
}

export function useDocumentsQuery(datasetId?: string | null) {
  return useQuery({
    queryKey: queryKeys.rag.documents(datasetId),
    queryFn: () => fetchDocuments(datasetId),
  })
}

export function useChunksQuery(documentId?: string | null) {
  return useQuery({
    queryKey: queryKeys.rag.chunks(documentId),
    queryFn: () => fetchChunks(documentId),
  })
}

export function useRAGAnalyticsQuery() {
  return useQuery({
    queryKey: queryKeys.rag.analytics(),
    queryFn: fetchRAGAnalytics,
  })
}

export function useKnowledgeGraphQuery(kbId: string = "kb_enterprise_01") {
  return useQuery({
    queryKey: queryKeys.rag.graph(kbId),
    queryFn: () => fetchKnowledgeGraph(kbId),
  })
}

export function useEvaluationsQuery() {
  return useQuery({
    queryKey: queryKeys.rag.evaluations(),
    queryFn: fetchEvaluations,
  })
}
