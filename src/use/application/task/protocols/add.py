from abc import abstractmethod
from typing import Protocol

from use.entities.task.models import Task, TaskCompleted
from use.entities.task.value_objects import TaskID


class TaskCreateProtocol(Protocol):
    @abstractmethod
    async def create_task(self, task: Task) -> TaskID: ...

    @abstractmethod
    async def create_completed_task(self, task: TaskCompleted) -> TaskID: ...
