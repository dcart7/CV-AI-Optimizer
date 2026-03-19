from dataclasses import dataclass


@dataclass
class JobAnalysis:
    required_skills: list[str]
    optional_skills: list[str]
    responsibilities: list[str]


def analyze_job_description(text: str) -> JobAnalysis:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    req_headers = {
        "requirements",
        "required",
        "required skills",
        "must have",
        "must-have",
        "qualifications",
    }
    opt_headers = {
        "nice to have",
        "nice-to-have",
        "preferred",
        "bonus",
    }
    resp_headers = {
        "responsibilities",
        "what you will do",
        "you will",
        "duties",
    }

    required: list[str] = []
    optional: list[str] = []
    responsibilities: list[str] = []
    current: list[str] | None = None

    for line in lines:
        lower = line.lower().strip(":")
        if lower in req_headers:
            current = required
            continue
        if lower in opt_headers:
            current = optional
            continue
        if lower in resp_headers:
            current = responsibilities
            continue

        if current is not None:
            item = line.lstrip("•- ").strip()
            if item:
                current.append(item)

    if not required:
        tokens = [
            t.strip("•- ").strip()
            for t in text.replace(";", ",").split(",")
            if len(t.strip()) > 2
        ]
        required = tokens[:25]

    return JobAnalysis(
        required_skills=required,
        optional_skills=optional,
        responsibilities=responsibilities,
    )
