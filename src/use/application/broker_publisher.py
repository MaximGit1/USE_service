from abc import abstractmethod
from typing import Protocol

from use.entities.user.enums import RoleEnum


class BrokerPublisherProtocol(Protocol):
    @abstractmethod
    async def verify_user_role(
        self,
        role: RoleEnum,
        user_id: int,
    ) -> bool: ...
