from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from use.entities.common.value_objects import ValueObject

ValueT = TypeVar("ValueT")
EntityId = TypeVar("EntityId", bound=ValueObject[Any])


@dataclass
class Entity(Generic[EntityId]):
    id: EntityId
