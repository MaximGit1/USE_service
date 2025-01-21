from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from use.application.task.response.models import (
    TaskBodyResponse,
    TaskIDResponse,
)
from use.application.task.service import TaskService
from use.entities.task.value_objects import TaskID
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
    pagination: PaginationParams,
    filters: SearchFiltersParams,
) -> list[TaskBodyResponse]:
    return await task_service.get_tasks(
        pagination=pagination.to_model(), filters=filters.to_model()
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
) -> TaskID:
    return await task_service.create_completed_task(
        task=task_data.get_response_model()
    )
