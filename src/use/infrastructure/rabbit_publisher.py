from typing import cast

from faststream.rabbit import RabbitBroker

from use.application.broker_publisher import BrokerPublisherProtocol
from use.entities.user.enums import RoleEnum


class RabbitUSEPublisher(BrokerPublisherProtocol):
    def __init__(self, broker: RabbitBroker) -> None:
        self._broker = broker

    async def verify_user_role(
        self,
        role: RoleEnum,
        user_id: int,
    ) -> bool:
        msg = await self._broker.request(
            message={"role": role, "user_id": user_id},
            queue="auth-verify-role",
            timeout=1,
        )
        res: bool = cast(bool, await msg.decode())
        return res


def create_rabbit_broker() -> RabbitBroker:
    return RabbitBroker()
