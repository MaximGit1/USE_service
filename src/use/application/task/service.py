from use.application.common.protocols import UoWProtocol
from use.application.common.request.models import PaginationParams
from use.application.task.exceptions import TaskNotFoundError
from use.application.task.protocols import TaskCreateProtocol, TaskReadProtocol
from use.application.task.request.models import (
    SearchFilters,
    TaskCompletedResponse,
    TaskResponse,
)
from use.application.task.response.models import (
    TaskBodyResponse,
    TaskIDResponse,
)
from use.entities.task.models import Task
from use.entities.task.value_objects import TaskID


class TaskService:
    def __init__(
        self, add: TaskCreateProtocol, read: TaskReadProtocol, uow: UoWProtocol
    ) -> None:
        self._add = add
        self._read = read
        self._uow = uow

    async def create_task(self, task: TaskResponse) -> TaskIDResponse:
        task_id = await self._add.create_task(task=task)
        await self._uow.commit()

        return TaskIDResponse(task_id.value)

    async def create_completed_task(
        self, task: TaskCompletedResponse
    ) -> TaskID:
        task_id = await self._add.create_completed_task(task=task)
        await self._uow.commit()

        return task_id

    async def get_tasks(
        self, pagination: PaginationParams, filters: SearchFilters
    ) -> list[TaskBodyResponse]:
        tasks = await self._read.get_tasks(
            pagination=pagination, filters=filters
        )
        return [
            self._convert_task_to_response_model(task=task, with_answer=False)
            for task in tasks
        ]

    @staticmethod
    def _convert_task_to_response_model(
        task: Task, *, with_answer: bool
    ) -> TaskBodyResponse:
        return TaskBodyResponse(
            id=task.id.value,
            body=task.body.value,
            type=task.type,
            answer=task.answer.value if with_answer else None,
            time_limit=task.time_limit.value,
        )

    async def get_task_by_id(self, task_id: int) -> TaskBodyResponse:
        task = await self._read.get_task_by_id(task_id=TaskID(task_id))
        if not task:
            raise TaskNotFoundError

        return self._convert_task_to_response_model(
            task=task, with_answer=False
        )
