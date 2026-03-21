from pydantic import BaseModel


class OptimizeRequest(BaseModel):
    cv_text: str
    job_text: str


class OptimizeResponse(BaseModel):
    optimized_cv: str
    feedback: str
