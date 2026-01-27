import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { documentService } from '../services/documentService'
import { askService } from '../services/askService'
import './Dashboard.css'

const Dashboard = () => {
  const { user, logout, isAdmin } = useAuth()
  const navigate = useNavigate()
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)    //tracks upload progress.
  const [uploadMessage, setUploadMessage] = useState('')
  const [query, setQuery] = useState('')
  const [answer, setAnswer] = useState('')     //backend’s answer.
  const [asking, setAsking] = useState(false)   //tracks Q&A request progress
  const [error, setError] = useState('')
  //File handling : Handles file input change by validating selected file type (PDF or DOCX) and updating state accordingly
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {          //list of files selected by the user.
      const selectedFile = e.target.files[0]
      if (selectedFile.type === 'application/pdf' ||           //MIME stands for Multipurpose Internet Mail Extensions.
          selectedFile.name.endsWith('.docx')) {
        setFile(selectedFile)
        setError('')
      } else {
        setError('Only PDF and DOCX files are supported')
        setFile(null)
      }
    }
  }
// Handles document upload by validating file selection, calling the upload service, and managing success/error states
  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) {            //Checks if a file is chosen
      setError('Please select a file')
      return
    }

    setUploading(true)
    setError('')
    setUploadMessage('')

    try {
      await documentService.uploadFile(file)
      setUploadMessage(`File "${file.name}" uploaded successfully!`)
      setFile(null)
      // Reset file input
      const fileInput = document.getElementById('file-input') as HTMLInputElement
      if (fileInput) fileInput.value = ''
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload file')
    } finally {
      setUploading(false)
    }
  }

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) {               //.trim removes whitespace from both ends of a string.
      setError('Please enter a question')
      return
    }

    setAsking(true)
    setError('')
    setAnswer('')

    try {
      const response = await askService.askQuestion(query)
      setAnswer(response.answer)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get answer')
    } finally {
      setAsking(false)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Document Q&A System</h1>
        <div className="header-actions">
          {isAdmin && (                  //conditional rendering - If isAdmin is true, then render what’s inside.
            <button onClick={() => navigate('/admin')} className="admin-button">
              Admin Dashboard
            </button>
          )}
          <span className="user-name">{user?.name || user?.email}</span>  //Displays the user’s name if available or email.
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-section">
          <h2>Upload Document</h2>
          <form onSubmit={handleUpload} className="upload-form">
            <div className="file-input-wrapper">
              <input
                type="file"
                id="file-input"
                accept=".pdf,.docx"
                onChange={handleFileChange}
                className="file-input"
              />
              <label htmlFor="file-input" className="file-label">
                {file ? file.name : 'Choose PDF or DOCX file'}     //tenary conditional operator - If file is selected, show its name; otherwise, prompt to choose a file.
              </label>
            </div>
            <button type="submit" disabled={uploading || !file} className="upload-button">
              {uploading ? 'Uploading...' : 'Upload'}   //Tenary conditional operator - If uploading is true, show 'Uploading...'; otherwise, show 'Upload'.
            </button>
          </form>
          {uploadMessage && <div className="success-message">{uploadMessage}</div>}
        </div>

        <div className="dashboard-section">
          <h2>Ask Question</h2>
          <form onSubmit={handleAsk} className="ask-form">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter your question about the uploaded documents..."
              rows={4}       //height of the textarea in number of text lines
              className="query-input"
            />
            <button type="submit" disabled={asking || !query.trim()} className="ask-button"> //disabled if asking is true or query is empty after trimming whitespace.
              {asking ? 'Asking...' : 'Ask Question'} // Tenary conditional operator - If asking is true, show 'Asking...'; otherwise, show 'Ask Question'.
            </button>
          </form>
          {answer && (
            <div className="answer-container">
              <h3>Answer:</h3>
              <p className="answer-text">{answer}</p>
            </div>
          )}
        </div>

        {error && <div className="error-message">{error}</div>}
      </main>
    </div>
  )
}

export default Dashboard
