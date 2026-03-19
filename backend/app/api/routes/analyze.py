from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.analysis import AnalysisResponse
from app.services.cv_parser import parse_cv

router = APIRouter()


@router.post("", response_model=AnalysisResponse)
async def analyze_cv(
    file: UploadFile = File(...),
    job_description: str = Form(...),
) -> AnalysisResponse:
    file_bytes = await file.read()
    parsed = parse_cv(file_bytes=file_bytes, filename=file.filename or "")
    return AnalysisResponse(
        score=0,
        missing_keywords=[],
        optimized_cv=parsed.raw_text,
        feedback="Stage 3: extracted plain text from CV PDF/TXT.",
    )
