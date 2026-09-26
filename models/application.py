from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from database import Base
from datetime import datetime


class Application(Base):
    __tablename__ = "applications"

    id = Column(String, primary_key=True, index=True)

    candidate_id = Column(
        String,
        ForeignKey("candidates.id"),
        nullable=False
    )

    jd_id = Column(
        String,
        ForeignKey("job_descriptions.id"),
        nullable=False
    )

    status = Column(
        String,
        default="Filtered",
        nullable=False
    )

    resume_score = Column(Float, nullable=True)
    qa_score = Column(Float, nullable=True)
    combined_score = Column(Float, nullable=True)

    decision_band = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )