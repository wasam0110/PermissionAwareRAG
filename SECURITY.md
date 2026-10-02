# Security Authority

## Status

- **Stage 0:** Complete
- **Stage 1:** Database security boundary implemented; final acceptance and expanded isolation coverage pending

The PRD is the primary product specification. This document is the security authority beneath it. Later stages may strengthen these rules but must not weaken them without a documented decision.

## Core Security Rules

1. Never commit real credentials, tokens, private keys, or sensitive document data.
2. Keep server-side secrets out of frontend-exposed variables.
3. Treat the browser and all client-supplied authorization data as untrusted.
4. Do not log passwords, tokens, credentials, authorization headers, prompts, document contents, or sensitive generated responses.
5. Use correlation IDs for request tracing without exposing private data.
6. Missing security context must fail closed.
7. Unauthorized content must never enter the LLM context.
8. Do not claim later-stage controls before they are implemented and tested.

## Stage 1 Database Boundary

Stage 1 uses separate PostgreSQL roles:

| Role | Purpose | RLS bypass |
|---|---|---|
| `rag_dev` | Local bootstrap/admin role | Yes; development-only |
| `rag_migration_admin` | Runs Alembic migrations | No |
| `rag_app` | Backend runtime role | No |

The backend must use `rag_app`, never the privileged `rag_dev` role. `rag_app` must not be a superuser, table owner, or member of a role that bypasses RLS.

## Tenant Isolation Invariants

1. Every tenant-owned resource has a non-null `tenant_id`.
2. PostgreSQL RLS is a mandatory security boundary.
3. Tenant context comes only from trusted server-side identity.
4. Client-supplied tenant IDs are never authoritative.
5. Cross-tenant reads, inserts, updates, and deletes are denied.
6. Chunk and vector access is tenant-isolated.
7. Deleted resources are excluded from tenant-scoped access.
8. RLS is enabled and forced on every tenant-owned table.
9. RLS is tested directly against PostgreSQL and through application behavior.
10. Authorization must not depend only on client-side state.

## Transaction-Local Tenant Context

Tenant context is set inside a transaction using PostgreSQL transaction-local settings:

```sql
SELECT set_config('app.tenant_id', '<trusted-tenant-uuid>', true);
