from dataclasses import dataclass

from use.entities.common.value_objects import ValueObject
from use.entities.user.exceptions import UserEntityValidationError


@dataclass(frozen=True)
class UserID(ValueObject[int]):
    pass


@dataclass(frozen=True)
class Username(ValueObject[str]):
    def validate(self) -> None:
        username_min_len = 4
        username_max_len = 15

        username_len = len(self.value)

        if username_len < username_min_len:
            error = (
                f"Username must be more than " f"{username_min_len} characters"
            )
            raise UserEntityValidationError(error)

        if username_len > username_max_len:
            error = (
                f"Username must be less than " f"{username_max_len} characters"
            )
            raise UserEntityValidationError(error)


@dataclass(frozen=True)
class RawPassword(ValueObject[str]):
    def validate(self) -> None:
        password_min_len = 8
        password_max_len = 32

        password_len = len(self.value)

        if password_len < password_min_len:
            error = (
                f"User password must be more than "
                f"{password_min_len} characters"
            )
            raise UserEntityValidationError(error)

        if password_len > password_max_len:
            error = (
                f"User password must be less than "
                f"{password_max_len} characters"
            )
            raise UserEntityValidationError(error)


@dataclass(frozen=True)
class HashedPassword(ValueObject[bytes]):
    pass
