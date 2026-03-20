from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so metadata is populated before create_all
from app.models.user import User  # noqa: F401
from app.models.analysis import Analysis  # noqa: F401
