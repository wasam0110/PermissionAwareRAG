# Architecture Decisions

## ADR-0001 — Standalone Dependencies

- **Date:** 2026-10-01
- **Status:** Accepted

Use standard open-source dependencies only. The project must not depend on Manus SDKs, MCP packages, Manus APIs, or Manus-hosted runtime assumptions.

**Reason:** Keep the project portable and independently deployable.

## ADR-0002 — Stage-Gated Implementation

- **Date:** 2026-10-01
- **Status:** Accepted

Implement one PRD stage at a time. Do not proceed until the current stage’s tests and acceptance criteria pass.

Stage 0 intentionally excludes authentication, RLS, document ingestion, and RAG.

**Reason:** Security boundaries must exist before higher-level features depend on them.

## ADR-0003 — Patched Next.js Release

- **Date:** 2026-10-01
- **Status:** Accepted

Use Next.js `14.2.35`.

**Reason:** The original Next.js `14.2.21` dependency produced a security warning. This keeps the project on the required Next.js 14 line while using a patched release.

## ADR-0004 — Python 3.11 Runtime

- **Date:** 2026-10-01
- **Status:** Accepted

Use Python 3.11 for:

- Local development
- CI
- Backend runtime
- Backend container

This supersedes the PRD’s initial Python 3.12 baseline. Tooling targets `py311`, and dependencies must remain compatible with Python 3.11.

## ADR-0005 — Local Service Ports

- **Date:** 2026-10-01
- **Status:** Accepted

Use non-default host ports to avoid conflicts with other local services:

| Service | Host port | Container port |
|---|---:|---:|
| PostgreSQL | `5433` | `5432` |
| Redis | `6380` | `6379` |

The Windows-hosted backend connects through:

```text
PostgreSQL: localhost:5433
Redis: localhost:6380
```

Commands executed inside containers use the container ports.

## ADR-0006 — Separate Database Roles

- **Date:** 2026-10-01
- **Status:** Accepted

Use separate PostgreSQL roles:

| Role | Responsibility |
|---|---|
| `rag_dev` | Local bootstrap/development administration |
| `rag_migration_admin` | Alembic migrations |
| `rag_app` | Runtime application access |

`rag_app` must not be a superuser or have `BYPASSRLS`.

**Reason:** Limit application privileges and establish a reliable RLS boundary.

## ADR-0007 — PostgreSQL RLS Tenant Boundary

- **Date:** 2026-10-01
- **Status:** Accepted

Use PostgreSQL Row-Level Security as the primary tenant-isolation boundary.

Trusted server-side identity establishes transaction-local context:

```sql
SELECT set_config('app.tenant_id', '<trusted-tenant-id>', true);
```

RLS policies compare row ownership with the active tenant context.

**Reason:** Application query filtering alone is insufficient. Database-level isolation must remain effective even when a query is overly broad.

RLS behavior must be verified with direct database and application-level tests.

## ADR-0008 — No Application Schema in Stage 0

- **Date:** 2026-10-01
- **Status:** Accepted

Stage 0 creates infrastructure, health checks, and migration tooling but no application tables.

**Reason:** Avoid introducing the security model before the project is ready for Stage 1.

Stage 1 introduces the first application schema migration.

## ADR-0009 — Authentication Storage Before Authentication Behavior

- **Date:** 2026-10-01
- **Status:** Accepted

Stage 1 may define database structures for:

- Users
- Roles
- Permissions
- Sessions
- Refresh tokens

This does not implement authentication.

Login, password verification, JWT/session behavior, MFA, refresh-token rotation, and complete RBAC/ABAC enforcement remain Stage 2 responsibilities.