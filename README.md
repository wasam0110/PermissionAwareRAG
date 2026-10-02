# Permission-Aware Multi-Tenant RAG

Standalone, security-first multi-tenant Retrieval-Augmented Generation platform.

## Current Status

- **Stage 0:** Complete
- **Stage 1:** Database security boundary implemented; expanded acceptance coverage pending

## Stack

- Python 3.11
- FastAPI and Uvicorn
- SQLAlchemy and Alembic
- PostgreSQL 16 with pgvector
- Redis 7
- Next.js 14, React, and TypeScript
- pytest, Ruff, mypy, ESLint, and Vitest
- Docker Compose

## Architecture

```text
Browser
   │
   ▼
Next.js Frontend
   │
   ▼
FastAPI Backend
   ├──► PostgreSQL + pgvector
   └──► Redis
```

The project is designed to be portable and does not depend on Manus SDKs, MCP packages, Manus APIs, or Manus-hosted runtime services.

## Local Development

Create the environment file:

```powershell
Copy-Item .env.example .env
```

Create and activate the Python environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements-dev.txt
```

Start local services:

```powershell
docker compose -f infra/docker/docker-compose.yml up -d
docker compose -f infra/docker/docker-compose.yml ps
```

Host ports:

```text
PostgreSQL: localhost:5433
Redis:      localhost:6380
```

Run the backend:

```powershell
uvicorn backend.main:app --reload
```

Run the frontend:

```powershell
cd frontend
npm install
npm run dev
```

## Database

Runtime database access uses the restricted role:

```text
rag_app
```

Alembic migrations use:

```text
rag_migration_admin
```

The backend must never use the privileged bootstrap role:

```text
rag_dev
```

Apply migrations:

```powershell
alembic -c alembic.ini upgrade head
```

Check migration state:

```powershell
alembic -c alembic.ini current
```

## Stage 1 Security Boundary

Stage 1 provides:

- Tenant-aware SQLAlchemy models
- Separate database roles
- PostgreSQL RLS and forced RLS
- Transaction-local tenant context
- Fail-closed behavior without tenant context
- Tenant-isolated documents and chunks
- Cross-tenant read, update, and delete tests
- Explicit application-role grants
- pgcrypto and pgvector extensions

The application role is not a superuser and does not have `BYPASSRLS`.

## Quality Checks

Backend:

```powershell
pytest
ruff check backend tests
mypy backend
```

Frontend:

```powershell
cd frontend
npm run lint
npm run test
npm run build
```

## Planned Stages

1. Multi-tenant database security boundary
2. Authentication, sessions, MFA, and RBAC/ABAC
3. Secure document management and ingestion
4. Permission-aware RAG
5. LLM security and output protection
6. Authenticated frontend
7. Public website, SEO, HTTPS, and accessibility
8. Privacy and abuse controls
9. Production infrastructure
10. Release readiness, observability, backup, and disaster recovery

## Security Principles

- Tenant isolation is enforced at the database layer.
- Client-controlled identity is never authoritative.
- Missing tenant context fails closed.
- Privileged database roles are not used for normal application access.
- Unauthorized content must not enter the LLM context.
- Documentation must reflect verified implementation status.
- A stage is not complete until its acceptance gate passes.