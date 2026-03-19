from dataclasses import dataclass


@dataclass
class ParsedCV:
    skills: list[str]
    work_experience: list[str]
    education: list[str]
    achievements: list[str]


def parse_cv(file_bytes: bytes, filename: str) -> ParsedCV:
    # TODO: implement PDF/TXT parsing
    return ParsedCV(skills=[], work_experience=[], education=[], achievements=[])
