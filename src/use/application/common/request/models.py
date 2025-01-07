from dataclasses import dataclass
from enum import StrEnum, auto


@dataclass
class PaginationParams:
    offset: int
    limit: int


class SortOrder(StrEnum):
    ASC = auto()
    DESC = auto()
