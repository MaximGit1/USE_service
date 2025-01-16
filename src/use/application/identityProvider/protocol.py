from abc import abstractmethod
from typing import Protocol

from use.entities.user.enums import RoleEnum


class IdentityProviderProtocol(Protocol):
    @abstractmethod
    def get_current_user_id(self) -> int: ...

    @abstractmethod
    async def verify_role(self, required_role: RoleEnum) -> bool: ...
