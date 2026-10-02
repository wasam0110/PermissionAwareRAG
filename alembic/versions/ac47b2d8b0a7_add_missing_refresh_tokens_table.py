"""add missing refresh tokens table

Revision ID: ac47b2d8b0a7
Revises: e81fde210ddd
Create Date: 2026-10-02 16:25:48.593143

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ac47b2d8b0a7"
down_revision: Union[str, Sequence[str], None] = "e81fde210ddd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "refresh_tokens",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "session_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "token_hash",
            sa.String(length=128),
            nullable=False,
        ),
        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "used_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["sessions.id"],
            name=op.f("fk_refresh_tokens_session_id_sessions"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            name=op.f("fk_refresh_tokens_tenant_id_tenants"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_refresh_tokens"),
        ),
        sa.UniqueConstraint(
            "token_hash",
            name=op.f("uq_refresh_tokens_token_hash"),
        ),
    )

    op.create_index(
        "ix_refresh_tokens_tenant_id",
        "refresh_tokens",
        ["tenant_id"],
    )

    op.create_index(
        "ix_refresh_tokens_session_id",
        "refresh_tokens",
        ["session_id"],
    )

    op.execute(
        sa.text(
            """
            ALTER TABLE refresh_tokens
            ENABLE ROW LEVEL SECURITY;

            ALTER TABLE refresh_tokens
            FORCE ROW LEVEL SECURITY;

            CREATE POLICY refresh_tokens_tenant_isolation
            ON refresh_tokens
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

            GRANT SELECT, INSERT, UPDATE, DELETE
            ON TABLE refresh_tokens
            TO rag_app;
            """
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.execute(
        sa.text(
            """
            REVOKE ALL PRIVILEGES
            ON TABLE refresh_tokens
            FROM rag_app;

            DROP POLICY IF EXISTS refresh_tokens_tenant_isolation
            ON refresh_tokens;
            """
        )
    )

    op.drop_index(
        "ix_refresh_tokens_session_id",
        table_name="refresh_tokens",
    )

    op.drop_index(
        "ix_refresh_tokens_tenant_id",
        table_name="refresh_tokens",
    )

    op.drop_table("refresh_tokens")