from .base import BaseModel
from .question import Question
from .student import Student
from peewee import ForeignKeyField, CharField


class QuestionStudent(BaseModel):
    question = ForeignKeyField(Question, column_name='question_id')
    student = ForeignKeyField(Student, column_name='student_id')
    result = CharField()

    class Meta:
        db_table = 'question_student'

    @classmethod
    def check_rate_correct(cls, student_id, classroom_id):
        from .home_work import HomeWork
        questions = list(HomeWork.select().where(HomeWork.classroom == classroom_id))
        questions = list(map(lambda x: x.id, questions))
        correct = list(
            cls.select().where(cls.student == student_id, cls.question << questions)
        )
        correct = list(map(lambda x: x.result, correct))
        return {'correct': len(correct)}
