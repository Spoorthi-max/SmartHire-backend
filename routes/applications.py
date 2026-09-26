from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from uuid import uuid4

from database import get_db
from models.application import Application
from models.candidate import Candidate
from models.job import Job


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


# -----------------------------
# Request schema
# -----------------------------

class ApplicationCreate(BaseModel):
    candidate_id: str
    jd_id: str


# -----------------------------
# Create Application
# -----------------------------

@router.post("/")
def create_application(
    application_data: ApplicationCreate,
    db: Session = Depends(get_db)
):
    # Check candidate
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == application_data.candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    # Check job
    job = (
        db.query(Job)
        .filter(Job.id == application_data.jd_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job description not found"
        )

    # Prevent duplicate applications
    existing_application = (
        db.query(Application)
        .filter(
            Application.candidate_id == application_data.candidate_id,
            Application.jd_id == application_data.jd_id
        )
        .first()
    )

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="Candidate has already applied to this job"
        )

    # Create application
    application = Application(
        id=str(uuid4()),
        candidate_id=application_data.candidate_id,
        jd_id=application_data.jd_id,
        status="Filtered"
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return {
        "message": "Application created successfully",
        "application": application_to_dict(application)
    }


# -----------------------------
# Get all applications
# -----------------------------

@router.get("/")
def get_applications(
    db: Session = Depends(get_db)
):
    applications = db.query(Application).all()

    return {
        "count": len(applications),
        "applications": [
            application_to_dict(application)
            for application in applications
        ]
    }


# -----------------------------
# Get application by ID
# -----------------------------

@router.get("/{application_id}")
def get_application(
    application_id: str,
    db: Session = Depends(get_db)
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application_to_dict(application)


# -----------------------------
# Get applications for candidate
# -----------------------------

@router.get("/candidate/{candidate_id}")
def get_candidate_applications(
    candidate_id: str,
    db: Session = Depends(get_db)
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    applications = (
        db.query(Application)
        .filter(Application.candidate_id == candidate_id)
        .all()
    )

    return {
        "candidate_id": candidate_id,
        "count": len(applications),
        "applications": [
            application_to_dict(application)
            for application in applications
        ]
    }


# -----------------------------
# Helper
# -----------------------------

def application_to_dict(application):
    return {
        "id": application.id,
        "candidate_id": application.candidate_id,
        "jd_id": application.jd_id,
        "status": application.status,
        "resume_score": application.resume_score,
        "qa_score": application.qa_score,
        "combined_score": application.combined_score,
        "decision_band": application.decision_band,
        "created_at": application.created_at,
        "updated_at": application.updated_at
    }