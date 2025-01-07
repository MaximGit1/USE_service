from dataclasses import dataclass
from enum import StrEnum, auto

from use.application.common.request.models import SortOrder


class SearchFilterTypes(StrEnum):
    ID = auto()
    USERNAME = auto()


@dataclass
class SearchFilters:
    order_by: SearchFilterTypes | None = None
    order: SortOrder | None = None
