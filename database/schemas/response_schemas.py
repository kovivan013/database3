from pydantic import BaseModel

class ResponseStructure(BaseModel):
    data: dict = {}

    def as_dict(self) -> dict:
        return self.__dict__

class DataStructure(BaseModel):
    status: int = 200
    data: dict = {}

    def as_dict(self) -> dict:
        return self.__dict__
