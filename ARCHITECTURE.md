# Architecture

## Status

- **Stage 0:** Complete
- **Stage 1:** Database security boundary implemented; expanded acceptance coverage pending

## System Overview

Standalone monorepo:

```text
Browser
   │
   ▼
Next.js 14 Frontend
   │
   ▼
FastAPI Backend
   ├──► PostgreSQL 16 + pgvector
   └──► Redis 7
```

The project uses Python 3.11, FastAPI, SQLAlchemy, Alembic, PostgreSQL with pgvector, Redis, Next.js, TypeScript, pytest, Ruff, mypy, ESLint, and Vitest.

Future stages may add object storage, background workers, embedding services, and an LLM provider.

## Frontend

The Next.js frontend uses the App Router, React, and TypeScript.

The browser is untrusted. The frontend must never be authoritative for:

- Tenant identity
- User identity
- Roles
- Permissions
- Document access
- Database credentials or server-side secrets

Authentication and application features are implemented in later stages.

## Backend

The FastAPI backend currently provides:

- Configuration loading
- Application startup and shutdown
- CORS configuration
- Correlation/request IDs
- Structured logging
- Health and readiness endpoints
- PostgreSQL connectivity checks
- Redis connectivity checks
- SQLAlchemy database access
- Transaction-local security-context helpers

The backend uses `rag_app` for runtime database access and must not use the privileged bootstrap role.

## PostgreSQL

PostgreSQL 16 with pgvector is the primary relational and vector database.

Stage 1 provides:

- Tenant-aware SQLAlchemy models
- Alembic migrations
- `pgcrypto` and `vector` extensions
- Tenant-owned tables
- Explicit tenant ownership
- Row-Level Security
- Forced Row-Level Security
- Fail-closed tenant policies
- Application-role grants
- Cross-tenant isolation tests

The migration role is:

```text
rag_migration_admin
```

The runtime application role is:

```text
rag_app
```

`rag_app` is not a superuser, does not have `BYPASSRLS`, and is not the owner of application tables.

## Redis

Redis 7 is a local dependency for future caching, sessions, and background coordination.

Redis is not an authorization source of truth. Authorization must be enforced by trusted backend and database controls.

## Database Roles

```text
rag_dev
    Local bootstrap/development administration

rag_migration_admin
    Alembic migrations and schema administration

rag_app
    Runtime backend access
    No SUPERUSER
    No BYPASSRLS
```

## Stage 1 Data Model

```text
Tenant
 ├── Users
 │    └── Roles
 │         └── Permissions
 ├── Collections
 │    └── Documents
 │         ├── Document ACLs
 │         └── Chunks / embeddings
 ├── Sessions
 ├── Refresh Tokens
 └── Audit Events
```

The current schema includes:

```text
tenants
users
roles
permissions
user_roles
role_permissions
collections
documents
document_acl
chunks
sessions
refresh_tokens
audit_events
```

## Trust and Tenant Boundaries

```text
Trusted server identity
        │
        ▼
Transaction-local tenant context
        │
        ▼
PostgreSQL transaction
        │
        ▼
RLS policies
        │
        ▼
Tenant-scoped data
```

Tenant context is set transaction-locally:

```sql
SELECT set_config('app.tenant_id', '<trusted-tenant-uuid>', true);
```

RLS policies compare `tenant_id` to:

```sql
NULLIF(current_setting('app.tenant_id', true), '')::uuid
```

When context is missing, tenant-owned rows are invisible. Transaction-local settings prevent tenant context from leaking through pooled connections.

## RLS Boundary

Tenant-owned tables use:

```text
ENABLE ROW LEVEL SECURITY
FORCE ROW LEVEL SECURITY
```

The database enforces:

- Tenant-specific reads
- Tenant-specific inserts
- Tenant-specific updates
- Tenant-specific deletes
- Tenant-specific document and chunk access
- Fail-closed behavior without tenant context

`role_permissions` derives tenant ownership through its related role. The `permissions` table contains global permission definitions.

## Current Verification

Implemented and verified:

- Database migration chain
- Restricted application role
- Non-bypass RLS configuration
- Tenant-aware schema
- RLS policies
- Application grants
- Missing-context filtering
- Cross-tenant document read isolation
- Cross-tenant update isolation
- Cross-tenant delete isolation

## Deferred Capabilities

Later stages will implement:

- Authentication and login
- Password hashing and verification
- JWT and refresh-token rotation
- MFA
- Complete RBAC/ABAC enforcement
- Secure uploads and malware scanning
- Document ingestion and processing
- Permission-aware retrieval
- Prompt-injection defenses
- LLM output controls
- Rate limiting and abuse prevention
- Production deployment, observability, backups, and disaster recovery