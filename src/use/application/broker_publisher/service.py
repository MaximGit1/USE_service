from typing import cast

from use.application.broker_publisher.protocol import (
    BrokerUSEPublisherProtocol,
)
from use.application.user.exceptions import UserHasNotPermissionsError
from use.entities.user.enums import RoleEnum


class BrokerPublisherService:
    def __init__(self, publisher: BrokerUSEPublisherProtocol) -> None:
        self._broker = publisher

    async def auth_verify_user_role(
        self, role: RoleEnum, user_id: int
    ) -> bool:
        res = await self._broker.request(
            msg={"role": role, "user_id": user_id},
            queue="auth-verify-role",
            time_limit=1,
        )
        status: bool = cast(bool, res)
        if not status:
            raise UserHasNotPermissionsError
        return status
