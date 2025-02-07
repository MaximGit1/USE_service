from dishka.integrations.faststream import FromDishka, inject
from faststream.rabbit import RabbitRouter

from use.application.task.service import TaskService
from use.presentation.task.schemes import TaskCompletedCreateScheme

router = RabbitRouter()


@router.subscriber("task-save-completed-task")
@inject
async def save_ran_task(
    task: TaskCompletedCreateScheme, service: FromDishka[TaskService]
) -> None:
    await service.create_completed_task(task=task.get_response_model())


@router.subscriber("task-delete-task")
@inject
async def delete_task_and_completed_tasks(
    task_id: int, service: FromDishka[TaskService]
) -> None:
    await service.delete_all_completed_tasks(base_task_id=task_id)
    await service.delete_base_task(task_id=task_id)
