from abc import abstractmethod
from typing import Protocol

from use.application.task.request.models import (
    TaskCompletedResponse,
    TaskResponse,
)
from use.entities.task.value_objects import TaskID


class TaskCreateProtocol(Protocol):
    @abstractmethod
    async def create_task(self, task: TaskResponse) -> TaskID: ...

    @abstractmethod
    async def create_completed_task(
        self, task: TaskCompletedResponse
    ) -> TaskID: ...
