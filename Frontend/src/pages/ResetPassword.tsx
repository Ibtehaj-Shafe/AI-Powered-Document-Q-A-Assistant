import { useState } from 'react'
import { useNavigate, Link, useSearchParams } from 'react-router-dom'
import { authService } from '../services/authService'
import './Auth.css'

const ResetPassword = () => {
  //state variables
  const [searchParams] = useSearchParams()     //useSearchParams is a hook that allows you to access the search params in the URL
  const [email, setEmail] = useState(searchParams.get('email') || '')    //searchParams.get('email') is a function that returns the value of the email parameter in the URL
  const [otp, setOtp] = useState('') 
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')   //message is a success message that is displayed when the password is reset successfully
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()   //useNavigate is a hook that allows you to navigate to a different page

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()  //Stops the browser from refreshing the page when the form is submitted.
    setError('')  //clear the previous error when the form is submitted
    setMessage('')  //clear the message when the form is submitted

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    if (newPassword.length < 6) {
      setError('Password must be at least 6 characters long')
      return
    }

    setLoading(true)

    try {
      await authService.resetPassword(email, otp, newPassword)
      setMessage('Password reset successfully! Redirecting to login...')
      setTimeout(() => {       //- built‑in JavaScript function that schedules code to run after a delay.  //2000 milliseconds = 2 seconds
        navigate('/login')
      }, 2000)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to reset password')   //tries to read the error message from the server’s response.
    } finally {
      setLoading(false)  //Stops the loading spinner when the form is submitted
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Reset Password</h2>
        <p style={{ marginBottom: '20px', color: '#666' }}>
          Enter the OTP sent to your email and your new password to reset your password.
        </p>
        <form onSubmit={handleSubmit}>
          {email && (       // conditional rendering - If email has a value (not empty), then render what’s inside.
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                value={email}
                readOnly
                className="readonly-input"
                style={{ backgroundColor: '#f5f5f5', cursor: 'not-allowed' }}
              />
            </div>
          )}
          {!email && (       // conditional rendering - If email does not have a value (empty), then render what’s inside.
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
          )}
          <div className="form-group">
            <label htmlFor="otp">OTP</label>
            <input
              type="text"
              id="otp"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              required
              placeholder="Enter the OTP sent to your email"
            />
          </div>
          <div className="form-group">
            <label htmlFor="newPassword">New Password</label>
            <input
              type="password"
              id="newPassword"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
              placeholder="Enter new password"
              minLength={6}
            />
          </div>
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm New Password</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required       // must be filled
              placeholder="Confirm new password"
              minLength={6}
            />
          </div>
          {error && <div className="error-message">{error}</div>}    
          {message && <div className="success-message">{message}</div>}
          <button type="submit" disabled={loading} className="submit-button">
            {loading ? 'Resetting...' : 'Reset Password'}
          </button>
        </form>
        <div className="auth-links">
          <Link to="/login">Back to Login</Link>
        </div>
      </div>
    </div>
  )
}

export default ResetPassword
