from abc import ABC, abstractmethod
from typing import Any


class CookieManagerInteractor(ABC):
    def __init__(self) -> None:
        self.request: Any = None
        self.response: Any = None

    @abstractmethod
    def set(self, value: str) -> None: ...

    @abstractmethod
    def get(self) -> str | None: ...

    @abstractmethod
    def delete(self) -> None: ...
