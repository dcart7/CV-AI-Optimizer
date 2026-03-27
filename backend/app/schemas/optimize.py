from pydantic import BaseModel, Field, field_validator

from app.schemas.pipeline import CvAnalysis, JobAnalysis


class OptimizeRequest(BaseModel):
    cv_text: str = Field(min_length=1, max_length=12000)
    job_text: str = Field(min_length=1, max_length=12000)
    cv_analysis: CvAnalysis | None = None
    job_analysis: JobAnalysis | None = None

    @field_validator("cv_text", "job_text", mode="before")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("must be a string")
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be empty")
        return cleaned


class OptimizeResponse(BaseModel):
    optimized_cv: str
    feedback: str
