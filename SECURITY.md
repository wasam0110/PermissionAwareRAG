# Security Authority

## Stage 0 invariants

- No real credentials are committed.
- The frontend contains only browser-safe public configuration.
- Health and readiness endpoints expose no secrets or connection strings.
- Structured logs use correlation IDs and do not log request bodies, prompts, documents, tokens, or credentials.
- Authentication, tenant context, RLS, authorization, ingestion, and RAG are not implemented yet and must not be implied by this stage.

The PRD is the primary product specification. This document is the security authority beneath it. Later stages may strengthen these rules but must not weaken them without an explicit documented decision.


## Stage 1 Security Invariants

1. Every tenant-owned resource has an explicit non-null `tenant_id`.
2. PostgreSQL RLS is a security boundary, not an optimization.
3. The application database role is not a superuser.
4. The application database role does not have `BYPASSRLS`.
5. Client-supplied tenant identifiers are never authoritative.
6. Tenant context is established only from trusted server-side identity.
7. Missing tenant context fails closed.
8. Cross-tenant reads, updates, deletes, and vector access are denied.
9. Authorization decisions are not stored only in client state.
10. Audit records include tenant and actor context without storing unnecessary sensitive content.
11. Deleted resources are not retrievable through tenant queries.
12. RLS policies are tested at the database level and through application behavior.
