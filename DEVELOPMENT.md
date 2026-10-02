# Development Setup

## Runtime

- Python 3.11
- Node.js 20+
- PostgreSQL 16 with pgvector
- Redis 7
- Docker Desktop with Compose
- Next.js 14

## Local Services

Start PostgreSQL and Redis from the repository root:

```powershell
docker compose -f infra/docker/docker-compose.yml up -d
docker compose -f infra/docker/docker-compose.yml ps
```

Expected:

```text
postgres   healthy
redis      healthy
```

Host ports:

```text
PostgreSQL: localhost:5433
Redis:      localhost:6380
```

Inside containers, the internal ports remain:

```text
PostgreSQL: 5432
Redis:      6379
```

Do not stop unrelated services using the default ports.

## Environment

Create the local environment file:

```powershell
Copy-Item .env.example .env
```

Do not commit `.env`. It contains local credentials and is ignored by Git.

Required local connection values:

```env
DATABASE_URL=postgresql+asyncpg://rag_app:change-me-app@localhost:5433/rag_dev
MIGRATION_DATABASE_URL=postgresql+psycopg://rag_migration_admin:change-me-migration@localhost:5433/rag_dev
REDIS_URL=redis://:change-me@localhost:6380/0
```

## Python Environment

Create and activate the virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements-dev.txt
```

## Backend

Run from the repository root:

```powershell
uvicorn backend.main:app --reload
```

Default URL:

```text
http://127.0.0.1:8000
```

Health check:

```text
GET http://127.0.0.1:8000/health
```

Readiness check:

```text
GET http://127.0.0.1:8000/ready
```

Readiness requires healthy PostgreSQL and Redis dependencies.

## Database and Migrations

Application runtime uses:

```text
rag_app
```

Alembic migrations use:

```text
rag_migration_admin
```

The backend must never use `rag_dev` as its runtime database identity.

Check migration state:

```powershell
alembic -c alembic.ini current
```

Apply migrations:

```powershell
alembic -c alembic.ini upgrade head
```

Do not use this unless an intentional local data reset is required:

```powershell
docker compose -f infra/docker/docker-compose.yml down -v
```

The `-v` flag deletes local PostgreSQL and Redis volumes.

## Frontend

From the repository root:

```powershell
cd frontend
npm install
npm run dev
```

Only browser-safe `NEXT_PUBLIC_*` values may be exposed. Server credentials must never be placed in frontend variables.

## Quality Checks

Run backend checks from the repository root:

```powershell
pytest
ruff check backend tests
mypy backend
```

Run frontend checks from `frontend`:

```powershell
npm run lint
npm run test
npm run build
```

## Current Stage

- **Stage 0:** Complete
- **Stage 1:** Database schema, roles, migrations, RLS, and initial isolation tests implemented
- **Stage 1 remaining:** Expanded isolation coverage and final acceptance review

Use a separate Git branch for each stage and push only after the relevant checks and documentation are complete.