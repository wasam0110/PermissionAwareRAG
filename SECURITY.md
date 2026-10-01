# Security Authority

## Stage 0 invariants

- No real credentials are committed.
- The frontend contains only browser-safe public configuration.
- Health and readiness endpoints expose no secrets or connection strings.
- Structured logs use correlation IDs and do not log request bodies, prompts, documents, tokens, or credentials.
- Authentication, tenant context, RLS, authorization, ingestion, and RAG are not implemented yet and must not be implied by this stage.

The PRD is the primary product specification. This document is the security authority beneath it. Later stages may strengthen these rules but must not weaken them without an explicit documented decision.
