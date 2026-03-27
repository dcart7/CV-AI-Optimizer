from sqlalchemy import Column, DateTime, Integer, JSON, Text
from sqlalchemy.sql import func

from app.db.base import Base


class KeywordList(Base):
    __tablename__ = "keyword_lists"

    id = Column(Integer, primary_key=True, index=True)
    source_text = Column(Text, nullable=False)
    skills = Column(JSON, nullable=False)
    requirements = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
