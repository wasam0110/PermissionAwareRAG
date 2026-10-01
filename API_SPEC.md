# API Specification

## Current Status

**Stage 0 — COMPLETE**

**Stage 1 — NOT YET IMPLEMENTED**

---

## Stage 0 API

Stage 0 exposes only process and dependency health endpoints.

| Method | Path | Purpose | Auth |
|---|---|---|---|
| GET | `/health` | Process liveness | None |
| GET | `/ready` | Dependency readiness | None |

No authentication or authorization is required for either endpoint.

---

## `GET /health`

Checks that the FastAPI process is running.

Example response:

```json
{
  "status": "ok"
}
```

This endpoint checks process liveness only.

It does not verify PostgreSQL or Redis availability.

---

## `GET /ready`

Checks the availability of the required Stage 0 dependencies:

- PostgreSQL
- Redis

When both dependencies are available, the endpoint returns HTTP `200`.

Example:

```json
{
  "status": "ready",
  "dependencies": {
    "database": true,
    "redis": true
  }
}
```

If PostgreSQL or Redis is unavailable, the endpoint returns HTTP `503`.

Example:

```json
{
  "status": "not_ready",
  "dependencies": {
    "database": false,
    "redis": true
  }
}
```

---

## Stage 0 Security Boundary

Stage 0 API endpoints do not accept or return:

- tenant identifiers
- user identities
- authentication credentials
- access tokens
- refresh tokens
- authorization decisions
- documents
- document contents
- prompts
- embeddings
- RAG responses
- application secrets

Health and readiness responses do not expose:

- passwords
- tokens
- database credentials
- Redis credentials
- connection strings

---

## Stage 1 API Direction

Stage 1 is primarily a database and security-boundary stage.

It is not intended to implement the complete authentication API.

Stage 1 will establish:

- tenant-aware database structures
- tenant ownership
- tenant context
- PostgreSQL RLS
- database constraints
- indexes
- audit structures
- database-level isolation

Application authentication endpoints remain a Stage 2 responsibility.

---

## Future API Stages

Later stages are expected to introduce APIs for:

- Authentication
- Session management
- Tenant-aware user operations
- Role and permission management
- Document management
- Document ingestion
- Query and RAG operations
- Audit/security operations

An API must not be considered implemented until its corresponding stage passes its completion gate.