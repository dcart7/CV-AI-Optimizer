from dataclasses import dataclass


@dataclass
class LLMResult:
    optimized_cv: str
    feedback: str


def generate_optimized_cv(cv_text: str, job_text: str) -> LLMResult:
    # TODO: integrate LLM provider
    return LLMResult(optimized_cv="", feedback="")
