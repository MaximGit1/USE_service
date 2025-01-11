from use.application.common.exceptions import ApplicationError


class CookieIsNoneError(ApplicationError):
    def __init__(self) -> None:
        super().__init__("Cookie was not set.")
