"""enforce tenant row security

Revision ID: REPLACE_WITH_GENERATED_REVISION
Revises: REPLACE_WITH_CURRENT_REVISION
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e326b4f6743b"
down_revision: Union[str, Sequence[str], None] = "ac47b2d8b0a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TENANT_TABLES = (
    "users",
    "roles",
    "collections",
    "documents",
    "document_acl",
    "chunks",
    "sessions",
    "refresh_tokens",
    "audit_events",
    "user_roles",
)


APPLICATION_TABLES = (
    "tenants",
    "users",
    "roles",
    "user_roles",
    "role_permissions",
    "collections",
    "documents",
    "document_acl",
    "chunks",
    "sessions",
    "refresh_tokens",
    "audit_events",
)


def upgrade() -> None:
    """Enable and enforce tenant isolation for all tenant-owned tables."""

    for table_name in TENANT_TABLES:
        op.execute(
            sa.text(
                f"""
                ALTER TABLE {table_name}
                    ENABLE ROW LEVEL SECURITY;

                ALTER TABLE {table_name}
                    FORCE ROW LEVEL SECURITY;

                DROP POLICY IF EXISTS {table_name}_tenant_isolation
                    ON {table_name};

                CREATE POLICY {table_name}_tenant_isolation
                    ON {table_name}
                    USING (
                        tenant_id = NULLIF(
                            current_setting('app.tenant_id', true),
                            ''
                        )::uuid
                    )
                    WITH CHECK (
                        tenant_id = NULLIF(
                            current_setting('app.tenant_id', true),
                            ''
                        )::uuid
                    );
                """
            )
        )

    op.execute(
        sa.text(
            """
            ALTER TABLE tenants
                ENABLE ROW LEVEL SECURITY;

            ALTER TABLE tenants
                FORCE ROW LEVEL SECURITY;

            DROP POLICY IF EXISTS tenants_isolation
                ON tenants;

            CREATE POLICY tenants_isolation
                ON tenants
                USING (
                    id = NULLIF(
                        current_setting('app.tenant_id', true),
                        ''
                    )::uuid
                )
                WITH CHECK (
                    id = NULLIF(
                        current_setting('app.tenant_id', true),
                        ''
                    )::uuid
                );
            """
        )
    )

    op.execute(
        sa.text(
            """
            ALTER TABLE role_permissions
                ENABLE ROW LEVEL SECURITY;

            ALTER TABLE role_permissions
                FORCE ROW LEVEL SECURITY;

            DROP POLICY IF EXISTS role_permissions_tenant_isolation
                ON role_permissions;

            CREATE POLICY role_permissions_tenant_isolation
                ON role_permissions
                USING (
                    EXISTS (
                        SELECT 1
                        FROM roles
                        WHERE roles.id = role_permissions.role_id
                          AND roles.tenant_id = NULLIF(
                              current_setting('app.tenant_id', true),
                              ''
                          )::uuid
                    )
                )
                WITH CHECK (
                    EXISTS (
                        SELECT 1
                        FROM roles
                        WHERE roles.id = role_permissions.role_id
                          AND roles.tenant_id = NULLIF(
                              current_setting('app.tenant_id', true),
                              ''
                          )::uuid
                    )
                );
            """
        )
    )

    op.execute(
        sa.text(
            """
            GRANT SELECT
                ON TABLE permissions
                TO rag_app;
            """
        )
    )

    for table_name in APPLICATION_TABLES:
        op.execute(
            sa.text(
                f"""
                GRANT SELECT, INSERT, UPDATE, DELETE
                    ON TABLE {table_name}
                    TO rag_app;
                """
            )
        )

    op.execute(
        sa.text(
            """
            GRANT USAGE, SELECT
                ON ALL SEQUENCES IN SCHEMA public
                TO rag_app;
            """
        )
    )


def downgrade() -> None:
    """Remove the tenant isolation policies and application grants."""

    for table_name in TENANT_TABLES:
        op.execute(
            sa.text(
                f"""
                DROP POLICY IF EXISTS {table_name}_tenant_isolation
                    ON {table_name};

                ALTER TABLE {table_name}
                    NO FORCE ROW LEVEL SECURITY;

                ALTER TABLE {table_name}
                    DISABLE ROW LEVEL SECURITY;
                """
            )
        )

    op.execute(
        sa.text(
            """
            DROP POLICY IF EXISTS tenants_isolation
                ON tenants;

            ALTER TABLE tenants
                NO FORCE ROW LEVEL SECURITY;

            ALTER TABLE tenants
                DISABLE ROW LEVEL SECURITY;

            DROP POLICY IF EXISTS role_permissions_tenant_isolation
                ON role_permissions;

            ALTER TABLE role_permissions
                NO FORCE ROW LEVEL SECURITY;

            ALTER TABLE role_permissions
                DISABLE ROW LEVEL SECURITY;

            REVOKE ALL PRIVILEGES
                ON TABLE
                    permissions,
                    tenants,
                    users,
                    roles,
                    user_roles,
                    role_permissions,
                    collections,
                    documents,
                    document_acl,
                    chunks,
                    sessions,
                    refresh_tokens,
                    audit_events
                FROM rag_app;

            REVOKE ALL PRIVILEGES
                ON ALL SEQUENCES IN SCHEMA public
                FROM rag_app;
            """
        )
    )
