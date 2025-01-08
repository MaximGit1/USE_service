from pydantic import BaseModel

from use.entities.user.value_objects import RawPassword, Username


class UserCreateScheme(BaseModel):
    username: str
    password: str

    def get_data(self) -> tuple[Username, RawPassword]:
        return Username(self.username), RawPassword(self.password)
