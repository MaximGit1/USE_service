from abc import abstractmethod
from typing import Protocol


class CacheProtocol(Protocol):
    @abstractmethod
    async def get(self, key: str) -> str | None: ...

    @abstractmethod
    async def set(self, key: str, value: str, time_: int) -> None: ...
