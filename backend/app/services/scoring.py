from dataclasses import dataclass


@dataclass
class ScoreResult:
    score: int
    missing_keywords: list[str]


def compute_score(cv_keywords: list[str], job_keywords: list[str]) -> ScoreResult:
    # TODO: weighted scoring
    if not job_keywords:
        return ScoreResult(score=0, missing_keywords=[])

    cv_set = {k.lower() for k in cv_keywords}
    job_set = {k.lower() for k in job_keywords}
    matched = cv_set.intersection(job_set)
    missing = sorted(job_set - cv_set)
    score = int((len(matched) / max(len(job_set), 1)) * 100)
    return ScoreResult(score=score, missing_keywords=missing)
