from abc import abstractmethod
from typing import Protocol

from use.entities.auth.models import (
    Token,
    TokenPayload,
)


class JWTManageProtocol(Protocol):
    @abstractmethod
    def generate_token(self, sub: int) -> Token: ...

    @abstractmethod
    def parse_token(self, token: Token) -> TokenPayload | None: ...
