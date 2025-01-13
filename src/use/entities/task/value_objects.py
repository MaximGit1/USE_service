from dataclasses import dataclass

from use.entities.common.value_objects import ValueObject
from use.entities.task.exceptions import TaskEntityValidationError


@dataclass(frozen=True)
class TaskID(ValueObject[int]):
    pass


@dataclass(frozen=True)
class TaskTitle(ValueObject[str]):
    def validate(self) -> None:
        min_len = 5
        max_len = 55

        value = self.value
        value_len = len(value)

        if value_len < min_len or value_len > max_len:
            error_msg = (
                f"The title length must be between {min_len} and {max_len}"
            )
            raise TaskEntityValidationError(error_msg)

        if not value[0].isalpha():
            error_msg = "The name must start with a capital letter"
            raise TaskEntityValidationError(error_msg)


@dataclass(frozen=True)
class TaskAnswer(ValueObject[str]):
    pass


@dataclass(frozen=True)
class TaskTimeLimit(ValueObject[int]):
    def validate(self) -> None:
        value = self.value
        time_limit = 120

        if value < time_limit or value < 1:
            error_msg = (
                "the task execution time must be "
                "less than 120 seconds and not less than 1 second"
            )
            raise TaskEntityValidationError(error_msg)


@dataclass(frozen=True)
class TaskBody(ValueObject[str]):
    pass


@dataclass(frozen=True)
class TaskCodeBody(ValueObject[str]):
    pass
