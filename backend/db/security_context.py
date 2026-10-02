from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeVar
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


async def set_security_context(
    session: AsyncSession,
    *,
    tenant_id: UUID | None,
    user_id: UUID | None = None,
) -> None:
    """
    Set transaction-local authorization context.

    This must be called inside an active database transaction. PostgreSQL
    automatically removes SET LOCAL values when the transaction ends.

    Passing None deliberately clears the value and causes tenant RLS policies
    to fail closed.
    """
    await session.execute(
        text("SELECT set_config('app.tenant_id', :tenant_id, true)"),
        {
            "tenant_id": str(tenant_id) if tenant_id is not None else "",
        },
    )

    await session.execute(
        text("SELECT set_config('app.user_id', :user_id, true)"),
        {
            "user_id": str(user_id) if user_id is not None else "",
        },
    )


async def clear_security_context(session: AsyncSession) -> None:
    """
    Clear the transaction-local authorization context.

    Empty values are intentional. The RLS policies interpret them as missing
    context and deny access to tenant-owned rows.
    """
    await set_security_context(
        session,
        tenant_id=None,
        user_id=None,
    )


async def get_security_context(
    session: AsyncSession,
) -> tuple[UUID | None, UUID | None]:
    """
    Read the current transaction-local authorization context.

    Return None for a missing or invalid context rather than trusting or
    propagating malformed values.
    """
    result = await session.execute(
        text(
            """
            SELECT
                NULLIF(current_setting('app.tenant_id', true), '') AS tenant_id,
                NULLIF(current_setting('app.user_id', true), '') AS user_id
            """
        )
    )
    row = result.one()

    def parse_uuid(value: str | None) -> UUID | None:
        if value is None:
            return None

        try:
            return UUID(value)
        except ValueError:
            return None

    return parse_uuid(row.tenant_id), parse_uuid(row.user_id)


async def in_security_context(
    session: AsyncSession,
    *,
    tenant_id: UUID,
    user_id: UUID | None = None,
    operation: Callable[[AsyncSession], Awaitable[T]],
) -> T:
    """
    Execute one operation inside a transaction-local security context.

    The caller supplies trusted server-side identity values only. Do not pass
    tenant or user identifiers directly from an HTTP request.
    """
    async with session.begin():
        await set_security_context(
            session,
            tenant_id=tenant_id,
            user_id=user_id,
        )
        return await operation(session)
