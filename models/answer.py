from sqlalchemy import Column, String, Float, ForeignKey, Text, DateTime, JSON
from database import Base
from datetime import datetime


class Answer(Base):
    __tablename__ = "answers"

    id = Column(String, primary_key=True, index=True)

    application_id = Column(
        String,
        ForeignKey("applications.id"),
        nullable=False
    )

    question_id = Column(
        String,
        ForeignKey("questions.id"),
        nullable=False
    )

    answer = Column(Text)

    score = Column(Float, nullable=True)
    justification = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)

    rubric_hits = Column(JSON, nullable=True)

    time_taken = Column(Float, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )