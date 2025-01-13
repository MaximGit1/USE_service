from dataclasses import (
    dataclass,
)

from use.entities.common.models import Entity
from use.entities.task.enums import TaskTypeEnum
from use.entities.task.value_objects import (
    TaskAnswer,
    TaskBody,
    TaskCodeBody,
    TaskID,
    TaskTimeLimit,
    TaskTitle,
)
from use.entities.user.value_objects import UserID


@dataclass(
    slots=True,
    kw_only=True,
)
class BaseTask(Entity[TaskID]):
    title: TaskTitle
    type: TaskTypeEnum
    answer: TaskAnswer
    time_limit: TaskTimeLimit


@dataclass(
    slots=True,
    kw_only=True,
)
class Task4(Entity[TaskID]):
    base_task_id: TaskID
    body: TaskBody


@dataclass(
    slots=True,
    kw_only=True,
)
class Task4Completed(Entity[TaskID]):
    base_task_id: TaskID
    user_id: UserID
    code_body: TaskCodeBody
    response_time: TaskTimeLimit
