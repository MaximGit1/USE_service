from use.application.common.exceptions import ApplicationError


class TaskNotFoundError(ApplicationError):
    def __init__(self) -> None:
        msg = "Task not found!"
        super().__init__(msg)


class TaskNotRunError(ApplicationError):
    def __init__(self) -> None:
        msg = "Task not run!"
        super().__init__(msg)
