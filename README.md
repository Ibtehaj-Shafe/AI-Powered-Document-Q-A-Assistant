# AI-Powered Document Q&A Assistant

A full-stack web application that allows users to upload documents (PDF/DOCX) and ask questions about their content using GenAI. Built with FastAPI (backend) and React + TypeScript (frontend).

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Docker Setup](#docker-setup)
- [API Documentation](#api-documentation)
- [Frontend Documentation](#frontend-documentation)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### User Features
- **Authentication**: Signup, Login, Forgot Password, Reset Password (OTP-based)
- **Document Upload**: Upload PDF and DOCX files
- **Question & Answer**: Ask questions about uploaded documents
- **AI-Powered Answers**: Context-aware responses using Groq LLM

### Admin Features
- **Admin Dashboard**: View system statistics
  - Total users
  - Total documents uploaded
  - Total questions asked
  - User statistics table

### Security
- JWT-based authentication
- Role-based access control (User/Admin)
- Password hashing with pwdlib
- Protected API routes

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **GenAI**: Groq LLM
- **Vector Database**: Pinecone
- **Embeddings**: Sentence Transformers
- **Document Processing**: PyPDF2, python-docx

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Styling**: CSS3

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (frontend)
- **ASGI Server**: Uvicorn (backend)

---

## 📁 Project Structure

```
Intern_Technical_Assessment/
├── Backend/                 # FastAPI backend
│   ├── crud/               # Database operations
│   ├── database/           # Database configuration
│   ├── dependencies/       # JWT, password utilities
│   ├── models/            # SQLAlchemy models
│   ├── routes/            # API endpoints
│   ├── schemas/           # Pydantic schemas
│   └── services/          # Business logic (GenAI, upload)
├── Frontend/              # React frontend
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── contexts/     # React contexts
│   │   ├── pages/        # Page components
│   │   ├── services/     # API service layer
│   │   └── utils/        # Utility functions
│   ├── Dockerfile
│   └── nginx.conf
├── main.py               # FastAPI application entry point
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile           # Backend Dockerfile (if exists)
└── README.md           # This file
```

---

## 📋 Prerequisites

### Required Software
- **Python 3.9+**
- **Node.js 16+** and npm
- **PostgreSQL 12+**
- **Docker** and **Docker Compose** (optional, for containerized setup)

### Required Accounts & API Keys
- **Pinecone Account**: For vector database
  - Create account at [pinecone.io](https://www.pinecone.io)
  - Create an index (dimension: 384 for all-MiniLM-L6-v2)
- **Groq API Key**: For LLM
  - Get API key from [console.groq.com](https://console.groq.com)
- **Email SMTP** (optional): For OTP emails
  - Gmail, SendGrid, or any SMTP service

---

## 🔐 Environment Variables

Create a `.env` file in the project root with the following variables:

### Database Configuration
```env
# PostgreSQL Database
db_user=postgres
db_pswd=your_password
db_host=localhost
db_port=5432
db_name=intern_assessment
```

### Authentication
```env
# JWT Secret Key (generate a strong random string)
Secret_Key=your-secret-key-here-minimum-32-characters
```

### Pinecone (Vector Database)
```env
# Pinecone API Key
db_key=your-pinecone-api-key

# Pinecone Index Name
index_name=your-index-name

# Pinecone Region (optional)
reg=us-east-1
```

### Groq (LLM)
```env
# Groq API Key
api_key=your-groq-api-key
```

### Email Configuration (for OTP)
```env
# SMTP Configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Frontend (optional, for local development)
```env
# Frontend .env (in Frontend directory)
VITE_API_BASE_URL=http://localhost:8000
```

---

## 🚀 Setup Instructions

### Option 1: Local Development (Without Docker)

#### Backend Setup

1. **Clone the repository** (or navigate to project directory)

2. **Create virtual environment**:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up PostgreSQL database**:
```bash
# Create database
createdb intern_assessment

# Or using psql
psql -U postgres
CREATE DATABASE intern_assessment;
```

5. **Create `.env` file** in project root with all required variables (see [Environment Variables](#environment-variables))

6. **Set up Pinecone**:
   - Create a Pinecone account
   - Create an index with:
     - Dimension: `384` (for all-MiniLM-L6-v2 model)
     - Metric: `cosine`
   - Get your API key
   - Add to `.env` file

7. **Run the backend**:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

#### Frontend Setup

1. **Navigate to Frontend directory**:
```bash
cd Frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Create `.env` file** (optional):
```env
VITE_API_BASE_URL=http://localhost:8000
```

4. **Run the frontend**:
```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

---

### Option 2: Docker Setup (Recommended)

1. **Create `.env` file** in project root with all required variables

2. **Build and start all services**:
```bash
docker-compose up --build
```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

4. **Stop services**:
```bash
docker-compose down
```

For detailed Docker setup, see [DOCKER_SETUP.md](./DOCKER_SETUP.md)

---

## 🏃 Running the Application

### Development Mode

**Backend**:
```bash
uvicorn main:app --reload
```

**Frontend**:
```bash
cd Frontend
npm run dev
```

### Production Mode

**Backend**:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
cd Frontend
npm run build
npm run preview
```

---

## 🐳 Docker Setup

### Quick Start with Docker Compose

1. **Ensure Docker and Docker Compose are installed**

2. **Create `.env` file** with all required variables

3. **Start all services**:
```bash
docker-compose up --build
```

This will start:
- PostgreSQL database (port 5432)
- Backend API (port 8000)
- Frontend (port 3000)

### Docker Services

- **db**: PostgreSQL database
- **backend**: FastAPI application
- **frontend**: React application (Nginx)

### Docker Commands

```bash
# Build and start
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

For detailed Docker documentation, see [DOCKER_SETUP.md](./DOCKER_SETUP.md)

---

## 📚 API Documentation

### Base URL
- Local: `http://localhost:8000`
- Docker: `http://localhost:8000`

### Interactive API Docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Authentication

All protected endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### API Endpoints

#### Authentication Endpoints

##### `POST /auth/signup`
Create a new user account.

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "user"
}
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user"
}
```

##### `POST /auth/login`
Authenticate user and get JWT tokens.

**Request Body**:
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response**: `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

##### `POST /auth/forgot-password`
Request OTP for password reset.

**Request Body**:
```json
{
  "email": "john@example.com"
}
```

**Response**: `200 OK`
```json
{
  "message": "If the email exists, an OTP has been sent"
}
```

##### `POST /auth/reset-password`
Reset password using OTP.

**Request Body**:
```json
{
  "email": "john@example.com",
  "otp": "123456",
  "new_password": "newpassword123"
}
```

**Response**: `200 OK`
```json
{
  "message": "Password reset successfully"
}
```

##### `POST /auth/refresh`
Refresh access token.

**Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response**: `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Document Endpoints

##### `POST /upload`
Upload a document (PDF or DOCX).

**Headers**:
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Request Body** (form-data):
- `file`: PDF or DOCX file

**Response**: `200 OK`
```json
{
  "id": 1,
  "filename": "document.pdf",
  "user_id": 1,
  "upload_date": "2024-01-15T10:30:00Z"
}
```

#### Question Endpoints

##### `POST /ask`
Ask a question about uploaded documents.

**Headers**:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "query": "What is the main topic of the document?"
}
```

**Response**: `200 OK`
```json
{
  "answer": "The main topic of the document is..."
}
```

#### Admin Endpoints

##### `GET /admin/dashboard`
Get admin dashboard statistics (Admin only).

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response**: `200 OK`
```json
{
  "message": "Welcome To Admin Dashboard.",
  "total_users": 10,
  "total_files_uploaded": 25,
  "total_questions_asked": 50,
  "user_stats": [
    {
      "user_id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "files_uploaded_count": 5,
      "questions_asked_count": 10
    }
  ]
}
```

#### User Endpoints

##### `GET /users/all`
Get all users (requires authentication).

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  }
]
```

---

## 🎨 Frontend Documentation

For detailed frontend documentation, see:
- [Frontend/README.md](./Frontend/README.md) - Frontend setup and usage
- [Frontend/FRONTEND_IMPLEMENTATION.md](./Frontend/FRONTEND_IMPLEMENTATION.md) - Implementation details

### Frontend Routes

- `/login` - Login page
- `/signup` - Signup page
- `/forgot-password` - Forgot password page
- `/reset-password` - Reset password page
- `/dashboard` - Main application (protected)
- `/admin` - Admin dashboard (protected, admin only)

---

## 🔧 Troubleshooting

### Backend Issues

#### Database Connection Error
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists: `createdb intern_assessment`

#### Pinecone Connection Error
- Verify API key is correct
- Check index name matches your Pinecone index
- Ensure index dimension is 384

#### Groq API Error
- Verify API key is valid
- Check API quota/limits

#### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version (3.9+)

### Frontend Issues

#### CORS Errors
- Frontend uses Vite proxy to avoid CORS
- Ensure backend is running on port 8000
- Check `vite.config.ts` proxy configuration

#### API Connection Error
- Verify backend is running
- Check `VITE_API_BASE_URL` in Frontend `.env`
- Check browser console for errors

#### Build Errors
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Check Node.js version (16+)

### Docker Issues

#### Port Already in Use
- Stop conflicting services
- Or modify ports in `docker-compose.yml`

#### Container Won't Start
- Check logs: `docker-compose logs`
- Verify `.env` file exists with all variables
- Ensure Docker has enough resources

#### Database Connection in Docker
- Use service name `db` as hostname (not `localhost`)
- Check network configuration in `docker-compose.yml`

---

## 📝 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Groq Documentation](https://console.groq.com/docs)

---

## 📄 License

This project is part of an Intern Technical Assessment.

---

## 👥 Contributors

- Backend: Tech Lead
- Frontend: Assessment Implementation

---

## ✅ Project Status

**Status**: ✅ Complete

All assessment requirements have been fulfilled:
- ✅ Authentication pages
- ✅ Document upload
- ✅ Question & Answer interface
- ✅ Admin dashboard
- ✅ Docker configuration
- ✅ API documentation

For detailed completion checklist, see [ASSESSMENT_COMPLETION_CHECKLIST.md](./ASSESSMENT_COMPLETION_CHECKLIST.md)
