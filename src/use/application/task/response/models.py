from dataclasses import dataclass


@dataclass
class TaskDone:
    result: bool
    completed_time: float


@dataclass
class TaskIDResponse:
    id: int


@dataclass
class TaskBodyResponse:
    id: int
    type: int
    body: str
    answer: str | None
    time_limit: int
