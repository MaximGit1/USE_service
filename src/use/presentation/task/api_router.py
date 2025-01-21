from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from use.application.task.response.models import (
    CompletedTaskBodyResponse,
    TaskBodyResponse,
    TaskIDResponse,
)
from use.application.task.service import TaskService
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
