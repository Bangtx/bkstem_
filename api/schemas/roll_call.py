from .schema import Schema
from datetime import date


class RollCallBase(Schema):
    date: date
    classroom: int
    student: int
    teacher: int
    absent_type: int


class RollCall(RollCallBase):
    pass


class RollCallCreate(RollCallBase):
    pass