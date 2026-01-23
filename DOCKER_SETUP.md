# Docker Setup Guide

## 📋 Overview

This project uses Docker and Docker Compose to containerize the entire application stack:
- **PostgreSQL Database** - Data persistence
- **Backend API** (FastAPI) - REST API server
- **Frontend** (React + TypeScript) - Web application

## 🐳 Docker Files

### Root Level
- `docker-compose.yml` - Orchestrates all services
- `.dockerignore` - Excludes files from Docker builds

### Frontend
- `Frontend/Dockerfile` - Multi-stage build for React app
- `Frontend/nginx.conf` - Nginx configuration for serving frontend
- `Frontend/.dockerignore` - Frontend-specific exclusions

### Backend
- `Dockerfile` (if exists) - Backend containerization
- Note: Backend Dockerfile should be created if not present

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Docker Compose v3.8+

### Steps

1. **Create `.env` file** in project root:
```env
# Database
db_user=postgres
db_pswd=postgres
db_host=localhost
db_port=5432
db_name=intern_assessment

# Backend
Secret_Key=your-secret-key-here
db_key=your-pinecone-key
index_name=your-index-name
api_key=your-groq-api-key
```

2. **Build and start all services:**
```bash
docker-compose up --build
```

3. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432

4. **Stop all services:**
```bash
docker-compose down
```

5. **Stop and remove volumes (clean slate):**
```bash
docker-compose down -v
```

---

## 📦 Service Details

### 1. Database Service (`db`)

**Image:** `postgres:15-alpine`

**Configuration:**
- Port: 5432 (configurable via `db_port`)
- Persistent volume: `postgres_data`
- Health checks enabled

**Environment Variables:**
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_DB` - Database name

### 2. Backend Service (`backend`)

**Configuration:**
- Port: 8000
- Hot reload enabled (development)
- Depends on database service
- Health checks enabled

**Environment Variables:**
- Database connection settings
- JWT secret key
- Pinecone API key
- Groq API key

**Note:** Requires `Dockerfile` in project root for backend.

### 3. Frontend Service (`frontend`)

**Configuration:**
- Port: 3000 (mapped to container port 80)
- Nginx web server
- API proxy configured
- Health checks enabled

**Build Process:**
1. Stage 1: Build React app with Node.js
2. Stage 2: Serve with Nginx

**Nginx Features:**
- SPA routing support (`try_files`)
- Gzip compression
- Static asset caching
- API proxy to backend
- Security headers

---

## 🔧 Docker Compose Configuration

### Networks
- `app-network`: Bridge network connecting all services

### Volumes
- `postgres_data`: Persistent database storage

### Health Checks
All services include health checks for dependency management.

---

## 🛠️ Development vs Production

### Development Mode
```bash
docker-compose up
```
- Hot reload enabled for backend
- Source code mounted as volumes
- Development-friendly settings

### Production Mode
For production, you should:
1. Remove volume mounts
2. Use production builds
3. Set proper environment variables
4. Use secrets management
5. Enable HTTPS
6. Configure proper logging

---

## 📝 Environment Variables

### Required Variables

**Database:**
- `db_user` - PostgreSQL username
- `db_pswd` - PostgreSQL password
- `db_name` - Database name

**Backend:**
- `Secret_Key` - JWT secret key
- `db_key` - Pinecone API key
- `index_name` - Pinecone index name
- `api_key` - Groq API key

**Frontend:**
- `VITE_API_BASE_URL` - API base URL (defaults to `/api`)

### Optional Variables
- `db_port` - Database port (default: 5432)
- `db_host` - Database host (default: localhost for local, `db` for Docker)

---

## 🔍 Troubleshooting

### Port Already in Use
If ports 3000, 8000, or 5432 are already in use:
1. Stop conflicting services
2. Or modify ports in `docker-compose.yml`:
```yaml
ports:
  - "3001:80"  # Change host port
```

### Database Connection Issues
- Ensure database service is healthy
- Check environment variables
- Verify network connectivity

### Frontend Not Loading
- Check nginx logs: `docker logs intern_assessment_frontend`
- Verify build completed successfully
- Check API proxy configuration

### Backend Errors
- Check backend logs: `docker logs intern_assessment_backend`
- Verify all environment variables are set
- Check database connection

### Clean Rebuild
```bash
# Stop and remove everything
docker-compose down -v

# Remove images
docker rmi intern_assessment_backend intern_assessment_frontend

# Rebuild from scratch
docker-compose up --build
```

---

## 📊 Service Logs

### View All Logs
```bash
docker-compose logs -f
```

### View Specific Service
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

---

## 🔐 Security Considerations

1. **Never commit `.env` files** - Use `.env.example`
2. **Use strong secrets** - Generate secure keys
3. **Limit port exposure** - Only expose necessary ports
4. **Use secrets management** - For production deployments
5. **Keep images updated** - Regularly update base images

---

## 📚 Additional Commands

### Rebuild Specific Service
```bash
docker-compose build frontend
docker-compose up -d frontend
```

### Execute Commands in Container
```bash
# Backend
docker-compose exec backend bash

# Frontend
docker-compose exec frontend sh

# Database
docker-compose exec db psql -U postgres -d intern_assessment
```

### View Container Status
```bash
docker-compose ps
```

### Stop Services
```bash
docker-compose stop
```

### Start Services
```bash
docker-compose start
```

---

## 🎯 Production Deployment

For production, consider:

1. **Separate docker-compose files:**
   - `docker-compose.yml` - Development
   - `docker-compose.prod.yml` - Production

2. **Use production builds:**
   - Optimized frontend build
   - No hot reload
   - Production database settings

3. **Add reverse proxy:**
   - Nginx or Traefik
   - SSL/TLS certificates
   - Load balancing

4. **Monitoring:**
   - Health check endpoints
   - Logging aggregation
   - Metrics collection

5. **Backup strategy:**
   - Database backups
   - Volume snapshots
   - Disaster recovery plan

---

## 📄 File Structure

```
.
├── docker-compose.yml          # Main compose file
├── .dockerignore               # Root dockerignore
├── Dockerfile                  # Backend Dockerfile (if exists)
├── Frontend/
│   ├── Dockerfile              # Frontend multi-stage build
│   ├── nginx.conf              # Nginx configuration
│   └── .dockerignore           # Frontend dockerignore
└── .env                        # Environment variables (not in git)
```

---

## ✅ Verification

After starting services, verify:

1. **Frontend:** http://localhost:3000 loads
2. **Backend:** http://localhost:8000/docs accessible
3. **Database:** Connection successful
4. **Health checks:** All services healthy

```bash
docker-compose ps
```

All services should show "healthy" status.
