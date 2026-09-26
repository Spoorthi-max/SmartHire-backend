from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from database import Base
from datetime import datetime


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(String, primary_key=True, index=True)

    application_id = Column(
        String,
        ForeignKey("applications.id"),
        nullable=False
    )

    interviewer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    interview_date = Column(DateTime, nullable=True)

    status = Column(
        String,
        default="Scheduled"
    )

    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )