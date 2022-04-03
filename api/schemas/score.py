from .schema import Schema
from datetime import date
from typing import List


class ScoreBase(Schema):
    date: date
    classroom: int
    student: int
    teacher: int


class Score(ScoreBase):
    score: List[float]


class ScoreCreate(ScoreBase):
    score: float