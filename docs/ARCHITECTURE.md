# Architecture

## Stage 0 boundary

Standalone monorepo with a FastAPI backend, Next.js frontend, local PostgreSQL/pgvector and Redis development services, and Alembic migration tooling.

```text
Browser -> Next.js frontend -> FastAPI API -> PostgreSQL / Redis
                                          -> later: object storage, workers, LLM provider
```

## Trust boundaries

- The browser is untrusted and receives no server secrets.
- The API is the future authorization boundary.
- PostgreSQL becomes the tenant-isolation boundary in Stage 1 through RLS.
- Redis is a cache/dependency, never the source of authorization truth.

Stage 0 intentionally does not implement authentication, RLS, document ingestion, RAG, workers, or Kubernetes deployment behavior.
