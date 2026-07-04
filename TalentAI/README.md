# TalentAI - Enterprise AI-Powered Campus Placement System

TalentAI is a placement management scaffold that demonstrates resume screening and candidate-role matching with an AI-service architecture.

## Architecture

- `backend` - FastAPI service for candidate ingestion, job definitions, and rule/RAG-style matching.
- `frontend` - React + TypeScript interface for recruiters and placement teams.
- `k8s` - Kubernetes manifests for deployment.
- `docker-compose.yml` - local multi-service run file.

## Run Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/docs`

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

## Run With Docker

```bash
docker compose up --build
```
