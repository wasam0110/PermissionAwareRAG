# Implementation Plan

## Stage-Gated Development

Implement one stage at a time. A stage is complete only after:

1. Implementation
2. Automated tests
3. Quality checks
4. Security verification
5. Documentation updates
6. Acceptance evidence

Do not begin the next stage until the current completion gate passes.

## Stage 0 — Repository Foundation

**Status: Complete**

Delivered:

- FastAPI and Next.js project foundations
- Python 3.11 and Node.js environments
- Docker Compose with PostgreSQL 16/pgvector and Redis 7
- Configuration and safe environment templates
- Structured logging and correlation IDs
- Health and readiness endpoints
- SQLAlchemy and Alembic setup
- Backend and frontend tests
- Ruff, mypy, ESLint, Vitest, and production build checks

Deferred from Stage 0:

- Authentication
- Authorization
- RLS
- Document ingestion
- Vector retrieval
- RAG
- LLM security
- Production deployment

## Stage 1 — Multi-Tenant Database Security Boundary

**Status: In progress — implementation and initial tests complete; final acceptance pending**

### Delivered

- SQLAlchemy declarative base and tenant-aware models
- Tables for tenants, users, roles, permissions, documents, ACLs, chunks, sessions, refresh tokens, and audit events
- Required foreign keys, constraints, indexes, and vector column
- PostgreSQL roles:
  - `rag_dev`
  - `rag_migration_admin`
  - `rag_app`
- `pgcrypto` and `vector` extensions
- Alembic migration chain
- Transaction-local tenant security context
- RLS and forced RLS on tenant-owned tables
- Fail-closed policies when tenant context is missing
- Explicit grants for `rag_app`
- Cross-tenant document read, update, and delete tests

### Remaining

- Expand isolation tests to every tenant-owned table
- Test mismatched-tenant inserts
- Test context reset after transaction completion
- Strengthen composite tenant ownership constraints
- Add deleted-resource and audit integrity tests
- Complete documentation and final acceptance review

### Completion Gate

- [ ] All tenant-owned tables are covered by isolation tests
- [ ] Missing tenant context returns no tenant-owned rows
- [ ] Mismatched-tenant inserts are rejected
- [ ] Cross-tenant reads, updates, and deletes are blocked
- [ ] Chunk/vector isolation passes
- [ ] Deleted resources cannot be retrieved
- [ ] Database and application tests pass
- [ ] Ruff and mypy pass
- [ ] Documentation matches the implementation

## Stage 2 — Authentication and Authorization

**Status: Planned**

- Password hashing and verification
- Login and logout
- Access and refresh tokens
- Session management and rotation
- MFA
- Authentication middleware
- RBAC and ABAC
- Authorization dependencies and tests

## Stage 3 — Secure Document Management

**Status: Planned**

- Secure document uploads
- File type and size validation
- Secure storage
- Document lifecycle
- Ingestion jobs
- Sandboxed parsing
- Chunking and embedding preparation
- Ingestion authorization and isolation
- Document security tests

## Stage 4 — Permission-Aware RAG

**Status: Planned**

- Tenant-aware retrieval
- Permission-aware vector search
- Document ACL enforcement
- Retrieval filtering
- Citation and source tracking
- RAG query pipeline
- Retrieval security tests

## Stage 5 — LLM Security

**Status: Planned**

- Prompt-injection defenses
- Retrieval-poisoning defenses
- Safe prompt construction
- Sensitive-data protection
- Output filtering
- Provider abstraction and isolation
- LLM security tests

## Stage 6 — Authenticated Frontend

**Status: Planned**

- Authentication UI
- Session handling
- Protected routes
- Tenant-aware interface
- Document management
- Query/RAG interface
- Role- and permission-aware controls
- Frontend security protections

## Stage 7 — Public Website and Accessibility

**Status: Planned**

- Public website
- HTTPS and security headers
- Metadata and SEO
- Social previews and favicon
- Accessibility
- Broken-link checks
- Clear CTA flow

## Stage 8 — Privacy and Abuse Controls

**Status: Planned**

- Cookie consent
- Privacy controls
- Analytics
- Spam protection
- Input validation
- Abuse controls
- Data-retention behavior

## Stage 9 — Production Infrastructure

**Status: Planned**

- Production containers
- Secret management
- TLS and deployment infrastructure
- Production PostgreSQL and Redis
- Kubernetes where required
- Monitoring and alerting
- Operational security

## Stage 10 — Release Readiness

**Status: Planned**

- Complete security test suite
- SAST, dependency, container, and secret scans
- Observability and audit verification
- Backup and restore testing
- Disaster recovery validation
- Release checks
- Final documentation
- Production-readiness gate