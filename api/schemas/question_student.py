from .schema import Schema


class QuestionStudentCreate(Schema):
    question: int
    student: int
    result: str


class QuestionStudentUpdate(QuestionStudentCreate):
    pass