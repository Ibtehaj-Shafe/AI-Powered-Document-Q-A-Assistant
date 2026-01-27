import axios from 'axios'   //- Imports the Axios library for making HTTP requests

// access_token and refresh_token

// Use Vite proxy to avoid CORS issues
// The proxy is configured in vite.config.ts to forward /api/* to http://localhost:8000/*
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'
//create - preconfigured Axios instance named api
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token   "- Runs before every request."

api.interceptors.request.use(
  (config) => {  //success handler function - It receives the request config object (which contains URL, headers, method, etc.).
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle token refresh   "- Runs after every response."
api.interceptors.response.use(
  (response) => response,          //suuccess handler - simply returns the response as is.
  async (error) => {                //error handler - handles errors, particularly 401 Unauthorized errors.
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await api.post('/auth/refresh', {             // post request to the backend endpoint /auth/refresh 
            refresh_token: refreshToken,
          })

          const { access_token, refresh_token } = response.data
          localStorage.setItem('access_token', access_token)
          localStorage.setItem('refresh_token', refresh_token)

          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'          //back to the login page so they can re‑authenticate.
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api
