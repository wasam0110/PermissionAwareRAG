# Security Test Plan

## Purpose

Verify that security boundaries are implemented before dependent features are added. Each stage requires tests, quality checks, security verification, and documentation updates.

## Current Status

- **Stage 0:** Complete
- **Stage 1:** Database schema, roles, RLS, and initial isolation tests implemented; expanded coverage pending
- **Stages 2–10:** Planned

Authentication, document ingestion, permission-aware retrieval, RAG, LLM security, and production deployment are not yet implemented.

## Test Environment

| Service | Host port | Container port |
|---|---:|---:|
| PostgreSQL 16 + pgvector | `5433` | `5432` |
| Redis 7 | `6380` | `6379` |

Database roles:

- `rag_dev` — local bootstrap/admin role
- `rag_migration_admin` — migration role
- `rag_app` — restricted application role

The application role must not be a superuser or have `BYPASSRLS`.

## Stage 0 Verification

Passed:

```text
pytest                         5 passed
ruff check backend tests       Passed
mypy backend                   Passed
Frontend lint                  Passed
Frontend tests                 Passed
Frontend production build      Passed
Docker service health          Passed
PostgreSQL connectivity        Passed
Redis connectivity             Passed
```

A Starlette/httpx deprecation warning remains non-blocking.

## Stage 1 Database Tests

Run the initial RLS suite:

```powershell
pytest tests/security/test_rls_isolation.py -q
```

Current tests verify:

- Missing tenant context returns no tenant-owned rows
- Tenant A can read its own document
- Tenant A cannot read Tenant B’s document
- Tenant A cannot update Tenant B’s document
- Tenant A cannot delete Tenant B’s document

Expected result:

```text
4 passed
```

## Required Database Checks

Verify migration state:

```powershell
alembic -c alembic.ini current
```

Verify RLS:

```sql
SELECT relname, relrowsecurity, relforcerowsecurity
FROM pg_class
WHERE relname IN (
    'tenants',
    'users',
    'roles',
    'user_roles',
    'role_permissions',
    'collections',
    'documents',
    'document_acl',
    'chunks',
    'sessions',
    'refresh_tokens',
    'audit_events'
)
ORDER BY relname;
```

Every tenant-owned table must show:

```text
relrowsecurity      = true
relforcerowsecurity = true
```

## Stage 1 Remaining Tests

Add coverage for:

- Users
- Roles
- Collections
- Document ACLs
- Chunks and vectors
- Sessions
- Refresh tokens
- Audit events
- `role_permissions` tenant derivation
- Mismatched-tenant inserts
- Tenant-context switching
- Context reset after transaction completion
- Deleted-resource exclusion
- Application-role privilege restrictions
- Database constraints and indexes

## Stage 2–10 Test Areas

Future stages must cover:

- Authentication, sessions, MFA, and RBAC/ABAC
- Secure uploads and ingestion
- Permission-aware retrieval
- Prompt injection and retrieval poisoning
- LLM output protection
- Frontend security
- HTTPS, headers, and accessibility
- Privacy, consent, and abuse controls
- Production infrastructure and secrets
- Observability, audit, backup, restore, and disaster recovery

## Quality Commands

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

## Security Principles

1. Tenant isolation is enforced at the database layer.
2. Client-controlled identity is never authoritative.
3. Missing tenant context fails closed.
4. The application never uses a privileged database role.
5. Unauthorized content must not enter the LLM context.
6. Documentation must match the verified implementation.
7. A later stage cannot be marked complete based only on planned code.