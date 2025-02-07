from typing import cast

from use.application.broker_publisher.protocol import (
    BrokerUSEPublisherProtocol,
)
from use.application.task.request.models import (
    TaskCompletedResponse,
    TaskRunBrokerRequest,
)
from use.application.user.exceptions import UserHasNotPermissionsError
from use.entities.user.enums import RoleEnum


class BrokerPublisherService:
    def __init__(self, publisher: BrokerUSEPublisherProtocol) -> None:
        self._broker = publisher

    async def auth_verify_user_role(
        self, role: RoleEnum, user_id: int
    ) -> bool:
        res = await self._broker.request(
            msg={"role": role, "user_id": user_id},
            queue="auth-verify-role",
            time_limit=1,
        )
        status: bool = cast(bool, res)
        if not status:
            raise UserHasNotPermissionsError
        return status

    async def task_send_task_to_run(self, data: TaskRunBrokerRequest) -> None:
        await self._broker.publish(
            msg=data,
            queue="task-run-task",
        )

    async def task_save_completed_task(
        self, data: TaskCompletedResponse
    ) -> None:
        await self._broker.publish(
            msg=data,
            queue="task-save-completed-task",
        )

    async def task_delete_all_data(self, task_id: int) -> None:
        await self._broker.publish(
            msg=task_id,
            queue="task-delete-task",
        )
