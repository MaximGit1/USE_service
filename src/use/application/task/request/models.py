from dataclasses import dataclass

from use.application.common.request.models import SortOrder
from use.entities.task.enums import TaskTypeEnum


@dataclass
class SearchFilters:
    order_by: TaskTypeEnum | None = None
    order: SortOrder | None = None
