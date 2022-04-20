from .base import BaseModel
from .question import Question
from .student import Student
from peewee import ForeignKeyField, CharField


class QuestionStudent(BaseModel):
    question = ForeignKeyField(Question, column_name='question_id')
    student = ForeignKeyField(Student, column_name='student_id')
    result = CharField

    class Meta:
        db_table = 'question_student'
