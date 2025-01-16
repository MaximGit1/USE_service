from use.application.common.protocols import UoWProtocol
from use.application.task.protocols import TaskCreateProtocol
from use.application.task.response.models import (
    TaskCompletedResponse,
    TaskResponse,
)
from use.entities.task.value_objects import TaskID


class TaskService:
    def __init__(self, add: TaskCreateProtocol, uow: UoWProtocol) -> None:
        self._add = add
        self._uow = uow

    async def create_task(self, task: TaskResponse) -> TaskID:
        task_id = await self._add.create_task(task=task)
        await self._uow.commit()

        return task_id

    async def create_completed_task(
        self, task: TaskCompletedResponse
    ) -> TaskID:
        task_id = await self._add.create_completed_task(task=task)
        await self._uow.commit()

        return task_id
