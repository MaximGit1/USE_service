from typing import Any

from faststream.rabbit import RabbitBroker

from use.application.broker_publisher.protocol import (
    BrokerUSEPublisherProtocol,
)


class BrokerUSEPublisher(BrokerUSEPublisherProtocol):
    def __init__(self, broker: RabbitBroker) -> None:
        self._broker = broker

    async def publish(self, msg: Any, queue: str) -> None:
        await self._broker.publish(
            message=msg,
            queue=queue,
        )

    async def request(self, msg: Any, queue: str, time_limit: float) -> Any:
        res = await self._broker.request(
            message=msg,
            queue=queue,
            timeout=time_limit,
        )
        return await res.decode()
