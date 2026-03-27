from fastapi import APIRouter, HTTPException

from app.schemas.optimize import OptimizeRequest, OptimizeResponse
from app.services.llm import LLMServiceError, generate_optimized_cv

router = APIRouter()


@router.post("/optimize", response_model=OptimizeResponse)
def optimize_cv(payload: OptimizeRequest) -> OptimizeResponse:
    try:
        result = generate_optimized_cv(
            cv_text=payload.cv_text,
            job_text=payload.job_text,
            cv_analysis=payload.cv_analysis,
            job_analysis=payload.job_analysis,
        )
    except LLMServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unexpected server error") from exc

    return OptimizeResponse(
        optimized_cv=result.optimized_cv,
        feedback=result.feedback,
    )
