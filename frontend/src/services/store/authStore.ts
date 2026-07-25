import { create } from "zustand"
import type { User } from "@/types/api"
import { getStoredToken, logoutUser } from "@/services/api/auth"

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isRestored: boolean
  setUser: (user: User | null) => void
  setToken: (token: string | null) => void
  setAuthenticated: (auth: boolean) => void
  setRestored: (restored: boolean) => void
  clearAuth: () => void
}

interface DecodedToken {
  user_id: number
  email: string
  exp?: number
}

// Simple base64 decoder to parse JWT payload without adding external dependencies
export const decodeJwt = (token: string): DecodedToken | null => {
  try {
    const base64Url = token.split(".")[1]
    if (!base64Url) return null
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/")
    const jsonPayload = decodeURIComponent(
      window
        .atob(base64)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    )
    return JSON.parse(jsonPayload)
  } catch (err) {
    console.error("Failed to decode JWT:", err)
    return null
  }
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isRestored: false,
  setUser: (user) => set({ user }),
  setToken: (token) => set({ token }),
  setAuthenticated: (isAuthenticated) => set({ isAuthenticated }),
  setRestored: (isRestored) => set({ isRestored }),
  clearAuth: () => {
    logoutUser()
    set({ user: null, token: null, isAuthenticated: false })
  }
}))

/**
 * Evaluates stored access tokens, restores authenticated states,
 * and clears expired sessions.
 */
export const restoreUserSession = (): void => {
  const token = getStoredToken()
  if (!token) {
    useAuthStore.setState({ isRestored: true, isAuthenticated: false })
    return
  }

  const decoded = decodeJwt(token)
  if (!decoded) {
    // Corrupt token - purge session
    useAuthStore.getState().clearAuth()
    useAuthStore.setState({ isRestored: true })
    return
  }

  // Verify token expiration date if it exists
  if (decoded.exp) {
    const nowSeconds = Math.floor(Date.now() / 1000)
    if (decoded.exp < nowSeconds) {
      // Session has expired
      console.warn("Session token expired. Logging user out.")
      useAuthStore.getState().clearAuth()
      useAuthStore.setState({ isRestored: true })
      return
    }
  }

  // Restore authenticated states
  useAuthStore.setState({
    user: { id: decoded.user_id, email: decoded.email },
    token,
    isAuthenticated: true,
    isRestored: true
  })
}
