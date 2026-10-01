# Architecture

## Current Status

**Stage 0 — COMPLETE**

**Stage 1 — PREPARED / NOT YET IMPLEMENTED**

This document describes the current architecture and clearly separates implemented behavior from future-stage behavior.

---

## Stage 0 Boundary

The project is a standalone monorepo containing:

- FastAPI backend
- Next.js frontend
- PostgreSQL 16 with pgvector
- Redis 7
- SQLAlchemy database layer
- Alembic migration tooling
- Automated testing and quality tooling

Current architecture:

```text
Browser
   │
   ▼
Next.js Frontend
   │
   ▼
FastAPI API
   │
   ├──────────────► PostgreSQL 16 + pgvector
   │
   └──────────────► Redis 7
```

Future architecture will add components such as object storage, background workers, embedding services, and an LLM provider.

---

## Stage 0 Components

### Frontend

The frontend is a Next.js 14 application using:

- App Router
- React
- TypeScript

The frontend currently provides the application skeleton.

It does not implement:

- authentication
- authorization
- tenant selection
- tenant authorization
- security-sensitive backend credentials

Only browser-safe configuration may be exposed to the frontend.

### Backend

The backend is a FastAPI application.

Stage 0 responsibilities include:

- application startup/shutdown
- configuration loading
- CORS configuration
- correlation/request ID handling
- structured logging
- health endpoint
- readiness endpoint
- PostgreSQL connectivity checks
- Redis connectivity checks

### PostgreSQL

PostgreSQL 16 with pgvector provides the local relational database.

Stage 0 deliberately creates no application schema.

Stage 1 will introduce the application's tenant-aware security schema and RLS policies.

### Redis

Redis 7 is configured as a local dependency.

Redis is not an authorization source of truth.

Authorization must ultimately be enforced by trusted backend/database controls.

---

## Trust Boundaries

### Browser

The browser is untrusted.

Client-controlled values must never be treated as authoritative for:

- tenant identity
- authorization
- roles
- permissions
- access control

### API

The API is the future application authorization boundary.

Stage 0 does not yet implement authentication or authorization.

### PostgreSQL

PostgreSQL becomes the tenant-isolation boundary in Stage 1 through Row-Level Security.

The intended model is:

```text
Trusted server-side identity
        │
        ▼
Tenant context
        │
        ▼
Database transaction
        │
        ▼
PostgreSQL RLS
        │
        ▼
Tenant-scoped data
```

### Redis

Redis is a dependency/cache.

It must never become the authoritative source of authorization truth.

---

## Database Roles

The local database uses separate roles:

```text
rag_dev
    │
    └── Local development/bootstrap administration

rag_migration_admin
    │
    └── Alembic migrations

rag_app
    │
    └── Runtime application access
```

The runtime application role must not be a PostgreSQL superuser and must not have `BYPASSRLS`.

---

## Stage 1 Architectural Direction

Stage 1 will introduce the foundational multi-tenant data model:

```text
Tenant
  │
  ├── Users
  │     └── Roles
  │           └── Permissions
  │
  ├── Documents
  │     └── Chunks
  │
  ├── Document ACLs
  │
  ├── Sessions
  │
  ├── Refresh Tokens
  │
  └── Audit Events
```

Every tenant-owned resource will have an explicit tenant relationship.

PostgreSQL RLS will enforce tenant isolation independently of application query intent.

---

## Tenant Context

Stage 1 is expected to establish tenant context using a transaction-local PostgreSQL setting.

Conceptually:

```sql
SET LOCAL app.tenant_id = '<trusted-tenant-id>';
```

RLS policies can then compare the row's `tenant_id` against the current transaction context.

Conceptually:

```sql
tenant_id = current_setting('app.tenant_id', true)::uuid
```

`SET LOCAL` is important because pooled connections must not retain tenant context between requests.

The exact implementation will be finalized and tested during Stage 1.

---

## Stage 1 Security Boundary

Stage 1 establishes the first actual application security boundary:

```text
Application
     │
     ▼
Trusted tenant context
     │
     ▼
PostgreSQL transaction
     │
     ▼
RLS policy
     │
     ├── Tenant A data → Tenant A only
     │
     └── Tenant B data → isolated
```

Missing tenant context must fail closed.

Cross-tenant access must be denied at the database layer.

---

## Explicitly Deferred

The following are not implemented in Stage 0:

- Authentication
- Login
- Password hashing/verification
- JWT
- MFA
- Authentication middleware
- Authorization middleware
- Document uploads
- Ingestion workers
- Embedding generation
- Vector retrieval
- RAG
- Prompt-injection defenses
- LLM output filtering
- Production Kubernetes
- Production observability
- Production backup/DR

These capabilities will be implemented in later stages according to the implementation plan.