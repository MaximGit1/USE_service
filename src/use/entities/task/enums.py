from enum import IntEnum

from use.entities.task.exceptions import TaskEntityValidationError


class TaskTypeEnum(IntEnum):
    TASK4 = 4
    TASK5 = 5

    @classmethod
    def get_type(cls, task_type: int) -> "TaskTypeEnum":
        v = cls._member_map_
        for value in v:
            if cls[value] == task_type:
                return cls[value]
        err_msg = f"task type cannot be {task_type}"
        raise TaskEntityValidationError(err_msg)
