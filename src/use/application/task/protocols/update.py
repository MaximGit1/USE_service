from abc import abstractmethod
from typing import Protocol

from use.entities.task.models import TaskCompleted


class TaskUpdateProtocol(Protocol):
    @abstractmethod
    async def completed_task(self, task: TaskCompleted) -> None: ...
