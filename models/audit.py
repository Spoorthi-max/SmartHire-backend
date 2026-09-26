from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from datetime import datetime


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=True)

    action = Column(String, nullable=False)

    entity_type = Column(String, nullable=True)

    entity_id = Column(String, nullable=True)

    details = Column(Text, nullable=True)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )