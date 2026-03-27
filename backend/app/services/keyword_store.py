import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.keyword_list import KeywordList

logger = logging.getLogger(__name__)


def save_keyword_list(
    db: Session,
    source_text: str,
    skills: list[str],
    requirements: list[str],
) -> int | None:
    record = KeywordList(
        source_text=source_text,
        skills=skills,
        requirements=requirements,
    )
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record.id
    except SQLAlchemyError as exc:
        db.rollback()
        logger.warning("Failed to save keyword list: %s", exc)
        return None
