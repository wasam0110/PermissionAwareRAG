from __future__ import annotations

import os
from collections.abc import Generator
from uuid import UUID, uuid4

import psycopg
import pytest

pytestmark = pytest.mark.integration


def database_url() -> str:
    url = os.getenv(
        "MIGRATION_DATABASE_URL",
        "postgresql+psycopg://"
        "rag_migration_admin:change-me-migration"
        "@localhost:5433/rag_dev",
    )
    return url.replace("postgresql+psycopg://", "postgresql://", 1)


def set_tenant_context(connection: psycopg.Connection, tenant_id: UUID) -> None:
    connection.execute(
        "SELECT set_config('app.tenant_id', %s, true)",
        (str(tenant_id),),
    )


def clear_tenant_context(connection: psycopg.Connection) -> None:
    connection.execute(
        "SELECT set_config('app.tenant_id', '', true)",
    )


@pytest.fixture
def seeded_tenants() -> Generator[tuple[UUID, UUID, UUID, UUID], None, None]:
    tenant_a = uuid4()
    tenant_b = uuid4()
    document_a = uuid4()
    document_b = uuid4()

    with psycopg.connect(database_url()) as connection:
        with connection.transaction():
            set_tenant_context(connection, tenant_a)

            connection.execute(
                """
                INSERT INTO tenants (id, name, slug)
                VALUES (%s, %s, %s)
                """,
                (tenant_a, "Tenant A", f"tenant-a-{tenant_a.hex}"),
            )

            connection.execute(
                """
                INSERT INTO documents (
                    id,
                    tenant_id,
                    title,
                    storage_key,
                    content_hash,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    document_a,
                    tenant_a,
                    "Tenant A document",
                    f"tenant-a/{document_a}",
                    f"hash-a-{document_a.hex}",
                    "ready",
                ),
            )

            set_tenant_context(connection, tenant_b)

            connection.execute(
                """
                INSERT INTO tenants (id, name, slug)
                VALUES (%s, %s, %s)
                """,
                (tenant_b, "Tenant B", f"tenant-b-{tenant_b.hex}"),
            )

            connection.execute(
                """
                INSERT INTO documents (
                    id,
                    tenant_id,
                    title,
                    storage_key,
                    content_hash,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    document_b,
                    tenant_b,
                    "Tenant B document",
                    f"tenant-b/{document_b}",
                    f"hash-b-{document_b.hex}",
                    "ready",
                ),
            )

    yield tenant_a, tenant_b, document_a, document_b

    with psycopg.connect(database_url()) as connection:
        with connection.transaction():
            set_tenant_context(connection, tenant_a)
            connection.execute(
                "DELETE FROM tenants WHERE id = %s",
                (tenant_a,),
            )

            set_tenant_context(connection, tenant_b)
            connection.execute(
                "DELETE FROM tenants WHERE id = %s",
                (tenant_b,),
            )


def app_connection() -> psycopg.Connection:
    return psycopg.connect(
        database_url()
        .replace(
            "rag_migration_admin:change-me-migration",
            "rag_app:change-me-app",
        )
    )


def test_missing_tenant_context_returns_no_rows(
    seeded_tenants: tuple[UUID, UUID, UUID, UUID],
) -> None:
    del seeded_tenants

    with app_connection() as connection:
        with connection.transaction():
            clear_tenant_context(connection)

            result = connection.execute(
                "SELECT COUNT(*) FROM documents",
            ).fetchone()

            assert result is not None
            assert result[0] == 0


def test_tenant_a_cannot_read_tenant_b_documents(
    seeded_tenants: tuple[UUID, UUID, UUID, UUID],
) -> None:
    tenant_a, tenant_b, document_a, document_b = seeded_tenants
    del tenant_b

    with app_connection() as connection:
        with connection.transaction():
            set_tenant_context(connection, tenant_a)

            visible_ids = {
                row[0]
                for row in connection.execute(
                    "SELECT id FROM documents ORDER BY id",
                ).fetchall()
            }

            assert document_a in visible_ids
            assert document_b not in visible_ids


def test_tenant_a_cannot_update_tenant_b_document(
    seeded_tenants: tuple[UUID, UUID, UUID, UUID],
) -> None:
    tenant_a, tenant_b, document_a, document_b = seeded_tenants
    del tenant_b, document_a

    with app_connection() as connection:
        with connection.transaction():
            set_tenant_context(connection, tenant_a)

            result = connection.execute(
                """
                UPDATE documents
                SET title = 'unauthorized update'
                WHERE id = %s
                """,
                (document_b,),
            )

            assert result.rowcount == 0


def test_tenant_a_cannot_delete_tenant_b_document(
    seeded_tenants: tuple[UUID, UUID, UUID, UUID],
) -> None:
    tenant_a, tenant_b, document_a, document_b = seeded_tenants
    del tenant_b, document_a

    with app_connection() as connection:
        with connection.transaction():
            set_tenant_context(connection, tenant_a)

            result = connection.execute(
                "DELETE FROM documents WHERE id = %s",
                (document_b,),
            )

            assert result.rowcount == 0
