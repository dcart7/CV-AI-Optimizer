import io
from dataclasses import dataclass

import pdfplumber


@dataclass
class ParsedCV:
    raw_text: str
    skills: list[str]
    work_experience: list[str]
    education: list[str]
    achievements: list[str]


def _clean_text(text: str) -> str:
    return " ".join(text.split())


def _extract_section(text: str, headers: list[str]) -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    out: list[str] = []
    capture = False
    for line in lines:
        if not line:
            continue
        lower = line.lower().strip(":")
        if any(lower == h for h in headers):
            capture = True
            continue
        if capture and lower in {"skills", "experience", "work experience", "education", "achievements"}:
            capture = False
        if capture:
            out.append(line)
    return out


def _extract_skills(text: str) -> list[str]:
    skills_lines = _extract_section(text, ["skills", "technical skills", "tech skills"])
    if skills_lines:
        joined = " ".join(skills_lines)
        parts = [p.strip("•- ").strip() for p in joined.replace(";", ",").split(",")]
        return [p for p in parts if p]
    return []


def _extract_experience(text: str) -> list[str]:
    return _extract_section(text, ["experience", "work experience", "professional experience"])


def _extract_education(text: str) -> list[str]:
    return _extract_section(text, ["education", "academic background"])


def parse_cv(file_bytes: bytes, filename: str) -> ParsedCV:
    if filename.lower().endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        raw_text = "\n".join(pages)
    else:
        raw_text = file_bytes.decode("utf-8", errors="ignore")

    cleaned = _clean_text(raw_text)
    return ParsedCV(
        raw_text=cleaned,
        skills=_extract_skills(raw_text),
        work_experience=_extract_experience(raw_text),
        education=_extract_education(raw_text),
        achievements=[],
    )
