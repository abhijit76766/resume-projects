from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .matcher import match_candidate
from .schemas import Candidate, JobRole, MatchRequest, MatchResponse

app = FastAPI(title="TalentAI Placement Matching API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEMO_CANDIDATES: list[Candidate] = [
    Candidate(
        name="Aarav Mehta",
        email="aarav@example.com",
        skills=["Python", "FastAPI", "React", "SQL", "Docker"],
        experience_years=1.2,
        resume_text="Built placement dashboards using React, FastAPI, SQL, Docker, and AWS basics.",
    ),
    Candidate(
        name="Nisha Rao",
        email="nisha@example.com",
        skills=["Java", "Spring Boot", "MySQL", "Git"],
        experience_years=0.8,
        resume_text="Java developer with internship experience in Spring Boot and MySQL.",
    ),
]

DEMO_ROLES: list[JobRole] = [
    JobRole(
        title="Full Stack AI Intern",
        required_skills=["Python", "React", "FastAPI", "SQL", "Docker"],
        description="Build AI-enabled placement workflows and recruiter dashboards.",
    )
]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/candidates", response_model=list[Candidate])
def list_candidates() -> list[Candidate]:
    return DEMO_CANDIDATES


@app.get("/roles", response_model=list[JobRole])
def list_roles() -> list[JobRole]:
    return DEMO_ROLES


@app.post("/match", response_model=MatchResponse)
def match(request: MatchRequest) -> MatchResponse:
    return match_candidate(request.candidate, request.role)
