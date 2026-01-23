import api from './api'

export interface UserStat {
  user_id: number
  name: string
  email: string
  files_uploaded_count: number
  questions_asked_count: number
}

export interface AdminDashboardResponse {
  message: string
  total_users: number
  total_files_uploaded: number
  total_questions_asked: number
  user_stats: UserStat[]
}

export const adminService = {
  getDashboard: async (): Promise<AdminDashboardResponse> => {
    const response = await api.get<AdminDashboardResponse>('/admin/dashboard')
    return response.data
  },
}
