from typing import Annotated, cast
from uuid import uuid4

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Request

from use.application.broker_publisher.service import BrokerPublisherService
from use.application.cache.service import CacheService
from use.application.identityProvider.service import IdentityProvider
from use.application.task.request.models import (
    TaskCompletedResponse,
    TaskRunBrokerRequest,
    TaskRunRequest,
)
from use.application.task.response.models import (
    CompletedTaskBodyResponse,
    TaskBodyResponse,
    TaskIDResponse,
    TaskRunResponse,
)
from use.application.task.service import TaskService
from use.entities.user.enums import RoleEnum
from use.presentation.common.schemes import PaginationParams
from use.presentation.task.schemes import (
    SearchFiltersParams,
    TaskCompletedCreateScheme,
    TaskCreateScheme,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"], route_class=DishkaRoute)


@router.get("/base/", response_model_exclude_none=True)
async def get_all_tasks(
    task_service: FromDishka[TaskService],
    pagination: Annotated[PaginationParams, Depends()],
    filters: Annotated[SearchFiltersParams, Depends()],
) -> list[TaskBodyResponse]:
    return await task_service.get_tasks(
        pagination=pagination.to_model(), filters=filters.to_model()
    )


@router.get("/base/{task_id}", response_model_exclude_none=True)
async def get_task_by_id(
    task_id: int,
    task_service: FromDishka[TaskService],
) -> TaskBodyResponse:
    return await task_service.get_task_by_id(task_id=task_id)


@router.get("/completed/{user_id}/{task_id}", response_model_exclude_none=True)
async def get_completed_task_by_id(
    user_id: int,
    task_id: int,
    task_service: FromDishka[TaskService],
) -> CompletedTaskBodyResponse:
    return await task_service.get_completed_task(
        task_id=task_id, user_id=user_id
    )


@router.post("/create/base/", status_code=201)
async def create_task(
    task_service: FromDishka[TaskService],
    task_data: TaskCreateScheme,
) -> TaskIDResponse:
    return await task_service.create_task(task=task_data.get_response_model())


@router.post("/create/completed/", status_code=201)
async def create_completed_task(
    task_service: FromDishka[TaskService],
    task_data: TaskCompletedCreateScheme,
) -> TaskIDResponse:
    return await task_service.create_completed_task(
        task=task_data.get_response_model()
    )


@router.post("/run/{task_id}/")
async def send_to_run_task(
    task_input: TaskRunRequest,
    task_service: FromDishka[TaskService],
    idp: FromDishka[IdentityProvider],
    request: Request,
    broker: FromDishka[BrokerPublisherService],
    cache_service: FromDishka[CacheService],
) -> TaskRunResponse:
    idp.update_service(request=request)
    user_id = idp.get_current_user_id()
    role_status = await broker.auth_verify_user_role(
        role=RoleEnum.USER, user_id=user_id
    )
    idp.verify_user(status=role_status)

    task = await task_service.get_task_by_id(
        task_id=task_input.task_id, with_answer=True
    )
    task_uuid = str(uuid4())

    run_data = TaskRunBrokerRequest(
        uuid=task_uuid,
        code=task_input.code,
        answer=cast(str, task.answer),
        time_limit=task.time_limit,
    )

    await broker.task_send_task_to_run(data=run_data)
    await cache_service.set_task_running_status(
        task_uuid=task_uuid,
        user_id=user_id,
    )

    await cache_service.check_run_task_status(
        task_uuid=task_uuid, user_id=user_id
    )
    completed_task = await cache_service.get_run_task_result(
        task_uuid=task_uuid
    )
    if completed_task.res:
        await broker.task_save_completed_task(
            data=TaskCompletedResponse(
                task_id=task_input.task_id,
                user_id=user_id,
                code=task_input.code,
                completed_time=completed_task.completed_time,
            )
        )
    return completed_task
