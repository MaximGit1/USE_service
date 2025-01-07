from dataclasses import (
    dataclass,
)

from use.entities.common.models import Entity
from use.entities.user.enums import RoleEnum
from use.entities.user.value_objects import (
    HashedPassword,
    UserID,
    Username,
)


@dataclass(
    slots=True,
    kw_only=True,
)
class User(Entity[UserID]):
    username: Username
    hashed_password: HashedPassword
    role: RoleEnum
    is_active: bool
