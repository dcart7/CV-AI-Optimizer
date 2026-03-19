from dataclasses import dataclass


@dataclass
class JobAnalysis:
    required_skills: list[str]
    optional_skills: list[str]
    responsibilities: list[str]


def analyze_job_description(text: str) -> JobAnalysis:
    # TODO: implement keyword extraction
    return JobAnalysis(required_skills=[], optional_skills=[], responsibilities=[])
