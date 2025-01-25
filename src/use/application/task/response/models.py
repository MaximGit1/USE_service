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


@dataclass
class CompletedTaskBodyResponse:
    id: int | None
    task_id: int
    user_id: int
    code: str
    completed_time: float


@dataclass
class TaskRunResponse:
    res: bool
    completed_time: float
