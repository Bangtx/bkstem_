from .schema import Schema


class QuestionBase(Schema):
    answers: dict
    result: str
    type: int


class Question(QuestionBase):
    id: int


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(Question):
    pass