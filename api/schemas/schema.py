from pydantic import BaseModel
from config.database import PeeweeGetterDict


class Schema(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
