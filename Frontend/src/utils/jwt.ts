// Simple JWT decoder (frontend only - no verification)
// This is safe for reading the payload, but verification should be done on the backend

export interface JWTPayload {
  sub: string // user_id
  role: string
  type: string
  exp: number
  iat: number
}

export const decodeJWT = (token: string): JWTPayload | null => {
  try {
    const base64Url = token.split('.')[1]
    if (!base64Url) return null
    
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )
    
    return JSON.parse(jsonPayload)
  } catch (error) {
    console.error('Error decoding JWT:', error)
    return null
  }
}

export const isTokenExpired = (token: string): boolean => {
  const payload = decodeJWT(token)
  if (!payload || !payload.exp) return true
  
  // Check if token is expired (with 5 second buffer)
  return Date.now() >= (payload.exp * 1000) - 5000
}
