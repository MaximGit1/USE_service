import asyncio

from dishka.integrations.faststream import setup_dishka
from dotenv import load_dotenv
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from use.main.di.main import container_factory
from use.presentation.auth.broker_router import router as auth_router


async def run_app(app_: FastStream) -> None:
    await app_.run()


if __name__ == "__main__":
    load_dotenv()
    broker = RabbitBroker()
    app = FastStream(broker)
    broker.include_router(auth_router)
    container = container_factory()
    setup_dishka(app=app, container=container)

    asyncio.run(run_app(app))
