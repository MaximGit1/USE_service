from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from use.application.user.protocols import UserCreateProtocol
from use.entities.user.enums import RoleEnum
from use.entities.user.value_objects import (
    HashedPassword,
    UserID,
    Username,
)
from use.infrastructure.database.models import users_table


class UserCreateRepository(UserCreateProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self, username: Username, password: HashedPassword
    ) -> UserID | None:
        stmt = (
            users_table.insert()
            .values(
                {
                    "username": username.value,
                    "hashed_password": password.value,
                    "role": RoleEnum.USER,
                    "is_active": True,
                }
            )
            .returning(users_table.c.id)
        )

        try:
            result = await self._session.execute(stmt)
            new_id = result.scalar_one()
        except IntegrityError:
            return None

        return UserID(new_id)
