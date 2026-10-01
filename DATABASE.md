# Database

## Current Status

**Stage 0 — COMPLETE**

**Stage 1 — PREPARED / NOT YET IMPLEMENTED**

---

## Stage 0 Database State

Stage 0 configures:

- PostgreSQL 16
- pgvector
- SQLAlchemy
- asyncpg
- psycopg
- Alembic

The database currently contains **no application tables**.

This is intentional.

Stage 0 establishes database connectivity and migration tooling without prematurely implementing the application's security model.

---

## Local PostgreSQL

The local PostgreSQL container uses:

```text
Database: rag_dev
Container port: 5432
Host port: 5433
```

The project therefore connects through:

```text
localhost:5433
```

The host port is `5433` because another PostgreSQL installation is already using host port `5432`.

The PostgreSQL container itself continues to listen on its standard internal port `5432`.

---

## Redis

The local Redis container uses:

```text
Container port: 6379
Host port: 6380
```

The project therefore connects through:

```text
localhost:6380
```

This avoids conflict with another locally running Redis service.

---

## Database Roles

The project uses three PostgreSQL roles.

### `rag_dev`

Local development/bootstrap administration role.

This role is not intended to be used by the FastAPI application at runtime.

### `rag_migration_admin`

Dedicated migration role.

Alembic uses this role for schema migrations.

### `rag_app`

Restricted application runtime role.

This role is intended for normal application database access.

It must not:

- be a PostgreSQL superuser
- have `BYPASSRLS`
- bypass tenant isolation
- act as a database administrator

---

## Current Database Verification

At the end of Stage 0, the database contains no application relations.

Expected output:

```text
Did not find any relations.
```

This is correct for Stage 0.

---

## Alembic

Alembic is configured for asynchronous SQLAlchemy/PostgreSQL connectivity.

The migration environment uses the dedicated migration database URL.

The current migration directory contains no application revision.

Therefore:

```text
Stage 0:
No application migration exists.
No application tables exist.
```

Stage 1 will create the first application migration.

---

## Stage 1 Planned Schema

Stage 1 will define the foundational multi-tenant security schema.

### Tenants

Represents an isolated customer or organization boundary.

### Users

Represents identities associated with tenants.

### Roles

Defines reusable authorization roles.

### Permissions

Defines granular authorization capabilities.

### Role/Permission Relationships

Associates roles with their permissions.

### User/Role Relationships

Associates users with roles within the appropriate tenant scope.

### Documents

Represents tenant-owned source documents.

### Chunks

Represents document fragments that will later support retrieval.

### Document ACLs

Represents document-level access control relationships.

### Sessions

Provides database structures required for future authenticated sessions.

### Refresh Tokens

Provides database structures required for future token/session management.

### Audit Events

Records security-relevant events with tenant and actor context without unnecessarily storing sensitive content.

---

## Tenant Ownership

Every tenant-owned resource must have an explicit, non-null tenant relationship.

Conceptually:

```text
Tenant
  │
  ├── Users
  ├── Documents
  ├── Sessions
  ├── Refresh Tokens
  └── Audit Events
```

Tenant ownership must not depend on a client-supplied tenant ID.

---

## Row-Level Security

PostgreSQL Row-Level Security will be implemented in Stage 1.

RLS is a security boundary, not merely a query optimization.

The intended model is:

```text
Request
   │
   ▼
Trusted tenant context
   │
   ▼
Database transaction
   │
   ▼
RLS policy
   │
   ├── Matching tenant → permitted
   │
   └── Different tenant → denied
```

---

## Tenant Context

Stage 1 is expected to use transaction-local tenant context:

```sql
SET LOCAL app.tenant_id = '<trusted-tenant-uuid>';
```

Policies can then compare the row tenant ID with the active transaction context.

Conceptually:

```sql
tenant_id = current_setting('app.tenant_id', true)::uuid
```

The implementation must ensure that missing context fails closed.

---

## Stage 1 Security Requirements

Stage 1 must ensure:

1. Every tenant-owned resource has a non-null `tenant_id`.
2. RLS is enabled on every tenant-owned table.
3. RLS policies enforce tenant isolation.
4. The runtime application role cannot bypass RLS.
5. Client-supplied tenant IDs are never authoritative.
6. Tenant context comes from trusted server-side identity.
7. Missing tenant context fails closed.
8. Cross-tenant reads are denied.
9. Cross-tenant updates are denied.
10. Cross-tenant deletes are denied.
11. Cross-tenant chunk/vector access is denied.
12. Deleted resources are not returned through tenant-scoped queries.
13. Required database constraints exist.
14. Required indexes exist.
15. RLS behavior is tested directly at the database level.
16. RLS behavior is tested through the application layer.

---

## Authentication Boundary

Authentication belongs to Stage 2.

Stage 1 may define database structures required for:

- users
- roles
- permissions
- sessions
- refresh tokens

but these structures do not mean authentication is implemented.

Stage 2 will implement:

- login
- password verification
- authentication middleware
- JWT/session behavior
- MFA
- refresh-token rotation
- RBAC/ABAC enforcement