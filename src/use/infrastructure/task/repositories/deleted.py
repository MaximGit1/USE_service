from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from use.application.task.protocols.delete import TaskDeleteProtocol
from use.entities.task.value_objects import TaskID
from use.infrastructure.database.models import (
    completed_tasks_table,
    tasks_table,
)


class TaskDeletedRepository(TaskDeleteProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def base_task(self, task_id: TaskID) -> None:
        stmt = delete(tasks_table).where(tasks_table.c.id == task_id.value)
        await self._session.execute(stmt)

    async def completed_task(self, task_id: TaskID) -> None:
        stmt = delete(completed_tasks_table).where(
            completed_tasks_table.c.id == task_id.value
        )
        await self._session.execute(stmt)
