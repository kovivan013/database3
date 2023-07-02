from pydantic import BaseModel

class DataStructure(BaseModel):
    data: dict = {}

    def as_dict(self):
        return self.__dict__