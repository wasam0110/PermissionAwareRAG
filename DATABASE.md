# Database

## Status

- **Stage 0:** Complete
- **Stage 1:** Schema and RLS foundation implemented; expanded isolation coverage pending

## Local Services

### PostgreSQL

```text
Database: rag_dev
Container port: 5432
Windows host port: 5433
```

Windows-hosted backend and Alembic connect through:

```text
localhost:5433
```

Commands executed inside the PostgreSQL container use:

```text
localhost:5432
```

PostgreSQL 16 uses:

- `pgcrypto` for UUID generation
- `vector` for pgvector embeddings

### Redis

```text
Container port: 6379
Windows host port: 6380
```

The backend connects through:

```text
localhost:6380
```

Redis is not an authorization source of truth.

## Database Roles

| Role | Purpose | RLS bypass |
|---|---|---|
| `rag_dev` | Local bootstrap/development administration | Yes; development-only |
| `rag_migration_admin` | Alembic migrations | No |
| `rag_app` | Backend runtime access | No |

The backend must use `rag_app`, never `rag_dev`. The application role is not a superuser, does not have `BYPASSRLS`, and is not the owner of application tables.

## Migration Chain

```text
e81fde210ddd
create stage 1 tenant security schema
        ↓
ac47b2d8b0a7
add missing refresh tokens table
        ↓
e326b4f6743b
enforce tenant row security
```

Alembic uses `MIGRATION_DATABASE_URL` and the `rag_migration_admin` role.

## Stage 1 Schema

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

### Ownership

All tenant-owned resources have a non-null `tenant_id`:

- Users
- Roles
- User-role assignments
- Collections
- Documents
- Document ACLs
- Chunks
- Sessions
- Refresh tokens
- Audit events

`role_permissions` derives tenant ownership through its related role.

`permissions` contains global permission definitions.

## Row-Level Security

Tenant-owned tables use:

```sql
ENABLE ROW LEVEL SECURITY;
FORCE ROW LEVEL SECURITY;
```

Policies compare row ownership with the transaction-local tenant context:

```sql
tenant_id = NULLIF(
    current_setting('app.tenant_id', true),
    ''
)::uuid
```

Tenant context is established inside a transaction:

```sql
SELECT set_config('app.tenant_id', '<trusted-tenant-uuid>', true);
```

The final argument makes the value transaction-local and prevents connection-pool leakage.

### Fail-Closed Behavior

When `app.tenant_id` is missing:

```text
No tenant context
        ↓
No tenant-owned rows visible
```

When Tenant A is active:

```text
Tenant A context
        ↓
Tenant B resource
        ↓
Not visible or writable
```

The client must never be trusted to provide the authoritative tenant identity.

## Stage 1 Security Requirements

The database must enforce:

1. Non-null tenant ownership.
2. RLS on every tenant-owned table.
3. Forced RLS for tenant-owned tables.
4. No RLS bypass by `rag_app`.
5. Fail-closed behavior without tenant context.
6. Cross-tenant read, insert, update, and delete denial.
7. Tenant-isolated document and vector access.
8. Required foreign keys, constraints, and indexes.
9. Direct database-level RLS tests.
10. Application-level isolation tests.

## Current Verification

Verified:

- Migration chain applied successfully
- All Stage 1 tables created
- `rag_app` can connect
- `rag_app` has no superuser or RLS-bypass privileges
- Missing tenant context hides tenant-owned rows
- Cross-tenant document reads are blocked
- Cross-tenant document updates are blocked
- Cross-tenant document deletes are blocked

Remaining:

- Expand tests to every tenant-owned table
- Test mismatched-tenant inserts
- Test context reset after transaction completion
- Strengthen composite tenant ownership constraints

## Authentication Boundary

Stage 1 creates database structures for users, roles, permissions, sessions, and refresh tokens. It does not implement authentication.

Stage 2 will implement:

- Login and password verification
- Authentication middleware
- JWT/session behavior
- MFA
- Refresh-token rotation
- Complete RBAC/ABAC enforcement