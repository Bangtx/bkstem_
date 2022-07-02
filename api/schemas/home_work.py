from .schema import Schema
from datetime import date


class HomeWorkCreate(Schema):
    date: date = date
    deadline: date = date
    classroom: int
    question: int
    schedule: int
    is_exactly: bool = False


class HomeWorkUpdate(HomeWorkCreate):
    pass


class UnitRequire(Schema):
    unit: int
    value: bool
