from collections.abc import Sequence
from typing import Any

from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from use.application.common.request.models import PaginationParams, SortOrder
from use.application.task.protocols import TaskReadProtocol
from use.application.task.request.models import SearchFilters
from use.entities.task.enums import TaskTypeEnum
from use.entities.task.models import Task, TaskCompleted
from use.entities.task.value_objects import (
    TaskAnswer,
    TaskBody,
    TaskID,
    TaskTimeLimit,
)
from use.entities.user.value_objects import UserID
from use.infrastructure.database.models import tasks_table


class TaskReadRepository(TaskReadProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_tasks(
        self, pagination: PaginationParams, filters: SearchFilters
    ) -> list[Task]:
        stmt = (
            select(tasks_table)
            .offset(pagination.offset)
            .limit(pagination.limit)
        )

        if filters.order_by is not None:
            stmt = stmt.where(tasks_table.c.type == filters.order_by)

        if filters.order:
            order_column = tasks_table.c.id
            if filters.order == SortOrder.ASC:
                stmt = stmt.order_by(order_column.asc())
            elif filters.order == SortOrder.DESC:
                stmt = stmt.order_by(order_column.desc())

        result = await self._session.execute(stmt)

        return self._load_tasks(result.all())

    @staticmethod
    def _load_task(row: Row[Any]) -> Task:
        return Task(
            id=TaskID(row.id),
            type=TaskTypeEnum.get_type(task_type=row.type),
            body=TaskBody(row.body),
            answer=TaskAnswer(row.answer),
            time_limit=TaskTimeLimit(row.time_limit),
        )

    def _load_tasks(self, rows: Sequence[Row[Any]]) -> list[Task]:
        return [self._load_task(row) for row in rows]

    async def get_completed_task(
        self, task_id: TaskID, user_id: UserID
    ) -> TaskCompleted | None:
        pass

    async def get_task_by_id(self, task_id: TaskID) -> Task | None:
        pass
