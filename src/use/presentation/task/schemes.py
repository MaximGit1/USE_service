from typing import Annotated

from annotated_types import Ge, Lt, MaxLen, MinLen
from pydantic import BaseModel

from use.application.common.request.models import SortOrder
from use.application.task.request.models import (
    SearchFilters,
    TaskCompletedResponse,
    TaskResponse,
    TaskRun,
)
from use.application.task.response.models import TaskDone
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


class TaskRunScheme(BaseModel):
    code: str
    time_limit: int
    answer: str

    def to_model(self) -> TaskRun:
        return TaskRun(
            code=self.code,
            time_limit=self.time_limit,
            answer=self.answer,
        )


class TaskDoneScheme(BaseModel):
    result: bool
    completed_time: float

    def to_model(self) -> TaskDone:
        return TaskDone(
            result=self.result,
            completed_time=self.completed_time,
        )


class SearchFiltersParams(BaseModel):
    order_by: TaskTypeEnum | None = None
    order: SortOrder | None = None

    def to_model(self) -> SearchFilters:
        return SearchFilters(
            order_by=self.order_by,
            order=self.order,
        )
