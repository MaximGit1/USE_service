from dataclasses import dataclass
from enum import StrEnum, auto


@dataclass(frozen=True)
class RoleInfo:
    name: str
    level: int


class RoleEnum(StrEnum):
    GUEST = auto()
    USER = auto()
    MODERATOR = auto()
    ADMIN = auto()

    def validate_role(self, role_name: str) -> bool:
        current_level = self.get_current_role().level
        min_level = self.get_role_by_name(role_name).level

        return current_level >= min_level

    def get_current_role(self) -> RoleInfo:
        match self:
            case self.USER:
                return RoleInfo(name="user", level=1)
            case self.MODERATOR:
                return RoleInfo(name="moderator", level=2)
            case self.ADMIN:
                return RoleInfo(name="admin", level=5)
            case _:
                return RoleInfo(name="guest", level=0)

    @classmethod
    def get_role_by_name(cls, role_name: str) -> RoleInfo:
        match role_name:
            case cls.USER:
                return RoleInfo(name="user", level=1)
            case cls.MODERATOR:
                return RoleInfo(name="moderator", level=2)
            case cls.ADMIN:
                return RoleInfo(name="admin", level=5)
            case _:
                return RoleInfo(name="guest", level=0)
