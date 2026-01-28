import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import './Auth.css'

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {    //“e is a form submit event coming from React”  React.FormEvent is a type definiion
    e.preventDefault()  //Prevents page refresh when form is submitted.
    setError('')        //Clear old error message.
    setLoading(true)    //Shows loading state (button disabled + "Logging in...")

    try {
      await login(email, password)
      navigate('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Invalid email or password')
    } finally {
      setLoading(false)   //Stop loading spinner whether success or failure
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Login</h2>
        <form onSubmit={handleSubmit} autoComplete='off'>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="Enter your email"
              autoComplete='username'
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter your password"
              autoComplete="current-password"
            />
          </div>

          
          {error && <div className="error-message">{error}</div>}
          <button type="submit" disabled={loading} className="submit-button">          {/*Disable button when loading is true */}
            {loading ? 'Logging in...' : 'Login'}                              {/*React ternary operator //If loading → show "Logging in..." Else → show "Login"*/}
          </button> 
        </form>
        <div className="auth-links">
          <Link to="/forgot-password">Forgot Password?</Link>
          <span>
            Don't have an account? <Link to="/signup">Sign up</Link>
          </span>
        </div>
      </div>
    </div>
  )
}

export default Login
