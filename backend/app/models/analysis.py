from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, Text
from sqlalchemy.sql import func

from app.db.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_cv = Column(Text, nullable=False)
    job_description = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)
    result_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
