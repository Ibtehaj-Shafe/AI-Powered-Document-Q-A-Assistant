import api from './api'  //preconfigured api instance used to make http req to backend
// admin dashboard api call


export interface UserStat {   //- TypeScript interface

  user_id: number
  name: string
  email: string
  files_uploaded_count: number
  questions_asked_count: number
}

export interface AdminDashboardResponse { //- TypeScript interface

  message: string
  total_users: number
  total_files_uploaded: number
  total_questions_asked: number
  user_stats: UserStat[]
}

export const adminService = {
  getDashboard: async (): Promise<AdminDashboardResponse> => {  //- “This function will eventually return an AdminDashboardResponse, but wrapped inside a Promise.”
    const response = await api.get<AdminDashboardResponse>('/admin/dashboard')       //calling backend API endpoint /admin/dashboard using GET method
    return response.data
  },
}

//- api.get itself returns a Promise (because HTTP requests are asynchronous).
// I don’t have the data right now, but I promise I’ll give it to you later — either successfully or with an error.