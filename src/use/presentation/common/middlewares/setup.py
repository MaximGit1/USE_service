from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .func import add_middleware
from .tracing import TracingMiddleware


def init_middleware(app: FastAPI) -> None:
    middlewares = [
        add_middleware(TracingMiddleware),
        add_middleware(
            CORSMiddleware,
            allow_origins=["https://127.0.0.1:5173"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PATCH", "DELETE"],
            allow_headers=["Content-Type"],
        ),
    ]

    for middleware in middlewares:
        app.add_middleware(
            middleware.cls, *middleware.args, **middleware.kwargs
        )
