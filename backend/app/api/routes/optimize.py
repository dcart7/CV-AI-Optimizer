from fastapi import APIRouter, HTTPException

from app.schemas.optimize import OptimizeRequest, OptimizeResponse
from app.services.llm import LLMServiceError, extract_job_keywords, generate_optimized_cv
from app.services.matching import compute_match_score
from app.services.recommendations import build_recommendations

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
        keyword_result = extract_job_keywords(payload.job_text)
        _, _, missing_skills = compute_match_score(
            payload.cv_text,
            keyword_result.skills,
        )
        recommendations = build_recommendations(missing_skills)
    except LLMServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unexpected server error") from exc

    return OptimizeResponse(
        optimized_cv=result.optimized_cv,
        feedback=result.feedback,
        missing_skills=missing_skills,
        recommendations=recommendations,
    )
