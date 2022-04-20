from .schema import Schema
from datetime import date


class HomeWorkCreate(Schema):
    date: date
    deadline: date
    classroom: int
    question: int


class HomeWorkUpdate(HomeWorkCreate):
    pass