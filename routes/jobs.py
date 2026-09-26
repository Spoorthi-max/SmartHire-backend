from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Optional

from database import get_db
from models.job import Job


router = APIRouter(
    prefix="/jobs",
    tags=["Job Descriptions"]
)


# -----------------------------
# Request schema
# -----------------------------

class JobCreate(BaseModel):
    id: str
    title: str
    location: str
    experience_years: int
    education: str
    must_have: List[str]
    nice_to_have: List[str]
    weights: Dict[str, float]
    pass_threshold: float
    confidence_cutoff: float
    summary: str


class JobUpdate(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    experience_years: Optional[int] = None
    education: Optional[str] = None
    must_have: Optional[List[str]] = None
    nice_to_have: Optional[List[str]] = None
    weights: Optional[Dict[str, float]] = None
    pass_threshold: Optional[float] = None
    confidence_cutoff: Optional[float] = None
    summary: Optional[str] = None


# -----------------------------
# Create Job Description
# -----------------------------

@router.post("/")
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    # Check if ID already exists
    existing_job = (
        db.query(Job)
        .filter(Job.id == job_data.id)
        .first()
    )

    if existing_job:
        raise HTTPException(
            status_code=400,
            detail="Job ID already exists"
        )

    job = Job(
        id=job_data.id,
        role=job_data.title,
        location=job_data.location,
        experience_years=job_data.experience_years,
        education=job_data.education,
        must_have=job_data.must_have,
        nice_to_have=job_data.nice_to_have,
        weights=job_data.weights,
        pass_threshold=job_data.pass_threshold,
        confidence_cutoff=job_data.confidence_cutoff,
        summary=job_data.summary
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "message": "Job description created successfully",
        "job": job_to_dict(job)
    }


# -----------------------------
# Get all Job Descriptions
# -----------------------------

@router.get("/")
def get_jobs(
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).all()

    return {
        "count": len(jobs),
        "jobs": [job_to_dict(job) for job in jobs]
    }


# -----------------------------
# Get one Job Description
# -----------------------------

@router.get("/{job_id}")
def get_job(
    job_id: str,
    db: Session = Depends(get_db)
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job description not found"
        )

    return job_to_dict(job)


# -----------------------------
# Update Job Description
# -----------------------------

@router.put("/{job_id}")
def update_job(
    job_id: str,
    job_data: JobUpdate,
    db: Session = Depends(get_db)
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job description not found"
        )

    update_data = job_data.model_dump(
        exclude_unset=True
    )

    # Map API field "title" to database field "role"
    if "title" in update_data:
        job.role = update_data.pop("title")

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return {
        "message": "Job description updated successfully",
        "job": job_to_dict(job)
    }


# -----------------------------
# Delete Job Description
# -----------------------------

@router.delete("/{job_id}")
def delete_job(
    job_id: str,
    db: Session = Depends(get_db)
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job description not found"
        )

    db.delete(job)
    db.commit()

    return {
        "message": "Job description deleted successfully",
        "job_id": job_id
    }


# -----------------------------
# Convert database object
# to API response
# -----------------------------

def job_to_dict(job):
    return {
        "id": job.id,
        "title": job.role,
        "location": job.location,
        "experience_years": job.experience_years,
        "education": job.education,
        "must_have": job.must_have,
        "nice_to_have": job.nice_to_have,
        "weights": job.weights,
        "pass_threshold": job.pass_threshold,
        "confidence_cutoff": job.confidence_cutoff,
        "summary": job.summary
    }