from dishka.integrations.faststream import FromDishka, inject
from faststream.rabbit import RabbitRouter

from use.application.user.service import UserService
from use.entities.user.enums import RoleEnum

router = RabbitRouter()


@router.subscriber("auth-verify-role")
@inject
async def verify_current_user_role(
    role: RoleEnum, user_id: int, user_service: FromDishka[UserService]
) -> bool:
    return await user_service.verify_role(user_id=user_id, required_role=role)
