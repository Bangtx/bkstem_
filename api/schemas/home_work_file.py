from schemas.schema import Schema
from datetime import date


class File(Schema):
    name: str
    payload: str
    type: str
    size: int


class HomeWorkFileBase(Schema):
    date: date
    deadline: date = None
    title: str


class HomeWorkFile(HomeWorkFileBase):
    date: date
    deadline: date = None


class HomeWorkFileCreate(HomeWorkFileBase):
    classroom_id: int
    file_question: int


class HomeWorkFileUpdate(HomeWorkFileCreate):
    pass
