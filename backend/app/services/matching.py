import re


def compute_match_score(cv_text: str, keywords: list[str]) -> tuple[int, list[str], list[str]]:
    normalized_cv = _normalize_text(cv_text)
    matched: list[str] = []
    missing: list[str] = []

    for keyword in _unique_preserve_order(keywords):
        if not keyword:
            continue
        normalized_kw = _normalize_text(keyword)
        if not normalized_kw:
            continue
        if normalized_kw in normalized_cv:
            matched.append(keyword)
        else:
            missing.append(keyword)

    total = len(matched) + len(missing)
    if total == 0:
        return 0, matched, missing
    match_percent = round((len(matched) / total) * 100)
    return match_percent, matched, missing


def _normalize_text(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return " ".join(cleaned.split())


def _unique_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result
