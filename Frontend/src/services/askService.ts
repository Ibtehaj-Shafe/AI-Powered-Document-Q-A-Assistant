import api from './api'

//ask service baxckend endpoint /ask/

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
