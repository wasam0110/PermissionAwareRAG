# Security Test Plan

## Current Status

**Stage 0 — COMPLETE**

**Stage 1 — TEST PLAN DEFINED / IMPLEMENTATION NOT YET COMPLETE**

Testing is stage-gated.

A stage cannot be considered complete based only on implementation claims. Required tests must pass before the completion gate is marked complete.

---

# Stage 0 Tests

## Application Health

Verify:

```text
GET /health
```

returns HTTP `200`:

```json
{
  "status": "ok"
}
```

This verifies process liveness only.

---

## Dependency Readiness

Verify:

```text
GET /ready
```

reports PostgreSQL and Redis availability.

When both dependencies are healthy:

```json
{
  "status": "ready",
  "dependencies": {
    "database": true,
    "redis": true
  }
}
```

If either dependency is unavailable, the endpoint must return HTTP `503`.

---

## Configuration

Verify:

- settings load successfully
- environment variables override defaults
- application startup succeeds
- PostgreSQL configuration loads
- Redis configuration loads
- no credentials are exposed through frontend configuration

---

## Correlation IDs

Verify:

- incoming `X-Request-ID` is preserved
- a correlation ID is generated when one is absent
- the correlation ID is returned in the response
- correlation IDs are not treated as authentication credentials

---

## Secret Exposure

Verify:

- no real secrets exist in frontend source
- health responses contain no credentials
- readiness responses contain no credentials
- readiness responses contain no connection strings
- logs do not contain request bodies
- logs do not contain credentials
- logs do not contain authorization tokens

---

# Stage 0 Quality Checks

The completed Stage 0 implementation passes:

```text
pytest
5 passed

ruff check backend tests
All checks passed

mypy backend
Success: no issues found

Frontend lint
Passed

Frontend tests
1 passed

Frontend production build
Passed
```

---

# Stage 1 Security Tests

Stage 1 must add tests for database-level tenant isolation.

## Schema Tests

Verify:

- required tables exist
- tenant-owned tables contain `tenant_id`
- tenant-owned `tenant_id` columns are non-null
- required foreign keys exist
- required unique constraints exist
- required indexes exist
- document/chunk relationships preserve tenant ownership

---

## Database Role Tests

Verify:

```text
rag_app
    superuser = false
    BYPASSRLS = false
```

The application role must not be able to bypass RLS.

---

## RLS Enablement

Verify that RLS is enabled on every tenant-owned table.

---

## Tenant Context

Verify that a trusted tenant context can be established for a transaction.

Conceptually:

```sql
SET LOCAL app.tenant_id = '<tenant-a>';
```

Verify that tenant context is transaction-local and cannot leak between pooled connections.

---

## Missing Tenant Context

Verify that no tenant-owned data is accessible when tenant context is absent.

Expected behavior:

```text
No tenant context
        ↓
No tenant-owned data accessible
```

---

## Same-Tenant Access

Verify that a tenant can access its own permitted resources.

Example:

```text
Tenant A context
        ↓
Tenant A document
        ↓
Accessible
```

---

## Cross-Tenant Read

Verify:

```text
Tenant A context
        ↓
Tenant B document
        ↓
Not accessible
```

---

## Cross-Tenant Update

Verify that Tenant A cannot update Tenant B resources.

---

## Cross-Tenant Delete

Verify that Tenant A cannot delete Tenant B resources.

---

## Cross-Tenant Chunk/Vector Access

Verify that Tenant A cannot retrieve Tenant B chunks or vector records.

Tenant isolation must remain intact when retrieval-related structures are queried.

---

## Application-Level Isolation

Repeat tenant-isolation tests through the application/database access layer rather than relying only on direct SQL tests.

---

## Deleted Resources

Verify that deleted resources are not returned by tenant-scoped queries.

---

## Audit Integrity

Verify that security-relevant audit events contain appropriate:

- tenant context
- actor context
- event type
- timestamp

without unnecessarily storing sensitive document contents or credentials.

---

# Stage 1 Completion Gate

Stage 1 cannot be marked complete until:

- [ ] schema tests pass
- [ ] constraint tests pass
- [ ] index tests pass
- [ ] database role security tests pass
- [ ] RLS enablement tests pass
- [ ] tenant-context tests pass
- [ ] missing-context tests pass
- [ ] same-tenant access tests pass
- [ ] cross-tenant read tests pass
- [ ] cross-tenant update tests pass
- [ ] cross-tenant delete tests pass
- [ ] chunk/vector isolation tests pass
- [ ] application-level isolation tests pass
- [ ] deleted-resource tests pass
- [ ] audit integrity tests pass
- [ ] migration succeeds on a clean database
- [ ] Ruff passes
- [ ] mypy passes
- [ ] existing Stage 0 tests continue to pass
- [ ] documentation matches implementation
- [ ] Stage 1 evidence is captured

---

# Later Security Testing

Later stages will add testing for:

- authentication
- MFA
- session security
- refresh-token rotation
- RBAC/ABAC
- secure uploads
- ingestion isolation
- prompt injection
- retrieval poisoning
- LLM output leakage
- rate limiting
- abuse prevention
- HTTPS
- security headers
- privacy/consent
- production infrastructure
- backup/restore
- observability