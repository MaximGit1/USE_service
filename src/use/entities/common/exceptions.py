class EntityError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
