from dataclasses import dataclass
from typing import NewType

from use.entities.auth.enums import TokenTypes

Token = NewType("Token", str)


@dataclass
class TokenPayload:
    sub: str
    expire: int
    token_type: TokenTypes

    def to_dict(self) -> dict[str, str | int | TokenTypes]:
        return {
            "sub": self.sub,
            "expire": self.expire,
            "token_type": self.token_type,
        }
