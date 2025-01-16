from abc import abstractmethod
from typing import Protocol

from use.application.common.request.models import PaginationParams
from use.application.task.request.models import SearchFilters
from use.entities.task.models import Task, TaskCompleted
from use.entities.task.value_objects import TaskID
from use.entities.user.value_objects import UserID


class TaskReadProtocol(Protocol):
    @abstractmethod
    async def get_tasks(
        self, pagination: PaginationParams, filters: SearchFilters
    ) -> list[Task]: ...

    @abstractmethod
    async def get_task_by_id(self, task_id: TaskID) -> Task | None: ...

    @abstractmethod
    async def get_completed_task(
        self, task_id: TaskID, user_id: UserID
    ) -> TaskCompleted | None: ...
