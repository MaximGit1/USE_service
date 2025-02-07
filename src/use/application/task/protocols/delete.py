from abc import abstractmethod
from typing import Protocol

from use.entities.task.value_objects import TaskID


class TaskDeleteProtocol(Protocol):
    @abstractmethod
    async def base_task(self, task_id: TaskID) -> None: ...

    @abstractmethod
    async def completed_task(self, task_id: TaskID) -> None: ...
