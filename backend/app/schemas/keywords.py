from pydantic import BaseModel, Field, field_validator


class KeywordExtractionRequest(BaseModel):
    job_text: str = Field(min_length=1, max_length=12000)

    @field_validator("job_text", mode="before")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("must be a string")
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be empty")
        return cleaned


class KeywordExtractionResult(BaseModel):
    skills: list[str]
    requirements: list[str]


class KeywordExtractionResponse(BaseModel):
    skills: list[str]
    requirements: list[str]
    keyword_list_id: int | None = None
    feedback: str
