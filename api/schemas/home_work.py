from .schema import Schema
from datetime import date


class HomeWorkCreate(Schema):
    date: date = date
    deadline: date = date
    classroom: int
    question: int
    schedule: int


class HomeWorkUpdate(HomeWorkCreate):
    pass