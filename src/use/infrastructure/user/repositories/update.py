from sqlalchemy import update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession

from use.application.user.protocols import UserUpdateProtocol
from use.entities.user.enums import RoleEnum
from use.entities.user.value_objects import UserID
from use.infrastructure.database.models import users_table


class UserUpdateRepository(UserUpdateProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def change_status(self, user_id: UserID, *, is_active: bool) -> None:
        stmt = (
            sa_update(users_table)
            .where(users_table.c.id == user_id.value)
            .values(is_active=is_active)
        )

        await self._session.execute(stmt)

    async def change_role(self, user_id: UserID, role: RoleEnum) -> None:
        stmt = (
            sa_update(users_table)
            .where(users_table.c.id == user_id.value)
            .values(role=role)
        )

        await self._session.execute(stmt)
