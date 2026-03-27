from sqlalchemy.orm import declarative_base

Base = declarative_base()


from app.models.user import User  # noqa: F401
from app.models.analysis import Analysis  # noqa: F401
from app.models.keyword_list import KeywordList  # noqa: F401
