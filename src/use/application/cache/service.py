import asyncio
import json

from use.application.cache.protocol import CacheProtocol
from use.application.task.exceptions import TaskNotRunError
from use.application.task.response.models import TaskRunResponse


class CacheService:
    def __init__(self, cache_repository: CacheProtocol) -> None:
        self._cache = cache_repository

    async def get_run_task_result(self, task_uuid: str) -> TaskRunResponse:
        for _ in range(60):
            res = await self._cache.get(key=task_uuid)
            if res:
                return TaskRunResponse(**json.loads(res))

            await asyncio.sleep(1.5)

        raise TaskNotRunError

    async def set_task_running_status(
        self, task_uuid: str, user_id: int
    ) -> None:
        key = self._create_task_run_status_key(
            task_uuid=task_uuid, user_id=user_id
        )
        await self._cache.set(
            key=key,
            value="running",
            time_=90,
        )

    async def check_run_task_status(
        self, task_uuid: str, user_id: int
    ) -> None:
        key = self._create_task_run_status_key(
            task_uuid=task_uuid, user_id=user_id
        )
        if not await self._cache.get(key=key):
            raise TaskNotRunError

    @staticmethod
    def _create_task_run_status_key(task_uuid: str, user_id: int) -> str:
        return f"{user_id}-{task_uuid}"
