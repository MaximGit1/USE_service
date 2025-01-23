from typing import Any

from use.application.auth.protocols import JWTManageProtocol
from use.application.cookie.exceptions import CookieIsNoneError
from use.application.cookie.interactor import CookieManagerInteractor
from use.application.identityProvider.protocol import IdentityProviderProtocol
from use.application.user.protocols import UserReadProtocol
from use.entities.auth.models import Token
from use.entities.user.enums import RoleEnum
from use.entities.user.value_objects import UserID


class IdentityProvider(IdentityProviderProtocol):
    def __init__(
        self,
        access_cookie: CookieManagerInteractor,
        user_read: UserReadProtocol,
        auth: JWTManageProtocol,
    ) -> None:
        self._access = access_cookie
        self._user = user_read
        self._auth = auth

    def get_current_user_id(self) -> int:
        token = self._access.get()

        if not token:
            raise CookieIsNoneError

        payload = self._auth.parse_token(token=Token(token))
        return int(payload.sub)

    async def verify_role(self, required_role: RoleEnum) -> bool:
        try:
            user_id = self.get_current_user_id()
            user = await self._user.get_by_id(user_id=UserID(user_id))
        except CookieIsNoneError:
            user = None

        role = user.role if user else RoleEnum.GUEST

        return RoleEnum.validate_role(
            user_role=role,
            min_role=required_role,
        )

    def update_service(self, request: Any = None) -> None:
        self._access.request = request

    @staticmethod
    def verify_user(*, status: bool) -> None:
        if status:
            raise CookieIsNoneError
