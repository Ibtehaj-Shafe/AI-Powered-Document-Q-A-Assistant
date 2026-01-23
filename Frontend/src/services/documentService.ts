import api from './api'

export interface DocumentResponse {
  id: number
  filename: string
  user_id: number
  upload_date: string
}

export const documentService = {
  uploadFile: async (file: File): Promise<DocumentResponse> => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post<DocumentResponse>('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
}
