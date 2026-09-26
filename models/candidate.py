from sqlalchemy import Column, String, Integer, ForeignKey, Text
from database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, index=True)

    user = Column(String)
    name = Column(String, nullable=False)
    email = Column(String)

    applied_jd = Column(
        String,
        ForeignKey("job_descriptions.id")
    )

    experience_years = Column(Integer)
    education = Column(String)
    location = Column(String)
    profile_type = Column(String)

    resume = Column(Text)