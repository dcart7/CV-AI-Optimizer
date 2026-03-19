from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    score: int
    missing_keywords: list[str]
    optimized_cv: str
    feedback: str
