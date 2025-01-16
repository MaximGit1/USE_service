from sqlalchemy.ext.asyncio import AsyncSession

from use.application.task.protocols import TaskCreateProtocol
from use.application.task.request.models import (
    TaskCompletedResponse,
    TaskResponse,
)
from use.entities.task.value_objects import TaskID
from use.infrastructure.database.models import (
    completed_tasks_table,
    tasks_table,
)


class TaskCreateRepository(TaskCreateProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_task(self, task: TaskResponse) -> TaskID:
        stmt = (
            tasks_table.insert()
            .values(task.get_data())
            .returning(tasks_table.c.id)
        )

        result = await self._session.execute(stmt)
        new_id = result.scalar_one()

        return TaskID(new_id)

    async def create_completed_task(
        self, task: TaskCompletedResponse
    ) -> TaskID:
        stmt = (
            completed_tasks_table.insert()
            .values(task.get_data())
            .returning(tasks_table.c.id)
        )
        result = await self._session.execute(stmt)
        new_id = result.scalar_one()

        return TaskID(new_id)
