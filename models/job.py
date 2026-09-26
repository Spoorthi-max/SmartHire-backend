from sqlalchemy import Column, String, Integer, Float, JSON
from database import Base


class Job(Base):
    __tablename__ = "job_descriptions"

    id = Column(String, primary_key=True, index=True)
    role = Column(String, nullable=False)
    location = Column(String)
    experience_years = Column(Integer)
    education = Column(String)

    must_have = Column(JSON)
    nice_to_have = Column(JSON)

    weights = Column(JSON)

    pass_threshold = Column(Float)
    confidence_cutoff = Column(Float)

    summary = Column(String)