from use.application.common.protocols import UoWProtocol
from use.application.common.request.models import PaginationParams
from use.application.task.exceptions import TaskNotFoundError
from use.application.task.protocols import TaskCreateProtocol, TaskReadProtocol
from use.application.task.protocols.update import TaskUpdateProtocol
from use.application.task.request.models import (
    SearchFilters,
    TaskCompletedResponse,
    TaskResponse,
)
from use.application.task.response.models import (
    CompletedTaskBodyResponse,
    TaskBodyResponse,
    TaskIDResponse,
)
from use.entities.task.models import Task, TaskCompleted
from use.entities.task.value_objects import TaskCodeBody, TaskID
from use.entities.user.value_objects import UserID


class TaskService:
    def __init__(
        self,
        add: TaskCreateProtocol,
        read: TaskReadProtocol,
        uow: UoWProtocol,
        update: TaskUpdateProtocol,
    ) -> None:
        self._add = add
        self._read = read
        self._update = update
        self._uow = uow

    async def create_task(self, task: TaskResponse) -> TaskIDResponse:
        task_id = await self._add.create_task(task=task)
        await self._uow.commit()

        return TaskIDResponse(task_id.value)

    async def create_completed_task(
        self, task: TaskCompletedResponse
    ) -> TaskIDResponse:
        exists_task = await self._read.get_completed_task(
            task_id=TaskID(task.task_id),
            user_id=UserID(task.user_id),
        )
        if exists_task:
            return await self._task_completed_update(
                task=task, exists_task=exists_task
            )

        task_id = await self._add.create_completed_task(task=task)
        await self._uow.commit()

        return TaskIDResponse(task_id.value)

    async def _task_completed_update(
        self, task: TaskCompletedResponse, exists_task: TaskCompleted
    ) -> TaskIDResponse:
        exists_task.code = TaskCodeBody(task.code)
        exists_task.completed_time = task.completed_time
        await self._update.completed_task(task=exists_task)
        task_id = exists_task.task_id
        await self._uow.commit()
        return TaskIDResponse(task_id.value)

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

    async def get_task_by_id(
        self, task_id: int, *, with_answer: bool = False
    ) -> TaskBodyResponse:
        task = await self._read.get_task_by_id(task_id=TaskID(task_id))
        if not task:
            raise TaskNotFoundError

        return self._convert_task_to_response_model(
            task=task, with_answer=with_answer
        )

    async def get_completed_task(
        self, task_id: int, user_id: int
    ) -> CompletedTaskBodyResponse:
        task = await self._read.get_completed_task(
            task_id=TaskID(task_id), user_id=UserID(user_id)
        )
        if not task:
            raise TaskNotFoundError

        return self._convert_completed_task_to_response_model(task=task)

    @staticmethod
    def _convert_completed_task_to_response_model(
        task: TaskCompleted,
    ) -> CompletedTaskBodyResponse:
        return CompletedTaskBodyResponse(
            id=task.id.value,
            code=task.code.value,
            task_id=task.task_id.value,
            user_id=task.user_id.value,
            completed_time=task.completed_time,
        )
