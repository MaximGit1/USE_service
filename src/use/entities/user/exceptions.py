from use.entities.common.exceptions import EntityError


class UserEntityValidationError(EntityError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message)
