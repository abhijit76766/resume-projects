from .schemas import Candidate, JobRole, MatchResponse


def normalize(items: list[str]) -> set[str]:
    return {item.strip().lower() for item in items if item.strip()}


def keyword_overlap(text: str, required_skills: set[str]) -> set[str]:
    resume_text = text.lower()
    return {skill for skill in required_skills if skill in resume_text}


def match_candidate(candidate: Candidate, role: JobRole) -> MatchResponse:
    candidate_skills = normalize(candidate.skills)
    required_skills = normalize(role.required_skills)
    direct_matches = candidate_skills & required_skills
    rag_style_matches = keyword_overlap(candidate.resume_text, required_skills)
    matched = sorted(direct_matches | rag_style_matches)
    missing = sorted(required_skills - set(matched))

    skill_score = len(matched) / len(required_skills) if required_skills else 1
    experience_bonus = min(candidate.experience_years / 5, 1) * 0.15
    score = min((skill_score * 0.85) + experience_bonus, 1.0)

    if score >= 0.75:
        recommendation = "Shortlist"
    elif score >= 0.5:
        recommendation = "Review manually"
    else:
        recommendation = "Do not shortlist"

    explanation = (
        f"{candidate.name} matches {len(matched)} of {len(required_skills)} required skills "
        f"for {role.title}. Missing skills: {', '.join(missing) if missing else 'none'}."
    )

    return MatchResponse(
        score=round(score * 100, 2),
        matched_skills=matched,
        missing_skills=missing,
        recommendation=recommendation,
        explanation=explanation,
    )
