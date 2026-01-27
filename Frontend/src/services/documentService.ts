import api from './api'


//- Defines the shape of the response you expect from the backend after uploading a file
// uploaded document api call


export interface DocumentResponse {
  id: number
  filename: string
  user_id: number
  upload_date: string
}

export const documentService = {
  uploadFile: async (file: File): Promise<DocumentResponse> => {
    const formData = new FormData()               //- Creates a FormData object (used for file uploads)
    formData.append('file', file)

    const response = await api.post<DocumentResponse>('/upload/', formData, {      //- Sends a POST request to the /upload/ endpoint with the file data
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
}
