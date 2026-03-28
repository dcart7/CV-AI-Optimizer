def build_recommendations(missing_skills: list[str]) -> list[str]:
    if not missing_skills:
        return [
            "Tighten bullet points to emphasize impact metrics (%, $, scale, time saved).",
            "Align the Summary with the top job requirements.",
            "Ensure Skills section mirrors the exact job keywords (only if truthful).",
        ]

    top_skills = missing_skills[:5]
    recommendations: list[str] = []
    for skill in top_skills[:3]:
        recommendations.append(
            f"Add a bullet in Experience that shows hands-on work with {skill}."
        )

    recommendations.append(
        "Add missing skills to a dedicated Skills section (only if you have real experience)."
    )

    if len(top_skills) >= 2:
        recommendations.append(
            f"Create a short project/achievement bullet highlighting {top_skills[0]} and {top_skills[1]}."
        )

    return recommendations
