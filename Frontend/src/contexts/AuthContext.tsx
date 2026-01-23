import React, { createContext, useContext, useState, useEffect } from 'react'
import type { ReactNode } from 'react'
import { authService } from '../services/authService'
import type { UserResponse } from '../services/authService'
import { decodeJWT, isTokenExpired } from '../utils/jwt'

interface AuthContextType {
  user: UserResponse | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  signup: (name: string, email: string, password: string, role?: 'user' | 'admin') => Promise<void>
  logout: () => void
  isAuthenticated: boolean
  isAdmin: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<UserResponse | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const initAuth = () => {
      const token = localStorage.getItem('access_token')
      if (token && !isTokenExpired(token)) {
        try {
          const payload = decodeJWT(token)
          if (payload) {
            setUser({
              id: parseInt(payload.sub),
              name: '', // We don't have name in token, will be set on login
              email: '', // We don't have email in token, will be set on login
              role: payload.role as 'user' | 'admin',
            })
          }
        } catch (error) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
        }
      } else if (token && isTokenExpired(token)) {
        // Token expired, clear it
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      }
      setLoading(false)
    }

    initAuth()
  }, [])

  const login = async (email: string, password: string) => {
    const response = await authService.login({ email, password })
    localStorage.setItem('access_token', response.access_token)
    localStorage.setItem('refresh_token', response.refresh_token)
    
    // Decode token to get user info
    const payload = decodeJWT(response.access_token)
    if (payload) {
      setUser({
        id: parseInt(payload.sub),
        name: email.split('@')[0], // Use email prefix as name placeholder
        email,
        role: payload.role as 'user' | 'admin',
      })
    }
  }

  const signup = async (name: string, email: string, password: string, role: 'user' | 'admin' = 'user') => {
    const userResponse = await authService.signup({ name, email, password, role })
    // After signup, automatically log in
    const loginResponse = await authService.login({ email, password })
    localStorage.setItem('access_token', loginResponse.access_token)
    localStorage.setItem('refresh_token', loginResponse.refresh_token)
    
    // Use the user data from signup response
    setUser(userResponse)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
  }

  const isAuthenticated = !!user && !!localStorage.getItem('access_token')
  const isAdmin = user?.role === 'admin'

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        signup,
        logout,
        isAuthenticated,
        isAdmin,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}
