from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://user:pass@localhost:5432/smart_cv"


settings = Settings()
