from use.application.common.exceptions import ApplicationError


class InvalidTokenTypeError(ApplicationError):
    def __init__(self, token_type: str) -> None:
        super().__init__(f"Invalid token type='{token_type}'.")


class TokenExpiredError(ApplicationError):
    def __init__(self) -> None:
        super().__init__("Token expired.")


class TokenBodyError(ApplicationError):
    def __init__(self) -> None:
        super().__init__("The token body was broken.")
