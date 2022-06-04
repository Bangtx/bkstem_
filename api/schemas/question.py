from .schema import Schema
from typing import Optional


class QuestionBase(Schema):
    answers: dict
    result: str
    type: int
    image: Optional[str]


class Question(QuestionBase):
    id: int


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(Question):
    pass