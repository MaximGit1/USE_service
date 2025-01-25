from functools import partial as part
from typing import TYPE_CHECKING, cast

from starlette import status as code
from starlette.responses import JSONResponse

from use.application.auth.exceptions import (
    InvalidTokenTypeError,
    TokenBodyError,
    TokenExpiredError,
)
from use.application.cookie.exceptions import CookieIsNoneError
from use.application.task.exceptions import TaskNotFoundError, TaskNotRunError
from use.application.user.exceptions import (
    UserAlreadyExistsError,
    UserBannedError,
    UserHasNotPermissionsError,
    UserInvalidCredentialsError,
    UserNotFoundError,
)
from use.entities.task.exceptions import TaskEntityValidationError
from use.entities.user.exceptions import UserEntityValidationError

if TYPE_CHECKING:
    from fastapi import FastAPI
    from starlette.requests import Request

    class StubError(Exception):
        message: str


async def _validate(_: "Request", exc: Exception, status: int) -> JSONResponse:
    exc = cast("StubError", exc)
    return JSONResponse(content={"detail": exc.message}, status_code=status)


def init_exc_handlers(app: "FastAPI") -> None:
    app.add_exception_handler(
        UserEntityValidationError,
        part(_validate, status=code.HTTP_422_UNPROCESSABLE_ENTITY),
    )
    app.add_exception_handler(
        UserAlreadyExistsError,
        part(_validate, status=code.HTTP_409_CONFLICT),
    )
    app.add_exception_handler(
        UserNotFoundError,
        part(_validate, status=code.HTTP_404_NOT_FOUND),
    )
    app.add_exception_handler(
        UserInvalidCredentialsError,
        part(_validate, status=code.HTTP_401_UNAUTHORIZED),
    )
    app.add_exception_handler(
        UserBannedError,
        part(_validate, status=code.HTTP_409_CONFLICT),
    )
    app.add_exception_handler(
        InvalidTokenTypeError,
        part(_validate, status=code.HTTP_401_UNAUTHORIZED),
    )
    app.add_exception_handler(
        TokenExpiredError,
        part(_validate, status=code.HTTP_401_UNAUTHORIZED),
    )
    app.add_exception_handler(
        TokenBodyError,
        part(_validate, status=code.HTTP_401_UNAUTHORIZED),
    )
    app.add_exception_handler(
        CookieIsNoneError,
        part(_validate, status=code.HTTP_401_UNAUTHORIZED),
    )
    app.add_exception_handler(
        TaskEntityValidationError,
        part(_validate, status=code.HTTP_422_UNPROCESSABLE_ENTITY),
    )
    app.add_exception_handler(
        TaskNotFoundError,
        part(_validate, status=code.HTTP_404_NOT_FOUND),
    )
    app.add_exception_handler(
        UserHasNotPermissionsError,
        part(_validate, status=code.HTTP_403_FORBIDDEN),
    )
    app.add_exception_handler(
        TaskNotRunError,
        part(_validate, status=code.HTTP_404_NOT_FOUND),
    )
