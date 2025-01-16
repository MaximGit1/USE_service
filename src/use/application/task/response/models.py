from dataclasses import dataclass
from typing import Any


@dataclass
class TaskResponse:
    type: int
    body: str
    answer: str
    time_limit: int

    def get_data(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class TaskCompletedResponse:
    task_id: int
    user_id: int
    code: str
    completed_time: int

    def get_data(self) -> dict[str, Any]:
        return self.__dict__
