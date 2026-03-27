from dataclasses import dataclass
from functools import lru_cache
import json
import logging

from google import genai
from google.genai import errors as genai_errors

from app.core.config import settings
from app.schemas.pipeline import CvAnalysis, JobAnalysis

logger = logging.getLogger(__name__)


@dataclass
class LLMResult:
    optimized_cv: str
    feedback: str


class LLMServiceError(RuntimeError):
    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.status_code = status_code


def generate_optimized_cv(
    cv_text: str,
    job_text: str,
    cv_analysis: CvAnalysis | None = None,
    job_analysis: JobAnalysis | None = None,
) -> LLMResult:
    cv_text = _truncate(cv_text, settings.max_cv_chars)
    job_text = _truncate(job_text, settings.max_job_chars)
    if cv_analysis is None:
        cv_analysis = analyze_cv_text(cv_text)
    if job_analysis is None:
        job_analysis = analyze_job_text(job_text)
    return _generate_with_gemini(
        cv_text=cv_text,
        job_text=job_text,
        cv_analysis=cv_analysis,
        job_analysis=job_analysis,
    )


def analyze_cv_text(cv_text: str) -> CvAnalysis:
    cv_text = _truncate(cv_text, settings.max_cv_chars)
    prompt = (
        "You are a CV analysis assistant. Extract structure and content from the CV.\n"
        "Return STRICT JSON only with the exact fields below.\n\n"
        "JSON schema:\n"
        "{\n"
        '  "summary": string,\n'
        '  "core_skills": string[],\n'
        '  "experience_bullets": string[],\n'
        '  "achievements": string[],\n'
        '  "gaps": string[]\n'
        "}\n\n"
        "Rules:\n"
        "- Use concise phrases.\n"
        "- Use action verbs when possible.\n"
        "- Do not invent facts.\n\n"
        f"CV:\n{cv_text}\n"
    )
    data = _generate_json_with_gemini(prompt)
    return CvAnalysis.model_validate(data)


def analyze_job_text(job_text: str) -> JobAnalysis:
    job_text = _truncate(job_text, settings.max_job_chars)
    prompt = (
        "You are a job description analysis assistant. Extract structure and ATS keywords.\n"
        "Return STRICT JSON only with the exact fields below.\n\n"
        "JSON schema:\n"
        "{\n"
        '  "title": string,\n'
        '  "responsibilities": string[],\n'
        '  "requirements": string[],\n'
        '  "keywords": string[],\n'
        '  "tools": string[],\n'
        '  "seniority": string\n'
        "}\n\n"
        "Rules:\n"
        "- Use concise phrases.\n"
        "- Keep keywords aligned to the posting.\n"
        "- Do not invent facts.\n\n"
        f"Job description:\n{job_text}\n"
    )
    data = _generate_json_with_gemini(prompt)
    return JobAnalysis.model_validate(data)


def _generate_with_gemini(
    cv_text: str,
    job_text: str,
    cv_analysis: CvAnalysis,
    job_analysis: JobAnalysis,
) -> LLMResult:
    if not settings.gemini_api_key:
        raise LLMServiceError("GEMINI_API_KEY is not set", status_code=500)

    client = _get_gemini_client()

    prompt = (
        "You are an expert CV optimizer. Rewrite the CV to match the job description.\n"
        "Goal: increase ATS match and hiring-manager clarity by 2–3x.\n\n"
        "Rules:\n"
        "- Use strong action verbs at the start of each bullet.\n"
        "- Keep an ATS-friendly, keyword-rich style aligned to the job description.\n"
        "- Use bullet points for experience and achievements.\n"
        "- Keep structure clean and scannable (section headers + bullets).\n"
        "- Preserve truthful content; do not invent skills, tools, or employers.\n"
        "- Prefer quantified impact (%, $, time saved, scale, volume) when present.\n"
        "- Remove fluff, tighten wording, keep it concise.\n"
        "- Output ONLY the improved CV text (no explanations, no extra labels).\n\n"
        f"CV analysis (JSON):\n{cv_analysis.model_dump_json()}\n\n"
        f"Job analysis (JSON):\n{job_analysis.model_dump_json()}\n\n"
        f"CV:\n{cv_text}\n\n"
        f"Job description:\n{job_text}\n\n"
        "Return the improved CV text."
    )

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )
    except genai_errors.ClientError as exc:
        message = str(exc)
        status_code = _map_gemini_error_to_status(message)
        logger.warning("Gemini client error: %s", message)
        raise LLMServiceError(f"GEMINI_ERROR: {message}", status_code=status_code) from exc
    except Exception as exc:
        message = str(exc)
        logger.exception("Gemini unexpected error: %s", message)
        raise LLMServiceError(f"GEMINI_ERROR: {message}", status_code=503) from exc

    optimized_cv = (getattr(response, "text", "") or "").strip()
    if not optimized_cv:
        raise LLMServiceError("GEMINI_ERROR: empty response", status_code=502)
    return LLMResult(
        optimized_cv=optimized_cv,
        feedback="Generated by Gemini API.",
    )


def _generate_json_with_gemini(prompt: str) -> dict:
    if not settings.gemini_api_key:
        raise LLMServiceError("GEMINI_API_KEY is not set", status_code=500)

    client = _get_gemini_client()
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )
    except genai_errors.ClientError as exc:
        message = str(exc)
        status_code = _map_gemini_error_to_status(message)
        logger.warning("Gemini client error: %s", message)
        raise LLMServiceError(f"GEMINI_ERROR: {message}", status_code=status_code) from exc
    except Exception as exc:
        message = str(exc)
        logger.exception("Gemini unexpected error: %s", message)
        raise LLMServiceError(f"GEMINI_ERROR: {message}", status_code=503) from exc

    raw_text = (getattr(response, "text", "") or "").strip()
    if not raw_text:
        raise LLMServiceError("GEMINI_ERROR: empty response", status_code=502)
    return _extract_json(raw_text)


def _extract_json(raw_text: str) -> dict:
    text = raw_text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise LLMServiceError("GEMINI_ERROR: invalid JSON response", status_code=502)
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError as exc:
        raise LLMServiceError("GEMINI_ERROR: invalid JSON response", status_code=502) from exc


def _truncate(value: str, limit: int) -> str:
    if limit <= 0:
        return ""
    if len(value) <= limit:
        return value
    return value[:limit].rstrip()


@lru_cache(maxsize=1)
def _get_gemini_client() -> genai.Client:
    return genai.Client(api_key=settings.gemini_api_key)


def _map_gemini_error_to_status(message: str) -> int:
    lowered = message.lower()
    if "resource_exhausted" in lowered or "quota" in lowered:
        return 429
    if "permission_denied" in lowered or "unauthorized" in lowered or "api key" in lowered:
        return 401
    if "deadline" in lowered or "timeout" in lowered or "unavailable" in lowered:
        return 503
    return 502
