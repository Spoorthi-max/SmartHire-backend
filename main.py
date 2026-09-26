from fastapi import FastAPI
from database import engine, Base

# Import all database models
from models.user import User
from models.job import Job
from models.candidate import Candidate
from models.question import Question
from models.application import Application
from models.answer import Answer
from models.interview import Interview
from models.audit import AuditLog

# Import routes
from routes.auth import router as auth_router
from routes.jobs import router as jobs_router
from routes.candidates import router as candidates_router
from routes.applications import router as applications_router


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="SmartHire API",
    description="AI-powered hiring screening and interview tracking backend",
    version="1.0.0"
)


# Register routes
app.include_router(auth_router)
app.include_router(jobs_router)
app.include_router(candidates_router)
app.include_router(applications_router)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "SmartHire Backend Running"
    }


# Health check endpoint
@app.get("/health")
def health():
    return {
        "status": "UP"
    }