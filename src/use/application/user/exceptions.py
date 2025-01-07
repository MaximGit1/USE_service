from use.application.common.exceptions import ApplicationError


class UserAlreadyExistsError(ApplicationError):
    def __init__(self, username: str) -> None:
        super().__init__(f"User with username '{username}' already exists.")


class UserNotFoundError(ApplicationError):
    def __init__(
        self, user_id: int | None = None, username: str | None = None
    ) -> None:
        msg = "User with "

        if user_id:
            msg += f"id={user_id} "
        if username:
            msg += f"username={username} "

        msg += "not found."

        super().__init__(msg)


class UserInvalidCredentialsError(ApplicationError):
    def __init__(self) -> None:
        super().__init__("Invalid user credentials: username or password.")


class UserBannedError(ApplicationError):
    def __init__(self) -> None:
        super().__init__("User banned.")
