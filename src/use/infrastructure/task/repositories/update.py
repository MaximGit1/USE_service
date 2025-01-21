from sqlalchemy import update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession

from use.application.task.protocols.update import TaskUpdateProtocol
from use.entities.task.models import TaskCompleted
from use.infrastructure.database.models import completed_tasks_table


class TaskUpdateRepository(TaskUpdateProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def completed_task(self, task: TaskCompleted) -> None:
        values = {
            "code": task.code.value,
            "completed_time": task.completed_time,
        }
        stmt = (
            sa_update(completed_tasks_table)
            .where(completed_tasks_table.c.id == task.id.value)
            .values(values)
        )
        await self._session.execute(stmt)
