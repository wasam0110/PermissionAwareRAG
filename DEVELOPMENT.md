# Development Setup

## Requirements

- Python 3.11+
- Node.js 20+
- Docker Engine and Docker Compose for PostgreSQL and Redis

## Start dependencies

```bash
docker compose -f infra/docker/docker-compose.yml up -d
cp .env.example .env
```

## Backend

```bash
python3.11 -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements-dev.txt
alembic -c alembic.ini upgrade head
uvicorn backend.main:app --reload
```

- `GET /health` checks process liveness only.
- `GET /ready` checks PostgreSQL and Redis dependency availability.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

The browser receives only `NEXT_PUBLIC_*` values. Secrets belong exclusively to the backend environment.

## Quality checks

```bash
pytest
ruff check backend tests
mypy backend
cd frontend && npm run lint && npm run test
```
