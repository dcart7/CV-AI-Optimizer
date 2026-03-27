from pydantic import BaseModel, Field


class AnalyzeCvRequest(BaseModel):
    cv_text: str = Field(min_length=1, max_length=12000)


class AnalyzeJobRequest(BaseModel):
    job_text: str = Field(min_length=1, max_length=12000)


class CvAnalysis(BaseModel):
    summary: str
    core_skills: list[str]
    experience_bullets: list[str]
    achievements: list[str]
    gaps: list[str]


class JobAnalysis(BaseModel):
    title: str
    responsibilities: list[str]
    requirements: list[str]
    keywords: list[str]
    tools: list[str]
    seniority: str


class AnalyzeCvResponse(BaseModel):
    cv_analysis: CvAnalysis
    feedback: str


class AnalyzeJobResponse(BaseModel):
    job_analysis: JobAnalysis
    feedback: str
