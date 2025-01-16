from typing import Annotated

from annotated_types import Ge, Lt, MaxLen, MinLen
from pydantic import BaseModel

from use.application.task.request.models import (
    TaskCompletedResponse,
    TaskResponse,
)
from use.entities.task.enums import TaskTypeEnum


class TaskCreateScheme(BaseModel):
    type: TaskTypeEnum
    body: Annotated[str, MinLen(20), MaxLen(1_000)]
    answer: Annotated[str, MinLen(1), MaxLen(500)]
    time_limit: Annotated[int, Ge(1), Lt(120)]

    def get_response_model(self) -> TaskResponse:
        return TaskResponse(
            type=self.type,
            body=self.body,
            answer=self.answer,
            time_limit=self.time_limit,
        )


class TaskCompletedCreateScheme(BaseModel):
    task_id: int
    user_id: int
    code: Annotated[str, MinLen(10), MaxLen(1_000)]
    completed_time: Annotated[int, Ge(1), Lt(120)]

    def get_response_model(self) -> TaskCompletedResponse:
        return TaskCompletedResponse(
            task_id=self.task_id,
            user_id=self.user_id,
            code=self.code,
            completed_time=self.completed_time,
        )
