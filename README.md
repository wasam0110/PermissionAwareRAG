# Permission-Aware Multi-Tenant RAG

Standalone, security-first multi-tenant retrieval-augmented generation platform.

## Stage 0 status

This repository currently implements the **Stage 0 project foundation** only. Authentication, RLS, document ingestion, RAG, and production Kubernetes behavior are intentionally deferred to later stages.

## Technology

- Backend: Python 3.12, FastAPI, Uvicorn, Pydantic Settings, SQLAlchemy, Alembic
- Data services: PostgreSQL 16 with pgvector, Redis 7
- Frontend: Next.js 14 App Router, TypeScript
- Quality: pytest, Ruff, mypy, ESLint, Vitest

The project uses ordinary open-source/runtime dependencies only. It does not require any Manus SDK, MCP package, Manus API, or Manus-hosted runtime.

See [DEVELOPMENT.md](DEVELOPMENT.md), [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md), and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
