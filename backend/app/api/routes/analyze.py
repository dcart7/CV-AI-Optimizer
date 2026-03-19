from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.analysis import AnalysisResponse

router = APIRouter()


@router.post("", response_model=AnalysisResponse)
async def analyze_cv(
    file: UploadFile = File(...),
    job_description: str = Form(...),
) -> AnalysisResponse:
    # TODO: wire services
    return AnalysisResponse(
        score=0,
        missing_keywords=[],
        optimized_cv="",
        feedback="",
    )
