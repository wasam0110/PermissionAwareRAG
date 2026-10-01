# Permission-Aware Multi-Tenant RAG

A standalone, security-first multi-tenant Retrieval-Augmented Generation (RAG) platform.

The project is implemented through explicit security and functionality stages. Each stage must pass its implementation, testing, documentation, and completion gate before the next stage begins.

---

## Current Status

**Stage 0 — Project Foundation: COMPLETE**

**Stage 1 — Multi-Tenant Database and PostgreSQL RLS: NEXT / NOT IMPLEMENTED**

Stage 0 establishes the repository, backend/frontend foundations, local infrastructure, configuration, logging, health/readiness endpoints, Alembic migration tooling, automated tests, and development quality checks.

Stage 1 will establish the first actual application security boundary through the multi-tenant database schema and PostgreSQL Row-Level Security.

Authentication, document ingestion, permission-aware retrieval, RAG, LLM security, and production deployment are intentionally deferred to later stages.

---

## Technology

### Backend

- Python 3.11
- FastAPI
- Uvicorn
- Pydantic Settings
- SQLAlchemy
- Alembic
- asyncpg
- psycopg
- Redis

### Database and Infrastructure

- PostgreSQL 16
- pgvector
- Redis 7
- Docker Compose

### Frontend

- Next.js 14
- React
- TypeScript
- App Router

### Quality

- pytest
- pytest-asyncio
- Ruff
- mypy
- ESLint
- Vitest

---

## Stage 0 Scope

Stage 0 provides:

- repository structure
- backend application skeleton
- frontend application skeleton
- environment configuration
- local PostgreSQL + pgvector
- local Redis
- database connectivity checks
- Redis connectivity checks
- health endpoint
- readiness endpoint
- structured logging
- correlation/request IDs
- CORS configuration
- Alembic configuration
- asynchronous Alembic migration support
- development quality tooling
- automated tests

Stage 0 deliberately does not implement:

- user authentication
- login
- password verification
- JWT issuance
- MFA
- tenant authorization
- PostgreSQL RLS
- document ingestion
- document processing
- vector retrieval
- RAG
- prompt-injection defenses
- LLM output protection
- production Kubernetes deployment

---

## Local Infrastructure

This project uses non-default host ports to avoid conflicts with other local services.

| Service | Container Port | Host Port |
|---|---:|---:|
| PostgreSQL | 5432 | 5433 |
| Redis | 6379 | 6380 |

The application therefore connects to:

```text
PostgreSQL: localhost:5433
Redis:      localhost:6380
```

The container ports remain PostgreSQL `5432` and Redis `6379`.

---

## Database Roles

The local PostgreSQL environment uses separate roles:

- `rag_dev` — local bootstrap/development administration
- `rag_migration_admin` — migration role
- `rag_app` — restricted application runtime role

The application must not use `rag_dev` as its runtime database role.

The `rag_app` role is configured without superuser or `BYPASSRLS` privileges so that PostgreSQL RLS can become a genuine database security boundary in Stage 1.

---

## Stage Plan

| Stage | Scope | Status |
|---|---|---|
| Stage 0 | Repository foundation and local infrastructure | **Complete** |
| Stage 1 | Multi-tenant schema and PostgreSQL RLS | **Next** |
| Stage 2 | Authentication, sessions, MFA, RBAC/ABAC | Planned |
| Stage 3 | Secure document management and ingestion | Planned |
| Stage 4 | Permission-aware RAG | Planned |
| Stage 5 | LLM security and output protection | Planned |
| Stage 6 | Authenticated frontend application | Planned |
| Stage 7 | Public website, SEO, HTTPS, accessibility | Planned |
| Stage 8 | Privacy, consent, analytics, spam controls | Planned |
| Stage 9 | Production infrastructure | Planned |
| Stage 10 | Security testing, observability, backup/DR, release | Planned |

---

## Stage 0 Quality Checks

The Stage 0 implementation has passed:

```text
pytest
5 passed

ruff check backend tests
All checks passed!

mypy backend
Success: no issues found

Frontend lint
Passed

Frontend tests
1 passed

Frontend production build
Passed
```

The Python test suite currently reports a deprecation warning related to the Starlette/httpx test-client integration. The warning does not cause the Stage 0 tests to fail.

---

## Stage Boundary

The Stage 0 completion boundary is intentional.

The repository is ready for Stage 1, but Stage 1 must not be considered implemented until:

1. The database schema exists.
2. Tenant ownership is explicitly represented.
3. PostgreSQL RLS policies are implemented.
4. The application database role is restricted.
5. Missing tenant context fails closed.
6. Cross-tenant access is denied.
7. Database-level RLS tests pass.
8. Application-level isolation tests pass.
9. Documentation and evidence are updated.
10. The Stage 1 completion gate passes.

---

## Documentation

Project documentation:

- [DEVELOPMENT.md](DEVELOPMENT.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [DATABASE.md](DATABASE.md)
- [API_SPEC.md](API_SPEC.md)
- [SECURITY.md](SECURITY.md)
- [SECURITY_TEST_PLAN.md](SECURITY_TEST_PLAN.md)
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)
- [DECISIONS.md](DECISIONS.md)

---

## Development

Start local infrastructure:

```bash
docker compose -f infra/docker/docker-compose.yml up -d
```

Start the backend:

```bash
uvicorn backend.main:app --reload
```

Start the frontend:

```bash
cd frontend
npm run dev
```

Run backend quality checks:

```bash
pytest
ruff check backend tests
mypy backend
```

Run frontend checks:

```bash
cd frontend
npm run lint
npm run test
npm run build
```

---

## Project Principles

The project follows these principles:

1. Security boundaries are implemented before dependent features.
2. Tenant isolation is enforced at the database layer.
3. Client-controlled identity is never authoritative.
4. Missing security context fails closed.
5. Privileged database roles are not used for normal application access.
6. Each stage must pass its completion gate before the next begins.
7. Documentation must reflect actual implementation status.
8. Future functionality must not be represented as already implemented.

---

## License

Project-specific licensing information will be added when finalized.