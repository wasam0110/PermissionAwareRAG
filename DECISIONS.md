# Architecture Decisions

## ADR-0001 — Standalone Project Dependencies

**Date:** 2026-10-01  
**Status:** Accepted

### Decision

Use standard open-source/runtime dependencies only.

The project must not depend on:

- Manus SDKs
- Manus MCP packages
- Manus APIs
- Manus-hosted runtime assumptions

### Reason

The project must remain portable and independently deployable.

### Consequence

External integrations must use ordinary environment variables and documented adapters.

---

## ADR-0002 — Stage-Gated Implementation

**Date:** 2026-10-01  
**Status:** Accepted

### Decision

Implement one PRD stage at a time and block progression until its acceptance criteria pass.

### Reason

Security boundaries must exist before higher-level features depend on them.

### Consequence

Stage 0 contains no:

- authentication
- RLS
- document ingestion
- RAG

Later stages cannot claim functionality that has not passed its completion gate.

---

## ADR-0003 — Patched Next.js 14 Release

**Date:** 2026-10-01  
**Status:** Accepted

### Decision

Use Next.js `14.2.35`.

### Reason

The initial Next.js 14.2.21 dependency emitted a security warning during installation.

### Consequence

The project remains on the required Next.js 14 line while using the patched release selected for the project.

---

## ADR-0004 — Python 3.11 Runtime

**Date:** 2026-10-01  
**Status:** Accepted

### Decision

Use Python 3.11 for:

- local development
- CI
- backend runtime
- backend container

### Reason

Python 3.11 is the runtime requirement selected for this project and supersedes the PRD's initial Python 3.12 baseline.

### Consequence

Project tooling targets `py311`.

Dependency compatibility must be maintained against Python 3.11.

---

## ADR-0005 — PostgreSQL Host Port 5433

**Date:** 2026-10-01  
**Status:** Accepted

### Decision

Use host port `5433` for this project's PostgreSQL container.

### Reason

Another PostgreSQL installation is already using host port `5432`.

Changing the host port avoids interfering with unrelated local projects.

### Configuration

```text
Host port:      5433
Container port: 5432
Database:       rag_dev
```

The application therefore connects to:

```text
localhost:5433
```

This is a local-development networking decision only.

---

## ADR-0006 — Redis Host Port 6380

**Date:** 2026-10-01  
**Status:** Accepted

### Decision

Use host port `6380` for this project's Redis container.

### Reason

Another local project is already using host port `6379`.

### Configuration

```text
Host port:      6380
Container port: 6379
```

The application therefore connects to:

```text
localhost:6380
```

The unrelated Redis service using port `6379` must not be stopped solely for this project.

---

## ADR-0007 — Separate Database Roles

**Date:** 2026-10-01  
**Status:** Accepted

### Decision

Use separate PostgreSQL roles for:

```text
rag_dev
rag_migration_admin
rag_app
```

### Responsibilities

```text
rag_dev
    ↓
Local development/bootstrap administration

rag_migration_admin
    ↓
Alembic migrations

rag_app
    ↓
Runtime application access
```

### Reason

Separating responsibilities reduces the privileges available to the application and establishes the foundation required for PostgreSQL RLS.

### Security Requirement

`rag_app` must not:

- be a PostgreSQL superuser
- have `BYPASSRLS`

---

## ADR-0008 — PostgreSQL RLS as Tenant Security Boundary

**Date:** 2026-10-01  
**Status:** Accepted

### Decision

Stage 1 will use PostgreSQL Row-Level Security as a primary tenant-isolation boundary.

### Reason

Application query filtering alone is not sufficient to establish a strong database-level tenant-isolation boundary.

### Intended Design

Tenant context will be established from trusted server-side identity and applied transaction-locally.

Conceptually:

```sql
SET LOCAL app.tenant_id = '<trusted-tenant-id>';
```

RLS policies will compare row ownership with the active tenant context.

### Consequence

Cross-tenant access must remain blocked even when an application query is incorrectly broad.

The implementation must be verified with database-level and application-level tests.

---

## ADR-0009 — No Application Schema in Stage 0

**Date:** 2026-10-01  
**Status:** Accepted

### Decision

Stage 0 creates no application database tables.

### Reason

Stage 0 establishes infrastructure and migration tooling without prematurely introducing the application's security model.

### Consequence

The database is intentionally empty of application relations at the Stage 0 completion boundary.

Stage 1 will introduce the first application schema migration.

---

## ADR-0010 — Stage 1 May Define Authentication Storage Without Implementing Authentication

**Date:** 2026-10-01  
**Status:** Accepted

### Decision

Stage 1 may create database structures for:

- users
- roles
- permissions
- sessions
- refresh tokens

without implementing the complete authentication system.

### Reason

The database security foundation must exist before authentication can safely depend on it.

### Consequence

Authentication behavior remains a Stage 2 responsibility.

Stage 1 must not be represented as implementing login, JWT authentication, MFA, or complete authorization behavior.