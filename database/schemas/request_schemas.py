from pydantic import BaseModel

class UserCreate(BaseModel):
    telegram_id: int
    username: str

    def as_dict(self) -> dict:
        return self.__dict__

class GetUser(BaseModel):
    telegram_id: int = 0

class ClassCreate(BaseModel):
    owner: int
    id: str
    name: str = ""
    description: str = ""
    invite_code: str = ""
    all_users: list = []
    admins: list = []

    def as_dict(self) -> dict:
        return self.__dict__