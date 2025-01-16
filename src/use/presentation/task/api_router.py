from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from use.application.task.service import TaskService
from use.entities.task.value_objects import TaskID
from use.presentation.task.schemes import (
    TaskCompletedCreateScheme,
    TaskCreateScheme,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"], route_class=DishkaRoute)


@router.post("/create/base/", status_code=201)
async def create_task(
    task_service: FromDishka[TaskService],
    task_data: TaskCreateScheme,
) -> TaskID:
    return await task_service.create_task(task=task_data.get_response_model())


@router.post("/create/completed/", status_code=201)
async def create_completed_task(
    task_data: TaskCompletedCreateScheme,
    task_service: FromDishka[TaskService],
) -> TaskID:
    return await task_service.create_completed_task(
        task=task_data.get_response_model()
    )
