from abc import abstractmethod
from typing import Protocol

from use.application.common.request.models import PaginationParams
from use.application.user.request.models import SearchFilters
from use.entities.user.models import User
from use.entities.user.value_objects import (
    UserID,
    Username,
)


class UserReadProtocol(Protocol):
    @abstractmethod
    async def get_by_id(self, user_id: UserID) -> User | None: ...

    @abstractmethod
    async def get_by_username(self, username: Username) -> User | None: ...

    @abstractmethod
    async def get_all(
        self, pagination: PaginationParams, filters: SearchFilters
    ) -> list[User]: ...
