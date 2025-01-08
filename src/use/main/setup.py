import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from use.main.di.main import container_factory
from use.presentation.common.exc_handlers import init_exc_handlers
from use.presentation.common.middlewares.setup import init_middleware
from use.presentation.user.api_router import router as user_router


def init_routers(app: FastAPI) -> None:
    routers = (user_router,)

    for router in routers:
        app.include_router(router)


def init_di(app: FastAPI) -> None:
    container = container_factory()

    setup_dishka(container, app)


def init_logger() -> logging.Logger:
    logger = logging.getLogger("api_logger")
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        log_file_path = (Path(__file__).parent / "../../../logs.log").resolve()

        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        handler = logging.FileHandler(
            filename=log_file_path,
            mode="a",
            encoding="utf-8",
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    logger = init_logger()

    logger.info("Application is starting...")

    yield

    logger.info("Application is stopping...")


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    init_di(app)
    init_routers(app)
    init_exc_handlers(app)
    init_middleware(app)

    return app
