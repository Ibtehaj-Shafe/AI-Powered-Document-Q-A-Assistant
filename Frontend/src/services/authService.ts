import api from './api'

export interface UserCreate {
  name: string
  email: string
  password: string
  role?: 'user' | 'admin'
}

export interface UserLogin {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface UserResponse {
  id: number
  name: string
  email: string
  role: 'user' | 'admin'
}

export const authService = {
  signup: async (userData: UserCreate): Promise<UserResponse> => {
    const response = await api.post<UserResponse>('/auth/signup', userData)
    return response.data
  },

  login: async (credentials: UserLogin): Promise<TokenResponse> => {
    const response = await api.post<TokenResponse>('/auth/login', credentials)
    return response.data
  },

  forgotPassword: async (email: string): Promise<{ message: string }> => {
    const response = await api.post('/auth/forgot-password', { email })
    return response.data
  },

  resetPassword: async (email: string, otp: string, newPassword: string): Promise<{ message: string }> => {
    const response = await api.post('/auth/reset-password', {
      email,
      otp,
      new_password: newPassword,
    })
    return response.data
  },

  refreshToken: async (refreshToken: string): Promise<TokenResponse> => {
    const response = await api.post<TokenResponse>('/auth/refresh', {
      refresh_token: refreshToken,
    })
    return response.data
  },
}
