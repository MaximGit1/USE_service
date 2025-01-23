from abc import abstractmethod
from typing import Any, Protocol


class BrokerUSEPublisherProtocol(Protocol):
    @abstractmethod
    async def publish(self, msg: Any, queue: str) -> None: ...

    @abstractmethod
    async def request(
        self, msg: Any, queue: str, time_limit: float
    ) -> Any: ...
