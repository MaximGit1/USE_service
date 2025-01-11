from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Request, Response

from use.application.auth.service import AuthService
from use.application.cookie.service import CookieService
from use.application.user.response.models import (
    UserIdResponse,
)
from use.application.user.service import UserService
from use.entities.user.enums import RoleEnum
from use.presentation.auth.schemes import UserLoginInput
from use.presentation.user.schemes import UserCreateScheme

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)


@router.post("/register/", status_code=201)
async def create_user(
    user_data: Annotated[UserCreateScheme, Depends()],
    user_service: FromDishka[UserService],
) -> UserIdResponse:
    username, password = user_data.get_data()

    return await user_service.create_user(username=username, password=password)


@router.post("/login/")
async def login(
    user_data: Annotated[UserLoginInput, Depends()],
    user_service: FromDishka[UserService],
    auth_service: FromDishka[AuthService],
    cookie_service: FromDishka[CookieService],
    response: Response,
) -> None:
    username, password = user_data.get_data()
    user_id = await user_service.authenticate_user(
        username=username, password=password
    )
    token = auth_service.login_user(user_id=user_id)

    cookie_service.update_service(response=response)
    cookie_service.set_access_token(token)


@router.post(
    "/logout/",
    summary="Logout user",
)
async def logout(
    response: Response,
    cookie_service: FromDishka[CookieService],
) -> None:
    cookie_service.update_service(response=response)
    cookie_service.delete_access_token()


@router.post("/verify-role/")
async def verify_role(
    role: RoleEnum,
    user_service: FromDishka[UserService],
    cookie_service: FromDishka[CookieService],
    auth_service: FromDishka[AuthService],
    request: Request,
    user_id: int | None = None,
) -> bool:
    if user_id is None:
        cookie_service.update_service(request=request)
        token = cookie_service.get_access_token()
        user_id = auth_service.get_user_id_by_access_token(access_token=token)

    return await user_service.verify_role(
        user_id=user_id,
        required_role=role,
    )


@router.post(
    "/my-id/",
    summary="Get current user id",
)
async def get_current_user_id(
    auth_service: FromDishka[AuthService],
    cookie_service: FromDishka[CookieService],
    request: Request,
) -> UserIdResponse:
    cookie_service.update_service(request=request)
    token = cookie_service.get_access_token()

    return UserIdResponse(
        user_id=auth_service.get_user_id_by_access_token(token)
    )
