# Architecture Decisions

## ADR-0001 — Standalone project dependencies

- Date: 2026-10-01
- Decision: Use standard open-source/runtime dependencies only; do not add Manus SDKs, MCP packages, Manus APIs, or hosted-runtime assumptions.
- Reason: The project must be portable and independently deployable.
- Consequence: Integrations use ordinary environment variables and documented adapters.

## ADR-0002 — Stage-gated implementation

- Date: 2026-10-01
- Decision: Implement one PRD stage at a time and block progression until its acceptance criteria pass.
- Reason: Security boundaries must exist before higher-level features depend on them.
- Consequence: Stage 0 contains no auth, RLS, ingestion, or RAG.

## ADR-0003 — Patched Next.js 14 release

- Date: 2026-10-01
- Decision: Use Next.js 14.2.35, the latest available release in the required Next.js 14 line.
- Reason: The initial 14.2.21 dependency emitted a security warning during installation.
- Consequence: The project remains on the PRD’s Next.js 14 line while avoiding the known warning.

## ADR-0004 — Python 3.11 runtime

- Date: 2026-10-01
- Decision: Use Python 3.11 for local development, CI, and the backend container.
- Reason: This is the project runtime requirement selected by the owner, superseding the PRD's initial Python 3.12 baseline.
- Consequence: Tooling targets `py311`; dependency compatibility must be checked against Python 3.11.
