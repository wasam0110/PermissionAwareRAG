# API Specification

Stage 0 exposes only:

| Method | Path | Purpose | Auth |
|---|---|---|---|
| GET | `/health` | Process liveness | None |
| GET | `/ready` | Dependency readiness | None |

Readiness returns HTTP 503 when PostgreSQL or Redis cannot be reached. No endpoint accepts or returns tenant, user, authorization, document, prompt, or secret data in Stage 0.
