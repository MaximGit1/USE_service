from dishka.integrations.faststream import FromDishka, inject
from faststream.rabbit import RabbitRouter

from use.application.task.service import TaskService
from use.presentation.task.schemes import TaskCompletedCreateScheme

router = RabbitRouter()


@router.subscriber("save-completed-task")
@inject
async def save_ran_task(
    task: TaskCompletedCreateScheme, service: FromDishka[TaskService]
) -> None:
    await service.create_completed_task(task=task.get_response_model())
