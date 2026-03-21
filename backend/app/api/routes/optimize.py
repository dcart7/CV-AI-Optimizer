from fastapi import APIRouter, HTTPException

from app.schemas.optimize import OptimizeRequest, OptimizeResponse
from app.services.llm import generate_optimized_cv

router = APIRouter()


@router.post("/optimize", response_model=OptimizeResponse)
def optimize_cv(payload: OptimizeRequest) -> OptimizeResponse:
    try:
        result = generate_optimized_cv(
            cv_text=payload.cv_text,
            job_text=payload.job_text,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return OptimizeResponse(
        optimized_cv=result.optimized_cv,
        feedback=result.feedback,
    )
