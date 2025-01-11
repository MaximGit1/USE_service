from datetime import UTC, datetime
from typing import Any

from jwt import (
    DecodeError,
    decode,
    encode,
)

from use.application.auth.exceptions import (
    InvalidTokenTypeError,
    TokenBodyError,
    TokenExpiredError,
)
from use.application.auth.protocols import JWTManageProtocol
from use.entities.auth.enums import TokenTypes
from use.entities.auth.models import (
    Token,
    TokenPayload,
)
from use.main.config import Config


class AccessManagerRepository(JWTManageProtocol):
    def __init__(self, config: Config) -> None:
        self._private_key = config.jwt.private_key
        self._public_key = config.jwt.public_key
        self._algorithm = config.jwt.algorithm
        self._token_expire_minutes = config.jwt.access_token_expire_minutes

    def generate_token(self, sub: int) -> Token:
        payload = self._generate_payload(sub=sub)
        return Token(
            encode(
                payload.to_dict(), self._private_key, algorithm=self._algorithm
            )
        )

    def parse_token(self, token: Token) -> TokenPayload:
        try:
            payload: dict[str, Any] = decode(
                token,
                self._public_key,
                algorithms=[self._algorithm],
            )
        except DecodeError as err:
            raise TokenBodyError from err

        expire = int(payload["expire"])

        if expire < int(datetime.now(UTC).replace(tzinfo=None).timestamp()):
            raise TokenExpiredError

        token_type = payload.get("token_type")

        if (token_type is None) or (token_type != TokenTypes.AccessToken):
            error_msg = token_type if token_type else "None token type"
            raise InvalidTokenTypeError(error_msg)

        return TokenPayload(
            sub=payload["sub"],
            token_type=TokenTypes.AccessToken,
            expire=expire,
        )

    def _generate_payload(self, sub: int) -> TokenPayload:
        now = datetime.now(UTC).replace(tzinfo=None)
        expire = now + self._token_expire_minutes
        expire_as_int = int(expire.timestamp())

        return TokenPayload(
            sub=str(sub),
            expire=expire_as_int,
            token_type=TokenTypes.AccessToken,
        )
