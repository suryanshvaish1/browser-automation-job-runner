from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

from .database import Base


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    url = Column(Text, nullable=False)

    goal = Column(Text, nullable=False)

    status = Column(String, nullable=False)

    result = Column(JSONB, nullable=True)

    error = Column(Text, nullable=True)

    logs = Column(JSONB, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow)