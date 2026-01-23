import api from './api'

export interface AskRequest {
  query: string
}

export interface AskResponse {
  answer: string
}

export const askService = {
  askQuestion: async (query: string): Promise<AskResponse> => {
    const response = await api.post<AskResponse>('/ask/', { query })
    return response.data
  },
}
