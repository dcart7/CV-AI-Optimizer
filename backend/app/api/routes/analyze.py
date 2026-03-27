from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.analysis import AnalysisResponse
from app.schemas.keywords import (
    KeywordExtractionRequest,
    KeywordExtractionResponse,
)
from app.schemas.matching import MatchRequest, MatchResponse
from app.services.cv_parser import parse_cv
from app.services.keyword_store import save_keyword_list
from app.services.llm import LLMServiceError, extract_job_keywords
from app.services.matching import compute_match_score
from app.db.session import get_db

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


@router.post("/keywords", response_model=KeywordExtractionResponse)
def extract_keywords(
    payload: KeywordExtractionRequest,
    db: Session = Depends(get_db),
) -> KeywordExtractionResponse:
    try:
        result = extract_job_keywords(payload.job_text)
    except LLMServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unexpected server error") from exc

    keyword_list_id = save_keyword_list(
        db=db,
        source_text=payload.job_text,
        skills=result.skills,
        requirements=result.requirements,
    )

    return KeywordExtractionResponse(
        skills=result.skills,
        requirements=result.requirements,
        keyword_list_id=keyword_list_id,
        feedback="Keyword list saved.",
    )


@router.post("/match", response_model=MatchResponse)
def match_cv_job(payload: MatchRequest) -> MatchResponse:
    try:
        keyword_result = extract_job_keywords(payload.job_text)
    except LLMServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unexpected server error") from exc

    keywords = keyword_result.skills + keyword_result.requirements
    match_percent, matched, missing = compute_match_score(payload.cv_text, keywords)

    return MatchResponse(
        match_percent=match_percent,
        matched_keywords=matched,
        missing_keywords=missing,
        total_keywords=len(matched) + len(missing),
        feedback="Match score computed from extracted keywords.",
    )
