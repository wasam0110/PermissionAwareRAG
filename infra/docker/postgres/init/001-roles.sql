-- Stage 1 local development roles.
-- These passwords are development placeholders only.
-- Replace them for any shared or production environment.

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS vector;

CREATE ROLE rag_migration_admin
    LOGIN
    PASSWORD 'change-me-migration'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    NOREPLICATION
    NOBYPASSRLS;

CREATE ROLE rag_app
    LOGIN
    PASSWORD 'change-me-app'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT
    NOREPLICATION
    NOBYPASSRLS;

-- Keep the bootstrap user separate from the application role.
ALTER DATABASE rag_dev OWNER TO rag_migration_admin;

REVOKE CREATE ON SCHEMA public FROM PUBLIC;

GRANT CONNECT ON DATABASE rag_dev
    TO rag_migration_admin, rag_app;

GRANT USAGE ON SCHEMA public
    TO rag_migration_admin, rag_app;

GRANT CREATE ON SCHEMA public
    TO rag_migration_admin;
