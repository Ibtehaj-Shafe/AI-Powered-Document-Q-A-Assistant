from fastapi import FastAPI
from Backend.database.database import Engine, Base
from Backend.routes import auth, user, admin, upload, ask

# Create tables
Base.metadata.create_all(bind=Engine)

app = FastAPI(
    title="Intern Technical Assessment",
    version="1.0",
    description="Implemented using FastAPI and PostgreSQL"
)

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(upload.router)
app.include_router(ask.router)
