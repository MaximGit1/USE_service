from typing import Any

from use.application.cookie.exceptions import CookieIsNoneError
from use.application.cookie.interactor import CookieManagerInteractor


class CookieService:
    def __init__(self, access_repository: CookieManagerInteractor) -> None:
        self._access = access_repository

    def set_access_token(self, token: str) -> None:
        self._access.set(token)

    def get_access_token(self) -> str:
        value = self._access.get()

        if not value:
            raise CookieIsNoneError

        return value

    def delete_access_token(self) -> None:
        self._access.delete()

    def update_service(
        self, *, request: Any = None, response: Any = None
    ) -> None:
        self._access.request = request
        self._access.response = response
