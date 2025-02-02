from typing import cast

from use.application.cookie.interactor import CookieManagerInteractor
from use.main.config import Config


class CookieAccessManagerRepository(CookieManagerInteractor):
    def __init__(
        self,
        config: Config,
    ) -> None:
        super().__init__()
        self._max_age = config.cookie.max_age_days
        self._token_key = config.cookie.access_token_key

    def get(self) -> str | None:
        return cast(str | None, self.request.cookies.get(self._token_key))

    def set(self, value: str) -> None:
        self.response.set_cookie(
            key=self._token_key,
            value=value,
            httponly=True,
            max_age=self._max_age,
            secure=True,
            samesite="None",
            path="/",
        )

    def delete(self) -> None:
        self.response.delete_cookie(key=self._token_key)
