from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.candidate import Candidate


router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"]
)


# -----------------------------
# Get all candidates
# -----------------------------

@router.get("/")
def get_candidates(
    db: Session = Depends(get_db)
):
    candidates = db.query(Candidate).all()

    return {
        "count": len(candidates),
        "candidates": [
            candidate_to_dict(candidate)
            for candidate in candidates
        ]
    }


# -----------------------------
# Get candidate by ID
# -----------------------------

@router.get("/{candidate_id}")
def get_candidate(
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

    return candidate_to_dict(candidate)


# -----------------------------
# Helper function
# -----------------------------

def candidate_to_dict(candidate):
    return {
        "id": candidate.id,
        "user": candidate.user,
        "name": candidate.name,
        "email": candidate.email,
        "applied_jd": candidate.applied_jd,
        "experience_years": candidate.experience_years,
        "education": candidate.education,
        "location": candidate.location,
        "profile_type": candidate.profile_type,
        "resume": candidate.resume
    }