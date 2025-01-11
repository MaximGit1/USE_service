from use.application.auth.exceptions import InvalidTokenTypeError
from use.application.auth.protocols import JWTManageProtocol
from use.entities.auth.models import (
    Token,
    TokenTypes,
)


class AuthService:
    def __init__(
        self,
        access_token_repository: JWTManageProtocol,
    ) -> None:
        self._access = access_token_repository

    def login_user(self, user_id: int) -> Token:
        return self._generate_access_token(sub=user_id)

    def _generate_access_token(self, sub: int) -> Token:
        return self._generate_token(
            sub=sub,
            token_type=TokenTypes.AccessToken,
        )

    def _generate_token(self, sub: int, token_type: TokenTypes) -> Token:
        if token_type == TokenTypes.AccessToken:
            return self._access.generate_token(sub=sub)
        if token_type == TokenTypes.RefreshToken:
            raise InvalidTokenTypeError(token_type=token_type)
        raise InvalidTokenTypeError(token_type=token_type)

    def get_user_id_by_access_token(self, access_token: str) -> int:
        payload = self._access.parse_token(token=Token(access_token))
        return int(payload.sub)
