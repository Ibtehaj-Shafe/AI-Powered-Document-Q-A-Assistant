import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { authService } from '../services/authService'
import './Auth.css'

const ForgotPassword = () => {
  //state variables for email, error message, and loading state
  const [email, setEmail] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {   //“e is a form submit event coming from React”
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await authService.forgotPassword(email)
      // OTP sent successfully, navigate to reset password page with email
      navigate(`/reset-password?email=${encodeURIComponent(email)}`)    //Go to reset password page and send email in URL.  //querry parameter
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to send OTP')
    } finally {
      setLoading(false)
    }
  }//$ is part of JavaScript template literals and is used to embed variables or expressions inside a string

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Forgot Password</h2>
        <p style={{ marginBottom: '20px', color: '#666' }}>
          Enter your email address and we'll send you an OTP to reset your password.
        </p>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="Enter your email"
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <button type="submit" disabled={loading} className="submit-button">
            {loading ? 'Sending OTP...' : 'Send OTP'}
          </button>
        </form>
        <div className="auth-links">
          <Link to="/login">Back to Login</Link>
        </div>
      </div>
    </div>
  )
}

export default ForgotPassword
