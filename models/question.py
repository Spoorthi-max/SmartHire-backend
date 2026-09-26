from sqlalchemy import Column, String, ForeignKey, Text, JSON
from database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True, index=True)

    jd_id = Column(
        String,
        ForeignKey("job_descriptions.id"),
        nullable=False
    )

    text = Column(Text, nullable=False)
    reference_answer = Column(Text)

    rubric = Column(JSON)