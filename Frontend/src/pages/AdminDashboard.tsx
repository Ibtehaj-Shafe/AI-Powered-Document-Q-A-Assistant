import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { adminService } from '../services/adminService'
import type { AdminDashboardResponse } from '../services/adminService'
import './AdminDashboard.css'

const AdminDashboard = () => {
  const { logout } = useAuth()
  const navigate = useNavigate()
  const [data, setData] = useState<AdminDashboardResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      const response = await adminService.getDashboard()
      setData(response)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  if (loading) {
    return (
      <div className="admin-dashboard-container">
        <div className="loading">Loading dashboard data...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="admin-dashboard-container">
        <div className="error-message">{error}</div>
      </div>
    )
  }

  return (
    <div className="admin-dashboard-container">
      <header className="admin-header">
        <h1>Admin Dashboard</h1>
        <div className="header-actions">
          <button onClick={() => navigate('/dashboard')} className="back-button">
            Back to Dashboard
          </button>
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </div>
      </header>

      <main className="admin-main">
        {data && (
          <>
            <div className="stats-grid">
              <div className="stat-card">
                <h3>Total Users</h3>
                <p className="stat-value">{data.total_users}</p>
              </div>
              <div className="stat-card">
                <h3>Total Files Uploaded</h3>
                <p className="stat-value">{data.total_files_uploaded}</p>
              </div>
              <div className="stat-card">
                <h3>Total Questions Asked</h3>
                <p className="stat-value">{data.total_questions_asked}</p>
              </div>
            </div>

            <div className="user-stats-section">
              <h2>User Statistics</h2>
              <div className="table-wrapper">
                <table className="user-stats-table">
                  <thead>
                    <tr>
                      <th>User ID</th>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Files Uploaded</th>
                      <th>Questions Asked</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.user_stats.length === 0 ? (
                      <tr>
                        <td colSpan={5} className="no-data">
                          No user statistics available
                        </td>
                      </tr>
                    ) : (
                      data.user_stats.map((stat) => (
                        <tr key={stat.user_id}>
                          <td>{stat.user_id}</td>
                          <td>{stat.name}</td>
                          <td>{stat.email}</td>
                          <td>{stat.files_uploaded_count}</td>
                          <td>{stat.questions_asked_count}</td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  )
}

export default AdminDashboard
