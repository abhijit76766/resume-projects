from pydantic import BaseModel, Field


class Candidate(BaseModel):
    name: str
    email: str
    skills: list[str] = Field(default_factory=list)
    experience_years: float = 0
    resume_text: str


class JobRole(BaseModel):
    title: str
    required_skills: list[str] = Field(default_factory=list)
    description: str


class MatchRequest(BaseModel):
    candidate: Candidate
    role: JobRole


class MatchResponse(BaseModel):
    score: float
    matched_skills: list[str]
    missing_skills: list[str]
    recommendation: str
    explanation: str
